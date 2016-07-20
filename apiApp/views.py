from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.template.context_processors import csrf
from django.template import loader
from django.shortcuts import get_object_or_404

from mainApp.models import Films, Categories
from mainApp.forms import FilmForm, CategoryForm


def __get_lists(request, model, filter_name='name'):
    list = model.objects.all()

    search = request.GET.get('search', False)
    if search:
        list = list.filter(**{
            filter_name+'__icontains': search
        })

    filter = request.GET.get('filter', False)
    if filter and (filter == 'F' or filter == 'T'):
        list = list.filter(is_active=(True if filter == 'T' else False))

    sortBy = request.GET.get('sortBy', False)
    if sortBy:
        if request.GET.get('sortDir', False) == 'desc':
            sortBy = '-'+sortBy
            list = list.order_by(sortBy)

    paginator = Paginator(list, request.GET.get('pageSize', 50))
    page = request.GET.get('page', 1)
    pages = paginator.num_pages

    try:
        elems = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не определена, или не число то запрашиваем первую
        elems = paginator.page(1)
    except EmptyPage:
        elems = paginator.page(paginator.num_pages)

    return elems, pages

# region Main
@user_passes_test(lambda u: u.is_superuser)
def active_elem(request, id, model, active=True):
    res = _fail()

    user = model.objects.get(id=id)
    if user:
        user.is_active = active
        user.save()

        res = _success()
    return res


@user_passes_test(lambda u: u.is_superuser)
def get_list(request, model, filter_name='name'):
    elems, pages = __get_lists(request, model, filter_name)
    res = _success(result=[model_to_dict(elem) for elem in elems], count=len(elems), pages=pages)
    return res


@user_passes_test(lambda u: u.is_superuser)
def elem_create(request, form, model):
    def get_field_name(form, code):
        return str(form.fields[code].label)
    res = _fail()

    if request.method == 'POST' and request.is_ajax():
        elem_id = request.POST.get('id', False)
        if not int(elem_id):
            elem = form(request.POST)
        else:
            elem = get_object_or_404(model, id=elem_id)
            elem = form(request.POST, instance=elem)
        if elem.is_valid():
            elem.save()
            res = _success()
        else:
            res = _fail(
                errors= elem.errors,
                fields_error = {key: get_field_name(elem, key) for key in elem.errors}
            )

    return res


@user_passes_test(lambda u: u.is_superuser)
def get_form(request, model, form, tpl="inc-form"):
    res = _fail()

    if request.method == 'POST' and request.is_ajax():
        id = request.POST.get('id', 0)
        try:
            elem = model.objects.get(id=id)
        except:
            elem = False

        _form = form(instance=(elem if elem else None))
        context = {'form': _form}

        context['id'] = id
        context.update(csrf(request))
        html = loader.render_to_string('admin/'+tpl+'.html',
                                       context)

        res = _success(html=html)
        return res
    raise Http404
# endregion


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

    elems, pages = __get_lists(request, User, 'username')
    res = _success(result=[mark_i_am(user) for user in elems], count=len(elems), pages=pages)
    return res


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