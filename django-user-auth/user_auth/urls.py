from .views import *
from django.urls import path

urlpatterns = [
    path("", login_view, name='login'),  # User login
    path("registration/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('password_reset/', MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/', MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
