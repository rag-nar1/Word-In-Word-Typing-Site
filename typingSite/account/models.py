from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    accuracy = models.IntegerField(default = 1000)
    last_accuracy = models.IntegerField(default = 1000)
    wpm = models.IntegerField(default = 1000)
    last_wpm = models.IntegerField(default = 1000)
    last_mistakes = models.IntegerField(default = 1000)
    accuracyA = models.IntegerField(default = 1000) 
    accuracyB = models.IntegerField(default = 1000)
    accuracyC = models.IntegerField(default = 1000)
    accuracyD = models.IntegerField(default = 1000)
    accuracyE = models.IntegerField(default = 1000)
    accuracyF = models.IntegerField(default = 1000)
    accuracyG = models.IntegerField(default = 1000)
    accuracyH = models.IntegerField(default = 1000)
    accuracyI = models.IntegerField(default = 1000)
    accuracyJ = models.IntegerField(default = 1000)
    accuracyK = models.IntegerField(default = 1000)
    accuracyL = models.IntegerField(default = 1000)
    accuracyM = models.IntegerField(default = 1000)
    accuracyN = models.IntegerField(default = 1000)
    accuracyO = models.IntegerField(default = 1000)
    accuracyP = models.IntegerField(default = 1000)
    accuracyQ = models.IntegerField(default = 1000)
    accuracyR = models.IntegerField(default = 1000)
    accuracyS = models.IntegerField(default = 1000)
    accuracyT = models.IntegerField(default = 1000)
    accuracyU = models.IntegerField(default = 1000)
    accuracyV = models.IntegerField(default = 1000)
    accuracyW = models.IntegerField(default = 1000)
    accuracyX = models.IntegerField(default = 1000)
    accuracyY = models.IntegerField(default = 1000)
    accuracyZ = models.IntegerField(default = 1000)

    def __str__(self):
        return self.user.username
