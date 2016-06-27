from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib
import urllib2
import sys
import os.path
from parseHandler import myContentHandler
from models import Alojamiento, Imagen, Comentario, Alojamiento_Seleccionado, CSS
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from operator import itemgetter
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login


# Create your views here.

@csrf_exempt
def inicio(request):
    base = {}
    lista_hoteles = []
    lista_usuarios = []
    esp = []
    if (len(Alojamiento.objects.all()) < 1):
        esp = procesar('es')
        print "LLAMO A BASE HOTELES\n"
        baseHoteles(esp)

    p_hoteles = Alojamiento.objects.all()
    c = 0
    for e in p_hoteles:
        if c < 5:
            print e.nombre
        c += 1

    print len(p_hoteles)
    print len(esp)

    hs = []
    alojamientos = Alojamiento.objects.all()
    comentarios = Comentario.objects.all()
    cont = 0
    print "cuantos comentarios hay "
    print len(comentarios)
    for c in comentarios:
        print c.alojamiento_id
        for a in alojamientos:
            if c.alojamiento_id == a:
                cont += 1
                #hs.append((a))
                base[a.id] = cont
                print "Encontrado alojamiento con comentarios"
                print a.nombre
    lista = sorted(base.items(), key = itemgetter(1), reverse = True)
    print "Longitud sorted"
    print len(lista)
    #for hotel in p_hoteles:
    #    id_hotel = hotel.id
    #    try:

            #print "cuantos comentarios hay "
            #print len(c)
    #        coments = Comentario.objects.filter(alojamiento_id = id_hotel)
    #        base[id_hotel] =len(coments)
    #    except Comentario.DoesNotExist:
#            pass
    #lista = sorted(base.items(), key = itemgetter(1), reverse = True)
    im = Imagen.objects.all()
    print "Longitud de imagenes"
    print len(im)
    i = 0
    cont1 = 0
    for h in lista:
        if i != 9:
            id_h = h[0]
            print "Identificador"
            print id_h
            comentario = h[1]
            if comentario !=0:
                try:
                    hospedaje = Alojamiento.objects.get(id = id_h)
                    print hospedaje.id
                    url = ""
                    for j in im:
                        #print j.alojamiento_id
                        if j.alojamiento_id == hospedaje:
                            url = j.url
                            print "Encontrada alojamiento con imagen"
                            print hospedaje.nombre
                    lista_hoteles.append((hospedaje,url))
                    usrs = User.objects.all()
                    print "Lista de usuarios"
                    print len(usrs)
                    for usr in usrs:
                        print "viendo hojas de estilo"
                        try:
                            hoja_estilo = CSS.objects.get(usuario = usr)
                            print "Hoja de estilo"
                            print hoja_estilo
                            login = hoja_estilo.usuario
                            titulo = hoja_estilo.titulo
                            if lista_usuarios[usr.name]:
                                 pass
                            else:
                                lista_usuarios.append((login, titulo))
                        except CSS.DoesNotExist:
                            lista_usuarios.append((usr.username, ("Pagina de " + usr.username)))
                except ObjectDoesNotExist:
                    pass
    print "Pasamos para imrimir diez alojamientos"
    print len(lista_hoteles)
    template = get_template('index.html')
    cont = RequestContext(request, {'alojamientos': lista_hoteles, 'usuarios': lista_usuarios})#le pasamos el objeto completo
    return HttpResponse(template.render(cont))


@csrf_exempt
def listarAlojamientos(request):
    hoteles = Alojamiento.objects.all()
    #for hotel in hoteles:
    #    print hotel.nombre+"\n"
    template = get_template('page1.html')
    #context = RequestContext({'alojamientos': hoteles},request) #le pasamos el objeto completo
    return HttpResponse(template.render({'alojamientos': hoteles},request))




@csrf_exempt
def baseHoteles(lista):

    for elemento in lista:
        #print c

        nombre_hotel = elemento['name']
        #if c < 5:
        #    print nombre_hotel
        #c += 1
        direccion_hotel = elemento['address'] +' , C.P. ' + elemento['zipcode']
        categoria_hotel = elemento['categoria']
        #print categoria_hotel
        try:
            estrellas_hotel = elemento['estrellas']
        except KeyError:
            #print "Categoria  desconocida\n"
            pass
        web_hotel = elemento['web']
        descripcion_hotel = elemento['body']

        info_hotel = Alojamiento(nombre = nombre_hotel, direccion = direccion_hotel, categoria = categoria_hotel, estrellas = estrellas_hotel, url = web_hotel, descripcion = descripcion_hotel)
        info_hotel.save()
        imagenes_hotel = elemento['url']
        if len(imagenes_hotel) != 0:
            for imagen in imagenes_hotel:
                img = Imagen(alojamiento_id =  info_hotel, url = imagen)
                img.save()



