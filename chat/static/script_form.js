// Make a get request to the server to add a friend
$('#AddFriendBtn').click(function() {
    $.ajax({
        type: "GET",
        url: "/chat/add_friend/?friend=" + $('#AddFriendInput').val(),
        data: {
          username: $('#AddFriendInput').val()
        },
        success: function(data) {
          console.log($('#AddFriendInput').val());
          console.log(data);
          if (data == 'success') {
            location.reload();
          } 
          else {
            alert(data);
          }
        }
    });
    return false;
  });
  
  // Make a get request to the server to remove a friend
  $('#RemoveFriendBtn').click(function() {
  $.ajax({
        type: "GET",
        url: "/chat/remove_friend/?friend=" + $('#AddFriendInput').val(),
        data: {
          username: $('#AddFriendInput').val()
        },
        success: function(data) {
          console.log($('#AddFriendInput').val());
          console.log(data);
          if (data == 'success') {
            location.reload();
          }
          else {
            alert(data);
          }
        }
    });
    return false;
  });


  $('#cancelBtn').click(function() {
    // empty the input fields after the user has clicked the cancel button
    var new_picture = $('#new_picture').val('');
    var username = $('#username').val('');
    var new_password = $('#password1').val('');
    var new_password2 = $('#password2').val('');
    var current_password = $('#password_old').val('');
  });
  
  $(document).ready(function() {
    $('#updateForm').on('submit', function(e) {
      e.preventDefault(); // prevent the form from being submitted the traditional way
  
      var formData = new FormData(this); // create a FormData object from the form's contents
  
      $.ajax({
        type: 'POST',
        url: '/chat/update/',
        data: formData, // include the FormData object in the request
        processData: false, // prevent jQuery from trying to process the form data
        //contentType: false,
        //contentType: 'application/json',
        //cache: false,
        //async: false,
        //enctype: 'multipart/form-data',
        contentType: false,
        success: function(response) {
          // handle the response here
          alert(response);
          console.log(response);
        }
      });
    });
  });