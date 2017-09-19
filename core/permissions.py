from rest_framework import permissions

from core.models import ResponsibleModel
from core.people import get_classes


class IsStudentsTenure(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
        classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
        return obj.matricule.classe in classes


class IsInGroupPermission(permissions.BasePermission):
    group = ()

    def has_permission(self, request, view):
        return len(request.user.groups.filter(name__in=self.group)) > 0


class IsSysadminPermission(IsInGroupPermission):
    group = ('sysadmin')


class IsDirectionPermission(IsInGroupPermission):
    group = ('sysadmin', 'direction')


class IsTeacherPermission(IsInGroupPermission):
    group = ('sysadmin', 'direction', 'professeur')


class IsEducatorPermission(IsInGroupPermission):
    group = ('sysadmin', 'direction', 'educator')


class IsSecretaryPermission(IsInGroupPermission):
    group = ('sysadmin', 'direction', 'secretaire')