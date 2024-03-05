from django import forms
from django.contrib.auth.models import User

class usernameForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']


class emailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

class passwordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput , label = 'Password')
    confirmpassword = forms.CharField(widget=forms.PasswordInput , label = 'Confirm Password')
    class Meta:
        model = User
        fields = ['password' , 'confirmpassword']

    def is_valid(self):
        valid = super(passwordForm, self).is_valid()
        if not valid:
            return valid
        if self.cleaned_data['password'] != self.cleaned_data['confirmpassword']:
            self.add_error('password', 'Passwords do not match')
            return False
        if(len(self.cleaned_data['password']) < 8):
            self.add_error('password', 'Password must be atleast 8 characters long')
            return False
        char = False
        num = False
        for c in self.cleaned_data['password']:
            if c.isalpha():
                char = True
            if c.isdigit():
                num = True
        if not char or not num:
            self.add_error('password', 'Password must contain atleast one letter and one number')
            return False
        return True
        
            
    