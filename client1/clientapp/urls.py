
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('login/', views.login_page, name='login')
]