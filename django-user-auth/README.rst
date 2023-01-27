=====
User Authentication
=====

user_auth is a Django app to conduct web-based user authentication. 
Users can create accounts, login and recover passwords if lost.
Since this app implements an abstract user model , 
remember to install it at the start of the project before calling the first migration.
Also keep in mind to not use ``User`` class but rather call our ``MyUser`` model , use the ``get_user_model()`` function.

Detailed documentation is in the "docs" directory.

Installation
-----------
To install the package and use it in your project run the command below in your project environment.::

`python3 -m pip install /path/to_file/django-user-auth-0.1.tar.gz`

replace with the path to the file


Quick start
-----------

1. Add "user_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'user_auth',
    ]

2. Add the following to your settings file to use it::

    AUTH_USER_MODEL = 'user_auth.MyUser'

    AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.ModelBackend',
	'user_auth.backends.MyUserBackend',
    ]

3. Setup the project to find static and media files by adding the following lines to your settings.py. Remember to import os::

	STATIC_URL = 'static/'
	MEDIA_URL = 'media/'
	STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

4. Add an email provider settings for password reset. Email settings may differ with providers so look it up::
	
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = ''
	EMAIL_PORT = ''
	EMAIL_HOST_USER = ''
	EMAIL_HOST_PASSWORD = ''
	EMAIL_USE_TLS = True

OR Use django's console email backend for testing, add it as shown below . It displays the password reset email in the console::
	
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

2. Include the user_auth URLconf in your project urls.py like this. Make sure to set up static and media files routing as shown below::

	from django.conf import settings
	from django.conf.urls.static import static
	urlpatterns = [
		... ,
		path('user_auth/', include('user_auth.urls')),
		... ,
	]
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)	
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


3. Run ``python manage.py migrate`` to create the user_auth models.

4. Start the development server and visit http://127.0.0.1:8000/user_auth/
   to create an account

5. You can also visit http://127.0.0.1:8000/user_auth/ to login or recover lost password.
