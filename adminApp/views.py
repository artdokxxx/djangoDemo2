from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.template import loader
from django.http import JsonResponse, Http404
from mainApp.forms import RegistrationForm, UserChangeForm
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def main(request):
    return render(request, 'admin/index.html')


@user_passes_test(lambda u: u.is_superuser)
def users_list(request):
    return render(request, 'admin/users.html')


@user_passes_test(lambda u: u.is_superuser)
def get_user_form(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('id', False)
        try:
            user = User.objects.get(id=user_id)
        except:
            user = False

        if user:
            user_form = UserChangeForm(instance=user)
            context={
                'form': user_form,
                'id': user_id
            }
        else:
            user_form = RegistrationForm()
            context={
                'form': user_form
            }
        context.update(csrf(request))
        html = loader.render_to_string('admin/user_form.html',
                                       context)
        data = {'success': True, 'html': html}
        return JsonResponse(data)
    raise Http404


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    def get_field_name(form, code):
        return str(form.fields[code].label)

    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('id', False)
        if not user_id:
            user = RegistrationForm(request.POST)
        else:
            user = get_object_or_404(User, id=user_id)
            user = UserChangeForm(request.POST or None, instance=user)
        if user.is_valid():
            user.save()
            data = {'success': True}
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'errors': user.errors,
                'fields_error': {
                    key: get_field_name(user, key) for key in user.errors
                }
            }
            return JsonResponse(data)

    raise Http404


@user_passes_test(lambda u: u.is_superuser)
def films(request):
    return render(request, 'admin/films.html')