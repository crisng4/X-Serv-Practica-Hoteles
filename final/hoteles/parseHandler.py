from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2
import sys
import os.path


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.inCategoria = False
        self.inEstrellas = False
        self.theContent = ""
        self.listDic = [] #Lista de diccs, uno por cada hotel encontrado en .xml
        self.dic = {}
        self.dic['url'] = []


    def startElement (self, name, attrs):
        if name in ['name', 'body', 'web', 'address', 'zipcode', 'url']:
            self.inContent = True
        elif name == 'item' and attrs["name"]=="Categoria": #TIPO HOTEL
            self.inCategoria = True
            self.inContent = True
        elif name == 'item' and attrs["name"]=="SubCategoria": #ESTRELLAS Y LLAVES
            self.inEstrellas = True
            self.inContent = True

    def endElement (self, name):
        if name in ['name', 'body', 'web', 'address', 'zipcode']:
            self.dic[name] = self.theContent.encode('utf-8')
        elif name == 'url':
            if len(self.dic['url']) < 5:
                self.dic['url'].append(self.theContent.encode('utf-8'))
        elif name == 'item' and self.theContent and self.inCategoria:
            self.dic['categoria'] = self.theContent.encode('utf-8')
            self.inCategoria = False
        elif name == 'item' and self.theContent and self.inEstrellas:
            self.dic['estrellas'] = self.theContent.encode('utf-8')
            self.inEstrellas = False
        elif name == 'service':
            self.listDic.append(self.dic)
            self.dic = {}
            self.dic['url'] = []
        self.inContent = False
        self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent += chars
            #self.theContent = self.theContent.encode('utf-8')

    def obtenerLista(self):
        return self.listDic
