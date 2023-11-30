from .const import (SERVICE_SET_BUZZER, SERVICE_SET_BRIGHTNESS, SERVICE_SET_POWEROFF_TIME, SERVICE_SET_CHILD_LOCK)
from .schema import (SERVICE_SCHEMA_SET_BUZZER, SERVICE_SCHEMA_SET_BRIGHTNESS, SERVICE_SCHEMA_SET_POWEROFF_TIME,
                     SERVICE_SCHEMA_SET_CHILD_LOCK)

SERVICE_TO_METHOD = {
    SERVICE_SET_BUZZER: {'method': 'set_buzzer',
                         'schema': SERVICE_SCHEMA_SET_BUZZER},
    SERVICE_SET_BRIGHTNESS: {'method': 'set_brightness',
                             'schema': SERVICE_SCHEMA_SET_BRIGHTNESS},
    SERVICE_SET_POWEROFF_TIME: {'method': 'set_power_off_time',
                                'schema': SERVICE_SCHEMA_SET_POWEROFF_TIME},
    SERVICE_SET_CHILD_LOCK: {'method': 'set_child_lock',
                             'schema': SERVICE_SCHEMA_SET_CHILD_LOCK},
}
