"""Config flow for Luna."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_CALENDAR_ENTITY,
    CONF_CONTROL_ENTITIES,
    CONF_DASHBOARD_VARIANT,
    CONF_ENERGY_ENTITY,
    CONF_OBSERVATION_ENTITIES,
    CONF_POWER_ENTITY,
    CONF_PRESENCE_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    DASHBOARD_CUSTOM,
    DASHBOARD_NATIVE,
    DEFAULT_DASHBOARD_VARIANT,
    DOMAIN,
    SOURCE_OPTION_KEYS,
)

CONF_OBSERVATIONS_ADD = "observations_add"
CONF_OBSERVATIONS_REMOVE = "observations_remove"
CONF_CONTROLS_ADD = "controls_add"
CONF_CONTROLS_REMOVE = "controls_remove"

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

MAIN_SOURCES_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_PRESENCE_ENTITY): EntitySelector(
            EntitySelectorConfig(
                domain=["binary_sensor", "person", "device_tracker", "input_boolean"]
            )
        ),
        vol.Optional(CONF_TEMPERATURE_ENTITY): EntitySelector(
            EntitySelectorConfig(domain=["sensor"])
        ),
        vol.Optional(CONF_ENERGY_ENTITY): EntitySelector(
            EntitySelectorConfig(domain=["sensor"])
        ),
        vol.Optional(CONF_POWER_ENTITY): EntitySelector(
            EntitySelectorConfig(domain=["sensor"])
        ),
        vol.Optional(CONF_CALENDAR_ENTITY): EntitySelector(
            EntitySelectorConfig(domain=["calendar"])
        ),
    }
)


def _friendly_options(
    hass: HomeAssistant,
    domains: set[str],
    *,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
) -> list[SelectOptionDict]:
    """Build native HA select options with friendly names and entity IDs."""
    included = include
    excluded = exclude or set()
    result: list[SelectOptionDict] = []

    for state in hass.states.async_all():
        entity_id = state.entity_id
        domain = entity_id.split(".", 1)[0]
        if domain not in domains or entity_id in excluded:
            continue
        if included is not None and entity_id not in included:
            continue

        friendly_name = state.attributes.get("friendly_name", entity_id)
        result.append(
            SelectOptionDict(
                value=entity_id,
                label=f"{friendly_name} ({entity_id})",
            )
        )

    return sorted(result, key=lambda item: str(item["label"]).casefold())


def _multi_select(options: list[SelectOptionDict]) -> SelectSelector:
    """Create a searchable native multi-select dropdown."""
    return SelectSelector(
        SelectSelectorConfig(
            options=options,
            multiple=True,
            mode=SelectSelectorMode.DROPDOWN,
        )
    )


class LunaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Luna."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> "LunaOptionsFlow":
        """Create the Luna options flow."""
        return LunaOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Luna", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_DASHBOARD_VARIANT,
                        default=DEFAULT_DASHBOARD_VARIANT,
                    ): vol.In(
                        {
                            DASHBOARD_NATIVE: "Native (alleen Home Assistant)",
                            DASHBOARD_CUSTOM: "Custom (Mushroom en card-mod)",
                        }
                    )
                }
            ),
        )


class LunaOptionsFlow(config_entries.OptionsFlowWithReload):
    """Configure the Home Assistant entities observed by Luna."""

    def _options(self) -> dict[str, Any]:
        """Return a mutable copy of the current persisted options."""
        return dict(self.config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage Luna mappings in one native multi-select form."""
        if user_input is not None:
            options = self._options()

            observations = set(options.get(CONF_OBSERVATION_ENTITIES, []))
            observations.update(user_input.get(CONF_OBSERVATIONS_ADD, []))
            observations.difference_update(
                user_input.get(CONF_OBSERVATIONS_REMOVE, [])
            )
            options[CONF_OBSERVATION_ENTITIES] = sorted(observations)

            controls = set(options.get(CONF_CONTROL_ENTITIES, []))
            controls.update(user_input.get(CONF_CONTROLS_ADD, []))
            controls.difference_update(user_input.get(CONF_CONTROLS_REMOVE, []))
            options[CONF_CONTROL_ENTITIES] = sorted(controls)

            return self.async_create_entry(data=options)

        options = self.config_entry.options
        observations = set(options.get(CONF_OBSERVATION_ENTITIES, []))
        controls = set(options.get(CONF_CONTROL_ENTITIES, []))
        main_sources = {
            entity_id
            for key in SOURCE_OPTION_KEYS
            if (entity_id := options.get(key)) is not None
        }

        schema: dict[vol.Optional, Any] = {}

        available_observations = _friendly_options(
            self.hass,
            OBSERVATION_DOMAINS,
            exclude=observations | main_sources,
        )
        if available_observations:
            schema[vol.Optional(CONF_OBSERVATIONS_ADD, default=[])] = _multi_select(
                available_observations
            )

        removable_observations = _friendly_options(
            self.hass,
            OBSERVATION_DOMAINS,
            include=observations,
        )
        if removable_observations:
            schema[vol.Optional(CONF_OBSERVATIONS_REMOVE, default=[])] = _multi_select(
                removable_observations
            )

        available_controls = _friendly_options(
            self.hass,
            CONTROL_DOMAINS,
            exclude=controls,
        )
        if available_controls:
            schema[vol.Optional(CONF_CONTROLS_ADD, default=[])] = _multi_select(
                available_controls
            )

        removable_controls = _friendly_options(
            self.hass,
            CONTROL_DOMAINS,
            include=controls,
        )
        if removable_controls:
            schema[vol.Optional(CONF_CONTROLS_REMOVE, default=[])] = _multi_select(
                removable_controls
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
        )

    async def async_step_sources(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Retain a dedicated main-source editor for compatibility."""
        if user_input is not None:
            options = self._options()
            for key in SOURCE_OPTION_KEYS:
                if key in user_input:
                    options[key] = user_input[key]
                else:
                    options.pop(key, None)
            return self.async_create_entry(data=options)

        return self.async_show_form(
            step_id="sources",
            data_schema=self.add_suggested_values_to_schema(
                MAIN_SOURCES_SCHEMA, self.config_entry.options
            ),
        )
