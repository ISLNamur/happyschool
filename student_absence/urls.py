from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views
from annuaire.views import SearchPeopleAPI

app_name = 'student_absence'

urlpatterns = [
    path('', views.StudentAbsenceView.as_view(), name="student_absence"),
    path('api/absence_count/', views.AbsenceCountAPI.as_view(), name="absence_count"),
    path('api/students_classes/', SearchPeopleAPI.as_view())
]

router = DefaultRouter()
router.register(r'api/student_absence', views.StudentAbsenceViewSet)
router.register(r'api/justification', views.JustificationViewSet)
router.register(r'api/classenote', views.ClasseNoteViewSet)
router.register(r'api/period', views.PeriodViewSet)

urlpatterns += router.urls