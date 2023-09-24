from django.urls import path
from . import views

urlpatterns= [
   
    
    path('',views.registeration,name='user_registeration'),
    path('signup',views.signuprequest,name='signup'),
    path('user-login-page',views.loginpage,name='login_page'),
    path('user-login',views.userloginrequest,name='login_request'),
   
    path('get_chat_messages/<int:conversation_id>/', views.get_chat_messages, name='get-chat-messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('userhome',views.userhome,name='user_home'),
    path('chat/<int:conversation_id>/',views.chat_detail,name='chat_detail'),






    # path('chat/<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    # path('get_chat_messages/<int:conversation_id>/', views.get_chat_messages, name='get-chat-messages'),
    # path('server_endpoint/', views.server_endpoint, name='your_server_endpoint'),
]