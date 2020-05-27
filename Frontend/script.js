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
socket.on('connect', function(data) {
	socket.emit('join', 'generate schedule');
});

function transmit(){
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
    socket.send(JSON.stringify(courses));
    }
