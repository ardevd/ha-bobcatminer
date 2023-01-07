"""Sensor platform for the Bobcat Miner."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BobcatMinerDataUpdateCoordinator

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
    "led_color": SensorEntityDescription(
        key="led", name="LED Color", icon="mdi:led-outline"
    ),
    "state": SensorEntityDescription(key="state", name="State", icon="mdi:console"),
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Sensor setup based on config entry created in the integrations UI."""

    coordinator: BobcatMinerDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    # Due to the Bobcat miner's aggressive rate limiting, we avoid initial data fresh on platform setup.
    # await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor in SENSORS.values():
        entities.append(BobcatMinerSensor(coordinator, sensor))

    async_add_entities(entities, True)


class BobcatMinerSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing a bobcat miner."""

    def __init__(
        self,
        coordinator: BobcatMinerDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize miner sensor."""
        super().__init__(coordinator)

        animal = coordinator.animal
        readable_animal = animal.replace("-", " ").title()

        self.entity_description = entity_description

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
        # Entity name property represents the entity itself
        self._attr_has_entity_name = True

    @property
    def name(self):
        """Name of the entity."""
        return self.entity_description.name

    @property
    def available(self):
        """Return sensor availability."""
        if self.coordinator.data and "state" in self.coordinator.data:
            # bobcatpy will return this if it fails to talk to bobcat
            return self.coordinator.data["state"] != "unavailable"

        # State key not present, assume miner is unavailable
        return False

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.entity_description.key in self.coordinator.data:
            return self.coordinator.data[self.entity_description.key]

        return None
