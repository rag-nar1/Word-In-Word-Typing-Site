from django import forms
from django.contrib.auth.forms import UserCreationForm as signupForm
from django.contrib.auth.models import User
class SignupForm(signupForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(signupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    