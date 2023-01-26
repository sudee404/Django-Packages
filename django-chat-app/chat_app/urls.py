from django.urls import path
from .consumers import ChatConsumer
from . import views

urlpatterns = [
    path('',views.chat_home,name='chat-home'),
    path('get/<int:pk1>/', views.get_room, name='get-room'),
    path('<str:room_name>/', views.chat_view, name='chat-view'),
    # path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi(), name='chat'),
]
