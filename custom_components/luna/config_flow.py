"""Config flow for Luna."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DASHBOARD_VARIANT,
    DASHBOARD_CUSTOM,
    DASHBOARD_NATIVE,
    DEFAULT_DASHBOARD_VARIANT,
    DOMAIN,
)


class LunaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Luna."""

    VERSION = 1

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

