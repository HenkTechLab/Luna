"""Constants for Luna."""

DOMAIN = "luna"

CONF_DASHBOARD_VARIANT = "dashboard_variant"
CONF_PRESENCE_ENTITY = "presence_entity"
CONF_TEMPERATURE_ENTITY = "temperature_entity"
CONF_ENERGY_ENTITY = "energy_entity"
CONF_POWER_ENTITY = "power_entity"
CONF_CALENDAR_ENTITY = "calendar_entity"
CONF_OBSERVATION_ENTITIES = "observation_entities"
CONF_CONTROL_ENTITIES = "control_entities"

DASHBOARD_NATIVE = "native"
DASHBOARD_CUSTOM = "custom"
DEFAULT_DASHBOARD_VARIANT = DASHBOARD_NATIVE

PLATFORMS = ["binary_sensor", "sensor"]

SOURCE_OPTION_KEYS = (
    CONF_PRESENCE_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    CONF_ENERGY_ENTITY,
    CONF_POWER_ENTITY,
    CONF_CALENDAR_ENTITY,
)

