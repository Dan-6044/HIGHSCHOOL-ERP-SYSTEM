from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    parents_name = models.CharField(max_length=255)
    reg_number = models.TextField()
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
    enroll_date = models.DateField()
    class_teacher = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name