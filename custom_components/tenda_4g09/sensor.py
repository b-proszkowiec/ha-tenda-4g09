"""Sensors for Tenda 4G09."""

from __future__ import annotations

from typing import Any
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_MANUFACTURER, DOMAIN, MODEL
from .coordinator import *


PARALLEL_UPDATES = 0

def get_router_status(data: object) -> RouterStatus:
    return data.status

def get_data_limit(data: object) -> DataLimitSetting:
    return data.data_limit

def get_connected_clients(data: object) -> list[dict]:
    clients: list[OnlineClient] = data.online_clients
    return [
        {
            "name": device.name,
            "ip": device.ip,
            "mac": device.device_id,
            "upload_speed": device.upload_speed,
            "download_speed": device.download_speed,
            "blocked": device.blocked,
            "guest": device.guest,
        }
        for device in clients
    ]

@dataclass(frozen=True, kw_only=True)
class TendaSensorEntityDescription(SensorEntityDescription):
    """Describe a Tenda 4G09 sensor."""

    value_fn: Callable[[object], object]
    attributes_fn: Callable[[Any], dict[str, Any]] | None = None


SENSORS: tuple[TendaSensorEntityDescription, ...] = (
    TendaSensorEntityDescription(
        key="wan_ip",
        translation_key="wan_ip",
        value_fn=lambda data: get_router_status(data).wan_info[0].ip,
    ),
    TendaSensorEntityDescription(
        key="lan_ip",
        translation_key="lan_ip",
        value_fn=lambda data: get_router_status(data).lan_ip,
    ),
    TendaSensorEntityDescription(
        key="lan_mac",
        translation_key="lan_mac",
        value_fn=lambda data: get_router_status(data).lan_mac,
    ),
    TendaSensorEntityDescription(
        key="rssi",
        translation_key="rssi",
        value_fn=lambda data: get_router_status(data).sim_info.rssi,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TendaSensorEntityDescription(
        key="connection_type",
        translation_key="connection_type",
        value_fn=lambda data: get_router_status(data).sim_info.connection_type,
    ),
    TendaSensorEntityDescription(
        key="internet_status",
        translation_key="internet_status",
        value_fn=lambda data: get_router_status(data).sim_info.internet_status,
    ),
    TendaSensorEntityDescription(
        key="sim_status",
        translation_key="sim_status",
        value_fn=lambda data: get_router_status(data).sim_info.sim_status
    ),
    TendaSensorEntityDescription(
        key="connected_clients",
        translation_key="connected_clients",
        value_fn=lambda data: get_router_status(data).client_count,
        attributes_fn=lambda data: {
            "devices": get_connected_clients(data),
        },
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TendaSensorEntityDescription(
        key="work_mode",
        translation_key="work_mode",
        value_fn=lambda data: get_router_status(data).work_mode,
    ),
    TendaSensorEntityDescription(
        key="device_name",
        translation_key="device_name",
        value_fn=lambda data: get_router_status(data).device_name,
    ),
    TendaSensorEntityDescription(
        key="download_speed",
        translation_key="download_speed",
        value_fn=lambda data: get_router_status(data).wan_info[0].download_speed,
        native_unit_of_measurement=UnitOfDataRate.KILOBYTES_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TendaSensorEntityDescription(
        key="upload_speed",
        translation_key="upload_speed",
        value_fn=lambda data: get_router_status(data).wan_info[0].upload_speed,
        native_unit_of_measurement=UnitOfDataRate.KILOBYTES_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    TendaSensorEntityDescription(
        key="total_used_mb",
        translation_key="total_used_mb",
        value_fn=lambda data: get_data_limit(data).total_used_mb,
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tenda 4G09 sensors."""

    coordinator: TendaCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        TendaSensor(
            coordinator,
            entry,
            description,
        )
        for description in SENSORS
    )


class TendaSensor(
    CoordinatorEntity[TendaCoordinator],
    SensorEntity,
):
    """Represent a Tenda 4G09 sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TendaCoordinator,
        entry: ConfigEntry,
        description: TendaSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self.entity_description = description

        self._attr_unique_id = (
            f"{entry.entry_id}_{description.key}"
        )

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Tenda 4G09",
            "manufacturer": ATTR_MANUFACTURER,
            "model": MODEL,
        }

    @property
    def native_value(self):
        """Return the current value."""

        return self.entity_description.value_fn(
            self.coordinator.data
        )

    @property
    def extra_state_attributes(self):
        if self.entity_description.attributes_fn:
            return self.entity_description.attributes_fn(
                self.coordinator.data
            )

        return None
