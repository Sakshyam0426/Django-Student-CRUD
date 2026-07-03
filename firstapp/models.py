from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)  # ← added
    enrolled_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Added'),
        ('EDIT', 'Edited'),
        ('DELETE', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)