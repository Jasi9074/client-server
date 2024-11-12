from .models import Employee


def get_requested_employees():
    """Return a list of employees who requested a password reset and their passcodes."""
    return Employee.objects.filter(password_reset_requested=True).values(
        "name", "confirmation_passcode"
    )
