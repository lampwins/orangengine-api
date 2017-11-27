# Create your tasks here
from __future__ import absolute_import, unicode_literals

from utilities.celery import DeviceTask, celery_logger
from api import celery_app


@celery_app.task(base=DeviceTask)
def dispatch_device(instance):
    dispatch_device.device_pool.dispatch_device(instance)
    device = dispatch_device.device_pool.device(instance.name)
    celery_logger.info("Refreshing device {}".format(instance.name))
    device.refresh()
    celery_logger.info("Refresh complete for device {}".format(instance.name))


@celery_app.task(base=DeviceTask)
def delete_device(name):
    dispatch_device.device_pool.delete_device(name)
    celery_logger.info("Deleted device {}".format(name))
