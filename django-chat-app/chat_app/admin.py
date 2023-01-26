from django.contrib import admin
from chat_app.models import ChatRoom

# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
	'''Admin View for ChatRoom'''

	list_display = ('name',)
	list_filter = ('name',)