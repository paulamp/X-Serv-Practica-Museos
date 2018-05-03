from django.db import models

# Create your models here.

class Museo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    horario = models.CharField(max_length=500)
    transporte = models.CharField(max_length=100)
    accesibilidad = models.IntegerField()
    url = models.CharField(max_length=250)
    direccion = models.CharField(max_length=250)
    localidad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    barrio = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
