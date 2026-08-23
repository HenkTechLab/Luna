"""Luna integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import issue_registry as ir

from .const import (
    CONF_DASHBOARD_VARIANT,
    DASHBOARD_CUSTOM,
    DEFAULT_DASHBOARD_VARIANT,
    DOMAIN,
)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Luna from YAML by rejecting YAML configuration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Luna from a config entry."""
    variant = entry.data.get(CONF_DASHBOARD_VARIANT, DEFAULT_DASHBOARD_VARIANT)
    dependency_note = (
        " Installeer ook Mushroom en card-mod via HACS."
        if variant == DASHBOARD_CUSTOM
        else ""
    )

    ir.async_create_issue(
        hass,
        DOMAIN,
        "finish_configuration",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="finish_configuration",
        translation_placeholders={
            "dashboard_file": f"luna-dashboard-{variant}.yaml",
            "dependency_note": dependency_note,
        },
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"dashboard_variant": variant}
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Luna config entry."""
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    ir.async_delete_issue(hass, DOMAIN, "finish_configuration")
    return True

