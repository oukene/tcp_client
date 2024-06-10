import logging

from .device import Device, TCPClientBase
from .const import *
from homeassistant.components.button import ButtonEntity
from .common import SettingManager
Any = object()

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN]["listener"] = []
    hub = hass.data[DOMAIN][config_entry.entry_id]
    device = Device(config_entry.data.get(CONF_DEVICE_NAME), config_entry)
    new_devices = []

    if setting := SettingManager().get_settings().get("button", {}):
        for s in setting:
            new_devices.append(TCPClientButton(hass, device, hub, s))

    if new_devices:
        async_add_devices(new_devices)


class TCPClientButton(TCPClientBase, ButtonEntity):
    """Representation of a Thermal Comfort Sensor."""
    _attr_has_entity_name = True

    def __init__(self, hass, device, hub, setting):
        """Initialize the sensor."""
        TCPClientBase.__init__(self, hass, hub, device, setting)

    def on_recv_data(self, data):
        """"""

    def press(self) -> None:
        command_setting = self._setting.get("command", {})
        if data := command_setting.get("press"):
            self._hub.send_packet(data)