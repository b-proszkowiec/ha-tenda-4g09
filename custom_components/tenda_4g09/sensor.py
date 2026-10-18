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
from homeassistant.const import UnitOfDataRate, UnitOfInformation, UnitOfFrequency, SIGNAL_STRENGTH_DECIBELS, SIGNAL_STRENGTH_DECIBELS_MILLIWATT
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

def get_serving_cell_info(data: object) -> LTEServingCell:
    return data.serving_cell_info

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
        key="signal_index",
        translation_key="signal_index",
        value_fn=lambda data: get_router_status(data).sim_info.rssi.value,
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
    TendaSensorEntityDescription(
        key="rat",
        translation_key="rat",
        value_fn=lambda data: (
            x.rat if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="duplex",
        translation_key="duplex",
        value_fn=lambda data: (
            x.duplex if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="mcc",
        translation_key="mcc",
        value_fn=lambda data: (
            x.mcc if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="mnc",
        translation_key="mnc",
        value_fn=lambda data: (
            x.mnc if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="cell_id",
        translation_key="cell_id",
        value_fn=lambda data: (
            x.cell_id if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="pci",
        translation_key="pci",
        value_fn=lambda data: (
            x.pci if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="earfcn",
        name="EARFCN",
        value_fn=lambda data: (
            x.earfcn if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="band",
        translation_key="band",
        value_fn=lambda data: (
            x.band if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="ul_bandwidth",
        translation_key="ul_bandwidth",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.MEGAHERTZ,
        value_fn=lambda data: (
            x.ul_bandwidth if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="dl_bandwidth",
        translation_key="dl_bandwidth",
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.MEGAHERTZ,
        value_fn=lambda data: (
            x.dl_bandwidth if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
    TendaSensorEntityDescription(
        key="rsrp",
        name="RSRP",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        value_fn=lambda data: (
            x.rsrp if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
        TendaSensorEntityDescription(
        key="rsrq",
        name="RSRQ",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        value_fn=lambda data: (
            x.rsrq if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
        TendaSensorEntityDescription(
        key="rssi",
        name="RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        value_fn=lambda data: (
            x.rssi if (x := get_serving_cell_info(data)) is not None else None
        )
    ),
        TendaSensorEntityDescription(
        key="sinr",
        name="SINR",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        value_fn=lambda data: (
            x.sinr if (x := get_serving_cell_info(data)) is not None else None
        )
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
