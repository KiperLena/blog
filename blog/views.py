from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView #импорт классов
from .models import * #импорт самой модели
from .forms import * #импорт формы
from django.urls import reverse_lazy #куда перенапрявляется(как редирект в функциях)
from .utils import * #импорт утилс
from django.contrib.auth.mixins import LoginRequiredMixin #аналог декоратора неавторизированных пользователей
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm #форма для авторизации
from django.contrib.auth import login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse



class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)  # {'name': 'Наталья', 'email': 'natalia@gmail.com', 'content': 'Сообщение на сайт'}
        subject = "Message"
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'content': form.cleaned_data['content'],
        }
        message = "\n".join(body.values())
        try:
            send_mail(
                subject,
                message,
                form.cleaned_data['email'],
                ['admin@localhost']
            )
        except BadHeaderError:
            return HttpResponse('Найден некорректный заголовок')
        return redirect('index')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs): #готовый метод
        context = super().get_context_data(**kwargs) #переопределение готового метода(вызвали переменные из родитюкласса)
        c_def = self.get_user_context(title='Регистрация') #наследование от датамиксин в утилс
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class BlogHome( DataMixin, ListView): #наслеуемся от ListView
    model = Blog #модель
    template_name = 'blog/index.html' #свойство готовое из ListView
    context_object_name = 'posts' #так мы будем обращаться на штмл странице к моделе Блог

    def get_context_data(self, *, object_list=None, **kwargs): #готовый метод
        context = super().get_context_data(**kwargs) #переопределение готового метода(вызвали переменные из родитюкласса)
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        # context['menu'] = menu
        c_def = self.get_user_context(title='Главная страница') #наследование от датамиксин в утилс
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('cat')



class ShowPost(DataMixin, DetailView): #просмотр поста
    model = Blog
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs): #готовый метод
        context = super().get_context_data(**kwargs) #переопределение готового метода(вызвали переменные из родитюкласса)
        # context['title'] = context['post']
        # context['menu'] = menu
        c_def = self.get_user_context(title=context['post'])  # наследование от датамиксин в утилс
        return dict(list(context.items()) + list(c_def.items()))


class BlogCategory(DataMixin, ListView):
    model = Blog
    template_name = 'blog/index.html'  # свойство готовое из ListView
    context_object_name = 'posts'  # так мы будем обращаться на штмл странице к моделе Блог
    allow_empty = False #если элемент пустой


    def get_queryset(self):
        return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs): #готовый метод
        context = super().get_context_data(**kwargs) #переопределение готового метода(вызвали переменные из родитюкласса)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        # context['menu'] = menu
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория -' + str(c.name), cat_selected=c.pk)  # наследование от датамиксин в утилс
        return dict(list(context.items()) + list(c_def.items()))

class AddPage(LoginRequiredMixin, DataMixin, CreateView): #наследуемся от создание элементов
    form_class = AddPostForm  #готовые элементы
    template_name = 'blog/addpage.html' #где будет выводиться форма
    success_url = reverse_lazy('index') #куда перенапрявляем после заполнения формы
    login_url = reverse_lazy('index') #куда перенапрявляет если незарегистрированный пользователь


    def get_context_data(self, *, object_list=None, **kwargs): #готовый метод
        context = super().get_context_data(**kwargs) #переопределение готового метода(вызвали переменные из родитюкласса)
        # context['title'] = 'Добавление статьи'
        # context['menu'] = menu
        c_def = self.get_user_context(title='Добавление статьи') #наследование от датамиксин в утилс
        return dict(list(context.items()) + list(c_def.items()))
