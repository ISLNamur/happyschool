from django.conf.urls import url

from . import views

app_name = 'absence_prof'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_absences$', views.get_absences, name='get_absences'),
    url(r'^add_absence/(?P<abs_id>[0-9]+)$', views.add_absence, name='add_absence'),
    url(r'^add_absence$', views.add_absence, name='add_absence'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
    url(r'^get_entries/$', views.get_entries, name='get_entries'),
]