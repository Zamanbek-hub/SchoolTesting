from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def check(request):
    student = Student.objects.get(id=1)
    question = Question.objects.get(id=1)
    # return HttpResponse(student.documents.url)
    return render(request, 'school/check.html', {'student':student, 'question':question})
