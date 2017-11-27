from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from firewall.models import Firewall
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
