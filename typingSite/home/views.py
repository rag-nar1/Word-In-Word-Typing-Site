from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from account.models import account
from .forms import SignupForm as signupForm
from django.core.mail import send_mail
import random
from dotenv import load_dotenv
import os
import operator
load_dotenv()


class home(View):
    def get(self, request):
        return render(request, 'home/home.html')


class signup(View):

    def addFormToSession(self, request , form):
        request.session['email'] = form.cleaned_data['email']
        request.session['username'] = form.cleaned_data['username']
        request.session['password'] = form.cleaned_data['password1']
    
    def get(self, request):
        if(request.user.is_authenticated):
            return redirect('home:home')
        msg = None
        if 'error' in request.session:
            msg = request.session['error']
        request.session.pop('error', None)
        form = signupForm()
        return render(request, 'registration/signup.html', {'form': form , 'error': msg})
    
    def post(self, request):
        form = signupForm(request.POST)
        msg = None
        if form.is_valid():
            prev_user = User.objects.filter(email = form.cleaned_data['email'])
            if prev_user:
                msg = 'Email already exists'
                return render(request, 'registration/signup.html', {'form': form , 'error': msg})
            self.addFormToSession(request , form)
            return redirect('home:signup_verify')
        return render(request, 'registration/signup.html', {'form': form })


class signup_verify(View):
    code_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    code_length = 6
    def generate_code(self):
        code = ''
        for i in range(self.code_length):
            code += self.code_char[random.randint(0, len(self.code_char) - 1)]
        return code
    
    def send_email(self, email, code):
        try:
            send_mail(
                subject='Verification code',
                message=f'Your verification code is {code}',
                from_email= os.getenv('gmail'),
                recipient_list=[email],
                fail_silently=False
            )
            return True
        except Exception as e:
            return "email can not be sent try another email"

    def empty_session(self, request):
        request.session['email'] = ''
        request.session['username'] = ''
        request.session['password'] = ''
        request.session['code'] = ''
    

    def get(self, request):
        # send email whith a verification code
        if not 'code' in request.session or request.session['code'] == '':
            code = self.generate_code()
            email = request.session['email']
            status = self.send_email(email, code)
            request.session['code'] = code
            if status != True:
                self.empty_session(request)
                request.session['error'] = status
                return redirect('home:signup')
        return render(request, 'registration/signup_verify.html')
    
    def post(self, request):
        code = request.POST['code']
        if code == request.session['code']:
            user = User.objects.create_user(
                username = request.session['username'],
                email = request.session['email'],
                password = request.session['password']
            )
            user.save()
            acc = account(user = user)
            acc.save()
            self.empty_session(request)
            return redirect('login')
        msg = 'Invalid code'
        return render(request, 'registration/signup_verify.html', {'error': msg})
    

class leaderboard(View):
    class lbAccount:
        def __init__(self, username, wpm, accuracy):
            self.username = username
            self.wpm = wpm
            self.accuracy = accuracy

    def accountsInPage(self ,pageNumber, accounts , order):
        # return 10 accounts in the page
        returnedAccounts = accounts[(pageNumber - 1) * 10 : pageNumber * 10]
        if order == 'wpm':
            # sort by wpm and if wpm is the same sort by accuracy
            returnedAccounts.sort(key = operator.attrgetter('wpm', 'accuracy'), reverse = True)
        else:
            # sort by accuracy and if accuracy is the same sort by wpm
            returnedAccounts.sort(key = operator.attrgetter('accuracy', 'wpm'), reverse = True)
        return returnedAccounts

    def transformAccounts(self, accounts):
        # transform accounts to lbAccount
        transformedAccounts = []
        for acc in accounts:
            username = acc.user.username
            wpm = acc.wpm
            accuracy = acc.accuracy
            if wpm == 1000:
                wpm = 0
            if accuracy == 1000:
                accuracy = 0
            transformedAccounts.append(self.lbAccount(username, wpm, accuracy))
        return transformedAccounts

    def get(self, request , page = 1):
        order = request.GET.get('order')
        # print(page, order)
        if order != 'wpm' and order != 'acc':
            order = 'wpm'
        page = int(page)
        accounts = account.objects.all()
        # cieling division
        maximumPage = len(accounts) // 10 + (len(accounts) % 10 != 0)
        if page > maximumPage:
            page = maximumPage
        if page < 1:
            page = 1
        accounts = self.transformAccounts(accounts)
        accounts = self.accountsInPage(page, accounts, order)
        if order == 'wpm':
            orderlabel = 'WPM'
        else:
            orderlabel = 'Accuracy'
        page = page - 1 
        context = {
            'accounts': accounts,
            'page': page,
            'maximumPage': maximumPage,
            'order': order,
            'orderlabel': orderlabel,
        }
        return render(request, 'home/leaderboard.html', context)


            

        


    
    



