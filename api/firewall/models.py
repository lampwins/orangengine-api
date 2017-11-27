# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_ipv46_address, RegexValidator
from django.core.exceptions import ValidationError

from .constants import *

# Create your models here.


validate_hostname = RegexValidator(regex=r'([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,6}')


class Firewall(models.Model):
    """
    A firewall represents all the parameters needed to connect to and maintain
    and instance of a hardware firewall.
    """

    name = models.SlugField()
    hostname = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True, help_text="Password or optional private key password if using key based authentication.")
    private_key = models.CharField(max_length=255, blank=True, null=True, help_text="Optional private key file name if using key based authentication")
    device_type = models.PositiveSmallIntegerField(choices=F_DEVICE_TYPE_CHOICES, help_text="Orangengine device type.")
    refresh_interval = models.PositiveIntegerField(default=15, help_text="Policy refresh interval in minutes")
    panorama_device_group = models.CharField(max_length=255, blank=True, null=True)
    palo_alto_api_key = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        """
        Validate that hostname is a valid hostname or IP Address
        """
        cleaned_data = super(Firewall, self).clean()
        if cleaned_data:
            hostname = cleaned_data.get('hostname', "")
        else:
            hostname = self.hostname

        try:
            validate_ipv46_address(hostname)
        except ValidationError:
            try:
                validate_hostname(hostname)
            except ValidationError:
                raise ValidationError({
                    'hostname': "Hostname is not valid"
                })
        

        if not self.password and not self.private_key:
            raise ValidationError('Must specify either password or private key name. Password is optional if using key based authentication.')

        if self.device_type == F_DEVICE_TYPE_PALO_ATLO_PANORAMA and not self.panorama_device_group:
            raise ValidationError({
                'panorama_device_group': 'Must specify a policy device group.'
            })

        if self.device_type in F_DEVICE_TYPE_PALO_ALTO_CHOICES and (self.password or self.private_key) and self.palo_alto_api_key:
            raise ValidationError('Cannot specify both api key and password/private key authentication.')

        return cleaned_data
