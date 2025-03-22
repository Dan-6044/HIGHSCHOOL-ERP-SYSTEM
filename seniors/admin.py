from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_class', 'category', 'birth_date')
    search_fields = ('full_name', 'student_class', 'category')


from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subjects', 'class_teacher', 'category', 'enroll_date')
    search_fields = ('full_name', 'email', 'subjects', 'class_teacher', 'category')
    list_filter = ('class_teacher', 'category', 'enroll_date')
    ordering = ('-enroll_date',)
