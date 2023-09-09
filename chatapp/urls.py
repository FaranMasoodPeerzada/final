from django.urls import path
from . import views

urlpatterns= [
    path('server_endpoint/', views.server_endpoint, name='your_server_endpoint'),

    path('',views.home,name='home'),
    path('chat/<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('get_chat_messages/<int:conversation_id>/', views.get_chat_messages, name='get-chat-messages'),
   
]