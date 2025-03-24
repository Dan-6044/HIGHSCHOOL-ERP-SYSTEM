from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    parents_name = models.CharField(max_length=255)
    reg_number = models.CharField(max_length=50, unique=True)
    parents_phone = models.CharField(max_length=15)
    birth_date = models.DateField()
    student_class = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subjects = models.CharField(max_length=255)
    teacher_phone = models.CharField(max_length=15)
    teacher_number = models.CharField(max_length=50, unique=True)
    class_teacher = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name
    

from django.db import models

class Fees(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="fees")
    expected_fees = models.IntegerField()
    paid_fees = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def unpaid_fees(self):
        return self.expected_fees - self.paid_fees

    def __str__(self):
        return f"{self.student.full_name} - {self.unpaid_fees} Ksh Unpaid"

class Results(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="results")
    reg_number = models.CharField(max_length=50)  # Store reg number
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, related_name="teacher_results")
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    term = models.CharField(max_length=50)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically set the reg_number based on the student before saving."""
        if not self.reg_number:
            self.reg_number = self.student.reg_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} ({self.reg_number}) - {self.subject}: {self.marks} Marks"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[("Attended", "Present"), ("Not Attended", "Absent"), ("Late", "Late")])
    assignment_marks = models.IntegerField(null=True, blank=True)  # Added field
    term = models.CharField(max_length=20, choices=[("Term 1", "Term 1"), ("Term 2", "Term 2"), ("Term 3", "Term 3")])  # Added field
    subject = models.CharField(max_length=100, null=True, blank=True)  # Added field

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"

from django.db import models

class Timetable(models.Model):  # Make sure this is the correct model name
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)  # Ensure field name matches the database
    teacher_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subject} ({self.day} - {self.time})"
