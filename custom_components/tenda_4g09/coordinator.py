"""Data coordinator for Tenda 4G09."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from tenda_4g09 import *

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class TendaData:
    """Data returned by the Tenda 4G09 router."""

    status: RouterStatus
    data_limit: DataLimitSetting
    wan_connected: bool
    online_clients: list[OnlineClient]
    serving_cell_info: LTEServingCell


class TendaCoordinator(DataUpdateCoordinator[TendaData]):
    """Coordinator for Tenda 4G09."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Tenda4G09,
        update_interval: int,
    ) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=update_interval
            ),
        )

        self.client = client
        self._last_reconnect: datetime | None = None
        self._reconnect_cooldown = timedelta(minutes=5)
        self.data = dict()

    def _should_reconnect(self) -> bool:
        """Return whether an automatic reconnect should be attempted."""

        if self._last_reconnect is None:
            return True

        return (
            datetime.now(timezone.utc) - self._last_reconnect
            >= self._reconnect_cooldown
        )

    async def _async_update_data(self) -> TendaData:
        """Fetch data from the router."""

        try:
            return await self.hass.async_add_executor_job(
                self._get_data
            )
        except Exception as err:
            _LOGGER.warning(
                "Error communicating with Tenda 4G09: %s",
                err,
            )
            raise UpdateFailed(
                f"Error communicating with Tenda 4G09: {err}"
            ) from err

    def _get_data(self) -> TendaData:
        """Fetch all required data synchronously."""

        try:
            if not self.client.logged_in:
                self.client.login()

            status: RouterStatus = self.client.get_status()
            wan_connected: bool = self.client.is_mobile_data_connected(status)
            data_limit: DataLimitSetting = self.client.get_data_limit_setting()
            online_clients: list[OnlineClient] = self.client.get_online_clients()
        except Exception:
            _LOGGER.exception("Error getting data with Tenda 4G09")
            raise

        previous_data = self.data
        try:
            serving_cell_info = (
                self.client
                .get_telnet_client(self.client.host_ip)
                .get_signal_info()
            )
        except Exception as err:
            _LOGGER.warning(
                "Unable to retrieve serving cell information: %s",
                err,
            )
            serving_cell_info = (
                previous_data.serving_cell_info
                if previous_data is not None
                else None
            )

        if not wan_connected and self._should_reconnect():
            _LOGGER.info("LTE connection is inactive, attempting reconnect")
            try:
                self.client.mobile_data_connect()
            except Exception:
                _LOGGER.exception("Unable to reconnect mobile data")
            else:
                self._last_reconnect = datetime.now(timezone.utc)

        return TendaData(
            status=status,
            data_limit=data_limit,
            wan_connected=wan_connected,
            online_clients=online_clients,
            serving_cell_info=serving_cell_info,
        )

    async def async_reconnect(self) -> None:
        """Reconnect the LTE/WAN connection."""

        try:
            await self.hass.async_add_executor_job(
                self._reconnect
            )
        except Exception as err:
            _LOGGER.error(
                "Failed to reconnect Tenda 4G09 WAN: %s",
                err,
            )
            raise

        await self.async_request_refresh()

    def _reconnect(self) -> None:
        """Reconnect the LTE/WAN connection synchronously."""

        if not self.client.logged_in:
            self.client.login()

        self.client.mobile_data_connect()
