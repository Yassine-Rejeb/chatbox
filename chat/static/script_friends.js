// This script is used to fill the friend list with friends
$(function() {
  $.ajax({
      type: "GET",
      url: "friends/",
      success: function(data) {
        res= data
        for (var i = 0; i < res.length; i++) {
          var template = Handlebars.compile( $("#friend-template").html() );
          var context={
            friend: res[i],
            profile_pic: '/chat/profile_pic/?username=' + res[i]
          }
            $("ul#friend-list").prepend(template(context));
      }
      },
    });
  return true;
});

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


// Update the profile settings
$('#UpdateProfileBtn').click(function() {
  $.ajax({
      type: "POST",
      url: "/chat/update/",
      data: {
        profile_pic: $('#profile_pic').val(),
        username: $('#username').val(),
        new_password: $('#password1').val(),
        new_password2: $('#password2').val(),
        current_password: $('#password_old').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(data) {
        console.log(data);
        if (data == 'success') {
          alert(data)
        }
        else {
          alert(data);
        }
      }
  });
  return false;
});