"""Luna integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_CONTROL_ENTITIES,
    CONF_DASHBOARD_VARIANT,
    CONF_OBSERVATION_ENTITIES,
    DASHBOARD_CUSTOM,
    DEFAULT_DASHBOARD_VARIANT,
    DOMAIN,
    PLATFORMS,
    SOURCE_OPTION_KEYS,
)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

CONFIGURATION_READY_ENTITY = "binary_sensor.luna_configuratie_gereed"
FINISH_CONFIGURATION_ISSUE = "finish_configuration"


@callback
def _sync_configuration_issue(hass: HomeAssistant, variant: str) -> None:
    """Keep the setup reminder aligned with the loaded Luna packages."""
    if hass.states.is_state(CONFIGURATION_READY_ENTITY, "on"):
        ir.async_delete_issue(hass, DOMAIN, FINISH_CONFIGURATION_ISSUE)
        return

    dependency_note = (
        " Installeer ook Mushroom en card-mod via HACS."
        if variant == DASHBOARD_CUSTOM
        else ""
    )
    ir.async_create_issue(
        hass,
        DOMAIN,
        FINISH_CONFIGURATION_ISSUE,
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="finish_configuration",
        translation_placeholders={
            "dashboard_file": f"luna-dashboard-{variant}.yaml",
            "dependency_note": dependency_note,
        },
    )


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Luna from YAML by rejecting YAML configuration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Luna from a config entry."""
    variant = entry.data.get(CONF_DASHBOARD_VARIANT, DEFAULT_DASHBOARD_VARIANT)

    @callback
    def _handle_configuration_ready_change(event: Event) -> None:
        """Update the reminder when the package readiness sensor changes."""
        _sync_configuration_issue(hass, variant)

    remove_ready_listener = async_track_state_change_event(
        hass, [CONFIGURATION_READY_ENTITY], _handle_configuration_ready_change
    )
    _sync_configuration_issue(hass, variant)

    observed_entities = {
        entry.options.get(option_key) for option_key in SOURCE_OPTION_KEYS
    }
    observed_entities.update(
        entry.options.get(CONF_OBSERVATION_ENTITIES, [])
    )
    observed_entities.discard(None)

    @callback
    def _handle_observed_source_change(
        event: Event[EventStateChangedData],
    ) -> None:
        """Record source changes for Luna's local learning timeline."""
        old_state = event.data["old_state"]
        new_state = event.data["new_state"]
        if (
            new_state is None
            or new_state.state in {STATE_UNKNOWN, STATE_UNAVAILABLE}
            or old_state is None
            or old_state.state in {STATE_UNKNOWN, STATE_UNAVAILABLE}
            or old_state.state == new_state.state
            or hass.states.get("input_text.luna_last_event") is None
        ):
            return

        source_name = new_state.attributes.get(
            "friendly_name", new_state.entity_id
        )
        value = (
            f"{source_name}: {old_state.state} → {new_state.state}"
        )[:255]
        hass.async_create_task(
            hass.services.async_call(
                "input_text",
                "set_value",
                {
                    "entity_id": "input_text.luna_last_event",
                    "value": value,
                },
                blocking=False,
            )
        )

    remove_source_listener = (
        async_track_state_change_event(
            hass,
            sorted(observed_entities),
            _handle_observed_source_change,
        )
        if observed_entities
        else None
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "dashboard_variant": variant,
        "remove_ready_listener": remove_ready_listener,
        "remove_source_listener": remove_source_listener,
        "control_entities": entry.options.get(CONF_CONTROL_ENTITIES, []),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Luna config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if not unload_ok:
        return False

    entry_data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if entry_data is not None:
        entry_data["remove_ready_listener"]()
        if entry_data["remove_source_listener"] is not None:
            entry_data["remove_source_listener"]()
    ir.async_delete_issue(hass, DOMAIN, FINISH_CONFIGURATION_ISSUE)
    return True

