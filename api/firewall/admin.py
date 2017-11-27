# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import ModelForm, PasswordInput

from .models import Firewall

# Register your models here.


class FirewallForm(ModelForm):
    class Meta:
        model = Firewall
        fields = [
            'name','hostname', 'username', 'password', 'private_key', 'device_type', 'panorama_device_group', 'palo_alto_api_key'
        ]
        widgets = {
            'password': PasswordInput(),
            'palo_alto_api_key': PasswordInput(),
        }


@admin.register(Firewall)
class FirewallAdmin(admin.ModelAdmin):
    list_display = [
        'name','hostname', 'username', 'device_type',
    ]
    form = FirewallForm
