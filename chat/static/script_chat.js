//--------------- Chat scripts --------------->
  //Sort the messages according to the time
    function sortMessages(msgList){
    var sorted = [];
    while (msgList.length > 0) {
        var min = msgList[0];
        var minIndex = 0;
        for (var i = 1; i < msgList.length; i++) {
        if (msgList[i].time < min.time) {
            min = msgList[i];
            minIndex = i;
        }
        }
        sorted.push(min);
        msgList.splice(minIndex, 1);
    }
        
    return sorted;
    } 

    chatHistory = $('.chat-history');
    chatHistoryList =  chatHistory.find('ul');

    //Remove old messages
    function removeOldMessages(){
    chatHistoryList.find('li').each(function(){
        $(this).remove();
    });
    }

    // Get messages 
    function getMessages(user){
    // Change the color back to normal
    var userElement = document.getElementById("userID-"+user);
    userElement.style.color = "";

    var url = '/chat/get_messages/?to=' + user;
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(data){
        //console.log(data);
        data = sortMessages(data);
        // how to loop over data and render them
        for (var i = 0; i < data.length; i++) {
            var message_template = Handlebars.compile( $("#message-template").html() );
            var message_response_template = Handlebars.compile( $("#message-response-template").html() )
            var context={
            msg: data[i]['msg'],
            time: data[i]['time'],
            user: ''
            }
            if (data[i]['sender'] == user) {
                context.user = user;
                chatHistoryList.append(message_response_template(context))
            }
            else {
                context.user = 'Me';
                chatHistoryList.append(message_template(context))
            }
        }
        // Scroll to the bottom of the chat
        chatHistory.scrollTop(chatHistory[0].scrollHeight);
        markAsRead(user);
        }
    });
    }

    // Open a chat with a user
    function openChat(event){
    // Get the text in the element I have clicked on
    var user = event.currentTarget.innerText;
    url = '/chat/profile_pic/?username=' + user;
    document.getElementById('otherEndUser').src = url;
    // Set the text in the chat div
    document.getElementsByClassName('chat-with')[0].innerText = 'Chat with ' + user;
    // Set the text in the input box
    document.getElementById('message-to-send').placeholder = 'Type your message to ' + user;
    removeOldMessages();
    getMessages(user);
    }

    // Open a chat with first friend automatically
    $(document).ready(function(){
    // Get Friends list
    $.ajax({
        type: "GET",
        url: "friends/",
        success: function(data) {
            res = data;
            var user = res[0];
            url = '/chat/profile_pic/?username=' + user;
            document.getElementById('otherEndUser').src = url;
            // Set the text in the chat div
            document.getElementsByClassName('chat-with')[0].innerText = 'Chat with ' + user;
            // Set the text in the input box
            document.getElementById('message-to-send').placeholder = 'Type your message to ' + user; 
            
            removeOldMessages();
            getMessages(user);
        }
        });
    });
//--------------- End Chat scripts --------------->



//--------------- Send message --------------->
    function sendMsg(){
    var msg = document.getElementById('message-to-send').value;
    var user = document.getElementsByClassName('chat-with')[0].innerText;
    user = user.replace('Chat with ', '');
    url = '/chat/send_message/'
    data = {
        'to':user,'msg':msg
    };

    // Clear the input box
    document.getElementById('message-to-send').value = '';

    // Send the message
    $.ajax({
        headers: {'X-CSRFToken': document.getElementById('csrf').querySelector('input').value},
        url: url,
        type: 'POST',
        data: data,
        success: function(response){
        //console.log(response);
        
        // Reload the messages
        removeOldMessages();
        getMessages(user);
        }
    });
    }
//--------------- End Send message --------------->




//--------------- Get New Messages --------------->
    function updateMessages(user){
        // Change the color back to normal
        var userElement = document.getElementById("userID-"+user);
        userElement.style.color = "";
        var url = '/chat/get_unread_messages/?to=' + user;
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data){
                console.log("An update on msgs:\n",data);
                data = sortMessages(data);
                // how to loop over data and render them
                for (var i = 0; i < data.length; i++) {
                    var message_template = Handlebars.compile( $("#message-template").html() );
                    var message_response_template = Handlebars.compile( $("#message-response-template").html() )
                    var context={
                        msg: data[i]['msg'],
                        time: data[i]['time'],
                        user: ''
                    }
                    if (data[i]['sender'] == user) {
                        context.user = user;
                        chatHistoryList.append(message_response_template(context))
                    }
                    else {
                        context.user = 'Me';
                        chatHistoryList.append(message_template(context))
                    }
                }
                // Scroll to the bottom of the chat
                chatHistory.scrollTop(chatHistory[0].scrollHeight);
                markAsRead(user);
            }
        });
    }
//--------------- End Get New Messages --------------->



//--------------- Mark as read --------------->
    function markAsRead(user){
        var url = '/chat/mark_as_read/?to=' + user;
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data){
                console.log("Marked as read:\n",data);
            }
        });
    }
//--------------- End Mark as read --------------->



//--------------- Check for new messages ---------------> 
    // Check for any new mshs at all
    function checkForNewMessagesAtAll(){
        url = '/chat/check_messages/';
        $.ajax({
            headers: {'X-CSRFToken': document.getElementById('csrf').querySelector('input').value},
            url: url,
            type: 'POST',
            dataType: 'json',
            success: function(data){
                //console.log(data);
                if (data != false) {
                //console.log('New messages from', data);
                // Change the color of all the usernames in the list to orange
                for (var i = 0; i < data.length; i++) {
                    var userElement = document.getElementById("userID-" + data[i]);
                    userElement.style.color = 'orange';
                    console.log('Changing color of', data[i]);
                }
                // Update the messages of the chat that is currently open
                var user = document.getElementsByClassName('chat-with')[0].innerText;
                user = user.replace('Chat with ', '');
                if (data.includes(user)) {
                    updateMessages(user);
                }
            }
            }
            });
    }
    // Check for new messages every 3 seconds
    setInterval(checkForNewMessagesAtAll, 1000);
//--------------- End Check for new messages --------------->