from django import forms
from .models import * #импорт всех классов
from django.core.exceptions import ValidationError  #выброс исключения(свои ошибки)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rowa': 10, 'class': 'form-input'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана' #дополнение если например категория не заполнена в форме


    def clean_title(self): #служебное название
        title = self.cleaned_data['title'] #данные которые заполнятся в стоке title
        if len(title) > 100: #если длина больше 100 символов
            raise ValidationError('Длина превышает 100 символов')

        return title


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, label="Имя")
    email = forms.EmailField(label="Email")
    content = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()





















