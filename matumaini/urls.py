from django.urls import path
from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('sdashboard', views.sdashboard, name='sdashbaord'),
    path('enroll/', views.enroll, name='enroll'),
    path('assignment/', views.assignment, name='assignment'),
    path('classes/', views.classes, name='classes'),
    path('result/', views.result, name='result'),
    path('fee/', views.fee, name='fee'),
    path('adminFee/', views.adminFee, name='adminFee'),
    path('attendance/', views.attendance, name='attendance'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
