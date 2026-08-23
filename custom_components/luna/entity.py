"""Shared entities that mirror user-selected Home Assistant sources."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, EventStateChangedData, State, callback
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN


class LunaSourceEntity(Entity):
    """Base entity that follows one configured Home Assistant entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        entry: ConfigEntry,
        source_entity_id: str | None,
        unique_suffix: str,
    ) -> None:
        """Initialize a Luna source entity."""
        self._source_entity_id = source_entity_id
        self._attr_unique_id = f"{entry.entry_id}_{unique_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Luna",
            manufacturer="HenkTechLab",
            model="Luna sensor bridge",
        )

    @property
    def source_state(self) -> State | None:
        """Return the current source state."""
        if self._source_entity_id is None:
            return None
        return self.hass.states.get(self._source_entity_id)

    @property
    def available(self) -> bool:
        """Return whether a configured source currently has a usable state."""
        source_state = self.source_state
        return source_state is not None and source_state.state not in {
            STATE_UNKNOWN,
            STATE_UNAVAILABLE,
        }

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Expose the mapping without copying sensitive source attributes."""
        source_state = self.source_state
        return {
            "source_entity_id": self._source_entity_id,
            "source_name": (
                source_state.attributes.get("friendly_name")
                if source_state is not None
                else None
            ),
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to the configured source."""
        if self._source_entity_id is None:
            return
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._source_entity_id],
                self._async_source_changed,
            )
        )

    @callback
    def _async_source_changed(
        self, event: Event[EventStateChangedData]
    ) -> None:
        """Write the new mirrored state immediately."""
        self.async_write_ha_state()
