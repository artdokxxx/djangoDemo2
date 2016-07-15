from django.shortcuts import render, redirect
from mainApp.models import Films
from mainApp.forms import RegistrationForm
from django.views.decorators.csrf import csrf_protect


def main(request):
    return render(request, 'index.html', {'films': Films.objects.all()})


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
