from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Answer

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean_login(self):
        return self.cleaned_data['login'].lower().strip()


class RegisterForm(forms.ModelForm):
    login = forms.CharField(label='Логин', error_messages={'required': 'Это поле обязательно'})
    email = forms.EmailField(label='Адрес электронной почты', error_messages={'required': 'Это поле обязательно'})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', error_messages={'required': 'Это поле обязательно'})
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля', error_messages={'required': 'Это поле обязательно'})    

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