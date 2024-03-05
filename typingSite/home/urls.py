from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
app_name = 'home'

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    # signup
    path('signup/', views.signup.as_view(), name='signup'),
    path('signup/verify/', views.signup_verify.as_view(), name='signup_verify'),
    
    # password reset
    path('password_reset/', PasswordResetView.as_view(template_name='home/password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name ="home/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="home/password_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="home/password_complate.html"), name='password_reset_complete'),

    # leader board
    path('leaderboard/', views.leaderboard.as_view(), name='leaderboard'),
    path('leaderboard/<int:page>/', views.leaderboard.as_view(), name='leaderboard'),
    path('leaderboard/<int:page>?order=<str:order>', views.leaderboard.as_view(), name='leaderboard'),
]