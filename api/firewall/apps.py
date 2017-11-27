# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class FirewallConfig(AppConfig):
    name = 'firewall'

    def ready(self):
        """
        Load signals and preform inital device dispatch and refresh
        """
        import firewall.signals

        from firewall.models import Firewall
        from firewall.tasks import dispatch_device
        from utilities.celery import celery_logger

        celery_logger.info("Starting initial device dispatch and refresh")
        for firewall in Firewall.objects.filter(enabled=True):
            # dispatch and refresh the deivce
            dispatch_device.delay(firewall)
        celery_logger.info("Inital device dispatch and refresh complete")


