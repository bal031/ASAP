    //var socket = io.connect('http://localhost:3000');
    var socket = io.connect('http://asap.ucsd.edu:80');
    // Client to server holders
    var user_data = [];
    var p_Event = []; 
    var p_Preference;
    var courses = [];
    var term;
    var waitlist;
   
    // Server to client holders
    var data_Load=[];
        
    
    function search(){
    $(document).ready(function(){       
      $('#selectable').html('');
      var file;
      // Select
      getTerm();
      
      if (term == "FA20")
      {
        file = "search.json";
      }
      else if (term == "S120")
      {
        file = "summer1.json";
      }
      else if (term == "S220")
      {
        file = "summer2.json";
      }
      else if (term == "SP20")
      {
        file = "spring.json"
      }  
      console.log("file:", file);    
      var searchField = $('#search').val();
      var expression = new RegExp(searchField, "i");
      $.getJSON(file, function(data) {
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
  $( '#selectable ').selectable({
     selected: function() {
       
        $( ".ui-selected", this ).each(function() {           
           var myId = $(this).prop('id');
           document.getElementById(myId).ondblclick = function() {fillList(myId)};  
           document.getElementById("add_class").onclick = function() {fillList(myId)};     
        });
     }                      
  });
});

$(document).ready(function(){
  var Load = window.sessionStorage.getItem('json');
  console.log(Load);
  data_Load = JSON.parse(Load);
  var tr = [];
  console.log(data_Load);
  for(i = 0; i<data_Load.display.length; i++){
      tr.push('<tr>');
      tr.push("<td>" + data_Load.display[i].name + "</td>");
      tr.push("<td>" + data_Load.display[i].professor + "</td>");
      tr.push("<td>" + data_Load.display[i].days+" "+formatTime(data_Load.display[i].start)+"-"+formatTime(data_Load.display[i].end) + "</td>");
      if (data_Load.display[i].waitlisted!=false){
        tr.push("<td class=\"uk-text-center\"><span class=\"uk-margin-medium-right\" uk-icon=\"check\"></span></td>");
      }
      else
      {
        tr.push("<td>" + " " + "</td>");
      }
      
      tr.push('</tr>');
    }
  $('#class_schedule').append($(tr.join('')));
  });


socket.on('connect', function(data) {
  socket.emit('join', 'Client enter the room!');       
});

$(document).ready(function(){
  var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: ['interaction', 'dayGrid', 'timeGrid', 'list'],
    defaultView: 'timeGridWeek',
    minTime: "07:00:00",
    maxTime: "23:00:00",    
      weekday: 'short'      
}); 

socket.on('comfirmation', function(msg){
  UIkit.notification(msg, {status:'success'});            

});



socket.on("schedule_ready", function(data){
  var eventSources = calendar.getEventSources();
  var len = eventSources.length;
  for (var i = 0; i < len; i++) { 
    eventSources[i].remove(); 
}    
  UIkit.notification("Building Schedule", {status:'primary'}); 
  //var classlist = JSON.parse(data);
  //data_Load.push(classlist);
  //console.log(data_Load);
      
//calendar.changeView( 'timeGridWeek');      

  window.sessionStorage.setItem('json', data);
  calendarEl = document.getElementById('calendar');
  var Load = window.sessionStorage.getItem('json');
  data_Load = JSON.parse(Load); 

  if(jQuery.isEmptyObject(data)||data_Load.schedule.length==0){
    UIkit.notification("Sorry (✖╭╮✖)!!! There doesn't seem to be a schedule that fit this preference. Please try again.", {status:'primary'});
    return; 
}

    calendar.addEventSource( data_Load.schedule);
    
  calendar.render();
  UIkit.notification("Successfully Built Schedule", {status:'success'}); 
  
});
}); 

function transmit(){
  getCourses();
  if(courses.length==0){
    alert("Please remember to select your courses.");
    return;
  }
  getPreference();
  getTerm();
  getWaitListStat();

  window.localStorage.clear();
  var user_data = {currentTerm: term, course: courses, personalEvent:p_Event, preference: p_Preference, waitlistStat:waitlist};
  console.log("sent package:", user_data);
  console.log(user_data);
  UIkit.notification("(*ˊᗜˋ*)/ᵗᑋᵃᐢᵏ ᵞᵒᵘ* For Waiting", {status:'primary'})
  
  //socket.emit('join', 'Client enter the room!');  
  socket.emit('generate', JSON.stringify(user_data)); 
  
  
  //Clear Arrays
  courses = [];
  //p_Event = []; //took out personal event clear
  p_Preference='';
  term = '';
  
}

function getTerm(){
  term = $("#cur_term").val();
  //document.getElementById("cur_term").disabled = true;
}

function getWaitListStat(){
  waitlist = $("#waitlist_Stat").is(":checked") ? "true" : "false";
}

function getPreference(){
    
    p_Preference = {prof_Rating: $("#prof_rating").val(), 
    avg_GPA: $("#avg_gpa").val(), avg_Time: $("#avg_time").val(), gap: $("#gap").val(),
    class_Days: $("#class_days").val(), time_Ref: $("#time_pref").val()}
 
}

function getCourses(){
    
    //var count = 1;
    
    $('#course-list').find('li').each(function() {
      var $this = $(this);
      // checkbox id   
      //var x = '#must_have_' + count;  
      var x = '#mh_'+$this.prop('id').replace(" ",'');
      console.log("must have", x)
      var checkState = $(x).is(":checked") ? "true" : "false";
    
      var course = { name: $this.attr('id'), must_have: checkState};  
      courses.push(course); 
      //count++;
    });
    
    console.log(courses); // display on console for debugging only
    
    }

function clearList(){
  $('#course-list').find('li').each(function(){
    var $this = $(this);
    $this.remove();
  })
}
    function addPE(){
      event.preventDefault();
      
      var count = 1;
      var days = [];
      var startStr = document.getElementById("s_time").value;
      var endStr = document.getElementById("e_time").value;
      
      var start = parseInt(startStr.replace(':',''),10);
      var end = parseInt(endStr.replace(':',''),10);
           
      var dayStr = "";
      $('#pe_days').find('input[type=checkbox]:checked').each(function() {
        dayStr += $(this).val() + " ";
        days.push($(this).val());
      });

      if(end<=start||startStr==""||endStr==""||days.length==0){
        UIkit.notification("¯\\(°_o)/¯ Invalid input. Better luck next time. ", {status:'warning'});
        return; 
      }
      
      var rand = Math.floor(Math.random() * 1000) + 1; 
      
        var personal_event = { courseName: "my_time", 
                                sectionID: "000000", 
                                instructionType:"NA", 
                                instructionDay: days,
                                startTime: start, 
                                endTime:end,
                                personalId: rand};  
       //p_Event.push(personal_event); 
       document.getElementById('event').reset();
       p_Event.push(personal_event);
      
      var index = p_Event.length-1;
        
      var div = [];
      var id = "\"pe_item" + index+rand+"\"";
      
      var html = "<div id="+id+">Personal Event   from:"+startStr+ " to "+ endStr + " Days: "+dayStr+"<button onclick=removePE("+rand+","+index+")>delete event</button></div>";
      div.push(html);
      $('#pe_list').append($(div.join('')));
      //console.log(personal_event); // display on console for debugging only
      UIkit.notification("Personal Event Added", {status:'success'})
      //localStorage.setItem('SelectedCourses', JSON.stringify(courses));
      
      //socket.on('connect', function(data) {
      //  socket.emit('personal event', JSON.stringify(personal_event));
       
      //});
      }

      function removePE(rand,id){
        var name= 'pe_item'+id+rand;
                
        document.getElementById(name).remove();        
        p_Event = removeFromArray(p_Event,rand);
      }

      function removeFromArray(array, value) {
       var temp = [];
      
       for(i=0; i<array.length;i++)
       {
         if (array[i].personalId!=value)
         {
           temp.push(array[i]);
         }
       }
       return temp;
    }

      function fillList(courseName) {
        
        var li = [];
        var html ="";
        var name = new String(courseName);
        var id = "\"" + courseName +"\"";
        var count = document.querySelectorAll("#course-list li").length+1;
        console.log("count of much_have",count);
        //var name = 'must_have_' + count;
        var name = 'mh_'+courseName.replace(" ",'');
        console.log("fillList", name);
        var str = "\""+name+"\"";
        html = "<li id="+id+">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input id="+str+" type=\"checkbox\" value=\"true\" checked>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+courseName+"</li>";
        li.push(html);
        $('#course-list').append($(li.join('')));
 
  document.getElementById(courseName).remove();
}

    /*  $("a").click(function(event){
        event.preventDefault();
      });*/

      function formatTime(h_24) {
        console.log("time:", h_24);
        var str;
        var min;
        if (h_24.length>=7)
        {
          str = h_24.substr(0,1);
          //min = h_24.su
        }
        str = h_24.substr(0,2);
        var num = parseInt(str,10);
        console.log("num",num);
        var hr=" ";
        //str = str.substr(3,5);
        var h = num % 12;
        if( h === 0){ h = 12;}
        if( num < 10) {
          str = h_24;
          hr = str.substr(0,4);}
        else {
          str = h_24.substr(3,2);
          hr = h+":"+str;
        }

        return  hr + (num < 12 ? 'AM' : 'PM');
    }