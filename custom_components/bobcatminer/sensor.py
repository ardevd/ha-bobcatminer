"""Sensor platform for the Bobcat Miner."""
from datetime import timedelta
from typing import Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=15)

SENSORS: dict[str, SensorEntityDescription] = {
    "created": SensorEntityDescription(
        key="created",
        name="Created",
        icon="mdi:clock-start",
    ),
    "temp": SensorEntityDescription(
        key="temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        name="Temperature",
    ),
    "ota_version": SensorEntityDescription(
        key="ota_version", name="OTA Version", icon="mdi:cloud-tags"
    ),
    "image": SensorEntityDescription(
        key="image", name="Miner Image", icon="mdi:docker"
    ),
    "image_version": SensorEntityDescription(
        key="image_version", name="Miner Image Version", icon="mdi:docker"
    ),
    "public_ip": SensorEntityDescription(
        key="public_ip", name="Public IP", icon="mdi:ip-network"
    ),
    "state": SensorEntityDescription(key="state", name="State", icon="mdi:console"),
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Sensor setup based on config entry created in the integrations UI."""

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor in SENSORS.values():
        entities.append(BobcatMinerSensor(coordinator, sensor))

    async_add_entities(entities, True)


class BobcatMinerSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing a bobcat miner."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize miner sensor."""
        super().__init__(coordinator)

        # Failed to get status_summary
        if "animal" not in coordinator.data:
            raise RuntimeError("Failed to get correct data from Bobcat")

        animal = coordinator.data["animal"]
        readable_animal = animal.replace("-", " ").title()

        self.entity_description = entity_description

        self._attr_extra_state_attributes = {}
        self._attr_unique_id = f"{readable_animal} {entity_description.key}"
        self._id = animal
        self._attr_name = f"{readable_animal} {entity_description.name}"
        self._available = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, animal)},
            name=readable_animal,
            manufacturer="Bobcat",
        )
        self._state = None

    @property
    def available(self):
        """Return sensor availability."""
        if "state" in self.coordinator.data:
            # bobcatpy will return this if it fails to talk to bobcat
            return self.coordinator.data["state"] != "unavailable"

        return self._available

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.entity_description.key in self.coordinator.data:
            return self.coordinator.data[self.entity_description.key]

        return None
