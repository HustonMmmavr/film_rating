"""films_ratings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^delete_film_rating', views.delete_film_rating),
    url(r'^status', views.root),
    url(r'^get_films_by_user/(?P<f_id>[-\w]+)', views.get_films_by_user),
    url(r'^get_users_by_film/(?P<f_id>[-\w]+)', views.get_films_by_user),
    url(r'^get_rating/(?P<f_id>[-\w]+)', views.get_rating),
    url(r'^set_rating', views.set_rating),
    url(r'^$', views.root),
]
