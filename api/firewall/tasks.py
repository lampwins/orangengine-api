# Create your tasks here
from __future__ import absolute_import, unicode_literals

from utilities.persistence import DeviceTask, celery_logger
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


@celery_app.task(base=DeviceTask)
def refresh_device(name):
    device = dispatch_device.device_pool.device(name)
    if device:
        celery_logger.info("Refreshing device {}".format(name))
        device.refresh()
        celery_logger.info("Refresh complete for device {}".format(name))
    else:
        celery_logger.warning("Refresh requested for device {} but it does not exist!".format(name))


@celery_app.task(base=DeviceTask)
def policy_match(name, criteria):
    device = policy_match.device_pool.device(name)
    return device.policy_match(criteria).to_json()
