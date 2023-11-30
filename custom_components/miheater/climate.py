"""
    Support for Xiaomi wifi-enabled home heaters via miio.
    author: motelica.ion@gmail.com
"""
import logging
import asyncio

from homeassistant.components.climate.const import (DOMAIN)
from homeassistant.const import (CONF_HOST, ATTR_ENTITY_ID, CONF_NAME, CONF_TOKEN)
from homeassistant.exceptions import PlatformNotReady

from .core.const import DATA_KEY
from .core.schema import SERVICE_SCHEMA
from .core.services import SERVICE_TO_METHOD
from .core.miheater import MiHeater

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['python-miio>=0.5.12']


# def setup_platform(hass, config, async_add_devices):
def setup_platform(hass, config, add_devices, discovery_info=None):
    from miio import Device, DeviceException
    """Perform the setup for Xiaomi heaters."""
    if DATA_KEY not in hass.data:
        hass.data[DATA_KEY] = {}

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)

    _LOGGER.info("Initializing Xiaomi heaters with host %s (token %s...)", host, token[:5])

    try:
        miio_device = Device(host, token)
        heater_info = miio_device.info()

        model = heater_info.model
        unique_id = "{}-{}".format(model, heater_info.mac_address)
        _LOGGER.info("%s %s %s detected",
                     model,
                     heater_info.firmware_version,
                     heater_info.hardware_version)
        mi_heater = MiHeater(miio_device, name, unique_id, hass, _LOGGER)
        hass.data[DATA_KEY][host] = mi_heater
        # async_add_devices([mi_heater], update_before_add=True)
        add_devices(mi_heater)

        async def async_service_handler(service):
            """Map services to methods on XiaomiAirConditioningCompanion."""
            method = SERVICE_TO_METHOD.get(service.service)
            params = {key: value for key, value in service.data.items()
                      if key != ATTR_ENTITY_ID}
            entity_ids = service.data.get(ATTR_ENTITY_ID)
            if entity_ids:
                devices = [device for device in hass.data[DATA_KEY].values() if
                           device.entity_id in entity_ids]
            else:
                devices = hass.data[DATA_KEY].values()

            update_tasks = []
            for dev in devices:
                if not hasattr(dev, method['method']):
                    continue
                await getattr(dev, method['method'])(**params)
                update_tasks.append(dev.async_update_ha_state(True))

            if update_tasks:
                await asyncio.wait(update_tasks, loop=hass.loop)

        for service_name in SERVICE_TO_METHOD:
            schema = SERVICE_TO_METHOD[service_name].get('schema', SERVICE_SCHEMA)
            hass.services.async_register(
                DOMAIN, service_name, async_service_handler, schema=schema)

    except DeviceException:
        _LOGGER.exception('Fail to setup Xiaomi heater')
        raise PlatformNotReady
