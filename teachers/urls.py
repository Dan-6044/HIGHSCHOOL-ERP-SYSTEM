from django.urls import path
from . import views  # Ensure views is imported

urlpatterns = [
    path('teachers', views.teachers, name='teachers'),
    path('tdashboard', views.tdashboard, name='tdashboard'),
    path('tenroll', views.tenroll, name='tenroll'),
    path('tclasses', views.tclasses, name='tclasses'),
    path('tattendance', views.tattendance, name='tattendance'),
     path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logouts/', views.logout_views, name='logouts'),

]
