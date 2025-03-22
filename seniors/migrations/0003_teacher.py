# Generated by Django 5.1.7 on 2025-03-22 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seniors', '0002_rename_background_student_reg_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subjects', models.CharField(max_length=255)),
                ('teacher_phone', models.CharField(max_length=15)),
                ('enroll_date', models.DateField()),
                ('class_teacher', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
    ]
