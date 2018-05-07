import xml.etree.ElementTree as ET
from models import Museo

class MuseoParser():

    def __init__(self):
        xml = "/home/usuario/Escritorio/PYTHON/X-Serv-Practica-Museos/myproject/museos/museos.xml"
        self.tree = ET.parse(xml)

    def cargar(self):
        root = self.tree.getroot()
        i = 1
        while i < len(root):
            museo = root[i]
            m = Museo()
            atributos = museo[1]
            for atributo in atributos:
                valor = atributo.attrib['nombre']
                if valor == 'NOMBRE':
                    m.nombre = atributo.text
                    continue
                if valor == 'DESCRIPCION-ENTIDAD':
                    m.descripcion_entidad = atributo.text
                    continue
                if valor == 'DESCRIPCION':
                    m.descripcion = atributo.text
                    continue
                if valor == 'HORARIO':
                    m.horario = atributo.text
                    continue
                if valor == 'TRANSPORTE':
                    m.transporte = atributo.text
                    continue
                if valor == 'ACCESIBILIDAD':
                    m.accesibilidad = atributo.text
                    continue
                if valor == 'CONTENT-URL':
                    m.url = atributo.text
                    continue
            localizacion = atributos.findall("*[@nombre='LOCALIZACION']")[0]
            nombre_via = ""
            clase_via = ""
            num = ""
            cp = ""
            latitud = ""
            longitud = ""
            for elemento in localizacion:
                valor = elemento.attrib['nombre']
                if valor == 'NOMBRE-VIA':
                    nombre_via = elemento.text
                    continue
                if valor == 'CLASE-VIAL':
                    clase_via = elemento.text
                    continue
                if valor == 'NUM':
                    num = elemento.text
                    continue
                if valor == 'CODIGO-POSTAL':
                    cp = elemento.text
                    continue
                if valor == 'LOCALIDAD':
                    m.localidad = elemento.text
                    continue
                if valor == 'PROVINCIA':
                    m.provincia = elemento.text
                    continue
                if valor == 'BARRIO':
                    m.barrio = elemento.text
                    continue
                if valor == 'DISTRITO':
                    m.distrito = elemento.text
                    continue
                if valor == 'LATITUD':
                    latitud = elemento.text
                    continue
                if valor == 'LONGITUD':
                    longitud = elemento.text
                    continue
            m.direccion = clase_via + "/" + nombre_via + "Num: " + num + "CP: " + cp
            m.ubicacion = "Latitud: " + latitud + "Longitud: " + longitud
            contactos = atributos.findall("*[@nombre='DATOSCONTACTOS']")[0]
            for contacto in contactos:
                valor = contacto.attrib['nombre']
                if valor == 'TELEFONO':
                    m.telefono = contacto.text
                if valor == 'EMAIL':
                    m.email = contacto.text
            m.save()
            i += 1
