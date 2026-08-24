"""Luna integration for Home Assistant."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, ServiceCall, callback
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
SERVICE_ADD_MAPPINGS = "add_mappings"
SERVICE_REMOVE_MAPPINGS = "remove_mappings"

OBSERVATION_DOMAINS = {"sensor", "binary_sensor"}
CONTROL_DOMAINS = {
    "light",
    "switch",
    "cover",
    "climate",
    "fan",
    "lock",
    "media_player",
}

MAPPING_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_OBSERVATION_ENTITIES, default=[]): vol.All(
            cv.ensure_list, [cv.entity_id]
        ),
        vol.Optional(CONF_CONTROL_ENTITIES, default=[]): vol.All(
            cv.ensure_list, [cv.entity_id]
        ),
    }
)


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


async def _async_update_mappings(
    hass: HomeAssistant, call: ServiceCall, *, remove: bool
) -> None:
    """Add or remove multiple observation/control mappings in one native action."""
    entries = hass.config_entries.async_entries(DOMAIN)
    if not entries:
        return

    entry = entries[0]
    new_options = dict(entry.options)

    requested_observations = {
        entity_id
        for entity_id in call.data.get(CONF_OBSERVATION_ENTITIES, [])
        if entity_id.split(".", 1)[0] in OBSERVATION_DOMAINS
        and not entity_id.startswith(("sensor.luna_", "binary_sensor.luna_"))
        and hass.states.get(entity_id) is not None
    }
    requested_controls = {
        entity_id
        for entity_id in call.data.get(CONF_CONTROL_ENTITIES, [])
        if entity_id.split(".", 1)[0] in CONTROL_DOMAINS
        and hass.states.get(entity_id) is not None
    }

    observations = set(new_options.get(CONF_OBSERVATION_ENTITIES, []))
    controls = set(new_options.get(CONF_CONTROL_ENTITIES, []))

    if remove:
        observations.difference_update(requested_observations)
        controls.difference_update(requested_controls)
    else:
        primary_sources = {
            entity_id
            for key in SOURCE_OPTION_KEYS
            if (entity_id := new_options.get(key))
        }
        observations.update(requested_observations - primary_sources)
        controls.update(requested_controls)

    new_options[CONF_OBSERVATION_ENTITIES] = sorted(observations)
    new_options[CONF_CONTROL_ENTITIES] = sorted(controls)

    if new_options == dict(entry.options):
        return

    hass.config_entries.async_update_entry(entry, options=new_options)
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Luna and register safe configuration-only services."""

    async def _handle_add_mappings(call: ServiceCall) -> None:
        await _async_update_mappings(hass, call, remove=False)

    async def _handle_remove_mappings(call: ServiceCall) -> None:
        await _async_update_mappings(hass, call, remove=True)

    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_MAPPINGS,
        _handle_add_mappings,
        schema=MAPPING_SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_REMOVE_MAPPINGS,
        _handle_remove_mappings,
        schema=MAPPING_SERVICE_SCHEMA,
    )
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
    observed_entities.update(entry.options.get(CONF_OBSERVATION_ENTITIES, []))
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

        source_name = new_state.attributes.get("friendly_name", new_state.entity_id)
        value = f"{source_name}: {old_state.state} → {new_state.state}"[:255]
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
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    entry_data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if entry_data is not None:
        entry_data["remove_ready_listener"]()
        if entry_data["remove_source_listener"] is not None:
            entry_data["remove_source_listener"]()
    ir.async_delete_issue(hass, DOMAIN, FINISH_CONFIGURATION_ISSUE)
    return True
