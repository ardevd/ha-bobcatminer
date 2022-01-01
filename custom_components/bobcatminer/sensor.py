"""Sensor platform for the Bobcat Miner."""
from datetime import timedelta
from typing import Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

SCAN_INTERVAL = timedelta(minutes=10)

SENSORS: Dict[str, SensorEntityDescription] = {
    "sync_gap": SensorEntityDescription(
        key="sync_gap",
        native_unit_of_measurement="blocks",
        name="Sync Gap",
        icon="mdi:cloud-sync",
    ),
    "miner_height": SensorEntityDescription(
        key="miner_height",
        native_unit_of_measurement="blocks",
        name="Miner Height",
        icon="mdi:progress-star",
    ),
    "temp": SensorEntityDescription(
        key="temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        name="Temperature",
    ),
    "ota_version": SensorEntityDescription(
        key="ota_version", name="OTA Version", icon="mdi:cloud-tags"
    ),
    "public_ip": SensorEntityDescription(
        key="public_ip", name="Public IP", icon="mdi:ip-network"
    ),
    "state": SensorEntityDescription(key="state", name="State", icon="mdi:console"),
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Sensor setup based on config entry created in the integrations UI."""

    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

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
    ):
        """Initialize miner sensor."""
        super().__init__(coordinator)
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
        return self._available

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.entity_description.key]
