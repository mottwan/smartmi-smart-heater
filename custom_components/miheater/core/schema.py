import voluptuous as vol
from homeassistant.const import CONF_HOST, ATTR_ENTITY_ID, CONF_NAME, CONF_TOKEN
from homeassistant.helpers import config_validation as cv
from homeassistant.components.climate import PLATFORM_SCHEMA

from .const import (CONF_BUZZER, CONF_BRIGHTNESS, CONF_POWEROFF_TIME, CONF_CHILD_LOCK)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_TOKEN): cv.string,
})

SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.entity_ids
})

SERVICE_SCHEMA_SET_BUZZER = SERVICE_SCHEMA.extend({
    vol.Required(CONF_BUZZER): vol.All(vol.Coerce(str), vol.Clamp('off', 'on'))
})

SERVICE_SCHEMA_SET_BRIGHTNESS = SERVICE_SCHEMA.extend({
    vol.Required(CONF_BRIGHTNESS): vol.All(vol.Coerce(int), vol.Range(min=0, max=2)),
})

SERVICE_SCHEMA_SET_POWEROFF_TIME = SERVICE_SCHEMA.extend({
    vol.Required(CONF_POWEROFF_TIME): vol.All(vol.Coerce(int), vol.Range(min=0, max=28800)),
})

SERVICE_SCHEMA_SET_CHILD_LOCK = SERVICE_SCHEMA.extend({
    vol.Required(CONF_CHILD_LOCK): vol.All(vol.Coerce(str), vol.Clamp('off', 'on'))
})
