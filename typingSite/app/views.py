from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import words , characters
from account.models import account 
from .forms import typingForm , homeForm
import json
import random
# Create your views here.

class home(LoginRequiredMixin , View):
    def get(self, request):
        form = homeForm()
        context = {
            'form' : form
        }
        return render(request, 'app/home.html' , context)
    
    def post(self, request):
        form = homeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            maxTime = data['maxTime']
            maxWords = data['maxWords']
            request.session['maxTime'] = maxTime
            request.session['maxWords'] = maxWords
            return redirect('app:typing')
        return render(request, 'app/home.html' , {'form' : form})
        
    

class typing(LoginRequiredMixin , View):

    def get_priority(self,acc):
        priority = []
        char = 'A'
        atr = 'accuracy'
        for i in range(26):
            curr = getattr(acc, atr + char)
            priority.append((curr, char))
            char = chr(ord(char) + 1)
        priority.sort()
        return priority
    
    def get_words(self , priority , wordcnt):
        wordscurr = []
        i = 0
        while i < 3:
            char = priority[i][1]
            char = characters(id = ord(char) - ord('A') + 1 , char = char)
            wordscurr += words.objects.filter(most_freq_char = char).order_by('used_cnt')[:wordcnt[i]]
            i += 1 
        return wordscurr
    
    def get_finalWords(self,wordscurr , totalchar):
        wordres = []
        for word in wordscurr:
            if totalchar - len(word.word) < 0:
                continue
            wordres.append(word)
            totalchar -= len(word.word)
            word.used_cnt += 1
            word.save()
        return wordres
    
    def get_finaltxt(self,wordres):
        finaltxt = ""
        #  rondomize the words
        random.shuffle(wordres)
        for word in wordres:
            finaltxt += word.word + " "
        return finaltxt


    def generate_words(self,acc , request):
        maxWords = 75
        if 'maxWords' in request.session:
            maxWords = int(request.session['maxWords'])
        totalchar = maxWords * 5
        wordcnt = [
                maxWords // 2,
                maxWords // 3,
                maxWords // 6,
            ]
        priority = self.get_priority(acc)
        wordscurr = self.get_words(priority , wordcnt)
        wordres = self.get_finalWords(wordscurr , totalchar)
        finaltxt = self.get_finaltxt(wordres)
        return finaltxt
    


    def get(self, request):
        acc = account.objects.get(user = request.user)
        words = self.generate_words(acc , request)
        form = typingForm(instance=acc)
        maxTime = 120
        if 'maxTime' in request.session:
            maxTime = request.session['maxTime']
        context = {
            'words' : words,
            'form' : form,
            'maxTime' : maxTime
        }
        return render(request, 'app/typing.html', context) 
    
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        acc = account.objects.get(user = request.user)
        for key , value in data.items():
            if(key == 'user') : continue                                                                                         
            setattr(acc, key , value)
        acc.save()
        return redirect('app:result')
    
class result(LoginRequiredMixin , View):
    def get(self, request):
        acc = account.objects.get(user = request.user)
        context = {
            'acc' : acc
        }
        return render(request, 'app/result.html', context)
    
        
    
    
