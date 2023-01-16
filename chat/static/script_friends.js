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
