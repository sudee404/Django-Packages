=====
Chat Application
=====

This application implements a real-time chat application 
with asynchronous sending a receiving of messages. 
It supports chatroom creation as well as persisting messages in the database


Installation
-----------
To install the package and use it in your project run the 
command below in your project environment ::

	python3 -m pip install /path/to_file/django-chat-app/dist/django-chat-app-0.1.tar.gz


Quick start
-----------

1. This app relies on daphne and channels so add them to your INSTALLED_APPS setting like this. 
Remember to add daphne to the top of the list::

    INSTALLED_APPS = [
	'daphne',
	'channels',
        ...
        'chat_app',
    ]
    


2. Add the following to your settings file to use it. This loads our asgi file::
	
	ASGI_APPLICATION = 'my_project.asgi.application'
	
	CHANNEL_LAYERS = {
		'default': {
			'BACKEND': 'channels.layers.InMemoryChannelLayer',
			},
		}


3. Setup the project to find static and media files by adding the following lines to your settings.py::

	# Remember to import os 
	STATIC_URL = 'static/'
	STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	STATICFILES_DIRS = [
		os.path.join(BASE_DIR, "chat_app", "static"),
	]

4. rewrite your project asgi file to match below ::

	# my_project/asgi.py
	from chat_app import routing
	from channels.auth import AuthMiddlewareStack
	from channels.routing import ProtocolTypeRouter, URLRouter
	from channels.security.websocket import AllowedHostsOriginValidator
	import os
	from django.core.asgi import get_asgi_application

	# Be sure to replace with your actual project's name
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

	django_asgi_app = get_asgi_application()
	application = ProtocolTypeRouter(
		{
			"http": django_asgi_app,
			"websocket": AllowedHostsOriginValidator(
				AuthMiddlewareStack(
					URLRouter(routing.websocket_urlpatterns))
			),
		}
	)
    
    
	
2. Include the URLconf in your project urls.py like this::
	
		urlpatterns = [
			... ,
   			path("chat/",include('chat_app.urls')),
			... ,
		]


3. Run ``python manage.py makemigrations`` then ``python manage.py migrate`` to create the models.

4. Start the development server and visit http://127.0.0.1:8000/chat/
   to view users. You have to login to access the chats, the view will 
   redirect to 'login' incase you have'nt done so 

5. Visit http://127.0.0.1:8000/chat/lobby where lobby is the room name.
