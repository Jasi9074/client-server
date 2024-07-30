from django.shortcuts import render, redirect
from .models import Employee, WorkSession
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

# from django.contrib.auth.models import User # Needed for profile update


def login_page(request):
    return render(request, "login.html")


def welcome_page(request):
    return render(request, "emp/welcome.html")


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("emp:dashboard"))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("emp:dashboard"))
                else:
                    return HttpResponse("Something happened: User is not active")
            else:
                messages.error(
                    request, "Invalid username or password. Please try again."
                )
    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "emp/login.html", context)


def register(request):

    if request.user.is_authenticated:
        return HttpResponse("First logout")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create a profile for the Employee
            Employee.objects.create(
                user=user,
                photo=request.FILES.get("photo"),
            )

            return HttpResponseRedirect(reverse("emp:user_login"))
    else:
        form = UserRegistrationForm()

    context = {"form": form}

    return render(request, "emp/register.html", context)


@login_required
def start_work(request):
    employee = Employee.objects.get(user=request.user)
    WorkSession.objects.create(employee=employee, start_time=timezone.now())
    return redirect("emp:dashboard")


@login_required
def end_work(request, session_id):
    session = WorkSession.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return redirect("emp:dashboard")


def dashboard(request):
    if request.user.is_authenticated:
        # return render(request, "emp/dashboard.html")
        employee = Employee.objects.get(user=request.user)
        sessions = WorkSession.objects.filter(employee=employee).order_by("-start_time")
        return render(request, "emp/dashboard.html", {"sessions": sessions})
    else:
        return HttpResponseRedirect(reverse("emp:user_login"))


@login_required()
def user_logout(request):
    username = request.user.first_name + " " + request.user.last_name
    logout(request)
    return HttpResponseRedirect(reverse("emp:goodbye") + f"?username={username}")


def goodbye(request):
    username = request.GET.get("username")
    if not username:
        username = "User"
    return render(request, "emp/goodbye.html", {"username": username})
