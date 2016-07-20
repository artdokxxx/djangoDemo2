from django.shortcuts import render, redirect
from mainApp.models import Films
from mainApp.forms import RegistrationForm
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    films = Films.objects.all()

    paginator = Paginator(films, request.GET.get('pageSize', 9))
    page = request.GET.get('page', 1)

    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не определена, или не число то запрашиваем первую
        films = paginator.page(1)
    except EmptyPage:
        films = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'films': films})


@csrf_protect
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        context = {'form': form}
    else:
        context = {'form': RegistrationForm()}
    return render(request, 'user/registration.html', context)
