import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.contrib import messages
from django.template import Context
from XMLparser import MuseoParser
from models import Museo

# Create your views here.

def info_museo(request, id):
    try:
        museo = Museo.objects.get(id=id)
        context ={
            'museo':museo
        }
        return render(request, 'museo.html',context)
    except:
        value = "Museo no disponible"
        value += '<br><a href="/">Home</a>'
        return HttpResponseRedirect(value)

def accesibles(request):
    lista = Museo.objects.filter(accesibilidad=1)
    context ={
        'museos':lista,
        'accesibles':True
    }
    return render(request, 'index.html',context)
def cargar(request):
    museos = Museo.objects.all()
    parse = MuseoParser()
    parse.cargar()
    return HttpResponseRedirect("/")

def home(request):
    museos = Museo.objects.all()
    museos = museos[:5]
    context ={
        'museos':museos
    }
    return render(request, 'index.html',context)

@csrf_exempt
def registro (request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('repeat_password')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            if not username or not password or not password2 or not nombre or not apellido:
                context ={
                    'error': "Rellena todos los campos"
                }
                return render(request, 'registro.html',context)
            try:
                User.objects.get(username=username)
                context ={
                    'error': "Este username ya existe"
                }
                return render(request, 'registro.html',context)
            except:
                pass
            if password == password2:
                user = User.objects.create_user(username=username,
                                                    password=password,
                                                    first_name=nombre,
                                                    last_name=apellido
                                                    )
                user.save()
                messages.success(request, "Usuario creado con exito")
            else:
                context ={
                    'error': "Tus claves no son iguales"
                }
                return render(request, 'registro.html',context)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'registro.html')

def user_login(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print ("HOLLLLAAA" +str(username))
            if not username or not password:
                return HttpResponseRedirect('/')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                value = "Credenciales Invalidos"
                value += '<br><a href="/">Home</a>'
                return HttpResponse(value)
    return HttpResponseRedirect('/')

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/')
    else:
        value = '<a href="/">Home</a>'
    return HttpResponse(value)

def notFound(request):
    value = "Recurso no disponible"
    value += '<br><a href="/">Home</a>'
    return HttpResponse(value)
