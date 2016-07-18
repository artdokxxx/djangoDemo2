from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.http import JsonResponse
from mainApp.models import Films
from mainApp.forms import FilmForm
from django.template.context_processors import csrf
from django.template import loader


@csrf_protect
def sign_in(request):
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


@user_passes_test(lambda u: u.is_superuser)
def users_lists(request):
    def mark_i_am(user):
        user = model_to_dict(user)
        if user['id'] == request.user.id:
            user['i_am'] = True

        return user

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

    res = _success(result=[mark_i_am(user) for user in users], count=len(users), pages=pages)
    return res


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, id):
    res = _fail()

    user = User.objects.get(id=id)
    if user:
        user.is_active = False
        user.save()

        res = _success()
    return res


@user_passes_test(lambda u: u.is_superuser)
def user_activation(request, id):
    res = _fail()

    user = User.objects.get(id=id)
    if user:
        user.is_active = True
        user.save()

        res = _success()
    return res


# region Films
@user_passes_test(lambda u: u.is_superuser)
def films_list(request):
    res = _fail()

    films_list = Films.objects.all()

    search = request.GET.get('search', False)
    if search:
        films_list = films_list.filter(name__contains=search)

    filter = request.GET.get('filter', False)
    if filter and (filter == 'F' or filter == 'T'):
        films_list = films_list.filter(is_active=(True if filter == 'T' else False))

    sortBy = request.GET.get('sortBy', False)
    if sortBy:
        if request.GET.get('sortDir', False) == 'desc':
            sortBy = '-'+sortBy
            films_list = films_list.order_by(sortBy)

    paginator = Paginator(films_list, request.GET.get('pageSize', 50))
    page = request.GET.get('page', 1)
    pages = paginator.num_pages

    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не определена, или не число то запрашиваем первую
        films = paginator.page(1)
    except EmptyPage:
        films = paginator.page(paginator.num_pages)

    res = _success(result=[model_to_dict(elem) for elem in films], count=len(films), pages=pages)
    return res


@user_passes_test(lambda u: u.is_superuser)
def film_delete(request, id):
    res = _fail()

    elem = Films.objects.get(id=id)
    if elem:
        elem.is_active = False
        elem.save()

        res = _success()
    return res


@user_passes_test(lambda u: u.is_superuser)
def film_activation(request, id):
    res = _fail()

    elem = Films.objects.get(id=id)
    if elem:
        elem.is_active = True
        elem.save()

        res = _success()
    return res


@user_passes_test(lambda u: u.is_superuser)
def film_create(request):
    def get_field_name(form, code):
        return str(form.fields[code].label)
    res = _fail()

    if request.method == 'POST' and request.is_ajax():
        film = None
        film_id = request.POST.get('id', False)
        if not film_id:
            film = FilmForm(request.POST)
        else:
            film = FilmForm(request.POST or None, instance=film)
        if film.is_valid():
            film.save()
            res = _success()
        else:
            res = _fail(
                errors= film.errors,
                fields_error = {key: get_field_name(film, key) for key in film.errors}
            )

    return res


@user_passes_test(lambda u: u.is_superuser)
def film_form(request):
    res = _fail()

    if request.method == 'POST' and request.is_ajax():
        id = request.POST.get('id', False)
        try:
            film = Films.objects.get(id=id)
        except:
            film = False

        _form = FilmForm(instance=(film if film else None))
        context = {'form': _form}

        context['id'] = id
        context.update(csrf(request))
        html = loader.render_to_string('admin/film_form.html',
                                       context)

        res = _success(html=html)
        return res
    raise Http404


# End region

@csrf_protect
def logout(request):
    auth.logout(request)
    return _success()


def _fail(**kwargs):
    kwargs['success'] = False
    return JsonResponse(kwargs)


def _success(**kwargs):
    kwargs['success'] = True
    return JsonResponse(kwargs)