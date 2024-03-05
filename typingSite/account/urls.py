from django.urls import path
from . import views

app_name = 'account'    

urlpatterns = [
    path('',views.profile.as_view() , name = 'profile'),
    path('settings/',views.settings.as_view() , name = 'settings'),
    path('settings/username/',views.username.as_view() , name = 'username'),
    path('settings/email/',views.email.as_view() , name = 'email'),
    path('settings/email/verify/',views.email_verify.as_view() , name = 'email_verify'),
    path('settings/password/',views.password.as_view() , name = 'password'),
]