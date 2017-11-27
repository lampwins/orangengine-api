from __future__ import unicode_literals

from rest_framework import serializers

from firewall.models import Firewall
from utilities.api import ChoiceFieldSerializer, ValidatedModelSerializer
from firewall.constants import *


#
# Firewall
#

class FirewallSerializer(serializers.ModelSerializer):
    device_type = ChoiceFieldSerializer(choices=F_DEVICE_TYPE_CHOICES)

    class Meta:
        model = Firewall
        fields = [
            'id', 'name', 'hostname', 'username', 'device_type', 'panorama_device_group',
        ]


class NestedFirewallSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='firewall-api:firewall-detail')

    class Meta:
        model = Firewall
        fields = [
            'id', 'name', 'hostname', 'url',
        ]


class WritableFirewallSerializer(ValidatedModelSerializer):

    class Meta:
        model = Firewall
        fields = [
            'name', 'hostname', 'username', 'password', 'private_key', 'device_type', 'panorama_device_group',
            'palo_alto_api_key',
        ]
