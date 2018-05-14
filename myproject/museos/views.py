#!/usr/bin/env python
# coding=utf-8
import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from XMLparser import MuseoParser
from models import Museo, Comentario, Perfil, Coleccion

# Create your views here.
@csrf_exempt
def museos(request):
    distrito = ""
    if request.method == "POST":
        distrito = request.POST.get('distrito')
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
def info_museo(request, id):
    if request.method == "POST":
        if request.user.is_authenticated():
            usuario = request.user
            try:
                museo = Museo.objects.get(id=id)
            except:
                value = "Museo no disponible"
                value += '<br><a href="/">Volver</a>'
                return HttpResponse(value)

            favorito = request.POST.get("favorito")
            if favorito:
                coleccion = Coleccion()
                coleccion.perfil = Perfil.objects.get(usuario=usuario.username)
                coleccion.museo = museo
                coleccion.save()

            quitar_favorito = request.POST.get("quitar")
            if quitar_favorito:
                perfil = Perfil.objects.get(usuario=usuario.username)
                coleccion = Coleccion.objects.filter(perfil=perfil,museo=museo).delete()

            comentando = request.POST.get('comentando')
            if comentando:
                contenido = request.POST.get('contenido')
                if contenido:
                    comentario = Comentario()
                    comentario.contenido = contenido
                    comentario.museo = museo
                    comentario.save()
                    museo.numComentario = museo.numComentario + 1
                    museo.save()
        return HttpResponseRedirect("/museos/"+str(id))
    else:
        try:
            museo = Museo.objects.get(id=id)
            comentarios = Comentario.objects.filter(museo=museo)
            seleccionado = False
            if request.user.is_authenticated():
                perfil = Perfil.objects.get(usuario=request.user.username)
                coleccion = Coleccion.objects.filter(museo=museo,perfil=perfil)
                if coleccion:
                    seleccionado = True
            context ={
                'museo':museo,
                'comentarios':comentarios,
                'seleccionado': seleccionado
            }
            return render(request, 'museo.html',context)
        except:
            value = "Museo no disponible"
            value += '<br><a href="/">Volver</a>'
            return HttpResponse(value)

def cargar(request):
    parse = MuseoParser()
    parse.cargar()
    return HttpResponseRedirect("/")

@csrf_exempt
def home(request):
    accesibles = False
    if request.method == "POST":
        accesibles = request.POST.get('accesibles')
        if accesibles:
            accesibles = True
    if accesibles:
        museos_comentarios = Museo.objects.filter( numComentario__gte=1, accesibilidad=1).order_by('numComentario')
    else:
        museos_comentarios = Museo.objects.filter( numComentario__gte=1).order_by('numComentario')
    museos = Museo.objects.all()
    museos_comentarios = museos_comentarios[:5]
    paginas = Perfil.objects.all()
    context = {
        'museos':museos,
        'museos_comentarios': museos_comentarios,
        'paginas':paginas,
        'accesibles':accesibles
    }
    return render(request, 'index.html',context)

@csrf_exempt
def perfil (request, usuario):
    if request.method == 'POST':
        if request.user.is_authenticated():
            if request.user.username == usuario:
                color = request.POST.get('color')
                size = request.POST.get('size')
                titulo = request.POST.get('titulo')
                try:
                    perfil = Perfil.objects.get(usuario=usuario)
                except:
                    value = "No tienes perfil"
                    value += '<br><a href="/">Volver</a>'
                    return HttpResponse(value)
                if color:
                    perfil.background = color
                if size:
                    perfil.size = size
                if titulo:
                    perfil.titulo = titulo
                perfil.save()
        return HttpResponseRedirect("/"+usuario)
    else:
        try:
            perfil = Perfil.objects.get(usuario=usuario)
            try:
                coleccion = Coleccion.objects.filter(perfil=perfil)
            except:
                coleccion = ""
            propietario = False
            if request.user.is_authenticated():
                if request.user.username == usuario:
                    propietario = True
            context= {
                'background': perfil.background,
                'titulo': perfil.titulo,
                'size': perfil.size,
                'usuario': perfil.usuario,
                'propietario': propietario,
                'coleccion': coleccion
            }
            return render(request, 'perfil.html',context)
        except:
            value = "Recursos no disponibles"
            value += '<br><a href="/">Volver</a>'
            return HttpResponse(value)


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
                perfil = Perfil()
                pagina = u"Página de "
                perfil.titulo = pagina + username
                perfil.background = "white"
                perfil.size = ".8em"
                perfil.usuario = username
                perfil.save()
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
