from typing import Final
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer, Tag, Profile
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from app.forms import LoginForm, RegisterForm, AnswerForm, QuestionForm
from django.shortcuts import resolve_url

all_tags: Final = Tag.objects.distinct().order_by('?')[:5]
top_members: Final = Profile.objects.distinct().order_by('?')[:5]

def index(request):
    questions = Question.objects.all()
    page, page_count = paginate(questions, request, 5)
    return render(request, 'index.html', {'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags, 'top_members': top_members})

def hot(request):
    hot_questions = Question.objects.order_by('-created_at')
    page, page_count = paginate(hot_questions, request, 5)
    return render(request, 'hot.html', {'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags, 'top_members': top_members})

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    next_url = request.GET.get('next', reverse('index'))
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        next_url = request.POST.get('next', reverse('index'))
        if form.is_valid():
            form.save()
            return redirect(next_url)
    return render(request, 'signup.html', {'all_tags': all_tags, 'form': form, 'next': next_url, 'top_members': top_members})

def login(request):
    next_url = request.GET.get('next', reverse('index'))
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next_url = request.POST.get('next', reverse('index'))
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(next_url)
            form.add_error('login', 'Неправильный логин или пароль')
    return render(request, 'login.html', {'all_tags': all_tags, 'form': form, 'next': next_url, 'top_members': top_members})

def tags(request, tag_title):
    tag = get_object_or_404(Tag, tag_title = tag_title)
    tag_questions = Question.objects.filter(tags=tag)
    page, page_count = paginate(tag_questions, request, per_page=5)
    return render(request, 'tags.html', {'current_tag_name': tag_title, 'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags, 'top_members': top_members})

@login_required(login_url='login')
def ask(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            new_question = form.save(commit=False)
            new_question.user = user_profile
            new_question.save()
            tags = form.cleaned_data['tags'].split(',')
            for tag_title in tags:
                tag, created = Tag.objects.get_or_create(tag_title=tag_title.strip())
                new_question.tags.add(tag)
            new_question.save()            
            return redirect('question', question_id=new_question.id)
    return render(request, 'ask.html', {'all_tags': all_tags, 'form': form, 'top_members': top_members})

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
            return redirect(f"{request.path}#answer-{new_answer.id}")
    return render(request, 'question.html', {'question': one_question, 'page': page, 'page_count': page_count, 'page_number': page.number, 'all_tags': all_tags, 'form': form, 'top_members': top_members})

@login_required
def settings(request):
    return render(request, 'settings.html', {'all_tags': all_tags, 'top_members': top_members})

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
