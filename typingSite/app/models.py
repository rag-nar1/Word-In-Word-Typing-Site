from django.db import models

# Create your models here.

class words(models.Model):
    word = models.CharField(max_length=50)
    most_freq_char = models.ForeignKey('characters' , on_delete=models.SET(None) , related_name='most_freq_char')
    most_freq_char2 = models.ForeignKey('characters' , on_delete=models.SET(None), related_name='most_freq_char2')
    most_freq_char3 = models.ForeignKey('characters' , on_delete=models.SET(None), related_name='most_freq_char3')
    used_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.word

class characters(models.Model):
    char = models.CharField(max_length=1)

    def __str__(self):
        return self.char
    
    