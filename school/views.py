from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator
from .serializer import *
from django.http import JsonResponse
import random
import datetime
from django.utils import timezone
from django.utils.timezone import utc
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import authenticate, login


# Create your views here.


def check(request):
    student = Student.objects.get(id=1)
    question = Question.objects.get(id=1)
    # return HttpResponse(student.documents.url)
    return render(request, 'school/check.html', {'student': student, 'question': question})


def index(request):
    return render(request, 'school/index.html')


def new(request):
    return render(request, 'school/new.html')


def rate(request):
    return render(request, 'school/rate.html')


def input(request):
    print(request.POST)
    return render(request, 'school/input.html')


def test(request):
    return render(request, 'school/testing.html')


def deadline(request):
    return render(request, 'school/deadline.html')


def sign_in(request):
    return render(request, 'school/sign_in.html')


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

        indexes = request.POST.get("indexes", None)
        answers = request.POST.get('answers', None)

        indexes = indexes[1:len(indexes)-1]
        indexes = indexes[1:len(indexes)-1]
        # indexes = indexes.translate({ord(']'): None})
        indexes = int(indexes)

        answers = answers[1:len(answers)-1]
        answers = answers[1:len(answers)-1]
        # answers = answers.replace('"', "'")
        # answers = answers.translate({ord(']'): None})
        # answers = answers.split(',')

        collection = {}
        collection[indexes] = answers

        for key, value in collection.items():
            if value != "":
                if Answer.objects.filter(question=Question.objects.get(id=key)).filter(student=Student.objects.get(id=student)).exists():
                    print("I am here")
                    pk1 = Question.objects.get(id=key)
                    pk2 = Student.objects.get(id=student)
                    answer = Answer.objects.filter(
                        question=pk1).filter(student=pk2).get()

                    answer.delete()

                    answer = Answer(answer=value, question=pk1, student=pk2)
                    answer.save()
                else:
                    # print("key =", key, "value =", value)
                    answer = Answer(answer=value, question=Question.objects.get(
                        id=key), student=Student.objects.get(id=student))
                    answer.save()

        serializer = QuestionModelSerializer(paginatorr.page(
            page_n).object_list, many=True)  # sending as json

        hours, minutes, seconds = calculate_time(
            Student.objects.get(id=student))

        if(hours == -1 and minutes == -1 and seconds == -1):
            print("Timerrrr")
            response = JsonResponse({"error": "there was an error"})
            response.status_code = 403  # To announce that the user isn't allowed to publish
            return response

        return JsonResponse(serializer.data, safe=False)

    page_range_to_list = list(page_range)

    filled_answers = []
    for i in page_range_to_list:

        if Answer.objects.filter(question=questions[i - 1]).filter(student=student).exists():
            check = AnswerCheck(
                page=i, id_answer=questions[i-1].id, answer=True)
        else:
            check = AnswerCheck(
                page=i, id_answer=questions[i-1].id, answer=False)

        filled_answers.append(check)

    subjects = Subject.objects.filter(grade=Grade.objects.get(id=grade))
    # print(filled_answers)
    hours, minutes, seconds = calculate_time(Student.objects.get(id=student))

    if(hours == -1 and minutes == -1 and seconds == -1):
        print("deadlinee")
        return HttpResponseRedirect(reverse_lazy('deadline',))

    context = {
        'paginatorr': paginatorr,
        'first_page': first_page,
        'page_range': page_range,
        'subjects': subjects,
        'filled_answers': filled_answers,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'grade': grade,
        'student': student,
    }

    print(type(hours))

    return render(request, 'school/ajax.html', context)