@csrf_exempt
def procesar(lengua):
    print "Entrando... \n"
    datos = make_parser()
    handler = myContentHandler()
    datos.setContentHandler(handler)
    if lengua == 'en':
        fuente_xml  = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_en.xml')
    if lengua == 'es':
        fuente_xml = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')
    if lengua == 'fr':
        fuente_xml  = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_fr.xml')
    datos.parse(fuente_xml)
    print "Obtenido xml... \n"
    lista_lengua = handler.obtenerLista()
    print "Procesado completado \n"
    return lista_lengua

@csrf_exempt
def filter(request):
    hoteles = []
    hoteles1 = []
    categoria_elegida = request.POST.get("categoria")
    #categoria_elegida = str(categoria_elegida) + "\n"

    subcategoria = request.POST.get("estrellas")
    print "CATEGORIA ELEGIDA: "+categoria_elegida
    print "SUBCATEGORIA ELEGIDA: "+subcategoria
    alojamientos = Alojamiento.objects.all()
    print len(alojamientos)

    if categoria_elegida == "todos":
        print "estoy dentro de todos\n"
        if subcategoria != "todos":
            print "estoy en la subcategoria "+subcategoria +"\n"
            for h in alojamientos:
                if h.estrellas == subcategoria:
                    hoteles.append((h))
        else:
            hoteles = alojamientos
    else:
        print "estoy en otra categoria "+ categoria_elegida+"\n"
        for h in alojamientos:
            if h.categoria == categoria_elegida:
                hoteles1.append((h))
                #print "estoy aniadiendo\n"
        if subcategoria != "todos":
            print "estoy en la subcategoria "+subcategoria +"\n"
            for h in hoteles1:
                if h.estrellas == subcategoria:
                    hoteles.append((h))

        else:
            print "estoy dentro de todos como subcategoria\n"
            hoteles = hoteles1
    template = get_template('page1.html')
    return HttpResponse(template.render({'alojamientos': alojamientos, 'todos':hoteles},request))

