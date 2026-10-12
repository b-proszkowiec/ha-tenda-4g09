"""The Tenda 4G09 integration."""

from __future__ import annotations

import logging

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import UpdateFailed

from tenda_4g09 import Tenda4G09

from .const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DOMAIN,
    SERVICE_RECONNECT,
)
from .coordinator import TendaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = [
    "sensor",
    "binary_sensor",
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(
    hass: HomeAssistant,
    config: dict[str, Any],
) -> bool:
    """Set up the Tenda 4G09 integration."""

    async def async_reconnect(call: ServiceCall) -> None:
        """Reconnect the LTE WAN connection."""

        entries = hass.config_entries.async_entries(DOMAIN)

        if not entries:
            raise HomeAssistantError(
                "No Tenda 4G09 integration is configured."
            )

        reconnected = False

        for entry in entries:
            coordinator: TendaCoordinator | None = hass.data[
                DOMAIN
            ].get(entry.entry_id)

            if coordinator is None:
                continue

            try:
                await coordinator.async_reconnect()
                reconnected = True
            except Exception as err:
                raise HomeAssistantError(
                    f"Failed to reconnect Tenda 4G09: {err}"
                ) from err

        if not reconnected:
            raise HomeAssistantError(
                "Tenda 4G09 integration is not loaded."
            )

    if not hass.services.has_service(
        DOMAIN,
        SERVICE_RECONNECT,
    ):
        hass.services.async_register(
            DOMAIN,
            SERVICE_RECONNECT,
            async_reconnect,
        )

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Tenda 4G09 from a config entry."""

    client = Tenda4G09(
        entry.data[CONF_HOST],
        entry.data[CONF_PASSWORD],
    )

    coordinator = TendaCoordinator(
        hass=hass,
        client=client,
        update_interval=entry.data[CONF_SCAN_INTERVAL],
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    try:
        await coordinator.async_config_entry_first_refresh()
    except UpdateFailed as err:
        _LOGGER.warning(
            "Unable to connect to Tenda 4G09 during startup: %s",
            err,
        )

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    entry.async_on_unload(
        entry.add_update_listener(async_reload_entry)
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a Tenda 4G09 config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        coordinator: TendaCoordinator = hass.data[DOMAIN].pop(
            entry.entry_id
        )

        await coordinator.async_shutdown()

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload the integration."""

    await hass.config_entries.async_reload(entry.entry_id)
