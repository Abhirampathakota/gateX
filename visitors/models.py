from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    label = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.start_time} - {self.end_time})"


class Student(models.Model):
    # Link to Login System (optional)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        # AUTO-GENERATE USER CREDENTIALS
        if not self.user:
            # Check if user already exists to avoid errors
            if not User.objects.filter(username=self.roll_number).exists():
                new_user = User.objects.create_user(username=self.roll_number, password=self.roll_number)
                new_user.first_name = f"Student {self.roll_number}"
                new_user.save()
                self.user = new_user
            else:
                self.user = User.objects.get(username=self.roll_number)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.roll_number} ({self.department})"


class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved (Show QR)'),
        ('INSIDE', 'Checked In'),
        ('COMPLETED', 'Checked Out'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.TextField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)

    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.roll_number} - {self.status}"