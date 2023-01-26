import re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation
from django import forms
from .models import MyUser


class LoginForm(forms.Form):
    # Login form for handling user login
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    # User registration form with password validation
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         
    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_notvalid': _("Password must of 8 Character which contain alphanumeric with atleast 1 special charater and 1 uppercase."),
    }
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-style',  'placeholder':"New Password"}),
        strip=False,
        
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-style',  'placeholder': "Confirm Password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        
        

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            # Regix to check the password must contains sepcial char, numbers, char with upeercase and lowercase.
            regex = re.compile(
                '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,30})')
            if (regex.search(password1) == None):
                raise forms.ValidationError(
                    self.error_messages['password_notvalid'],
                    code='password_mismatch',
                )

        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        # instance = MyUser.objects.get(id=self.user.id)
        # if not instance.first_login:
        #     instance.first_login = True
        #     instance.save()
        return self.user
