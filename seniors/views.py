from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User


def admin(request):
    return render(request, 'adminLandingPage.html')

from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Teacher, Fees

def dashboard(request):
    total_students = Student.objects.count()  # Count all students
    total_teachers = Teacher.objects.count()  # Count all teachers

    # Sum of paid fees, ensuring it doesn't return None
    total_paid_fees = Fees.objects.aggregate(total_paid=Sum('paid_fees'))['total_paid'] or 0

    # Fetching the latest 5 students and teachers
    students = Student.objects.all()[:5]  
    teachers = Teacher.objects.all()[:5]  

    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_paid_fees": total_paid_fees,
        "students": students,
        "teachers": teachers,
    }

    return render(request, "dashboard.html", context)



from django.shortcuts import render
from .models import Timetable

def sanitize_key(key):
    """Replaces dots and dashes with underscores to make keys template-safe."""
    return key.replace(".", "_").replace("-", "_")

def sattendance(request):
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

    return render(request, 'Sattendance.html', {'timetable_data': timetable_data})


    


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Teacher  
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sstudents(request):
    if request.method == "POST":
        full_name = request.POST.get('names')
        parents_name = request.POST.get('parents')
        reg_number = request.POST.get('reg_number')
        parents_phone = request.POST.get('phonenumber')
        birth_date = request.POST.get('date')
        student_class = request.POST.get('class')
        category = request.POST.get('category')

        # Save to the database
        Student.objects.create(
            full_name=full_name,
            parents_name=parents_name,
            reg_number=reg_number,
            parents_phone=parents_phone,
            birth_date=birth_date,
            student_class=student_class,
            category=category
        )

        return redirect('sstudents')

    return render(request, 'Sstudents.html')

@csrf_exempt
def steachers(request):
    if request.method == "POST":
        full_name = request.POST.get('names')
        email = request.POST.get('email')
        subjects = request.POST.get('subjects')
        teacher_phone = request.POST.get('phonenumber')
        teacher_number = request.POST.get('teachernumber')
        class_teacher = request.POST.get('class')
        category = request.POST.get('category')

        # Save to the database
        Teacher.objects.create(
            full_name=full_name,
            email=email,
            subjects=subjects,
            teacher_phone=teacher_phone,
            teacher_number=teacher_number,
            class_teacher=class_teacher,
            category=category
        )

        return redirect('steachers')

    return render(request, 'Steachers.html')





from django.shortcuts import render
from .models import Student, Results

def sresult(request):
    class_selected = request.GET.get('class_name', '')  # Get selected class from dropdown

    students = []
    if class_selected:  # If a class is selected, filter students using student_class
        students = Student.objects.filter(student_class=class_selected)

    results_data = []
    for student in students:
        student_results = Results.objects.filter(student=student)

        student_info = {
            'name': student.full_name,  # Assuming full_name is used instead of name
            'reg_number': student.reg_number,
            'subjects': {}
        }

        # Convert marks into grades
        for result in student_results:
            if result.marks < 40:
                grade = 'D'
            elif 40 <= result.marks < 60:
                grade = 'C'
            elif 60 <= result.marks < 80:
                grade = 'B'
            else:
                grade = 'A'

            student_info['subjects'][result.subject] = grade

        results_data.append(student_info)

    return render(request, 'Sresult.html', {
        'class_selected': class_selected,
        'students': results_data
    })



from django.shortcuts import render
from .models import Student, Fees

def sadminFee(request):
    students = Student.objects.all()
    
    def get_student_fees(student):
        fees = Fees.objects.filter(student=student).first()  # Get the first fees record
        expected_fees = fees.expected_fees if fees else 0
        paid_fees = fees.paid_fees if fees else 0
        unpaid_fees = expected_fees - paid_fees
        return {"student": student, "expected_fees": expected_fees, "paid_fees": paid_fees, "unpaid_fees": unpaid_fees}

    # Categorize students and calculate fees
    form_1_students = [get_student_fees(s) for s in students.filter(student_class__icontains="form 1")]
    form_2_students = [get_student_fees(s) for s in students.filter(student_class__icontains="form 2")]
    form_3_students = [get_student_fees(s) for s in students.filter(student_class__icontains="form 3")]
    form_4_students = [get_student_fees(s) for s in students.filter(student_class__icontains="form 4")]

    context = {
        "form_1_students": form_1_students,
        "form_2_students": form_2_students,
        "form_3_students": form_3_students,
        "form_4_students": form_4_students,
    }

    return render(request, "Sadminfees.html", context)



def logouts_view(request):
    logout(request)  # Logs out the user
    return redirect('admin')  # Redirect to the home page

def accessup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_id = user.id  # Get the user's ID

            # Log the user in automatically after registration
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to home after successful registration
        else:
            # Pass the form errors to the template
            return render(request, 'access.html', {'form': form, 'signup_errors': form.errors})

    else:
        form = SignupForm()

    return render(request, 'access.html', {'form': form})

def accessin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('accessin')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                auth_login(request, authenticated_user)
                return redirect(reverse('dashboard'))  # Redirect to dashboard
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'access.html')  # Ensure the correct template name


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Fees, Student

@csrf_exempt  # Required for AJAX requests
def submit_fees(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        expected_fees = request.POST.get("expected_fees")
        paid_fees = request.POST.get("paid_fees")

        try:
            student = get_object_or_404(Student, id=student_id)

            # Retrieve all fee records for the student
            fees_records = Fees.objects.filter(student=student)

            if fees_records.exists():
                # If multiple records exist, keep the first and delete the rest
                fees = fees_records.first()
                fees_records.exclude(id=fees.id).delete()
            else:
                # Create a new fee record if none exists
                fees = Fees(student=student)

            # Update the fee record
            fees.expected_fees = expected_fees
            fees.paid_fees = paid_fees
            fees.save()

            return JsonResponse({
                "success": True, 
                "message": "Fees updated successfully!" if fees_records.exists() else "Fees added successfully!"
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


from django.shortcuts import render, redirect
from .models import Timetable  # Make sure you import the correct model

def add_subject(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        time = request.POST.get('time')
        subject = request.POST.get('subject')  # Ensure field name matches the model
        teacher_no = request.POST.get('teacher_no')

        # Save subject to the database with the correct model
        Timetable.objects.create(day=day, time=time, subject=subject, teacher_no=teacher_no)

        return redirect('sattendance')  # Redirect to updated timetable

    return render(request, 'Sattendance.html')



