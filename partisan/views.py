from django.shortcuts import render
from django.http import HttpResponse
from django_project import settings

def home(request):
  return HttpResponse('<h1>Hello Wisdfasdfs</h1><strong>sec: ' + settings.SECRET_KEY)

