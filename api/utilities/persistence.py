import orangengine
from celery.utils.log import get_task_logger
from celery import Task


celery_logger = get_task_logger(__name__)


class OEDeviceInstancePool(object):
    """
    The instance pool is a singleton initialized in the base device task (also a singleton).
    Given that we run celery with one worker, this singleton acts as the instance pool
    of devices for orangengine.
    """

    def __init__(self):
        self._devices = {}

    def dispatch_device(self, model):
        """
        Given a model api DB, dispatch an orangengine device instance and store it in the
        device map. Replace an existing instance (for this model) in the map if necisary.
        """

        conn_params = {
            'host': model.hostname,
            'username': model.username,
            'password': model.password,
            'device_type': model.get_device_type_display(),
            'apikey': model.palo_alto_api_key,
        }

        celery_logger.info("Dispatching device: %s", model.name)
        device = orangengine.dispatch(**conn_params)
        self._devices[model.name] = device

    def delete_device(self, name):
        """
        Delete a device by name from the device map
        """
        if name in self._devices.keys():
            del self._devices[name]

    def device(self, name):
        """
        Return a device from the device map with the given name.
        """
        return self._devices.get(name)


class DeviceTask(Task):
    """
    Base task for all tasks related to devices
    Provides access to the device instance pool
    """

    _device_pool = None

    @property
    def device_pool(self):
        """
        Property for the device pool
        Returns a singleton instance of the instance pool
        """
        if DeviceTask._device_pool is None:
            DeviceTask._device_pool = OEDeviceInstancePool()
        return DeviceTask._device_pool
