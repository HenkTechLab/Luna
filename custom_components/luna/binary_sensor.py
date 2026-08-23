"""Binary sensor platform for Luna."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_PRESENCE_ENTITY
from .entity import LunaSourceEntity

PRESENT_STATES = {"home", "occupied", "on", "present", "true"}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Luna presence mirror."""
    async_add_entities(
        [LunaPresenceBinarySensor(entry, entry.options.get(CONF_PRESENCE_ENTITY))]
    )


class LunaPresenceBinarySensor(LunaSourceEntity, BinarySensorEntity):
    """Represent presence selected in the Luna options flow."""

    _attr_device_class = BinarySensorDeviceClass.PRESENCE
    _attr_icon = "mdi:home-account"
    _attr_suggested_object_id = "luna_aanwezigheid"
    _attr_translation_key = "presence"

    def __init__(
        self, entry: ConfigEntry, source_entity_id: str | None
    ) -> None:
        """Initialize the Luna presence sensor."""
        super().__init__(entry, source_entity_id, "presence")

    @property
    def is_on(self) -> bool | None:
        """Return whether the selected presence source means present."""
        source_state = self.source_state
        if source_state is None:
            return None
        return source_state.state.lower() in PRESENT_STATES
