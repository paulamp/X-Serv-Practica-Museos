#!/usr/bin/env python
# coding=utf-8
import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from xml.etree.ElementTree import tostring
import xml.etree.ElementTree as ET
from django.template import Context
from XMLparser import MuseoParser
from models import Museo, Comentario, Perfil, Coleccion

# Create your views here.

def mostrarAbout (request):
    return render(request, 'about.html')

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

def calcular_paginacion(url,museos):
    numero_paginacion = ""
    total = len(museos)
    cociente = total/5
    resto = total%5
    if resto != 0:
        cociente += 1
    paginas = cociente
    inicio = 0
    final = 5
    for numero in range(paginas):
        numero_paginacion += "<li><a href='"+str(url)+"offset="+str(inicio)+"&max="+str(final)+"'>"+str(numero+1)+"</a></li>"
        inicio += 5
        final += 5
    return numero_paginacion


@csrf_exempt
def home(request):
    accesibles = request.GET.get('accesibles',False)
    cargar = request.GET.get('cargar',False)
    if accesibles:
        total_museos = Museo.objects.filter( numComentario__gte=1, accesibilidad=1).order_by('-numComentario')
        numero_paginacion = calcular_paginacion("/?accesibles=True&",total_museos)
    elif cargar:
        parse = MuseoParser()
        parse.cargar()
        return HttpResponseRedirect("/")
    else:
        total_museos = Museo.objects.filter( numComentario__gte=1).order_by('-numComentario')
        numero_paginacion = calcular_paginacion("/?",total_museos)

    museos = Museo.objects.all()
    offset = request.GET.get('offset', 0)
    max = request.GET.get('max', 5)
    museos_comentarios = total_museos[int(offset):int(max)]
    paginas = Perfil.objects.all()
    context = {
        'museos':museos,
        'museos_comentarios': museos_comentarios,
        'paginas':paginas,
        'accesibles':accesibles,
        'paginacion': numero_paginacion,
        'home':True
    }
    return render(request, 'index.html',context)

def xml_usuario(request, usuario):
    try:
        perfil = Perfil.objects.get(usuario=usuario)
        try:
            seleccionados = Coleccion.objects.filter(perfil=perfil)
        except:
            seleccionados = ""
        coleccion = ET.Element("coleccion")
        for seleccionado in seleccionados:
            museo = ET.SubElement(coleccion, "museo")
            ET.SubElement(museo, "atributo", name="NOMBRE").text = seleccionado.museo.nombre
            ET.SubElement(museo, "atributo", name="DESCRIPCION-ENTIDAD").text = seleccionado.museo.descripcion_entidad
            ET.SubElement(museo, "atributo", name="HORARIO").text = seleccionado.museo.horario
            ET.SubElement(museo, "atributo", name="TRANSPORTE").text = seleccionado.museo.transporte
            ET.SubElement(museo, "atributo", name="DESCRIPCION").text = seleccionado.museo.descripcion
            ET.SubElement(museo, "atributo", name="ACCESIBILIDAD").text = str(seleccionado.museo.accesibilidad)
            ET.SubElement(museo, "atributo", name="CONTENT-URL").text = seleccionado.museo.url
            localizacion = ET.SubElement(museo, "atributo", name="LOCALIZACION")
            ET.SubElement(localizacion, "atributo", name="DIRECCION").text = seleccionado.museo.direccion
            ET.SubElement(localizacion, "atributo", name="LOCALIDAD").text = seleccionado.museo.localidad
            ET.SubElement(localizacion, "atributo", name="PROVINCIA").text = seleccionado.museo.provincia
            ET.SubElement(localizacion, "atributo", name="BARRIO").text = seleccionado.museo.barrio
            ET.SubElement(localizacion, "atributo", name="DISTRITO").text = seleccionado.museo.distrito
            ET.SubElement(localizacion, "atributo", name="UBICACION").text = seleccionado.museo.ubicacion
            contactos = ET.SubElement(museo, "atributo", name="DATOSCONTACTOS")
            ET.SubElement(contactos, "atributo", name="TELEFONO").text = seleccionado.museo.telefono
            ET.SubElement(contactos, "atributo", name="EMAIL").text = seleccionado.museo.email
        xmlstr = tostring(coleccion)
        return HttpResponse(xmlstr,content_type='text/xml')
    except:
        value = "XML no disponible"
        value += '<br><a href="/">Volver</a>'
        return HttpResponse(value)

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
                url = "/"+str(usuario)+"?"
                numero_paginacion = calcular_paginacion(url,coleccion)
                offset = request.GET.get('offset', 0)
                max = request.GET.get('max', 5)
                coleccion = coleccion[int(offset):int(max)]
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
                'coleccion': coleccion,
                'paginacion': numero_paginacion
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
                perfil.size = ".9em"
                perfil.usuario = username
                perfil.save()
            else:
                context ={
                    'error': u"Las contraseñas no son iguales"
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
