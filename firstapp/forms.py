from django import forms
from .models import Student
import re

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'email', 'phone', 'address', 'date_of_birth', 'gender', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student ID'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError("Name should only contain letters and spaces.")
        return name.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\d{7,15}$', phone):
            raise forms.ValidationError("Phone number must be 7-15 digits only.")
        return phone

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        qs = Student.objects.filter(student_id=student_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This Student ID is already in use.")
        return student_id