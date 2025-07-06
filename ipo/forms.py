from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Name')
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        name = self.cleaned_data.get('name', '').strip()
        if name:
            parts = name.split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data.get('username', '').lower()
        return super().clean() 