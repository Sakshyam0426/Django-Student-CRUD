from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import StudentSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Student, ActivityLog
from .forms import StudentForm
from rest_framework.permissions import IsAuthenticated
import csv

# ─── AUTH VIEWS ───────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'firstapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            send_mail(
                subject='Welcome to Student Management System',
                message=f'Hi {username},\n\nYour account has been created successfully. You can now log in and get started.\n\nThanks!',
                from_email=None,
                recipient_list=[email],
                fail_silently=True,
            )

            messages.success(request, 'Account created! Please login.')
            return redirect('login')
    return render(request, 'firstapp/register.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect!')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match!')
        elif len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters!')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')
    return render(request, 'firstapp/change_password.html')

# ─── DASHBOARD ────────────────────────────────────────────

@login_required(login_url='login')
def dashboard(request):
    total_students = Student.objects.count()
    recent_students = Student.objects.order_by('-enrolled_data')[:5]
    male_count = Student.objects.filter(gender='M').count()
    female_count = Student.objects.filter(gender='F').count()
    other_count = Student.objects.filter(gender='O').count()

    context = {
        'total_students': total_students,
        'recent_students': recent_students,
        'male_count': male_count,
        'female_count': female_count,
        'other_count': other_count,
    }
    return render(request, 'firstapp/dashboard.html', context)

# ─── STUDENT LIST + SEARCH + PAGINATION + SORT ───────────

ALLOWED_SORT_FIELDS = ['name', 'student_id', 'email', 'enrolled_data']

@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')

    if sort not in ALLOWED_SORT_FIELDS:
        sort = 'name'

    if query:
        students = Student.objects.filter(
            name__icontains=query
        ) | Student.objects.filter(
            student_id__icontains=query
        ) | Student.objects.filter(
            email__icontains=query
        )
    else:
        students = Student.objects.all()

    if order == 'desc':
        students = students.order_by(f'-{sort}')
    else:
        students = students.order_by(sort)

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'firstapp/student_list.html', {
        'students': page_obj,
        'query': query,
        'page_obj': page_obj,
        'sort': sort,
        'order': order,
    })

# ─── ADD STUDENT ──────────────────────────────────────────

@login_required(login_url='login')
def student_add(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to add students.")
        return redirect('student_list')
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        student = form.save()
        ActivityLog.objects.create(
            user=request.user,
            action='ADD',
            student_name=student.name,
            details=f'Student ID: {student.student_id}'
        )
        messages.success(request, 'Student added successfully!')
        return redirect('student_list')
    return render(request, 'firstapp/student_add.html', {'form': form})

# ─── STUDENT DETAIL ───────────────────────────────────────

@login_required(login_url='login')
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'firstapp/student_detail.html', {'student': student})

# ─── EDIT STUDENT ─────────────────────────────────────────

@login_required(login_url='login')
def student_edit(request, id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to edit students.")
        return redirect('student_list')
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        ActivityLog.objects.create(
            user=request.user,
            action='EDIT',
            student_name=student.name,
            details=f'Student ID: {student.student_id}'
        )
        messages.success(request, f'{student.name} updated successfully!')
        return redirect('student_list')
    return render(request, 'firstapp/student_edit.html', {
        'form': form,
        'student': student
    })

# ─── DELETE STUDENT ───────────────────────────────────────

@login_required(login_url='login')
def student_delete(request, id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete students.")
        return redirect('student_list')
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        name = student.name
        student_id_num = student.student_id
        student.delete()
        ActivityLog.objects.create(
            user=request.user,
            action='DELETE',
            student_name=name,
            details=f'Student ID: {student_id_num}'
        )
        messages.success(request, f'{name} deleted successfully!')
        return redirect('student_list')
    return render(request, 'firstapp/student_confirm_delete.html', {
        'student': student
    })

# ─── BULK DELETE ──────────────────────────────────────────

@login_required(login_url='login')
def bulk_delete(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete students.")
        return redirect('student_list')

    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_students')
        if selected_ids:
            students_to_delete = Student.objects.filter(id__in=selected_ids)
            count = students_to_delete.count()
            for student in students_to_delete:
                ActivityLog.objects.create(
                    user=request.user,
                    action='DELETE',
                    student_name=student.name,
                    details=f'Student ID: {student.student_id} (bulk delete)'
                )
            students_to_delete.delete()
            messages.success(request, f'{count} student(s) deleted successfully!')
        else:
            messages.warning(request, 'No students were selected.')
    return redirect('student_list')

# ─── EXPORT CSV ───────────────────────────────────────────

@login_required(login_url='login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Student ID', 'Email', 'Phone', 'Address', 'Gender', 'Date of Birth', 'Enrolled Date'])

    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.name,
            student.student_id,
            student.email,
            student.phone,
            student.address,
            student.get_gender_display(),
            student.date_of_birth,
            student.enrolled_data,
        ])
    return response

# ─── PRINT STUDENT CARD ───────────────────────────────────

@login_required(login_url='login')
def student_card(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'firstapp/student_card.html', {'student': student})


# ─── API ENDPOINTS ─────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    serializer = StudentSerializer(student)
    return Response(serializer.data)