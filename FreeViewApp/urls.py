"""FreeViewApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from mainApp.views import *
import adminApp.views as admin
import apiApp.views as api

from django.contrib.auth.models import User
from mainApp.models import *
from mainApp.forms import *


urlpatterns = [
    url(r'^$', main, name='main_page')  #Главная страница
]

# Users
urlpatterns += [
    url(r'^user\/registration\/$', user_registration, name='registration'),  #Регистрация
]

# API
urlpatterns += [
    url(r'^api\/sign_in\/$', api.sign_in),  #Авторизация
    url(r'^api\/logout\/$', api.logout),  #Выход из учётной записи
    url(r'^api\/users\/delete\/(?P<id>\d+)\/$', api.active_elem, {'model': User, 'active': False}),  #Деактивация пользователя
    url(r'^api\/users\/activation\/(?P<id>\d+)\/$', api.active_elem, {'model': User}),  #Активация пользователя
    url(r'^api\/users\/get\/$', api.users_lists),  #Получение списка пользователей

    url(r'^api\/films\/delete\/(\d+)\/$', api.active_elem, {'model': Films, 'active': False}), # Деактивация пользователя
    url(r'^api\/films\/activation\/(\d+)\/$', api.active_elem, {'model': Films}), # Активация пользователя
    url(r'^api\/films\/get\/$', api.get_list, {'model': Films}), # Получение списка пользователей
    url(r'^api\/films\/form\/$', api.get_form, {'model': Films, 'form': FilmForm}), # Получение формы редактирования создания пользователя
    url(r'^api\/films\/change\/$', api.elem_create, {'model': Films, 'form': FilmForm}), # Создание/Изменение пользователя

    url(r'^api\/categories\/delete\/(\d+)\/$', api.active_elem, {'model': Categories, 'active': False}), # Деактивация категории
    url(r'^api\/categories\/activation\/(\d+)\/$', api.active_elem, {'model': Categories}), # Активация категории
    url(r'^api\/categories\/get\/$', api.get_list, {'model': Categories}), # Получение списка категорий
    url(r'^api\/categories\/form\/$', api.get_form, {'model': Categories, 'form': CategoryForm}), # Получение формы редактирования создания категории
    url(r'^api\/categories\/change\/$', api.elem_create, {'model': Categories, 'form': CategoryForm}), # Создание/Изменение категории
]


# ADMIN
urlpatterns += [
    url(r'^admin\/$', admin.main, name='dashboard'),  #Дашбоард
    url(r'^admin\/users\/$', admin.users_list, name='users'),  #Управление пользователями
    url(r'^admin\/users\/form\/$', admin.get_user_form),  #Получение формы редактирования создания пользователя
    url(r'^admin\/users\/change\/$', admin.create_user),  #Создание/Изменение пользователя
    url(r'^admin\/films\/$', admin.films, name='films'), #Управление фильмами
    url(r'^admin\/categories\/$', admin.categories, name='categories'), #Управление фильмами
]