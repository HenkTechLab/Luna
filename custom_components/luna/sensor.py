"""Sensor platform for Luna."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_CALENDAR_ENTITY,
    CONF_CONTROL_ENTITIES,
    CONF_ENERGY_ENTITY,
    CONF_OBSERVATION_ENTITIES,
    CONF_POWER_ENTITY,
    CONF_PRESENCE_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    DOMAIN,
)
from .entity import LunaSourceEntity


@dataclass(frozen=True, kw_only=True)
class LunaSourceDescription:
    """Describe one stable Luna source sensor."""

    option_key: str
    translation_key: str
    object_id: str
    icon: str
    forwarded_attributes: tuple[str, ...] = ()


SOURCE_DESCRIPTIONS = (
    LunaSourceDescription(
        option_key=CONF_TEMPERATURE_ENTITY,
        translation_key="temperature",
        object_id="luna_temperatuur",
        icon="mdi:thermometer",
    ),
    LunaSourceDescription(
        option_key=CONF_ENERGY_ENTITY,
        translation_key="energy",
        object_id="luna_energie",
        icon="mdi:lightning-bolt",
    ),
    LunaSourceDescription(
        option_key=CONF_POWER_ENTITY,
        translation_key="power",
        object_id="luna_vermogen",
        icon="mdi:flash",
    ),
    LunaSourceDescription(
        option_key=CONF_CALENDAR_ENTITY,
        translation_key="calendar",
        object_id="luna_agenda",
        icon="mdi:calendar",
        forwarded_attributes=(
            "message",
            "start_time",
            "end_time",
            "location",
            "all_day",
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Luna source and mapping summary sensors."""
    entities: list[SensorEntity] = [
        LunaMirroredSensor(entry, description)
        for description in SOURCE_DESCRIPTIONS
    ]
    entities.extend(
        [
            LunaMappingCountSensor(entry, "sources"),
            LunaMappingCountSensor(entry, "controls"),
        ]
    )
    async_add_entities(entities)


class LunaMirroredSensor(LunaSourceEntity, SensorEntity):
    """Mirror a selected sensor or calendar entity."""

    def __init__(
        self, entry: ConfigEntry, description: LunaSourceDescription
    ) -> None:
        """Initialize a mirrored Luna sensor."""
        self._description = description
        self._attr_translation_key = description.translation_key
        self._attr_suggested_object_id = description.object_id
        self._attr_icon = description.icon
        super().__init__(
            entry,
            entry.options.get(description.option_key),
            description.translation_key,
        )

    @property
    def native_value(self) -> str | None:
        """Return the source state unchanged."""
        source_state = self.source_state
        return source_state.state if source_state is not None else None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Forward the unit exposed by the selected source."""
        source_state = self.source_state
        if source_state is None:
            return None
        return source_state.attributes.get("unit_of_measurement")

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        """Expose mapping information and selected calendar metadata."""
        attributes = dict(super().extra_state_attributes)
        source_state = self.source_state
        if source_state is not None:
            for key in self._description.forwarded_attributes:
                if key in source_state.attributes:
                    attributes[key] = source_state.attributes[key]
        return attributes


class LunaMappingCountSensor(SensorEntity):
    """Show how many observation or control entities are configured."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_native_unit_of_measurement = "entities"

    def __init__(self, entry: ConfigEntry, mapping_type: str) -> None:
        """Initialize a mapping count sensor."""
        self._entry = entry
        self._mapping_type = mapping_type
        self._attr_unique_id = f"{entry.entry_id}_{mapping_type}_count"
        self._attr_translation_key = f"linked_{mapping_type}"
        self._attr_suggested_object_id = (
            "luna_gekoppelde_bronnen"
            if mapping_type == "sources"
            else "luna_gekoppelde_apparaten"
        )
        self._attr_icon = (
            "mdi:database-eye"
            if mapping_type == "sources"
            else "mdi:devices"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Luna",
            manufacturer="HenkTechLab",
            model="Luna sensor bridge",
        )

    @property
    def native_value(self) -> int:
        """Return the number of configured entities."""
        return len(self._configured_entities)

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        """List configured entity IDs for transparent troubleshooting."""
        return {"entity_ids": self._configured_entities}

    @property
    def _configured_entities(self) -> list[str]:
        """Return the configured entities for this summary."""
        if self._mapping_type == "controls":
            return list(self._entry.options.get(CONF_CONTROL_ENTITIES, []))

        entities = [
            self._entry.options.get(key)
            for key in (
                CONF_PRESENCE_ENTITY,
                CONF_TEMPERATURE_ENTITY,
                CONF_ENERGY_ENTITY,
                CONF_POWER_ENTITY,
                CONF_CALENDAR_ENTITY,
            )
        ]
        entities.extend(
            self._entry.options.get(CONF_OBSERVATION_ENTITIES, [])
        )
        return [entity_id for entity_id in entities if entity_id]
