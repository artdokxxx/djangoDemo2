from django.db import models
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import JsonResponse


@csrf_protect
def sign_in(request):
    # FIXME: Добавить try catch
    res = _fail()
    login = request.POST.get('login', None)
    pwd = request.POST.get('pwd', None)
    user = auth.authenticate(username=login, password=pwd)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            res = _success(username=login)
        else:
            res = _fail(err='Ваша учетная запись заблокирована')
    else:
        res = _fail(err='Ошибка входа')

    return res


@csrf_protect
def logout(request):
    # FIXME: Добавить try catch
    auth.logout(request)
    return _success()


def _fail(**kwargs):
    kwargs['success'] = False
    return JsonResponse(kwargs)


def _success(**kwargs):
    kwargs['success'] = True
    return JsonResponse(kwargs)