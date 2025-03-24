from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User

def teachers(request):
    return render(request, 'teachersLandingPage.html')

from django.shortcuts import render
from django.db.models import Sum
from seniors.models import Student, Teacher, Fees, Timetable  # Import Timetable correctly

def sanitize_key(key):
    """Replaces dots and dashes with underscores to make keys template-safe."""
    return key.replace(".", "_").replace("-", "_")

def tdashboard(request):
    total_students = Student.objects.count()  # Count all students
    total_teachers = Teacher.objects.count()  # Count all teachers

    # Ensure the sum of paid_fees is numeric, handling possible string values
    total_paid_fees = Fees.objects.aggregate(total_paid=Sum('paid_fees'))['total_paid']
    
    if total_paid_fees is None:  # If no fees exist, default to 0
        total_paid_fees = 0

    # Timetable Data
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = [
        "8.00-8.40", "8.40-9.20", "9.20-10.00", "10.00-10.40",
        "11.00-11.40", "11.40-12.20", "12.20-13.00",
        "14.00-14.40", "14.40-15.20", "15.20-16.00"
    ]

    # Initialize timetable dictionary with sanitized keys
    timetable_data = {day: {sanitize_key(time): "" for time in time_slots} for day in days}

    # Retrieve and organize timetable entries
    timetable_entries = Timetable.objects.all().order_by('day', 'time')
    for entry in timetable_entries:
        sanitized_time = sanitize_key(entry.time)
        timetable_data[entry.day][sanitized_time] = f"{entry.subject} ({entry.teacher_no})"

    # Pass everything into the context
    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_paid_fees": total_paid_fees,
        "timetable_data": timetable_data,  # Added timetable data
    }

    return render(request, "tdashboard.html", context)


def tclasses(request):
    return render(request, 'tclasses.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from seniors.models import Student, Attendance, Teacher
from datetime import date

def tattendance(request):
    # Debugging: Print session data before using it
    print("Session Data in tattendance:", request.session.items())

    # Ensure teacher is authenticated via session
    teacher_email = request.session.get("teacher_email")
    teacher_number = request.session.get("teacher_number")

    if not teacher_email or not teacher_number:
        messages.error(request, "You must be logged in as a teacher.")
        return redirect("teacher_auth")  # Redirect to teacher login if not authenticated

    # Get the teacher object from session data
    teacher = get_object_or_404(Teacher, email=teacher_email, teacher_number=teacher_number)

    # Get class name from query parameters
    class_selected = request.GET.get("class_name")
    students = Student.objects.filter(student_class=class_selected) if class_selected else None
    
    if request.method == "POST":
        subject = request.POST.get("subject")  # Retrieve subject input

        for student in students:
            # Get submitted data
            attendance_date = request.POST.get(f"date_{student.id}", str(date.today()))
            assignment_marks = request.POST.get(f"assignmentresult_{student.id}")
            term = request.POST.get(f"term_{student.id}")
            status = request.POST.get(f"attendance_{student.id}")

            if status and assignment_marks and term:
                # Check if attendance already exists for the student and date
                existing_attendance = Attendance.objects.filter(
                    student=student,
                    date=attendance_date
                ).first()

                if existing_attendance:
                    # Update existing attendance
                    existing_attendance.status = status
                    existing_attendance.assignment_marks = assignment_marks
                    existing_attendance.term = term
                    existing_attendance.subject = subject
                    existing_attendance.teacher = teacher  # Update teacher if needed
                    existing_attendance.save()
                else:
                    # Create a new attendance record
                    Attendance.objects.create(
                        student=student,
                        reg_number=student.reg_number,
                        teacher=teacher,
                        status=status,
                        date=attendance_date,
                        assignment_marks=assignment_marks,
                        term=term,
                        subject=subject
                    )
        
        messages.success(request, "Attendance recorded successfully!")
        return redirect(request.path + f"?class_name={class_selected}")
    
    return render(request, "tattendance.html", {
        "students": students,
        "teacher": teacher,
        "class_selected": class_selected,
    })



def logout_views(request):
    logout(request)  # Logs out the user
    return redirect('teachers')  # Redirect to the home page

from django.contrib import messages
from django.shortcuts import render, redirect
from seniors.models import Teacher

def teacher_auth(request):
    if request.method == 'POST':
        teacher_number = request.POST.get('teacher_number')
        email = request.POST.get('email')

        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number, email=email)

            # Store teacher details in session
            request.session["teacher_name"] = teacher.full_name
            request.session["teacher_number"] = teacher.teacher_number
            request.session["teacher_email"] = teacher.email

            # Debugging: Print stored session data
            print("Stored in Session:", request.session.get("teacher_name"), request.session.get("teacher_email"))

            return redirect("tdashboard")  # Redirect to teacher dashboard
        except Teacher.DoesNotExist:
            messages.error(request, "Invalid Teacher Number or Email.")
    
    return render(request, "auth.html")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from seniors.models import Student, Results, Teacher

def tenroll(request):
    # Debugging: Print session data before using it
    print("Session Data in tenroll:", request.session.items())

    # Ensure teacher is authenticated via session
    teacher_email = request.session.get("teacher_email")
    teacher_number = request.session.get("teacher_number")

    if not teacher_email or not teacher_number:
        messages.error(request, "You must be logged in as a teacher.")
        return redirect("teacher_auth")  # Redirect to teacher login if not authenticated

    # Get the teacher object from session data
    teacher = get_object_or_404(Teacher, email=teacher_email, teacher_number=teacher_number)

    # Get class name from query parameters
    class_selected = request.GET.get("class_name")
    students = Student.objects.filter(student_class=class_selected) if class_selected else None

    if request.method == "POST":
        subject = request.POST.get("subject")
        
        if not subject:
            messages.error(request, "Please enter a subject.")
            return redirect(request.path + f"?class_name={class_selected}")

        for student in students:
            marks = request.POST.get(f"marks_{student.id}")
            term = request.POST.get(f"term_{student.id}")

            if marks:
                # Check if the result already exists for the student, subject, and term
                existing_result = Results.objects.filter(
                    student=student, 
                    subject=subject, 
                    term=term
                ).first()

                if existing_result:
                    # Update existing result
                    existing_result.marks = int(marks)
                    existing_result.teacher = teacher  # Update teacher if needed
                    existing_result.save()
                else:
                    # Create a new result entry
                    Results.objects.create(
                        student=student,
                        reg_number=student.reg_number,  # Store reg number
                        teacher=teacher,  # Use session-authenticated teacher
                        subject=subject,
                        marks=int(marks),
                        term=term
                    )

        messages.success(request, "Results saved successfully!")
        return redirect(request.path + f"?class_name={class_selected}")

    return render(request, "tenroll.html", {
        "students": students,
        "teacher": teacher,
        "class_selected": class_selected
    })
