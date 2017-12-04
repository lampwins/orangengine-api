from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from firewall.models import Firewall
from firewall.tasks import refresh_device, dispatch_device
from firewall import filters
from utilities.api import FieldChoicesViewSet, WritableSerializerMixin
from . import serializers


#
# Field choices
#

class FirewallFieldChoicesViewSet(FieldChoicesViewSet):
    fields = (
        (Firewall, ['device_type']),
    )


#
# Firewalls
#

class FirewallViewSet(WritableSerializerMixin, ModelViewSet):
    queryset = Firewall.objects.all()
    serializer_class = serializers.FirewallSerializer
    write_serializer_class = serializers.WritableFirewallSerializer
    filter_class = filters.FirewallFilter

    @detail_route(url_path='refresh', methods=['post'])
    def refresh(self, request, pk=None):
        """
        Refresh a firewall. Fires a celery task to perform the refresh.
        """
        firewall = get_object_or_404(Firewall, pk=pk)

        # permission check
        if not request.user.has_perm('firewall.firewall'):
            raise PermissionDenied()

        # enqueue task to refresh firewall
        refresh_device.delay(firewall.name)

        return Response({'message': 'Device refresh successfully requested.'}, status=status.HTTP_202_ACCEPTED)

    @detail_route(url_path='dispatch', methods=['post'])
    def dispatch_firewall(self, request, pk=None):
        """
        Dispatch a firewall. Fires a celery task to perform the dispatch.
        """
        firewall = get_object_or_404(Firewall, pk=pk)

        # permission check
        if not request.user.has_perm('firewall.firewall'):
            raise PermissionDenied()

        # enqueue task to refresh firewall
        dispatch_device.delay(firewall)

        return Response({'message': 'Device dispatch successfully requested.'}, status=status.HTTP_202_ACCEPTED)
