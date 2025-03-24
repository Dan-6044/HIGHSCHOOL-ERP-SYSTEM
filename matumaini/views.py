from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User


def student(request):
    return render(request, 'studentLandingPage.html')


from django.shortcuts import render, redirect
from django.db.models import Sum
from seniors.models import Student, Teacher, Fees, Timetable  

def sanitize_key(key):
    """Replaces dots and dashes with underscores to make keys template-safe."""
    return key.replace(".", "_").replace("-", "_")

def student_dashboard(request):
    # Ensure student is logged in
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_auth")  # Redirect if not authenticated

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect("student_auth")  # Redirect if student not found

    # Fetch student class
    student_class = student.student_class

    # Fetch total paid fees for the student
    total_paid_fees = Fees.objects.filter(student=student).aggregate(total_paid=Sum('paid_fees'))['total_paid']
    total_paid_fees = total_paid_fees if total_paid_fees else 0  # Default to 0 if no fees found

    # Fetch general school stats
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()

    # Define timetable structure
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = [
        "8.00-8.40", "8.40-9.20", "9.20-10.00", "10.00-10.40",
        "11.00-11.40", "11.40-12.20", "12.20-13.00",
        "14.00-14.40", "14.40-15.20", "15.20-16.00"
    ]
    
    timetable_data = {day: {sanitize_key(time): "" for time in time_slots} for day in days}

    # ✅ Fetch all timetable entries (without filtering by class)
    timetable_entries = Timetable.objects.all().order_by('day', 'time')

    for entry in timetable_entries:
        sanitized_time = sanitize_key(entry.time)
        timetable_data[entry.day][sanitized_time] = f"{entry.subject} ({entry.teacher_no})"

    # Context to pass to template
    context = {
        "student_name": student.full_name,
        "student_class": student_class,  # ✅ Adding student_class to context
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_paid_fees": total_paid_fees,  # ✅ Adding total paid fees to context
        "timetable_data": timetable_data,
    }

    return render(request, "studentDashboard.html", context)





def enroll(request):
    return render(request, 'enroll.html')

def classes(request):
    return render(request, 'classes.html')


def assignment(request):
    return render(request, 'assignment.html')


from django.shortcuts import render, redirect
from seniors.models import Attendance, Student

def assignment(request):
    # Ensure student is logged in
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_auth")  # Redirect to login if not authenticated

    try:
        student = Student.objects.get(id=student_id)  # Get the logged-in student
    except Student.DoesNotExist:
        return redirect("student_auth")  # Redirect if student is not found

    # Fetch attendance records only for the authenticated student
    attendance_records = Attendance.objects.filter(student=student).order_by("-date")

    context = {
        "student_name": student.full_name,
        "attendance_records": attendance_records,
    }

    return render(request, "assignment.html", context)





from django.shortcuts import render, redirect
from django.contrib import messages
from seniors.models import Results, Student

def result(request):
    # Check if student is authenticated (session contains student data)
    student_id = request.session.get("student_id")
    student_name = request.session.get("student_name")
    student_reg_number = request.session.get("student_reg_number")

    if not student_id or not student_name or not student_reg_number:
        messages.error(request, "You are not authenticated. Please log in.")
        return redirect("student_auth")  # Redirect to login page

    try:
        student = Student.objects.get(id=student_id, full_name=student_name, reg_number=student_reg_number)
    except Student.DoesNotExist:
        messages.error(request, "Student record not found.")
        return redirect("student_auth")

    # Fetch student's results
    student_results = Results.objects.filter(student=student)

    # Organize results into a dictionary for easier template rendering
    student_info = {
        "name": student.full_name,
        "reg_number": student.reg_number,
        "class": student.student_class,
        "subjects": {}  # Store subjects and marks
    }

    for result in student_results:
        student_info["subjects"][result.subject] = result.marks  # Store subject marks

    return render(request, "result.html", {"student": student_info})


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('student')  # Redirect to the home page


from django.shortcuts import render, redirect
from django.db.models import Sum
from seniors.models import Student, Fees

def fee(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_auth")  # Redirect if not authenticated

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect("student_auth")  # Redirect if student not found

    # Fetch fees details
    expected_fees = 50000  # Example: Set expected fees manually or fetch from a model
    paid_fees = Fees.objects.filter(student=student).aggregate(total_paid=Sum('paid_fees'))['total_paid']
    paid_fees = paid_fees if paid_fees else 0
    unpaid_fees = expected_fees - paid_fees

    # Pass context
    context = {
        "student_name": student.full_name,
        "student_reg_number": student.reg_number,
        "student_class": student.student_class,
        "expected_fees": expected_fees,
        "paid_fees": paid_fees,
        "unpaid_fees": unpaid_fees,
    }

    return render(request, "fee.html", context)



def adminFee(request):
    return render(request, 'adminfees.html')

def attendance(request):
    return render(request, 'attendance.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from seniors.models import Student

def student_auth(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        reg_number = request.POST.get('reg_number')

        try:
            student = Student.objects.get(full_name=full_name, reg_number=reg_number)

            # Store student details in session
            request.session["student_id"] = student.id  # Store student ID for easy access
            request.session["student_name"] = student.full_name
            request.session["student_reg_number"] = student.reg_number
            request.session["student_class"] = student.student_class

            # Ensure session data is saved
            request.session.modified = True  

            # Debugging: Print stored session data
            print("Stored in Session:", request.session.get("student_id"), request.session.get("student_name"))

            return redirect("student_dashboard")  # Redirect to student dashboard
        except Student.DoesNotExist:
            messages.error(request, "Invalid Full Name or Registration Number.")
            return redirect("student_auth")  # Reload authentication page

    return render(request, "signing.html")


