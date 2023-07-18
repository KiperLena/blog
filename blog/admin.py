from django.contrib import admin
from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from django.utils.safestring import mark_safe #импорт для предпросмотра картинок в админской странице

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    prepopulated_fields = {'slug': ('title',)} #параметр для перевода названия в слаг
    list_display = ('id', 'title', 'time_created', 'get_html_photo', 'is_published') #список отображаемых элементов в админ панели
    list_display_links = ('id', 'title') #чтобы эти строки были кликабельны и можно было по нимм зайти в запись
    search_fields = ('title', 'content') #поиск в админке
    list_filter = ('is_published', 'time_created')#список фильтра
    list_editable = ('is_published', ) #редактируем автоматически на странице админа(галочки) не заходя в конкретную запись
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_created', 'time_update')
    readonly_fields = ('get_html_photo', 'time_created', 'time_update') #вывод данных нередактируемых
    save_on_top = True


    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width='50'>")

    get_html_photo.short_description = "Миниатюра" #как будет называться столбец в админке на русском языке

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # поиск в админке


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_header = "Админ-панель блога"
admin.site.site_title = "Админ-панель блога"
