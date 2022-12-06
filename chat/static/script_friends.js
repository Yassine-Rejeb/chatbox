/*(function(){
  var friends = {
    init: function() {
      this.cacheDOM();
      this.render();
    },
    cacheDOM: function() {
      this.$list = $('.friend-list');
      //this.$button = $('button');
      this.$listItem = $('#friend-list');
      //this.$chatHistoryList =  this.$chatHistory.find('ul');
    },
    getFriends: function() {
      data = fetch('/chat/friends')
      .then(response => response.json());
      return data;
    },
    render: function() {
      friends = this.getFriends();
      for (friend in friends) {
        var template = Handlebars.compile( $("#friend-template").html() );
        profile_image = fetch('/chat/profile_image/' + friend)
        var context = {'friend': friend};
      for (var i = 0; i < friends.length; i++) {
        this.$list.append(this.$listItem);
      }
    }
      console.log(context);
  },
    
    
    scrollToBottom: function() {
       this.$chatHistory.scrollTop(this.$chatHistory[0].scrollHeight);
  },
    getCurrentTime: function() {
      return new Date().toLocaleTimeString().
              replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
    },
    getRandomItem: function(arr) {
      return arr[Math.floor(Math.random()*arr.length)];
    }
    
  };
  
  friends.init();
  
  var searchFilter = {
    options: { valueNames: ['name'] },
    init: function() {
      var userList = new List('people-list', this.options);
      var noItems = $('<li id="no-items-found">No items found</li>');
      
      userList.on('updated', function(list) {
        if (list.matchingItems.length === 0) {
          $(list.list).append(noItems);
        } else {
          noItems.detach();
        }
      });
    }
  };
  
  searchFilter.init();
  
})();*//*
$.ajax({
  url: 'friends',
  success: function(data) {
  console.log(data);
  //$('#the-div-that-should-be-refreshed').html(data);
  let list = document.getElementById("friend-list");
  data.forEach((item)=>{
  let li = document.createElement("li");
  li.innerText = item;
  list.appendChild(li);
});
  }
});*/

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
          /*$.ajax({
            type: 'GET',
            url: 'profile_pic/?username=' + res[i],
            dataType: 'image/png',
            async: true,
            success: function (data) {
                console.log(data);
                $("#template-img").attr("src", 'data:image/png;base64,'+data);
            }
        });*/
            $("ul#friend-list").prepend(template(context));
      }   
      },
    });  
  return true;    
});
