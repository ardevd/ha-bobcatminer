"""Button platform for the Bobcat miner"""
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.button import ButtonDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .const import DOMAIN
from .coordinator import BobcatMinerDataUpdateCoordinator

@dataclass
class BobcatMinerButtonDescriptionMixIn:
    """Required attributes for BobcatMinerButtonDescription."""

    press_action: Callable[[DataUpdateCoordinator], Awaitable]


@dataclass
class BobcatMinerButtonDescription(
    ButtonEntityDescription, BobcatMinerButtonDescriptionMixIn
):
    """Bobcat Miner Button description."""


REBOOT_BUTTON = BobcatMinerButtonDescription(
    key="reboot",
    name="Reboot Miner",
    icon="mdi:reboot",
    device_class=ButtonDeviceClass.RESTART,
    press_action=lambda miner: miner.reboot(),
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
    async_add_entities()


class BobcatMinerButton(CoordinatorEntity, ButtonEntity):
    """Bobcat Miner Button entity"""

    def __init__(
        self,
        coordinator: BobcatMinerDataUpdateCoordinator,
        entity_description: ButtonEntityDescription,
    ) -> None:
        """Initialize the miner Button"""
        super().__init__(coordinator)

        # Failed to get status_summary
        if "animal" not in coordinator.data:
            raise RuntimeError("Failed to get correct data from Bobcat")

        animal = coordinator.data["animal"]
        readable_animal = animal.replace("-", " ").title()

        self.entity_description = entity_description
        self._attr_unique_id = f"{readable_animal} {entity_description.key}"
        self._id = animal
        self._attr_name = f"{readable_animal} {entity_description.name}"
        # Entity name property represents the entity itself
        self._attr_has_entity_name = True

    @property
    def name(self):
        """Name of the entity."""
        return self.entity_description.name

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.press_action(self.coordinator.bobcat)
