from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Answer, Question

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean_login(self):
        return self.cleaned_data['login'].lower().strip()


class RegisterForm(forms.ModelForm):
    login = forms.CharField(label='Логин', error_messages={'required': 'Это поле обязательно'})
    email = forms.EmailField(label='Адрес электронной почты', error_messages={'required': 'Это поле обязательно'})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', error_messages={'required': 'Это поле обязательно', 'min_length': 'Пароль должен содержать не менее 8 символов', 'max_length': 'Пароль слишком длинный'}, min_length=8, max_length=20)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля', error_messages={'required': 'Это поле обязательно', 'min_length': 'Пароль должен содержать не менее 8 символов', 'max_length': 'Пароль слишком длинный'}, min_length=8, max_length=20)    

    class Meta:
        model = User
        fields = ('login', 'email', 'password')

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise ValidationError('Пароли не совпадают')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['login']
        
        user.set_password(self.cleaned_data['password'])

        user.save()

        return user
    
class AnswerForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш ответ'}), label='Ваш ответ', error_messages={'required': 'Это поле обязательно'})
 
    class Meta:
        model = Answer
        fields = ('body',)    

class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Тема вопроса', error_messages={'required': 'Это поле обязательно', 'max_length': 'Тема слишком длинная'}, max_length=50)
    body = forms.CharField(label='Текст вопроса', error_messages={'required': 'Это поле обязательно'}, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите ваш вопрос'}))
    tags = forms.CharField(label='Тэги', error_messages={'required': 'Это поле обязательно'}, widget=forms.Textarea(attrs={'class': 'text-area', 'rows': 1,'placeholder': 'Введите ваши тэги'}))

    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')