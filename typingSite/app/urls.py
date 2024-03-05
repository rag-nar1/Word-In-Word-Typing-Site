from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('typing/', views.typing.as_view(), name='typing'),
    path('result/', views.result.as_view(), name='result'),
]