@csrf_exempt
def mostrarAlojamiento(request, id):
    alojamiento = None;
    imagenes = None;
    comentarios = None
    try:
        alojamiento = Alojamiento.objects.get(id=int(id))
        #print alojamiento
        #print alojamiento.id
        i =  Imagen.objects.all()
        imagenes = Imagen.objects.filter(alojamiento_id = alojamiento.id)
        #print "IMAGENES DEL HOTEL \n"
        #print len(imagenes)
        #for j in i:
            #if j.alojamiento_id ==


        comentarios = Comentario.objects.filter(alojamiento_id=alojamiento)
        if len(imagenes)==0:
            imagenes = []
        if len(comentarios)==0:
            comentarios = []
    except ObjectDoesNotExist:
        print "No existe el alojamiento"
    except ValueError:
        pass
    template = get_template('page3.html')
    return HttpResponse(template.render({'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios},request))
    #return render_to_response('page3.html',{'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios},context_instance=RequestContext(request))

@csrf_exempt
def login(request):
    req ={}
    req.update(csrf(request))
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username = username, password = password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect("/")

    else:
        return HttpResponseRedirect("/")


@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def escribirComentario(request,idh):
    if request.user.is_authenticated():
        #username = request.user.username
        comentario = request.POST.get("comentario")
        alojamiento = Alojamiento.objects.get(id=idh)
        nuevo_comentario = Comentario(cuerpo=comentario, alojamiento_id=alojamiento)
        nuevo_comentario.save()
        return HttpResponseRedirect("/alojamientos/" + str(idh))
    else:
        return HttpResponseRedirect("/alojamientos/" + str(idh))

@csrf_exempt
def hotelFavorito(request, id):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            usr = User.objects.get(username=username)
            hotel = Alojamiento.objects.get(id=id)
            imagenes = Imagen.objects.filter(alojamiento_id = hotel)
            print len(imagenes)
            print "cuantas imagenes"
            coments = Comentario.objects.filter(alojamiento_id=hotel)
            if len(imagenes)==0:
                imagenes = []
            if len(coments)==0:
                comentarios = []
            try:
                Alojamiento_Seleccionado.objects.get(alojamiento_id=hotel)
                template = get_template('page3a.html')
                context = RequestContext(request, {'alojamiento': hotel, 'imagenes': imagenes, 'comentarios': coments}) #le pasamos el objeto completo
                return HttpResponse(template.render(context))
            except Alojamiento_Seleccionado.DoesNotExist:
                favorito = Alojamiento_Seleccionado(alojamiento_id=hotel, usuario=usr)
                favorito.save()
                template = get_template('page3.html')
                context = RequestContext(request, {'alojamiento': hotel, 'imagenes': imagenes, 'comentarios': coments}) #le pasamos el objeto completo
                return HttpResponse(template.render(context))
        except ObjectDoesNotExist:
            print "No existe el alojamiento marcado."

@csrf_exempt
def cambiarIdioma(request, id):
    lista_i = []
    idioma = request.POST.get("idioma")
    alojamiento = Alojamiento.objects.get(id=id)
    imagenes = Imagen.objects.filter(alojamiento_id = alojamiento)
    coments = Comentario.objects.filter(alojamiento_id=alojamiento)
    if len(imagenes)==0:
        imagenes = []
    if len(coments)==0:
        comentarios = []
    name = alojamiento.nombre
    if idioma=="espaniol":
        return HttpResponseRedirect("/alojamientos/" + str(id))
    if idioma=="ingles":
        lista_i = procesar("en")
    if idioma=="frances":
        lista_i = procesar("fr")
    for l in lista_i:
        if l["name"]==name:
            body = l["body"]
            alojamiento.descripcion = body
    template = get_template('page3.html')
    context = RequestContext(request, {'alojamiento': alojamiento, 'imagenes': imagenes, 'comentarios': coments}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))

@csrf_exempt
def pagUsuario(request, user):
    print user
    list_aloj = []
    #username = request.user.username
    try:
        css = CSS.objects.get(usuario=user)
        titulo = css.titulo
        u = user
        usuario = User.objects.get(username=user)
    except CSS.DoesNotExist:
        usuario = User.objects.get(username=user)
        u = usuario.username
        titulo = ""
    try:
        aloj_seleccionados = Alojamiento_Seleccionado.objects.filter(usuario=usuario)
        for alojamiento in aloj_seleccionados:
            imagenes = Imagen.objects.filter(alojamiento_id = alojamiento.alojamiento_id)
            if len(imagenes)>0:
                list_aloj.append((alojamiento, imagenes[0].url))
            else:
                list_aloj.append((alojamiento, ""))
    except ObjectDoesNotExist:
            print "No existen favoritos..."
    template = get_template('pag4.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'usuario': u, 'titulo': titulo}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))


@csrf_exempt
def cambiartitulo(request):
    list_aloj = []
    if request.user.is_authenticated():
        username = request.user.username
        titulo = request.POST.get("titulo")
        try:
            css = CSS.objects.get(usuario=username)
            css.titulo = titulo
            css.save()
            usuario = User.objects.get(username=username)
        except CSS.DoesNotExist:
            css = CSS(titulo=titulo, usuario=username, tamannoFuente=0.0, colorFondo="#20B2AA")
            css.save()
            usuario = User.objects.get(username=username)
    else:
        titulo = ""
        usuario = User.objects.get(username=request.user.username)
        username = usuario.username
    try:
        aloj_seleccionados = Alojamiento_Seleccionado.objects.filter(usuario=usuario)
        for alojamiento in aloj_seleccionados:
            imagenes = Imagen.objects.filter(alojamiento_id = alojamiento.alojamiento_id)
            if len(imagenes)>0:
                list_aloj.append((alojamiento, imagenes[0].url))
            else:
                list_aloj.append((alojamiento, ""))
    except ObjectDoesNotExist:
            print "No existen favoritos..."
    return HttpResponseRedirect("/pag4.html")
    template = get_template('pag4.html')
    context = RequestContext(request, {'alojamientos': list_aloj, 'usuario': username, 'titulo': titulo}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))


@csrf_exempt
def miPagina(request):
    if request.user.is_authenticated():
        username = request.user.username
        return HttpResponseRedirect("/" + username)

@csrf_exempt
def about(request):
    template = get_template('page2.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
