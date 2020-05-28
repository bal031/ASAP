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

var socket = io.connect('http://localhost:3000');


function transmitCourses(){
    var courses = [];
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
    
    socket.on('connect', function(data) {
      socket.emit('generate schedule', JSON.stringify(courses));
     
    });
    }

    function transmitPE(){
      event.preventDefault();
      var p_Event = []; // 
      var count = 1;
      var days = [];
      var start = 0;
      var end = 0;


      $('#pe_days').find('input[type=checkbox]:checked').each(function() {
        days.push($(this).val());
      });

           
        var personal_event = { courseName: "my_time", 
                                sectionID: "-1", 
                                instructionType:"NA", 
                                instructionDay: days,
                                startTime: document.getElementById("s_time").value + document.getElementById("from_time").value, 
                                endTime:document.getElementById("e_time").value + document.getElementById("to_time").value};  
       //p_Event.push(personal_event); 
    
      
      console.log(personal_event); // display on console for debugging only
      //localStorage.setItem('SelectedCourses', JSON.stringify(courses));
      
      socket.on('connect', function(data) {
        socket.emit('add personal event', JSON.stringify(personal_event));
       
      });
      }
      $("a").click(function(event){
        event.preventDefault();
      });
