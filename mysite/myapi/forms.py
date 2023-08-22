import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




from .castomUser import CustomUser




class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']









class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_format = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_format, email):
            raise ValidationError(_('Invalid email'))
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or (not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password)):
            raise ValidationError(_('Invalid password'))
        return password

class CreateUser(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label=_("Username"), max_length=100, error_messages={'required': _('Please enter a username.')})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, error_messages={'required': _('Please enter a password.')})
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput, error_messages={'required': _('Please confirm the password.')})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Password and confirm password do not match."))

class UserAndLoginDataForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'