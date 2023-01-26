from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseNotFound
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def chat_home(request):
    context = {}
    context['users'] = User.objects.exclude(pk=request.user.id)
    return render(request, 'chat_home.html', context)


def get_room(request, pk1):
    
    if request.method == 'GET' and request.user.is_authenticated:
        user1 = request.user
        user2 = get_user_model().objects.get(pk=pk1)
        name = f"{sorted([user1.username, user2.username])[0]}_{sorted([user1.username, user2.username])[1]}"
        chat_room, created = ChatRoom.objects.get_or_create(
            name=name, defaults={"is_private": True}
        )
        print('\\nOne\n\n')
        if created:
            chat_room.users.add(user1, user2)
            print('\\nTwo\n\n')

        if user1 in chat_room.users.all() and user2 in chat_room.users.all():
            print('\\nThree\n\n')
            return HttpResponse(chat_room.name)
        else:
            return HttpResponse("You are not authorized to view this chat room.")
    return HttpResponseNotFound("Chat not found.")

@login_required(redirect_field_name='chat-view',login_url='login')
def chat_view(request, room_name):
    context = {}
    context['users'] = User.objects.exclude(pk=request.user.id)
    context['room_name'] = room_name
    context['chat_name'] = [name for name in room_name.split('_') if name != request.user.username][0]
    context['messages'] = Message.objects.filter(chat_room__name = room_name)
    return render(request, 'chat_room.html', context)
