import logging
from homeassistant.const import (
     STATE_ON, STATE_OFF,
)
import threading
from operator import eq
from .device import Device, TCPClientBase
from .const import *
from homeassistant.components.binary_sensor import BinarySensorEntity
from .common import SettingManager
Any = object()

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN]["listener"] = []
    hub = hass.data[DOMAIN][config_entry.entry_id]
    device = Device(NAME, config_entry)
    new_devices = []

    if setting := SettingManager().get_settings().get("binary_sensor", {}):
        for s in setting:
            new_devices.append(TCPClientSwitch(hass, device, hub, s))

    if new_devices:
        async_add_devices(new_devices)


class TCPClientSwitch(TCPClientBase, BinarySensorEntity):
    """Representation of a Thermal Comfort Sensor."""
    _attr_has_entity_name = True

    def __init__(self, hass, device, hub, setting):
        """Initialize the sensor."""
        TCPClientBase.__init__(self, hass, hub, device, setting)
        self._attr_is_on = False
        self._timer = None
        self._attr_device_class = setting.get("device_class")

    def state_change(self, state):
        self._attr_is_on = state
        self.async_write_ha_state()
        if state:
            if timer := self._setting.get("off_timer"):
                if self._timer != None:
                    _LOGGER.debug("timer cancel")
                    self._timer.cancel()
                _LOGGER.debug("create timer")
                self._timer = threading.Timer(timer, self.state_change, [False])
                self._timer.start()

    def on_recv_data(self, data):
        """"""
        state_setting = self._setting.get("state", {})
        # _LOGGER.debug("data is : " + str(data) + ", on data : " + bytearray.fromhex(state_setting.get("on")))
        if eq(bytearray.fromhex(state_setting.get(STATE_ON)), data):
            self.state_change(True)
        elif eq(bytearray.fromhex(state_setting.get(STATE_OFF)), data):
            self.state_change(False)

