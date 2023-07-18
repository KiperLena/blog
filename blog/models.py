from django.db import models
from django.urls import reverse #куда отправляем

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название") #название статьи
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL") # слаг
    content = models.TextField(blank=True, verbose_name="Контент")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото") #фото и куда будут они отправляться , в какую папку
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации") #дата создания , автоматически один раз\
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления") #дата создается фиксированным временем при изменении
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано") #опубликовано или нет.по умолчанию опубликовано
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta: #служебный класс
        verbose_name = "Новость" # перевод на русский на странице админа в единственом числе
        verbose_name_plural = "Новости" # перевод на русский на странице админа если много
        ordering = ['-time_created']



class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название") # название категории
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL") #слаг

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta: #служебный класс
        verbose_name = "Категория" # перевод на русский на странице админа в единственом числе
        verbose_name_plural = "Категории" # перевод на русский на странице админа если много






