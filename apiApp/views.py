from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
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


#@user_passes_test(lambda u: u.is_superuser)
def lists(request):
    res = _fail()

    users_list = User.objects.all()

    search = request.GET.get('search', False)
    if search:
        users_list = users_list.filter(username__contains=search)

    filter = request.GET.get('filter', False)
    if filter and (filter == 'F' or filter == 'T'):
        users_list = users_list.filter(is_active=(True if filter == 'T' else False))

    sortBy = request.GET.get('sortBy', False)
    if sortBy:
        if request.GET.get('sortDir', False) == 'desc':
            sortBy = '-'+sortBy
            users_list = users_list.order_by(sortBy)

    paginator = Paginator(users_list, request.GET.get('pageSize', 50))
    page = request.GET.get('page', 1)
    pages = paginator.num_pages

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не определена, или не число то запрашиваем первую
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    res = _success(result=[model_to_dict(user) for user in users], count=len(users), pages=pages)
    return res


#@user_passes_test(lambda u: u.is_superuser)
def delete(request, id):
    res = _fail()

    user = User.objects.get(id=id)
    if user:
        user.is_active = False
        user.save()

        res = _success()
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