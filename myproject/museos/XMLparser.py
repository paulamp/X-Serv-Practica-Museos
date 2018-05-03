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
            print str(i)
            museo = root[i]
            m = Museo()
            m.nombre = museo[1][1].text
            m.descripcion = museo[1][2].text
            m.horario = museo[1][3].text
            m.transporte = museo[1][4].text
            m.accesibilidad = museo[1][5].text
            m.url = museo[1][6].text
            m.direccion = museo[1][7][1].text + "/" + museo[1][7][0].text + "Num: " + museo[1][7][3].text \
                        + "CD " + museo[1][7][6].text
            m.localidad = museo[1][7][4].text
            m.provincia = museo[1][7][5].text
            m.barrio = museo[1][7][7].text
            m.distrito = museo[1][7][8].text
            m.ubicacion = "Latitud: " + museo[1][7][11].text + "Longitud: " + museo[1][7][12].text
            m.telefono = museo[1][8][0].text
            m.email = museo[1][8][2].text
            m.save()
            i += 1
