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
    list_display = ('full_name', 'email', 'subjects', 'class_teacher', 'category', 'teacher_number')
    search_fields = ('full_name', 'email', 'subjects', 'class_teacher', 'category')
    list_filter = ('class_teacher', 'category', 'teacher_number')
    ordering = ('-teacher_number',)


from django.contrib import admin
from .models import Fees

class FeesAdmin(admin.ModelAdmin):
    list_display = ('student', 'expected_fees', 'paid_fees', 'created_at')  # Columns to show
    search_fields = ('full_name',)  # Allow searching by student name
    list_filter = ('created_at',)  # Filter by date

admin.site.register(Fees, FeesAdmin)


from django.contrib import admin
from .models import Results, Attendance

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ("student", "reg_number", "teacher", "subject", "marks", "term", "date_recorded")
    search_fields = ("student__full_name", "reg_number", "subject", "teacher__full_name")
    list_filter = ("subject", "term", "teacher")

    def get_queryset(self, request):
        """Ensure all results are shown in the admin panel."""
        return super().get_queryset(request).select_related("student", "teacher")

# Alternatively, you can register without the decorator:
# admin.site.register(Results, ResultsAdmin)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'subject', 'assignment_marks', 'term', 'status')
    list_filter = ('date', 'term', 'status')
    search_fields = ('student__full_name', 'subject')

from django.contrib import admin
from .models import Timetable  # Import the Timetable model

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'time', 'subject', 'teacher_no')  # Fields to display in the admin panel
    search_fields = ('day', 'subject', 'teacher_no')  # Enables search functionality
    list_filter = ('day', 'time')  # Adds filters for easier navigation
