from django.urls import path
from . import views

# Namespace
app_name = 'emp'

# URL Patterns
urlpatterns = [
    # path('', views.welcome_page, name='welcome'),
    # path('login/', views.login_page, name='login'),
    path('', views.server_page, name='server'),
    path('client/', views.client_page, name='client'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('start/', views.start_work, name='start_work'),
    path('end/<int:session_id>/', views.end_work, name='end_work'),
    path('update-description/<int:session_id>/', views.update_session_description, name='update_session_description'),
    path('server-login/',views.server_login,name = 'server_login'),
    path('login/',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout ,name = 'user_logout'),
    path('register/',views.register,name = 'register'),
    path('goodbye/',views.goodbye,name = 'goodbye'),
]
