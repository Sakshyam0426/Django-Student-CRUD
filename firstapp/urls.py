from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('add/', views.student_add, name='student_add'),
    path('detail/<int:id>/', views.student_detail, name='student_detail'),
    path('edit/<int:id>/', views.student_edit, name='student_edit'),
    path('delete/<int:id>/', views.student_delete, name='student_delete'),
    path('students/bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('export/', views.export_csv, name='export_csv'),
    path('card/<int:id>/', views.student_card, name='student_card'),
    path('register/', views.register_view, name='register'),
    path('change-password/', views.change_password, name='change_password'),
]