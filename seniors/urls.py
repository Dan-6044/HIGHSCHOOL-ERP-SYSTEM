from django.urls import path
from . import views

urlpatterns = [
    path('admin', views.admin, name='admin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('sattendance', views.sattendance, name='sattendance'),
    path('steachers', views.steachers, name='steachers'),
    path('sstudents', views.sstudents, name='sstudents'),
    path('sresult', views.sresult, name='sresult'),
    path('sadminFee', views.sadminFee, name='sadminFee'),
   
    path('accessin/', views.accessin, name='accessin'),
    path('accessup/', views.accessup, name='accessup'),
    path('logoutz/', views.logouts_view, name='logoutz'),
]
