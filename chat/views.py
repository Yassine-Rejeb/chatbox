from datetime import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse,HttpResponseNotFound
from django.shortcuts import redirect
from . import models

# INDEX PAGE
def index(response):
    # NO INDEX PAGE, SO REDIRECT TO CHAT PAGE
    return redirect('/chat/')

# CHECK IF USER IS LOGGED IN
def unknown(response):
    # CHECK IF USER IS LOGGED IN
    if 'username' not in response.session:
        return True
    return False

# LOGOUT USER
def Logout(response):
    # LOGOUT USER
    del response.session['username']
    return redirect('/login/')

# GET PROFILE PIC
def getProfilePic(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Profile Pic request Page Opened!')
    
    # GET USERNAME
    if response.GET['username']:
        username = response.GET['username']
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    # GET PROFILE PIC
    try:
        return FileResponse(open('media/profile_pics/'+username+'.jpg', 'rb'))
    except FileNotFoundError:
        return FileResponse(open("media/profile_pics/default.png", 'rb'))

# GET FRIEND LIST
def getFriends(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Friends Page Opened!')

    # DB CONNECTION
    dbConn = models.mongoConnection()
    
    # GET FRIEND LIST
    friends = dbConn.findFriends(response.session['username'])
    #print("RESULT:",json.dumps(friends))
    
    # CLOSE DB CONNECTION
    dbConn.close()
    
    return JsonResponse(friends,safe=False)

def addFriend(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Add Friend Request Page Opened!')
    toBeAdded = response.GET['friend']
    dbConn = models.mongoConnection()

    # CHECK IF TOBEADDED IS A VALID USER
    if dbConn.findUsername(toBeAdded)==None :
        print("user not found!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("User not found!")
    elif toBeAdded==response.session['username']:
        print("user is current user!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("You can't add yourself!")
    elif dbConn.findFriend(response.session['username'], toBeAdded)!=None:
        print("user is already a friend!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("User is already a friend!")
    else:
        print("user found!")
        # ADD TOBEADDED TO CURRENT USER'S FRIENDS LIST
        dbConn.addFriend(response.session['username'], toBeAdded)

        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("success")

def removeFriend(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Remove Friend Request Page Opened!')
    toBeRemoved = response.GET['friend']
    dbConn = models.mongoConnection()

    # CHECK IF TOBEREMOVED IS A VALID USER
    
    if dbConn.findUsername(toBeRemoved)==None :
        print("user not found!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("User not found!")
    elif toBeRemoved==response.session['username']:
        print("user is current user!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("You can't remove yourself!")
    elif dbConn.findFriend(response.session['username'], toBeRemoved)==None:
        print("user is not a friend!")
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("User is not a friend!")
    elif dbConn.findUsername(toBeRemoved)!=None and toBeRemoved!=response.session['username'] and dbConn.findFriend(response.session['username'], toBeRemoved)!=None:
        # REMOVE TOBEREMOVED FROM CURRENT USER'S FRIENDS LIST
        dbConn.removeFriend(response.session['username'], toBeRemoved)

        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("success")
        #return redirect('/chat/')
    else:
        # CLOSE DB CONNECTION
        dbConn.close()
        return HttpResponse("User not found!")

def updatePassword(session,current_user,pass1,pass2):
    # CHECK IF NEW PASSWORDS MATCH
    if pass1 != pass2:
        return "New passwords do not match.\n"
    else:
        dbConn = models.mongoConnection()
        dbConn.updatePassword(current_user,pass1)
        return "Password updated.\n"

def updateUserName(session,current_user,username):
    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF USERNAME IS TAKEN
    if dbConn.findUsername(username) != None:
        return "Username is taken.\n"
    else:
        # UPDATE USERNAME
        dbConn.updateUsername(current_user,username)

        # UPDATE profile_pic FILENAME
        try:
            os.rename('media/profile_pics/'+current_user+'.jpg', 'media/profile_pics/'+username+'.jpg')
        except FileNotFoundError:
            pass
        return "Username updated.\n"

def updatePicture(session,pic):
    # CHECK IF FILE IS AN IMAGE
    if type(pic) == str:
        return "File is not an image.\n"
    if pic.content_type == 'image/jpeg' or pic.content_type == 'image/png':
        # CHECK IF FILE IS TOO BIG
        if pic.size > 5000000:
            return "File is too big.\n"
        else:
            # SAVE FILE

            with open('media/profile_pics/'+session['username']+'.jpg', 'wb+') as destination:
                for chunk in pic.chunks():
                    destination.write(chunk)
            return "Picture updated.\n"

def encryptPassword(password):
    # Hash a password with SHA256
    import hashlib
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

def update(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Update Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    if response.method == 'POST':
        #username = response.POST['username']
        username = ''
        new_password = response.POST['new_password']
        new_password2 = response.POST['new_password2']
        current_password = response.POST['current_password']
        # CHECK IF NEW PICTURE IS EMPTY
        if 'new_picture' in response.FILES:
            new_picture = response.FILES['new_picture']
        else:
            new_picture = ''
        # INIT LOG
        update_log = ''
        dbConn = models.mongoConnection()
        if username == '' and new_password == '' and new_password2 == '' and new_picture == '':
            return HttpResponse("No data to update!")

        # CHECK IF CURRENT PASSWORD IS CORRECT
        dbConn = models.mongoConnection()
        if dbConn.findPassword(current_user) != encryptPassword(current_password):
            update_log += "Current password is incorrect.\n"
        else:
            # UPDATE USERNAME
            if username != '':
                update_log += updateUserName(response.session,current_user,username)

            # UPDATE PASSWORD
            if new_password != '':
                update_log += updatePassword(response.session,current_user,new_password,new_password2)

            # UPDATE PICTURE
            if new_picture != None:
                update_log += updatePicture(response.session,new_picture)

        # CLOSE DB CONNECTION
        dbConn.close()

        # RETURN LOG
        return HttpResponse(update_log)
    return HttpResponse("Something Wrong Happened!\nContact an Admin!")

def sendMsg(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Send Message Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    # GET POST DATA
    to = response.POST['to']
    msg = response.POST['msg']
    #print('to:',to)
    #print('msg:',msg)

    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF TO IS A VALID USER
    if dbConn.findUsername(to) == None:
        #print('User not found!')
        dbConn.close()
        return HttpResponse("User not found!")
    elif dbConn.findUsername(to) == current_user:
        #print('You cannot send a message to yourself!')
        dbConn.close()
        return HttpResponse("You cannot send a message to yourself!")
    # Check if user is a friend
    elif dbConn.findFriend(current_user,to) == None:
        #print('You are not friends with this user!')
        dbConn.close()
        return HttpResponse("You are not friends with this user!")
    else:
        # SEND MESSAGE
        dbConn.sendMsg(current_user,to,msg,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #print('Message sent!', current_user, to, msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        dbConn.close()
        return HttpResponse("Message sent!")

# CHECK WHETHER THERE IS UNREAD MESSAGES AT ALL
def checkMsgs(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Check Message Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF THERE ARE UNREAD MESSAGES
    state = dbConn.checkMsgs(current_user)
    #print('state:',state)

    # CHECK IF THERE ARE UNREAD MESSAGES
    if state == False:
        return HttpResponse("false")
    else:
        return JsonResponse(state, safe=False)

def getMsg(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Get Message Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    # GET POST DATA
    to = response.GET['to']
    #print('to:',to)

    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF TO IS A VALID USER
    if dbConn.findUsername(to) == None:
        return HttpResponse("User not found!")
    else:
        # GET MESSAGES
        messages = dbConn.getMsg(current_user,to)
        #print('messages:',messages)
        return JsonResponse(messages, safe=False)

# GET NEW MESSAGES
def getUnreadMsg(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Get New Message Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    # GET POST DATA
    to = response.GET['to']
    #print('to:',to)

    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF TO IS A VALID USER
    if dbConn.findUsername(to) == None:
        dbConn.close()
        return HttpResponse("User not found!")
    else:# dbConn.checkMsg(to, current_user) == False:
        # GET MESSAGES
        messages = dbConn.getUnreadMsg(current_user,to)
        #print('messages:',messages)
        dbConn.close()
        #print('messages:',messages)
        return JsonResponse(messages, safe=False)

def markAsRead(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    
    #print('Mark As Read Page Opened!')

    # GET CURRENT USER
    current_user = response.session['username']
    
    # GET POST DATA
    to = response.GET['to']
    #print('to:',to)

    # DB CONNECTION
    dbConn = models.mongoConnection()

    # CHECK IF TO IS A VALID USER
    if dbConn.findUsername(to) == None:
        dbConn.close()
        return HttpResponse("User not found!")
    else:
        # MARK AS READ
        dbConn.markAsRead(current_user,to)
        dbConn.close()
        return HttpResponse("Messages marked as read!")

def chat(response):
    # CHECK IF USER IS LOGGED IN
    if unknown(response):
        return redirect('/login/')
    #print('Chat Page Opened!')
    
    # GET USERNAME
    #print("Session USER:",response.session['username'])
    return render(response, "chat/chat.html",  {'current_user': response.session['username']})