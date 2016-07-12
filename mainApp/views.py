from django.shortcuts import render
from mainApp.models import Films


def main(request):
    return render(request, 'index.html', {'films': Films.objects.all()})