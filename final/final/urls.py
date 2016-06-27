"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views import static
from hoteles import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.inicio),
    url(r'^style/(.*)$', static.serve,
{'document_root': 'templates/style/'}),
    url(r'^alojamientos/images/(.*)$', static.serve,
{'document_root': 'templates/style/'}),
    url(r'^alojamientos$',views.listarAlojamientos),
    url(r'^filter$', views.filter),
    url(r'index.html$', views.inicio),
    url(r'page1.html$', views.listarAlojamientos),
    url(r'page3.html$', views.mostrarAlojamiento),
    url(r'pag4.html', views.miPagina),
    url(r'page2.html', views.about),
    url(r'^alojamientos/(\d+)$',views.mostrarAlojamiento),
    url(r'style/(.*)$', static.serve,
    {'document_root': 'templates/style/'}),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^escribirComentario/(.+)$',views.escribirComentario),
    url(r'^hotelFavorito/(.+)$',views.hotelFavorito),
    url(r'^cambiarIdioma/(.+)$',views.cambiarIdioma),
    #url(r'^paginaUsuario/(.+)$',views.paginaUsuario),
    #url(r'^miPagina/(.+)$',views.miPagina),
    #url(r'^(.*)$',views.paginaUsuario),
    url(r'(.*)',views.pagUsuario),
    url(r'cambiartitulo$',views.cambiartitulo),
    url(r'miPagina$',views.miPagina),
    url(r'^about/',views.about),
    #url(r'mostrarXml$',views.mostrarXml),
    #url(r'^(.*)$','hoteles.views.pagUsuario'),



]
