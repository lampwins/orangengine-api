from __future__ import unicode_literals

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Firewall
from .tasks import dispatch_device, delete_device


@receiver(post_save, sender=Firewall)
def post_save_firewall(instance, **kwargs):
    """
    Dispatch a device into the orangengine instance pool
    """
    if instance.enabled:
        dispatch_device.delay(instance)
    elif not kwargs['created']:
        # updated to disable the device
        delete_device(instance.name)


@receiver(post_delete, sender=Firewall)
def post_delete_firewall(instance, **kwargs):
    """
    Delete a device from the orangengine instance pool
    """
    delete_device.delay(instance.name)
