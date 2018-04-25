from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from django.utils import timezone
from django.db.models import CharField
from django.views.generic import TemplateView

from core.models import ResponsibleModel
from core.people import get_classes
from core.permissions import IsSecretaryPermission
from core.serializers import ResponsibleSerializer


class BaseFilters(filters.FilterSet):
    unique = filters.CharFilter('unique_by', method='unique_by')

    class Meta:
        fields_to_filter = set()

        def generate_filters(fields) -> dict:
            filters = {}
            for f in fields:
                is_date_or_time = f.startswith("date") or f.startswith("time")
                filters[f] = ['exact'] if not is_date_or_time else ['lt', 'gt']
            return filters
        fields = generate_filters(fields_to_filter)
        filter_overrides = {
            CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

    def unique_by(self, queryset, name, value):
        if value:
            # Distinct query in postgrsql asks to order_by the same column.
            return queryset.order_by(value).distinct(value)
        else:
            return queryset


class BaseModelViewSet(ModelViewSet):
    filter_access = False
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = (DjangoModelPermissions,)
    all_access = ()

    def get_queryset(self):
        if not self.filter_access or self.request.user.groups.filter(name__in=self.all_access).exists():
            return self.queryset
        else:
            teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
            return self.queryset.filter(matricule__classe__in=classes)

    def perform_create(self, serializer):
        serializer.save(
            datetime_encodage=timezone.now(),
            user=self.request.user.username,
        )


class MembersView(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  TemplateView):
    template_name = "core/members.html"
    permission_required = ('core.add_responsiblemodel')


class ProfilView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profil.html'


class MembersAPI(ModelViewSet):
    queryset = ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)
    serializer_class = ResponsibleSerializer
    permission_classes = (IsAuthenticated, IsSecretaryPermission)

    def get_queryset(self):
        person_type = self.request.GET.get('person_type', None)
        if person_type == 'secretary':
            return ResponsibleModel.objects.filter(is_secretary=True)
        elif person_type == 'others':
            return ResponsibleModel.objects.filter(is_teacher=False, is_educator=False, is_secretary=False)
        else:
            return ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)
