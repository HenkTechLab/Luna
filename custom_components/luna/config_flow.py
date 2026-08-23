"""Config flow for Luna."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

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
)

OPTIONS_SCHEMA = vol.Schema(
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
        vol.Optional(CONF_OBSERVATION_ENTITIES): EntitySelector(
            EntitySelectorConfig(
                domain=["sensor", "binary_sensor"], multiple=True
            )
        ),
        vol.Optional(CONF_CONTROL_ENTITIES): EntitySelector(
            EntitySelectorConfig(
                domain=[
                    "light",
                    "switch",
                    "cover",
                    "climate",
                    "fan",
                    "lock",
                    "media_player",
                ],
                multiple=True,
            )
        ),
    }
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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage Luna source mappings."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )

