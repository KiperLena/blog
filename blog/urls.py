from django.urls import path
from .views import * #импортируем из вьюз все
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', BlogHome.as_view(), name='index'), #связь пути с классом обработчиком
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'), #связь пути с классом обработчиком
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'), #связь пути с классом обработчиком
    path('addpage/', AddPage.as_view(), name='add_page'), #добавить статью на странице
    path('register/', RegisterUser.as_view(), name='register'), #регистрация
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('contact/', ContactFormView.as_view(), name='contact'),
]






