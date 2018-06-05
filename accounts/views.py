from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from . import models as accounts_models
from . import permissions as accounts_permissions
from . import serializers as accounts_serializers


class UserViewSet(ModelViewSet):
    permission_classes = (accounts_permissions.UserPermission, )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return accounts_serializers.UserEditSerializer

        return accounts_serializers.UserSerializer

    def get_queryset(self):
        queryset = accounts_models.User.objects.all().order_by('first_name', 'email')

        if self.request.query_params.get('search', None):
            term = self.request.query_params.get('search')
            first_name_q = Q(first_name__icontains=term)
            last_name_q = Q(last_name__icontains=term)
            queryset = queryset.filter(first_name_q | last_name_q)

        return queryset
