from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^$', views.index, name='appels'),
    url(r'^get_appels$', views.get_appels, name='get_appels'),
    url(r'^nouvel_appel$', views.nouvel_appel, name='nouvel_appel'),
    url(r'^traiter_appel/(?P<appelId>[0-9]+)$', views.traiter_appel, name='traiter_appel'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
    url(r'vue', views.test_vue, name='test_vue'),
]

router = DefaultRouter()
router.register(r'api', views.AppelViewSet)

urlpatterns += router.urls