"""Config flow for Tenda 4G09."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
import voluptuous as vol

from tenda_4g09 import Tenda4G09

from .const import (
    CONF_HOST,
    CONF_PASSWORD,
    DOMAIN,
)


async def _validate_input(
    hass: HomeAssistant,
    user_input: dict[str, Any],
) -> None:
    """Validate the connection to the router."""

    client = Tenda4G09(
        user_input[CONF_HOST],
        user_input[CONF_PASSWORD],
    )

    try:
        await hass.async_add_executor_job(client.login)

        await hass.async_add_executor_job(client.get_status)

    finally:
        try:
            await hass.async_add_executor_job(client.logout)
        except Exception:
            pass


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate authentication failed."""


class Tenda4G09ConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Tenda 4G09."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the user step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                user_input[CONF_HOST].strip().lower()
            )

            self._abort_if_unique_id_configured()

            try:
                await _validate_input(
                    self.hass,
                    user_input,
                )

            except Exception as err:
                error_name = type(err).__name__

                if "Authentication" in error_name:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"

            else:
                return self.async_create_entry(
                    title=f"Tenda 4G09 ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST
                ): str,

                vol.Required(
                    CONF_PASSWORD
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
