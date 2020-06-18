from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator
from .serializer import *
from django.http import JsonResponse
import random


# Create your views here.


def check(request):
    student = Student.objects.get(id=1)
    question = Question.objects.get(id=1)
    # return HttpResponse(student.documents.url)
    return render(request, 'school/check.html', {'student': student, 'question': question})


def index(request):
    return render(request, 'school/index.html')

def rate(request):
    return render(request, 'school/rate.html')


def input(request):
    print(request.POST)
    return render(request, 'school/input.html')


def test(request):
    return render(request, 'school/testing.html')


def pagination(request):
    questions = Question.objects.all().order_by('id')

    paginator = Paginator(questions, 5)

    page = request.GET.get('page')

    questions = paginator.get_page(page)

    return render(request, 'school/pagination.html', {'questions': questions})


def pagination_pro(request, student, grade,  variant_of_subject):
    # model
    questions = Question.objects.filter(
        variant=variant_of_subject).order_by('id')
    # number of items on each page
    number_of_item = 1
    # Paginator
    paginatorr = Paginator(questions, number_of_item)
    # query_set for first page
    first_page = paginatorr.page(1).object_list
    # range of page ex range(1, 3)
    page_range = paginatorr.page_range

    #
    if request.method == 'POST':
        # return HttpResponse('hellow')
        page_n = request.POST.get('page_n', None)  # getting number of page

        answers = request.POST.get('answers', None)
        answers = answers.translate({ord('"'): None})
        answers = answers.translate({ord('['): None})
        answers = answers.translate({ord(']'): None})
        answers = answers.split(',')

        collection = {}
        for i in range(len(answers)):
            if i % 2 == 0 and answers[i+1] != "":
                collection[answers[i]] = answers[i+1]
        print(collection)

        for key, value in collection.items():
            if Answer.objects.filter(question=Question.objects.get(id=key)).filter(student=Student.objects.get(id=1)).exists():

                p1 = Question.objects.get(id=key)
                p2 = Student.objects.get(id=1)
                answer = Answer.objects.filter(question=p1).filter(student=p2)

                answer.delete()
                # answer = Answer(answer = value, question = Question.objects.get(id=key), student = Student.objects.get(id=1))
                # answer.save()
            # else:
            print("key =", key, "value =", value)
            answer = Answer(answer=value, question=Question.objects.get(
                id=key), student=Student.objects.get(id=1))
            answer.save()

        serializer = QuestionModelSerializer(paginatorr.page(
            page_n).object_list, many=True)  # sending as json

        return JsonResponse(serializer.data, safe=False)

    page_range_to_list = list(page_range)

    filled_answers = []
    for i in page_range_to_list:
        if Answer.objects.filter(question=questions[i - 1]).filter(student=student).exists():
            check = AnswerCheck(
                page=i, id_answer=questions[i-1].id, answer=True)
        else:
            check = AnswerCheck(
                page=i, id_answer=questions[i-1].id)
        filled_answers.append(check)
    subjects = Subject.objects.filter(grade=Grade.objects.get(grade=grade))
    # print(filled_answers)

    context = {
        'paginatorr': paginatorr,
        'first_page': first_page,
        'page_range': page_range,
        'subjects': subjects,
        'filled_answers': filled_answers,
    }

    return render(request, 'school/ajax.html', context)


def serial_answers(request):
    if request.method == 'POST':
        question = request.POST.get('question', None)
        question = int(question.translate({ord('"'): None}))

        filledAnswers = []

        try:
            filledAnswers.append(Answer.objects.get(question=int(question)))
        except:
            ans = Answer(answer="", question=Question.objects.get(
                id=question), student=Student.objects.get(id=1))
            filledAnswers.append(ans)

        serializer = AnswerModelSerializer(filledAnswers, many=True)

        return JsonResponse(serializer.data, safe=False)
    return HttpResponse("false")


def testing_page(request):
    subjects = Subject.objects.filter(grade=Grade.objects.get(grade=6))
    print(subjects)

    if request.method == 'POST':
        selected_subject = int(request.POST.get('selected_subject', None))
        print(selected_subject)
        variant = Testing.objects.filter(
            student=1, subject=selected_subject).get().variant
        print(variant)
        # return reverse('pagination_p', kwargs={'subject': selected_subject})
        return HttpResponseRedirect(reverse_lazy('pagination_p', kwargs={'student': 1, 'grade': 6, 'variant_of_subject': variant}))

    for subject in subjects:
        if Testing.objects.filter(student=1).filter(subject=subject):
            pass
        else:
            # testing = Testing.objects.filter(student=1).filter(subject = subject)
            # testing.delete()
            variants = Variant.objects.filter(subject=subject)
            random_variant = random.choice(variants)
            # print(random_variant)
            testing = Testing(student=Student.objects.get(
                id=1), subject=Subject.objects.get(id=subject.id), variant=random_variant)

            testing.save()
    return render(request, 'school/ajax.html', {'subjects': subjects})


def create_test(request):
    for z in range(1, 7):
        for i in range(0, 20):
            # true_answer = str(i)
            image_path = 'questions/zvezda_chernyj_fon_svet_118237_4016x2881_1.jpg'
            question = Question(
                question=image_path, variant=Variant.objects.get(id=z))
            question.save()
    return HttpResponse("yes")


def moderator(request):
    return render(request, 'school/moderator.html')
