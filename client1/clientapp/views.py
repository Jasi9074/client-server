from django.shortcuts import render


def welcome_page(request):
    return render(request, 'welcome.html')

def login_page(request):
    return render(request, 'login.html')

