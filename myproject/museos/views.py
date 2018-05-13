#!/usr/bin/env python
# coding=utf-8
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
from models import Museo, Comentario

# Create your views here.
@csrf_exempt
def museos(request):
    distrito = ""
    if request.method == "POST":
        distrito = request.POST.get('distrito')
        print ("AAA"+str(distrito))
        if distrito == "TODOS":
            museos = Museo.objects.all()
        else:
            museos = Museo.objects.filter(distrito=distrito)

    else:
        museos = Museo.objects.all()
    distritos = Museo.objects.values_list('distrito').distinct()
    context ={
        'museos':museos,
        'distritos': distritos,
        'seleccionado': distrito
    }
    return render(request, 'museos.html',context)

@csrf_exempt
def comentario(request, id_museo):
    if request.method == "POST":
        if request.user.is_authenticated():
            usuario = request.user
            contenido = request.POST.get('contenido')
            try:
                museo = Museo.objects.get(id=id_museo)
            except:
                value = "Museo no disponible"
                value += '<br><a href="/">Volver</a>'
                return HttpResponse(value)
            if not contenido:
                value = "No hay comentario"
                value += '<br><a href="/">Volver</a>'
                return HttpResponse(value)
            comentario = Comentario()
            comentario.contenido = contenido
            comentario.museo = museo
            comentario.save()
            museo.numComentario = museo.numComentario + 1
            museo.save()
    return HttpResponseRedirect("/museos/"+str(id_museo))

def info_museo(request, id):
    try:
        museo = Museo.objects.get(id=id)
        comentarios = Comentario.objects.filter(museo=museo)
        context ={
            'museo':museo,
            'comentarios':comentarios
        }
        return render(request, 'museo.html',context)
    except:
        value = "Museo no disponible"
        value += '<br><a href="/">Volver</a>'
        return HttpResponse(value)

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
    museos = Museo.objects.filter( numComentario__gte = 1).order_by('numComentario')
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
                value += '<br><a href="/">Volver</a>'
                return HttpResponse(value)
    return HttpResponseRedirect('/')

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')

def notFound(request):
    value = "Recurso no disponible"
    value += '<br><a href="/">Volver</a>'
    return HttpResponse(value)
