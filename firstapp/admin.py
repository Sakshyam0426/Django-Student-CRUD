from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'email', 'phone', 'enrolled_data']

admin.site.register(Student, StudentAdmin)