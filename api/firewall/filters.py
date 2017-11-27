from __future__ import unicode_literals

import django_filters
from django.db.models import Q

from utilities.filters import NumericInFilter
from .models import Firewall


class FirewallFilter(django_filters.FilterSet):
    id__in = NumericInFilter(name='id', lookup_expr='in')
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = Firewall
        fields = ['name', 'hostname', 'username', 'device_type', 'panorama_device_group']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(hostname__icontains=value) |
            Q(device_type__icontains=value) |
            Q(admin_contact__icontains=value) |
            Q(panorama_device_group__icontains=value)
        )
