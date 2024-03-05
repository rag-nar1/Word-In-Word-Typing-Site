from django import forms
from account.models import account

class typingForm(forms.ModelForm):
    class Meta:
        model = account
        fields = "__all__"


class homeForm(forms.Form):
    maxTime = forms.ChoiceField(choices=[(30 , "30s") , (60 , "60s") , (120 , "120s")] , widget=forms.RadioSelect , label='Max Time')
    maxWords = forms.ChoiceField(choices=[(25 , 25) , (50 , 50) , (75 , 75)] , widget=forms.RadioSelect , label='Max Words')
    fields = ['maxTime' , 'maxWords']
    def is_valid(self) -> bool:
        return super().is_valid()
        
