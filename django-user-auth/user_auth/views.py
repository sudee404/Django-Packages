from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from user_auth.models import MyUser
from .forms import RegisterForm, LoginForm, CustomSetPasswordForm


def register_view(request):
    """
    Handles user registration.
    On GET request, it renders the registration template.
    On POST request, it validates the form data, creates a new user and logs them in.
    If the form is not valid, it returns a JSON response with the status 'error' and the form errors.
    On successful registration, it returns a JSON response with the status 'success'.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'base_form.html', {})



def login_view(request):
    """
    Handles user login.
    On GET request, it renders the login template.
    On POST request, it validates the form data  and logs them in.
    If the form is not valid, it returns a JSON response with the status 'error' and the form errors.
    On successful login, it returns a JSON response with the status 'success'.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
            else:
                form.add_error(None, "Invalid email or password")

        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'base_form.html', {})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('index')


class MyPasswordResetView(PasswordResetView):
    template_name = 'my_password_reset_form.html'
    email_template_name = 'my_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = MyUser.objects.get(email=email)
            return super().form_valid(form)
        except MyUser.DoesNotExist:
            messages.warning(self.request, 'No user found with this email')
            return self.form_invalid(form)


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'my_password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'my_password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    post_reset_login = True

    def form_valid(self, form):
        print("valid")
        form.save()
        return super().form_valid(form)


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'my_password_reset_complete.html'
