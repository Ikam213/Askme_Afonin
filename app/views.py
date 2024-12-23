from typing import Final
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer, Tag, Profile
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from app.forms import LoginForm, RegisterForm, AnswerForm

all_tags: Final = Tag.objects.distinct().order_by('tag_title')

def index(request):
    questions = Question.objects.all()
    page, page_count = paginate(questions, request, 5)
    return render(request, 'index.html', {'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags })

def hot(request):
    hot_questions = Question.objects.order_by('-created_at')
    page, page_count = paginate(hot_questions, request, 5)
    return render(request, 'hot.html', {'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags  })

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('lo'))
    return render(request, 'signup.html', {'all_tags': all_tags, 'form': form})

def login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            form.add_error('login', 'Неправильный логин или пароль')
    return render(request, 'login.html', {'all_tags': all_tags, 'form': form})

def tags(request, tag_title):
    tag = get_object_or_404(Tag, tag_title = tag_title)
    tag_questions = Question.objects.filter(tags=tag)
    page, page_count = paginate(tag_questions, request, per_page=5)
    return render(request, 'tags.html', {'current_tag_name': tag_title, 'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags  })

@login_required
def ask(request):
    return render(request, 'ask.html', {'all_tags': all_tags})

def question(request, question_id):
    one_question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=one_question)
    page, page_count = paginate(answers, request, 5)
    form = AnswerForm
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            new_answer = form.save(commit=False)
            new_answer.user = user_profile
            new_answer.question = one_question
            new_answer.save()
            return redirect(reverse('question', args=[question_id]))
    return render(request, 'question.html', {'question': one_question, 'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags, 'form': form  })

@login_required
def settings(request):
    return render(request, 'settings.html', {'all_tags': all_tags})

def paginate(object_list, request, per_page):
    paginator = Paginator(object_list, per_page)
    
    try:
        current_page_number = request.GET.get("page", 1)
        page = paginator.page(current_page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page, paginator.num_pages

def logout(request):
    auth.logout(request)
    return redirect(('index'))
