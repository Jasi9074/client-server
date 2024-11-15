from django.urls import path,include
from . import views

# Namespace
app_name = 'emp'

# URL Patterns
urlpatterns = [
    # path('', views.welcome_page, name='welcome'),
    #path('login/', views.login_page, name='login'),
    path('', views.server_page, name='server'),
    # path('client/', views.user_login, name='client'),
    path('dashboard/',views.server_dashboard,name = 'dashboard'),
    path('start/', views.start_work, name='start_work'),
    path('end/<int:session_id>/', views.end_work, name='end_work'),
    path('server-login/',views.server_login,name = 'server_login'),
    #path('login/',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout ,name = 'user_logout'),
    #path('register/',views.register,name = 'register'),
    #path('goodbye/',views.goodbye,name = 'goodbye'),
    path('employee_selection/', views.employee_selection, name='employee_selection'),
    #path('password_login/', views.password_login, name='password_login'),
    path('machine-selection/', views.machine_selection, name='machine_selection'),
    path('select-machine/', views.select_machine, name='select_machine'),
    path('complaint_selection<str:page_id>/', views.complaint_selection, name='complaint_selection'),
    path('logout_and_redirect/', views.logout_and_redirect, name='logout_and_redirect'),
    path('save_complaint/', views.save_complaint, name='save_complaint'),
    path('tempend/', views.temp_end_work, name='temp_end_work'), # temp fix
    path('request_passcode/<str:username>/', views.request_passcode, name='request_passcode'),
    path('verify_passcode/<str:username>/', views.verify_passcode, name='verify_passcode'),
    path('password_reset/<str:username>/', views.custom_password_reset, name='password_reset'),
]
