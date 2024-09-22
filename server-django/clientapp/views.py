from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, WorkSession
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from itertools import groupby
from datetime import date
from django.http import JsonResponse

def server_login(request):
    return render(request, "server/login.html")


def login_page(request):
    return render(request, "emp/login.html")


def server_page(request):
    return render(request, "server/welcome.html")


def client_page():
    return HttpResponseRedirect(reverse("emp:employee_selection"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("First logout")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            Employee.objects.create(
                user=user,
                photo=request.FILES.get("photo"),
            )

            return HttpResponseRedirect(reverse("emp:server"))
    else:
        form = UserRegistrationForm()

    context = {"form": form}

    return render(request, "emp/register.html", context)


@login_required
def start_work(request):
    employee = Employee.objects.get(user=request.user)
    employee.is_working = True

    description = request.POST.get("description", "")
    machine_number = request.POST.get("machine", None)

    WorkSession.objects.create(
        employee=employee,
        start_time=timezone.now(),
        description=description,
        machine=machine_number
    )

    response = redirect("emp:dashboard")
    if machine_number:
        response.set_cookie("machine", machine_number, max_age=30*24*60*60)  # 30 days
    return response


@login_required
def end_work(request, session_id):
    employee = Employee.objects.get(user=request.user)
    employee.is_working = False

    session = WorkSession.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return redirect("emp:dashboard")


@login_required
def pause_work(request, session_id):
    session = WorkSession.objects.get(id=session_id)
    session.paused = True
    session.pause_time = timezone.now()
    session.save()
    return redirect("emp:dashboard")


@login_required
def resume_work(request, session_id):
    session = WorkSession.objects.get(id=session_id)
    if session.paused:
        pause_duration = timezone.now() - session.pause_time
        session.start_time += pause_duration
        session.paused = False
        session.pause_time = None
        session.save()
    return redirect("emp:dashboard")


@login_required
def update_session_description(request, session_id):
    if request.method == "POST":
        session = get_object_or_404(WorkSession, id=session_id)
        session.description = request.POST.get("description", "")
        session.save()
    return redirect("emp:dashboard")


def dashboard(request):
    if request.user.is_authenticated:
        employee = Employee.objects.get(user=request.user)
        sessions = WorkSession.objects.filter(employee=employee).order_by("-start_time")

        sessions_grouped_by_day = {}
        for day, group in groupby(sessions, key=lambda s: s.start_time.date()):
            sessions_grouped_by_day[day] = list(group)

        latest_session = sessions.first()
        today = date.today()

        context = {
            "latest_session": latest_session,
            "sessions_grouped_by_day": sessions_grouped_by_day,
            "today": today,
        }
        return render(request, "emp/dashboard.html", context)
    else:
        return HttpResponseRedirect(reverse("emp:employee_selection"))


@login_required
def user_logout(request):
    username = request.user.first_name + " " + request.user.last_name
    logout(request)
    return HttpResponseRedirect(reverse("emp:goodbye") + f"?username={username}")


def goodbye(request):
    username = request.GET.get("username")
    if not username:
        username = "User"
    return render(request, "emp/goodbye.html", {"username": username})


def machine_selection(request):
    context = {
        'range': range(1, 25)  # Machines M1 to M24
    }
    return render(request, 'emp/machine_selection.html', context)

def select_machine(request):
    if request.method == 'POST':
        selected_machine = request.POST.get('machine')
        if not selected_machine:
            return redirect('emp:machine_selection')  # Handle no selection case

        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return redirect('emp:machine_selection')  # Handle case where Employee is not found

        # Create or update WorkSession based on your needs
        WorkSession.objects.create(
            employee=employee,
            start_time=timezone.now(),
            description=f'Selected machine: M{selected_machine}',
            machine=selected_machine  # Assign selected machine
        )

        # Redirect to the complaint_selection page with the selected machine number
        return redirect('emp:complaint_selection', page_id=selected_machine)

    return redirect('emp:machine_selection')

def complaint_selection(request, page_id):
    context = {
        'page_id': page_id,
        'complaints': range(1, 13)  # This creates a list of numbers from 1 to 12
    }
    return render(request, 'emp/complaint_selection.html', context)

def employee_selection(request):
    if request.method == "POST":
        # Get the username from hidden input field after employee selection
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # Authenticate the user with the provided password
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                # Log in the user and redirect to the machine selection page
                login(request, user)
                request.session.pop('logged_out_employee_username', None)  # Clear the logged_out_employee_username variable
                return HttpResponseRedirect(reverse("emp:machine_selection"))
            else:
                return HttpResponse("User is not active")
        else:
            # Show error if authentication fails
            messages.error(request, "Invalid password. Please try again.")
            return HttpResponseRedirect(reverse("emp:employee_selection"))

    # Fetch all employees to display in the profile selection page
    employees = Employee.objects.all()
    logged_out_employee_username = request.session.get('logged_out_employee_username', None)
    return render(request, 'emp/employee_selection.html', {
        'employees': employees,
        'logged_out_employee_username': logged_out_employee_username
    })

def logout_and_redirect(request):
    # Get the username of the logged-out employee and store it in the session
    logged_out_employee_username = request.user.username
    request.session['logged_out_employee_username'] = logged_out_employee_username

    # Perform the logout
    logout(request)
    return redirect('emp:employee_selection')
import json


def save_complaint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            complaint = data.get('complaint')
            issue = data.get('issue')

            # Assuming you're retrieving the current employee's work session
            employee = Employee.objects.get(user=request.user)
            work_session = WorkSession.objects.filter(employee=employee, end_time__isnull=True).last()

            if work_session:
                work_session.complaint = complaint
                work_session.issue = issue
                work_session.confirmed = True  # Set confirmation status to true
                work_session.save()

                return JsonResponse({'status': 'success', 'message': 'Complaint saved successfully!'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'No active work session found.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON data.'})
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found.'})

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
