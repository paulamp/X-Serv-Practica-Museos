from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Museo(models.Model):
    nombre = models.CharField(max_length=50, default="")
    descripcion_entidad = models.CharField(max_length=500,default="")
    descripcion = models.CharField(max_length=500,default="")
    horario = models.CharField(max_length=500,default="")
    transporte = models.CharField(max_length=100,default="")
    accesibilidad = models.IntegerField()
    url = models.CharField(max_length=250,default="")
    direccion = models.CharField(max_length=250,default="")
    localidad = models.CharField(max_length=50,default="")
    provincia = models.CharField(max_length=50,default="")
    barrio = models.CharField(max_length=50,default="")
    distrito = models.CharField(max_length=50,default="")
    ubicacion = models.CharField(max_length=50,default="")
    telefono = models.CharField(max_length=25,default="")
    email = models.CharField(max_length=50,default="")
    numComentario = models.IntegerField(default=0)

class Comentario(models.Model):
    museo = models.ForeignKey(Museo)
    contenido = models.CharField(max_length=400, default="")

class Perfil(models.Model):
    usuario = models.CharField(max_length=30)
    size = models.CharField(max_length=20)
    background = models.CharField(max_length=30)
    titulo = models.CharField(max_length=50)

class Coleccion(models.Model):
    perfil = models.ForeignKey(Perfil)
    museo = models.ForeignKey(Museo)
    date = models.DateField(default=datetime.date.today)
