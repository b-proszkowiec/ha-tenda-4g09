"""Binary sensors for Tenda 4G09."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import ATTR_MANUFACTURER, DOMAIN, MODEL
from .coordinator import TendaCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tenda 4G09 binary sensors."""

    coordinator: TendaCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_entities(
        [
            TendaWanConnectedSensor(
                coordinator,
                entry,
            )
        ]
    )


class TendaWanConnectedSensor(
    CoordinatorEntity[TendaCoordinator],
    BinarySensorEntity,
):
    """Represent WAN connectivity."""

    _attr_has_entity_name = True
    _attr_translation_key = "wan_connected"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
        coordinator: TendaCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self._attr_unique_id = (
            f"{entry.entry_id}_wan_connected"
        )

        self._attr_device_info = {
            "identifiers": {
                (DOMAIN, entry.entry_id)
            },
            "name": "Tenda 4G09",
            "manufacturer": ATTR_MANUFACTURER,
            "model": MODEL,
        }

    @property
    def is_on(self) -> bool:
        """Return true if WAN is connected."""

        return self.coordinator.data.wan_connected
