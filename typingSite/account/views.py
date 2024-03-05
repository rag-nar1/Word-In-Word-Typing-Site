from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import account
from .forms import usernameForm , emailForm , passwordForm
from home.views import signup_verify
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

class profile(LoginRequiredMixin ,View):
    def get(self , request):
        acc = account.objects.get(user = request.user)
        chars = []
        c = "A"
        atr = "accuracy"
        for i in range(26):
            dictc = {"char" : c , "acc" : getattr(acc , atr + c)}
            chars.append(dictc)
            c = chr(ord(c) + 1)
        context = {
            'acc' : acc,
            'chars' : chars
        }
        return render(request , 'account/profile.html', context)

class settings(LoginRequiredMixin ,View):
    def get(self , request):
        return render(request , 'account/settings.html')

        
class username(LoginRequiredMixin ,View):
    def get(self , request):
        form = usernameForm(instance = request.user)
        context = {
            'form' : form
        }
        return render(request , 'account/form.html' , context)
    def post(self , request):
        form = usernameForm(request.POST , instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        return render(request , 'account/form.html' , {'form' : form})
        

class email(LoginRequiredMixin ,View):
    def get(self , request):
        form = emailForm(instance = request.user)
        context = {
            'form' : form
        }
        return render(request , 'account/form.html' , context)
    def post(self , request):
        form = emailForm(request.POST , instance = request.user)
        if form.is_valid():
            prev_user = User.objects.filter(email = form.cleaned_data['email'])
            if prev_user:
                return render(request , 'account/form.html' , {'form' : form , 'error' : 'Email already exists'})
            request.session['email'] = form.cleaned_data['email']
            return redirect('account:email_verify')
        return render(request , 'account/form.html' , {'form' : form})

            

class email_verify(LoginRequiredMixin , View):
    
    def get(self , request):
        if not 'code' in request.session:
            code = signup_verify.generate_code(signup_verify)
            request.session['code'] = code
            signup_verify.send_email(signup_verify , request.session['email'] , request.session['code'])
        return render(request , 'registration/signup_verify.html')
    
    def post(self , request):
        code = request.POST['code']
        if code == request.session['code']:
            user = request.user
            user.email = request.session['email']
            user.save()
            request.session.pop('code')
            request.session.pop('email')
            return redirect('account:profile')
        return render(request , 'registration/signup_verify.html' , {'error' : 'Invalid code'})

class password(LoginRequiredMixin ,View):
    def get(self , request):
        form = passwordForm()
        return render(request , 'account/form.html' , {'form' : form})
    def post(self , request):
        form = passwordForm(request.POST , instance = request.user)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirmpassword']:
                return render(request , 'account/form.html' , {'form' : form , 'error' : 'Passwords do not match'})
            user = request.user
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('account:profile')
        return render(request , 'account/form.html' , {'form' : form})
            
    