from django.urls import path, include
from django.contrib import auth
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.chat, name="chat room"),
    path("logout/", views.Logout, name="logout"),
    path("friends/", views.getFriends, name="friends"),
    path("profile_pic/", views.getProfilePic, name="profile pic"),
    path("add_friend/", views.addFriend, name="add friend"),
    path("remove_friend/", views.removeFriend, name="add friend"),
    path("update/", views.update, name="update"),
    path("send_message/", views.sendMsg, name="send message"),
    path("get_messages/", views.getMsg, name="get messages"),
    path("check_messages/", views.checkMsgs, name="check messages"),
    path("get_unread_messages/", views.getUnreadMsg, name="get unread messages"),
    path("mark_as_read/", views.markAsRead, name="mark as read"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)