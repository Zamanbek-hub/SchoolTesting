from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from .serializer import *
from django.http import JsonResponse

# Create your views here.
def check(request):
    student = Student.objects.get(id=1)
    question = Question.objects.get(id=1)
    # return HttpResponse(student.documents.url)
    return render(request, 'school/check.html', {'student':student, 'question':question})


def index(request):
    return render(request, 'school/index.html')



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

    return render (request, 'school/pagination.html', {'questions':questions})


def pagination_pro(request):
    #model
    questions = Question.objects.all().order_by('id')
    #number of items on each page
    number_of_item = 3
    #Paginator
    paginatorr = Paginator(questions,number_of_item)
    #query_set for first page
    first_page = paginatorr.page(1).object_list
    #range of page ex range(1, 3)
    page_range = paginatorr.page_range
    context = {
    'paginatorr':paginatorr,
    'first_page':first_page,
    'page_range':page_range
    }
    #
    
    if request.method == 'POST':
        # return HttpResponse('hellow')
        page_n = request.POST.get('page_n', None) #getting number of page
        
        answers = request.POST.get('answers', None) 
        answers = answers.translate({ord('"'):None})
        answers = answers.translate({ord('['):None})
        answers = answers.translate({ord(']'):None})
        answers = answers.split(',')

        collection = {}
        for i in range(len(answers)):
            if i % 2 == 0 and answers[i+1] != "":
                collection[answers[i]] = answers[i+1]
        print(collection)

        for key, value in collection.items():
            if Answer.objects.filter(question =  Question.objects.get(id = key)).exists() and Answer.objects.filter(student = Student.objects.get(id=1)).exists():
                
                p1 = Question.objects.get(id=key)
                p2 = Student.objects.get(id=1)
                answer = Answer.objects.filter(question=p1).filter(student=p2)
                # print("WE are here = " + answer._meta.get_field('answer'))
                # if answer._meta.get_field('answer') != value:
                   
                answer.delete()
                    # answer = Answer(answer = value, question = Question.objects.get(id=key), student = Student.objects.get(id=1))
                    # answer.save()
            # else:
            answer = Answer(answer = value, question = Question.objects.get(id=key), student = Student.objects.get(id=1))
            answer.save()
        # return HttpResponse(answer)
        #   article json
        # filledAnswers = []
        # filledAnswers.append(Answer.objects.get(id = 1))
        # filledAnswers.append(Answer.objects.get(id = 2))
        # filledAnswers.append(Answer.objects.get(id = 3))
        serializer = pagination_ser(paginatorr.page(page_n).object_list, many=True) #sending as json
        # serializer_2 = serializa_answer(filledAnswers,many=True)
        

        return JsonResponse(serializer.data,safe=False)
    return render(request, 'school/ajax.html',context)

def serial_answers(request):
    if request.method == 'POST':
        answers = request.POST.get('answers2', None) 
        answers = answers.translate({ord('"'):None})
        answers = answers.translate({ord('['):None})
        answers = answers.translate({ord(']'):None})
        answers = answers.split(',')

        print(answers)
        filledAnswers = []
        for item in answers:
            print(item)
            try:
                filledAnswers.append(Answer.objects.get(question = int(item)))
            except:
                ans = Answer(answer="", question = Question.objects.get(id=2), student = Student.objects.get(id=1))
                filledAnswers.append(ans)

        serializer_2 = serializa_answer(filledAnswers,many=True)
        print(serializer_2)
        return JsonResponse(serializer_2.data,safe=False)
    return HttpResponse("false")



def create_test(request):
    for i in range(4, 20):
        true_answer = str(i)
        image_path = 'questions/zvezda_chernyj_fon_svet_118237_4016x2881_1.jpg'
        question = Question(question = image_path, trueanswer = true_answer, variant = Variant.objects.get(variant = 1))
        question.save()
    return HttpResponse("yes")







def moderator(request):
    return render(request, 'school/moderator.html')