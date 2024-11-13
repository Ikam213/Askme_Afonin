import copy
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'title': 'Title ' + str(i+1),
        'id': i,
        'text': 'This is the text of the question ' + str(i+1)
    } for i in range(30)
]

ANSWERS = [
    {
        'title': 'Title ' + str(i+1),
        'id': i,
        'text': 'This is the text of the answer ' + str(i+1)
    } for i in range(5)
]

TAG_QUESTIONS = [
    {
        'title': 'Title ' + str(i+1),
        'id': i,
        'text': 'This is the text of the question ' + str(i+1)
    } for i in range(8, 15)
]

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={ 'questions': page.object_list, 'page_obj': page })

def hot(request):
    HOT_QUESTIONS = copy.deepcopy(QUESTIONS)
    HOT_QUESTIONS.reverse()
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(HOT_QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html', context={ 'questions': page.object_list, 'page_obj': page })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def tags(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(TAG_QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'tags.html', context={ 'questions': page.object_list, 'page_obj': page })

def ask(request):
    return render(request, 'ask.html')

def question(request, question_id):
    one_question = QUESTIONS[question_id - 1]
    return render(request, 'question.html', context={'answers': ANSWERS, 'question': one_question})

def settings(request):
    return render(request, 'settings.html')
