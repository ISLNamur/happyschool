# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url
from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
#
urlpatterns = [
    # url(r'^get_pdf_council/(?P<date_from>.*)/(?P<date_to>.*)/', views.get_pdf_council, name='get_pdf_council'),
    # url(r'^get_pdf_council/', views.get_pdf_council, name='get_pdf_council'),
    # url(r'^get_pdf_retenues/(?P<date>.*)/(?P<date2>.*)/', views.get_pdf_retenues, name='get_pdf_retenues'),
    # url(r'^get_pdf_retenues/(?P<date>.*)', views.get_pdf_retenues, name='get_pdf_retenues'),
    # url(r'^get_pdf_retenues/', views.get_pdf_retenues, name='get_pdf_retenues'),
    path('', views.DossierEleveView.as_view(), name='dossier_eleve'),
    path('ask_sanctions', views.AskSanctionsView.as_view()),
    path('api/statistics/<int:matricule>/', views.StatisticAPI.as_view(), name='statistics'),
    path('upload_file/', views.UploadFileView.as_view(), name='upload_file'),
    path('upload_file/<int:pk>/', views.UploadFileView.as_view(), name='remove_file'),
    path('get_pdf/', views.CasElevePDFGenAPI.as_view()),
    path('get_pdf_list/', views.CasEleveListPDFGen.as_view()),
    path('get_pdf_council/', views.AskSanctionCouncilPDFGenAPI.as_view()),
    path('get_pdf_retenues/', views.AskSanctionRetenuesPDFGenAPI.as_view()),
    path('get_pdf_retenue/<int:sanction>/', views.RetenuePDF.as_view()),
]

router = DefaultRouter()
router.register(r'api/cas_eleve', views.CasEleveViewSet)
router.register(r'api/info', views.InfoViewSet)
router.register(r'api/sanction_decision', views.SanctionDecisionViewSet)
router.register(r'api/ask_sanctions', views.AskSanctionsViewSet)

urlpatterns += router.urls
