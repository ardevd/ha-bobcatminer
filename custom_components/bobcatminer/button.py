"""Button platform for the Bobcat miner"""
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
    ButtonDeviceClass,
)

from .const import DOMAIN
from .coordinator import BobcatMinerDataUpdateCoordinator
from bobcatpy import Bobcat


@dataclass
class BobcatMinerButtonDescriptionMixIn:
    """Required attributes for BobcatMinerButtonDescription."""

    press_action: Callable[[Bobcat], Awaitable]


@dataclass
class BobcatMinerButtonDescription(
    ButtonEntityDescription, BobcatMinerButtonDescriptionMixIn
):
    """Bobcat Miner Button description."""


REBOOT_BUTTON = BobcatMinerButtonDescription(
    key="reboot",
    name="Reboot Miner",
    device_class=ButtonDeviceClass.RESTART,
    press_action=lambda miner: miner.reboot(),
)

RESET_BUTTON = BobcatMinerButtonDescription(
    key="reset",
    name="Reset Miner",
    icon="mdi:eraser",
    press_action=lambda miner: miner.reset(),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Button setup based on config entry"""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    entities.append(BobcatMinerButton(coordinator, REBOOT_BUTTON))
    entities.append(BobcatMinerButton(coordinator, RESET_BUTTON))
    async_add_entities(entities, True)


class BobcatMinerButton(CoordinatorEntity, ButtonEntity):
    """Bobcat Miner Button entity"""

    def __init__(
        self,
        coordinator: BobcatMinerDataUpdateCoordinator,
        entity_description: BobcatMinerButtonDescription,
    ) -> None:
        """Initialize the miner Button"""
        super().__init__(coordinator)

        animal = coordinator.animal
        readable_animal = animal.replace("-", " ").title()

        self.entity_description = entity_description
        self._attr_unique_id = f"{readable_animal} {entity_description.key}"
        self._id = animal
        self._attr_name = f"{readable_animal} {entity_description.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, animal)},
            name=readable_animal,
            manufacturer="Bobcat",
        )
        # Entity name property represents the entity itself
        self._attr_has_entity_name = True

    @property
    def name(self):
        """Name of the entity."""
        return self.entity_description.name

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.press_action(self.coordinator.bobcat)
