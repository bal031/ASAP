    var socket = io.connect('http://localhost:3000');
    // Client to server holders
    var user_data = [];
    var p_Event = []; 
    var p_Preference = [];
    var courses = [];
    var term = [];
    var calendarEl; 
    // Server to client holders
    var data_Load=[];
        
    
    function search(){
    $(document).ready(function(){       
      $('#selectable').html('');     
      var searchField = $('#search').val();
      var expression = new RegExp(searchField, "i");
      $.getJSON('search.json', function(data) {
       $.each(data, function(key, value){
        if (value.name.search(expression) != -1)
        {
            var id = "\"" + value.name +"\"";   
         $('#selectable').append("<li id=" +id+">"+value.name+"</li>");
        }
       });   
      });  
    });
}

$(document).ready(function(){
  var Load = window.sessionStorage.getItem('json');
  console.log(Load);
  data_Load = JSON.parse(Load);
  var tr = [];
  console.log(data_Load);
      tr.push('<tr>');
      tr.push("<td>" + data_Load.display[0].name + "</td>");
      tr.push("<td>" + data_Load.display[0].professor + "</td>");
      tr.push("<td>" + data_Load.display[0].days+" "+data_Load.display[0].start+"-"+data_Load.display[0].end + "</td>");
      tr.push("<td>" + " " + "</td>");
      tr.push('</tr>');
     
  $('#class_schedule').append($(tr.join('')));
  });

socket.on('connect', function(data) {
  socket.emit('join', 'Client enter the room!');       
});

socket.on("schedule_ready", function(data){
  console.log(data); 

  UIkit.notification("Building Schedule", {status:'primary'}); 
  //var classlist = JSON.parse(data);
  //data_Load.push(classlist);
  //console.log(data_Load);
  window.sessionStorage.setItem('json', data);
  calendarEl = document.getElementById('calendar');
  var Load = window.sessionStorage.getItem('json');
  data_Load = JSON.parse(Load);
  
  
  console.log(data_Load.schedule[0]);

  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: ['interaction', 'dayGrid', 'timeGrid', 'list'],
    header:{right: 'dayGridMonth,timeGridWeek'},
    events: [data_Load.schedule[0]]
});  

  calendar.render();
  
});


function transmit(){
  getCourses();
  getPreference();
  getTerm();  
  window.localStorage.clear();
  var user_data = {currentTerm: term, course: courses, personalEvent:p_Event, preference: p_Preference};
  
  console.log(user_data);
  UIkit.notification("Thank You For Waiting", {status:'primary'})
  
  //socket.emit('join', 'Client enter the room!');  
  socket.emit('generate', JSON.stringify(user_data)); 
  
  socket.on('comfirmation', function(msg){
    UIkit.notification(msg, {status:'success'});    
    console.log(msg);
  });

   event.preventDefault();
  //Clear Arrays
  courses = [];
  p_Event = [];
  p_Preference = [];
  term = [];
  
}

function getTerm(){
  var curr_Term = {term : $("#cur_term").val()};
  term.push(curr_Term);
}

function getPreference(){
    
    var ref = {transportation: $("#trans").val(), prof_Rating: $("#prof_rating").val(), 
    avg_GPA: $("#avg_gpa").val(), avg_Time: $("#avg_time").val(), gap: $("#gap").val(),
    class_Days: $("#class_days").val(), time_Ref: $("#time_pref").val()}
 
  p_Preference.push(ref);
}

function getCourses(){
    
    var count = 1;
    
    $('#course-list').find('li').each(function() {
      var $this = $(this);
      // checkbox id   
      var x = '#must_have_' + count;  
      
      var checkState = $(x).is(":checked") ? "true" : "false";
    
      var course = { name: $this.attr('id'), must_have: checkState};  
      courses.push(course); 
      count++;
    });
    
    console.log(courses); // display on console for debugging only
    //localStorage.setItem('SelectedCourses', JSON.stringify(courses));
    /*
    socket.on('connect', function(data) {
      socket.emit('generate schedule', JSON.stringify(courses));
     
    });*/
    }

    function getPE(){
      event.preventDefault();
      
      var count = 1;
      var days = [];
      var startStr = document.getElementById("s_time").value;
      var endStr = document.getElementById("e_time").value;
      
      var start = parseInt(startStr.replace(':',''),10);
      var end = parseInt(endStr.replace(':',''),10);


      $('#pe_days').find('input[type=checkbox]:checked').each(function() {
        days.push($(this).val());
      });

           
        var personal_event = { courseName: "my_time", 
                                sectionID: "000000", 
                                instructionType:"NA", 
                                instructionDay: days,
                                startTime: start, 
                                endTime:end};  
       //p_Event.push(personal_event); 
       document.getElementById('event').reset();
       p_Event.push(personal_event);
      
      console.log(personal_event); // display on console for debugging only
      UIkit.notification("Personal Event Added", {status:'success'})
      //localStorage.setItem('SelectedCourses', JSON.stringify(courses));
      
      //socket.on('connect', function(data) {
      //  socket.emit('personal event', JSON.stringify(personal_event));
       
      //});
      }

      function fillList(courseName) {
        
        var name = new String(courseName);
        var id = "\"" + courseName +"\"";
        var count = document.querySelectorAll("#course-list li").length+1;
        var name = 'must_have_' + count;
        var str = "\""+name+"\"";
       
        
  document.getElementById("course-list").innerHTML += "<li id="+id+">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input id="+str+" type=\"checkbox\">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+courseName+"</li>";
  event.preventDefault();
  document.getElementById(courseName).remove();
}

      $("a").click(function(event){
        event.preventDefault();
      });

   /*
   <script>var availableTags = [
    "CSE",
    "BDE",
    "ENG",
    "CSE 12",
    "CSE 21",
    "ECE 15",
    "CSE 100",
    "CSE 110",
    "CSE 140L",
    "ECE 144",
    "WAR 1",
    "REL 101",
    
];
$( "#search" ).autocomplete({
    source: availableTags
});
</script>
*/

