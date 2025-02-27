"""Entities for GoXLR Utility integration."""
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.light import LightEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GoXLRUtilityDataUpdateCoordinator


class ItemType(Enum):
    """Enum for GoXLR Utility item types."""

    ACCENT = "accent"
    BUTTON_ACTIVE = "button_active"
    BUTTON_INACTIVE = "button_inactive"
    FADER_BOTTOM = "fader_bottom"
    FADER_TOP = "fader_top"


class GoXLRUtilityEntity(CoordinatorEntity[GoXLRUtilityDataUpdateCoordinator]):
    """Defines a base GoXLR Utility entity."""

    def __init__(
        self,
        coordinator: GoXLRUtilityDataUpdateCoordinator,
        entry_data: dict[str, Any],
        key: str,
        name: str | None,
    ) -> None:
        """Initialize the GoXLR Utility entity."""
        super().__init__(coordinator)
        keys = [
            coordinator.data.hardware.usb_device.manufacturer_name,
            coordinator.data.hardware.usb_device.product_name,
        ]
        self._device_name = " ".join(keys)
        self._key = f"{'_'.join(keys).lower()}_{key}"
        self._name = f"{self._device_name} {name}"
        self._configuration_url = (
            f"http://{entry_data[CONF_HOST]}:{entry_data[CONF_PORT]}"
        )
        self._hw_version = ".".join(
            [str(item) for item in coordinator.data.hardware.usb_device.version]
        )
        self._identifier = coordinator.data.hardware.serial_number
        self._manufacturer = coordinator.data.hardware.usb_device.manufacturer_name
        self._model = coordinator.data.hardware.usb_device.product_name

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this entity."""
        return self._key

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this GoXLR Utility instance."""
        return DeviceInfo(
            configuration_url=self._configuration_url,
            hw_version=self._hw_version,
            identifiers={(DOMAIN, self._identifier)},
            manufacturer=self._manufacturer,
            model=self._model,
            name=self._device_name,
        )


@dataclass
class GoXLRUtilityBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing GoXLR Utility binary sensor entities."""

    value: Callable = round
    item_key: str | None = None


@dataclass
class GoXLRUtilityLightEntityDescription(LightEntityDescription):
    """Class describing GoXLR Utility light entities."""

    item_type: ItemType = ItemType.ACCENT
    item_key: str = ""
    hex: Callable = round


@dataclass
class GoXLRUtilitySensorEntityDescription(SensorEntityDescription):
    """Class describing GoXLR Utility sensor entities."""

    value: Callable = round