def serial_answers(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id', None)
        student_id = int(request.POST.get('student_id', None))
        print("student_id = ", student_id)
        print("question_id = ", question_id)
        question_id = int(question_id.translate({ord('"'): None}))

        filledAnswers = []

        try:
            # filledAnswers.append(Answer.objects.get(question=int(
            #     question)), student=Student.objects.get(id=student_id))
            answer = Answer.objects.get(question=Question.objects.get(
                id=question_id), student=Student.objects.get(id=student_id))
            print("Answer : ", answer)
            filledAnswers.append(answer)
        except:
            ans = Answer(answer="", question=Question.objects.get(
                id=question_id), student=Student.objects.get(id=student_id))
            filledAnswers.append(ans)

        serializer = AnswerModelSerializer(filledAnswers, many=True)

        return JsonResponse(serializer.data, safe=False)
    return HttpResponse("false")


def formatting_time(duration):
    seconds = duration.seconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return hours, minutes, seconds


def calculate_time(student):
    time = timezone.now() - student.start
    grade = student.grade
    difference = grade.duration - time

    print("timeee:", time.seconds)

    if(time.seconds > grade.duration.seconds):
        return -1, -1, -1

    hours, minutes, seconds = formatting_time(difference)
    return hours, minutes, seconds


def testing_page(request, grade, student):
    # print("hereeeeeeeeeee")

    subjects = Subject.objects.filter(grade=Grade.objects.get(id=grade))
    print(subjects)

    hours, minutes, seconds = calculate_time(Student.objects.get(id=student))

    if request.method == 'POST':
        selected_subject = int(request.POST.get('selected_subject', None))
        hidden_id = request.POST.get('hidden_id', None)
        hidden_answer = request.POST.get('hidden_answer', None)
        print("hidden_id:", hidden_id)
        print("hidden_answer:", hidden_answer)
        print("student_id:", student)

        if hidden_answer != "":
            if hidden_answer != "" and hidden_id != "":
                hidden_id = int(hidden_id)

                if Answer.objects.filter(question=Question.objects.get(id=hidden_id)).filter(student=Student.objects.get(id=student)).exists():

                    pk1 = Question.objects.get(id=hidden_id)
                    pk2 = Student.objects.get(id=student)
                    answer = Answer.objects.filter(
                        question=pk1).filter(student=pk2).get()

                    answer.delete()
                    print("samee")

                answer = Answer(answer=hidden_answer,
                                question=Question.objects.get(id=hidden_id), student=Student.objects.get(id=student))
                answer.save()
                print("sameeee2")

        variant = Testing.objects.filter(
            student=student, subject=selected_subject).get().variant
        print(variant)
        # return reverse('pagination_p', kwargs={'subject': selected_subject})
        return HttpResponseRedirect(reverse_lazy('pagination_p', kwargs={'student': student, 'grade': grade, 'variant_of_subject': variant}))

    for subject in subjects:
        if Testing.objects.filter(student=Student.objects.get(id=student)).filter(subject=subject).exists():
            pass
        else:
            # testing = Testing.objects.filter(student=1).filter(subject = subject)
            # testing.delete()
            variants = Variant.objects.filter(subject=subject)
            random_variant = random.choice(variants)
            # print(random_variant)
            testing = Testing(student=Student.objects.get(
                id=student), subject=Subject.objects.get(id=subject.id), variant=random_variant)

            testing.save()

    if(hours == -1 and minutes == -1 and seconds == -1):
        return HttpResponseRedirect(reverse_lazy('deadline',))

    return render(request, 'school/ajax.html',
                  {'subjects': subjects,
                   'hours': hours,
                   'minutes': minutes,
                   'seconds': seconds,
                   'grade': grade,
                   'student': student, })


def sign_in_test(request):
    if request.method == 'POST':
        username = request.POST.get('username_phone', None)
        password = request.POST.get('password', None)

        check_if_user_exists = User.objects.filter(
            username=username).exists()

        print(check_if_user_exists)

        if check_if_user_exists:

            print("gjlkjh;lj;")
            # a = login(username="+7 (708)-050-52-67", password="just")
            # print(a)
            user = authenticate(
                username=username, password=password)

            # a = login(username="+7 (708)-050-52-67", password="just")
            print(user)
            if user is not None:
                print("We are here")
                student = Student.objects.get(user=user)

                return HttpResponseRedirect(reverse_lazy('testing_page', kwargs={'grade': student.grade.id, 'student': student.id}))

            else:
                raise Http404(
                    'Something maybe you entered the data incorrectly')

        else:
            raise Http404('Something maybe you entered the data incorrectly')


def create_user(request):
    # try:
    if request.method == 'POST':
        name = request.POST.get('fullname', None)
        school = request.POST.get('school', None)
        address = request.POST.get('address', None)
        phone = request.POST.get('phone', None)
        parents_phone = request.POST.get('parents_phone', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        print(password)

        user = User(username=phone, first_name=name,
                    email=email)
        user.set_password(password)
        user.save()

        student = Student(user=user, school=school, phone=phone, parents_phone=parents_phone,
                          grade=Grade.objects.get(id=1), address=address, start=timezone.now())
        student.save()

        return HttpResponseRedirect(reverse_lazy('testing_page', kwargs={'grade': 1, 'student': student.id}))

    return HttpResponse("sda")

    # except:
    #     raise Http404('Something maybe you entered the data incorrectly')


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
