from django.urls import path
from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # Fixed name
    path('enroll/', views.enroll, name='enroll'),
    path('assignment/', views.assignment, name='assignment'),
    path('classes/', views.classes, name='classes'),
    path('result/', views.result, name='result'),
    path('fee/', views.fee, name='fee'),
    path('adminFee/', views.adminFee, name='adminFee'),
    path('attendance/', views.attendance, name='attendance'),
    path('student_auth/', views.student_auth, name='student_auth'),
        path('logout/', views.logout_view, name='logout'),
]
