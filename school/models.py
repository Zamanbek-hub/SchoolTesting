from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Grade(models.Model):
    grade = models.PositiveIntegerField()
    duration = models.DurationField(blank=True, default=0)

    def __str__(self):
        return str(self.grade)

class Subject(models.Model):
    subject = models.CharField('Subject', max_length = 100,)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

class Variant(models.Model):
    variant = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.variant



class Teacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.create)

    def __str__(self):
        return 'teacher'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, default=User.objects.create)
    school = models.CharField('school', max_length = 40,blank=True)
    phone = models.CharField('phone', max_length = 16,blank=True)
    result = models.CharField('result', max_length = 4,blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    start = models.DateTimeField(default='SOME STRING')
    
    def __str__(self):
        return self.user.first_name


class Question(models.Model):
    question = models.ImageField(upload_to='questions',blank=True)
    variant = models.ForeignKey(Variant, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.id)

class Answer(models.Model):
    answer = models.TextField(blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer
        

class Testing(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
