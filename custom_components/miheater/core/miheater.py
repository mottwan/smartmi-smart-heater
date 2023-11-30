from homeassistant.const import (ATTR_TEMPERATURE, TEMP_CELSIUS)
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.components.climate import ClimateEntity
from homeassistant.exceptions import PlatformNotReady
from homeassistant.components.climate.const import (ATTR_HVAC_MODE, HVAC_MODE_HEAT, HVAC_MODE_OFF)

from .const import (MIN_TEMPERATURE, MAX_TEMPERATURE, CONF_BUZZER, CONF_CHILD_LOCK, CONF_POWEROFF_TIME, CONF_BRIGHTNESS,
                    SUPPORT_FLAGS)
from .operation_mode import OperationMode


class MiHeater(ClimateEntity):
    """Representation of a MiHeater device."""

    def __init__(self, device, name, unique_id, _hass, logger):
        """Initialize the miheater.py."""
        self._logger = logger
        self._device = device
        self._name = name
        self._state_attrs = {}
        self._target_temperature = 0
        self._current_temperature = 0
        self._power = None
        self._power_off_time = None
        self._buzzer = None
        self._brightness = None
        self._child_lock = None
        self._hvac_mode = None
        self.entity_id = generate_entity_id('climate.{}', unique_id, hass=_hass)

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self) -> str:
        """Return the current state."""
        return self.hvac_mode

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def hvac_modes(self):
        """Return the list of available hvac modes."""
        return [mode.value for mode in OperationMode]

    @property
    def hvac_mode(self):
        """Return hvac mode i.e. heat, cool, fan only."""
        return self._hvac_mode

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    async def async_update(self):
        from miio import DeviceException
        """Update the state of this device."""
        try:
            power = self._device.send('get_prop', ['power'])[0]
            humidity = self._device.send('get_prop', ['relative_humidity'])[0]
            target_temperature = self._device.send('get_prop', ['target_temperature'])[0]
            current_temperature = self._device.send('get_prop', ['temperature'])[0]
            power_off_time = self._device.send('get_prop', ['poweroff_time'])[0]
            buzzer = self._device.send('get_prop', ['buzzer'])[0]
            brightness = self._device.send('get_prop', ['brightness'])[0]
            child_lock = self._device.send('get_prop', ['child_lock'])[0]
            if power == 'off':
                self._hvac_mode = 'off'
            else:
                self._hvac_mode = "heat"
            self._power_off_time = None
            self._buzzer = None
            self._brightness = None
            self._child_lock = None
            self._target_temperature = current_temperature != 16
            self._current_temperature = current_temperature != 16
            self._power = power != "off"
            self._state_attrs.update({
                ATTR_HVAC_MODE: power if power == "off" else "heat",
                ATTR_TEMPERATURE: target_temperature,
                "power": power,
                "humidity": humidity,
                "poweroff_time": power_off_time,
                "buzzer": buzzer,
                "brightness": brightness,
                "child_lock": child_lock,
                "current_temperature": current_temperature
            })
        except DeviceException:
            self._logger.exception('Fail to get_prop from Xiaomi miheater.py')
            raise PlatformNotReady

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @property
    def min_temperature(self):
        """Return the minimum temperature."""
        return MIN_TEMPERATURE

    @property
    def max_temperature(self):
        """Return the maximum temperature."""
        return MAX_TEMPERATURE

    @property
    def current_operation(self):
        """Return current operation."""
        return OperationMode.Off.value if self._power == 'off' else OperationMode.Heat.value

    @property
    def operation_list(self):
        """List of available operation modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self._device.send('set_target_temperature', [int(temperature)])
        await self.async_turn_on()

    async def async_set_brightness(self, **kwargs):
        """Set new led brightness."""
        brightness = kwargs.get(CONF_BRIGHTNESS)
        if brightness is None:
            return
        await self._device.send('set_brightness', [int(brightness)])

    async def async_set_power_off_time(self, **kwargs):
        """Set new led brightness."""
        power_off_time = kwargs.get(CONF_POWEROFF_TIME)
        if power_off_time is None:
            return
        await self._device.send('set_poweroff_time', [int(power_off_time)])

    async def async_set_child_lock(self, **kwargs):
        """Set new led brightness."""
        child_lock = kwargs.get(CONF_CHILD_LOCK)
        if child_lock is None:
            return
        await self._device.send('set_child_lock', [str(child_lock)])

    async def async_set_buzzer(self, **kwargs):
        """Set new led brightness."""
        buzzer = kwargs.get(CONF_BUZZER)
        if buzzer is None:
            return
        await self._device.send('set_buzzer', [str(buzzer)])

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if hvac_mode == OperationMode.Heat.value:
            await self._device.send('set_power', ['on'])
        elif hvac_mode == OperationMode.Off.value:
            await self._device.send('set_power', ['off'])
        else:
            self._logger.error("Unrecognized operation mode: %s", hvac_mode)
