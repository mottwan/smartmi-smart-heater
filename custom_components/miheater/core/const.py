from homeassistant.components.climate.const import SUPPORT_TARGET_TEMPERATURE

CONF_BUZZER = 'buzzer'
CONF_BRIGHTNESS = 'brightness'
CONF_POWEROFF_TIME = 'poweroff_time'
CONF_CHILD_LOCK = 'lock'
DOMAIN = 'miheater'
DEFAULT_NAME = 'MiHeater'
DATA_KEY = "climate.xiaomi_miio_heater"  # 'climate.xiaomi_miio_heater'
MIN_TEMPERATURE = 16
MAX_TEMPERATURE = 32
SERVICE_SET_BUZZER = 'xiaomi_heater_set_buzzer'
SERVICE_SET_BRIGHTNESS = 'xiaomi_heater_set_brightness'
SERVICE_SET_POWEROFF_TIME = 'xiaomi_heater_set_poweroff_time'
SERVICE_SET_CHILD_LOCK = 'xiaomi_heater_set_child_lock'
SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE)

