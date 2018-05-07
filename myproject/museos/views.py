import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from XMLparser import MuseoParser
from models import Museo

# Create your views here.

def cargar(request):
    museos = Museo.objects.all()
    parse = MuseoParser()
    parse.cargar()
    return HttpResponseRedirect("/")

def home(request):
    museos = Museo.objects.all()
    context ={
        'museos':museos
    }
    return render(request, 'index.html',context)

def user_login(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                return HttpResponseRedirect('/')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
    return HttpResponseRedirect('/')

def user_logout(request):
    if request.user.is_authenticated():
        value = "Logout " + str(request.user.username)
        logout(request)
        value += '<br><a href="/">Home</a>'
    else:
        value = '<a href="/">Home</a>'
    return HttpResponse(value)

def notFound(request):
    value = "Recurso no disponible"
    value += '<br><a href="/">Home</a>'
    return HttpResponse(value)
