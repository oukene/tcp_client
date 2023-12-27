import logging
from homeassistant.const import (
    STATE_UNKNOWN
)

from operator import eq
from .device import Device, TCPClientBase
from .const import *
from homeassistant.components.sensor import SensorEntity
from .common import SettingManager
Any = object()

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN]["listener"] = []
    hub = hass.data[DOMAIN][config_entry.entry_id]
    device = Device(NAME, config_entry)
    new_devices = []

    if setting := SettingManager().get_settings().get("sensor", {}):
        for s in setting:
            new_devices.append(TCPClientSwitch(hass, device, hub, s))

    if new_devices:
        async_add_devices(new_devices)


class TCPClientSwitch(TCPClientBase, SensorEntity):
    """Representation of a Thermal Comfort Sensor."""
    _attr_has_entity_name = True

    def __init__(self, hass, device, hub, setting):
        """Initialize the sensor."""
        TCPClientBase.__init__(self, hass, hub, device, setting)
        self._attr_native_value = STATE_UNKNOWN

    def state_change(self, state):
        self._attr_native_value = state
        self.async_write_ha_state()

    def on_recv_data(self, data):
        """"""
        state_setting = self._setting.get("state", {})
        _LOGGER.debug("sensor state : " +str(state_setting))
        for state, value in state_setting.items():
            _LOGGER.debug("state : " + str(state) + ", value : " + str(value))
            if eq(bytearray.fromhex(value), data):
                self.state_change(state)
        
