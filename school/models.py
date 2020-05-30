from django.db import models

# Create your models here.
class Grade(models.Model):
    grade = models.PositiveIntegerField()

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
        return str(self.variant)

class Question(models.Model):
    question = models.ImageField(upload_to='questions',blank=True)
    trueanswer = models.TextField(blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Student(models.Model):
    name = models.CharField('Name', max_length = 30,)
    surname = models.CharField('Name', max_length = 30,)
    documents = models.ImageField(upload_to='documents',blank=True)
    email = models.CharField('email', max_length = 70,)
    phone = models.CharField('phone', max_length = 15,)
    result = models.PositiveIntegerField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        # return self.name + " " + self.surname
        return str(self.id)

class Answer(models.Model):
    BOOL_CHOICES_RIGHT = ((True, 'Right'), (False, 'Wrong'))

    answer = models.TextField(blank=True)
    right = models.BooleanField(default=False, choices = BOOL_CHOICES_RIGHT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
