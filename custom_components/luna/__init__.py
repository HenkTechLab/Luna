"""Luna integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers import issue_registry as ir

from .const import (
    CONF_DASHBOARD_VARIANT,
    DASHBOARD_CUSTOM,
    DEFAULT_DASHBOARD_VARIANT,
    DOMAIN,
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

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "dashboard_variant": variant,
        "remove_ready_listener": remove_ready_listener,
    }
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Luna config entry."""
    entry_data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if entry_data is not None:
        entry_data["remove_ready_listener"]()
    ir.async_delete_issue(hass, DOMAIN, FINISH_CONFIGURATION_ISSUE)
    return True

