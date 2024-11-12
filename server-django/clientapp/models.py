from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(self.user.id, filename)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    is_working = models.BooleanField(default=False)
    password_reset_requested = models.BooleanField(default=False)
    confirmation_passcode = models.CharField(max_length=6, null=True, blank=True)

    def generate_passcode(self):
        self.confirmation_passcode = str(random.randint(100000, 999999))
        self.password_reset_requested = True
        self.save()

    def __str__(self):
        return "{}".format(self.user.username)


class WorkSession(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    machine = models.CharField(max_length=10, blank=True, null=True)
    complaint = models.CharField(max_length=255, blank=True, null=True)
    issue = models.CharField(max_length=255, blank=True, null=True)
    confirmed = models.BooleanField(default=False)  # Add this to store confirmation status

    def __str__(self):
        return f"{self.employee.name} from {self.start_time} to {self.end_time if self.end_time else 'Ongoing'}"


    def duration(self):
        """Calculate duration of the work session in a readable format."""
        if self.end_time:
            duration = self.end_time - self.start_time
        else:
            duration = timezone.now() - self.start_time

        total_seconds = duration.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m"
