from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='infirmerie'),
    url(r'^get_malades$', views.get_malades, name='get_malades'),
    url(r'^ajouter_malade$', views.ajouter_malade, name='ajouter_malade'),
    url(r'^encoder_sortie/(?P<passageId>[0-9]+)$', views.encoder_sortie, name='encoder_sortie'),
    url(r'^get_entries/$', views.get_entries, name='get_entries'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
]
