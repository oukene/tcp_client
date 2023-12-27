import asyncio
from .const import *
import logging
from homeassistant.helpers.entity import async_generate_entity_id

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + ".{}"

class Device:
    def __init__(self, name, config):
        self._id = f"{name}_{config.entry_id}"
        self._name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self.firmware_version = VERSION
        self.model = NAME
        self.manufacturer = NAME

    @property
    def device_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    # def register_callback(self, callback):
    #     self._callbacks.add(callback)

    # def remove_callback(self, callback):
    #     self._callbacks.discard(callback)

    # async def publish_updates(self):
    #     for callback in self._callbacks:
    #         callback()

    # def publish_updates(self):
    #     for callback in self._callbacks:
    #         callback()


class TCPClientBase:
    """Base representation of a Hello World Sensor."""

    should_poll = False

    def __init__(self, hass, hub, device, setting):
        """Initialize the sensor."""
        self._device = device
        self.hass = hass
        self._hub = hub
        self._setting = setting

        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, "{}_{}".format(DOMAIN, setting.get("name")), current_ids="", hass=hass)

        _LOGGER.debug("create switch entity id : " + str(self.entity_id))

        hub.add_entity(self)

        self._attr_name = "{}".format(setting.get("name"))
        self._attr_unique_id = self.entity_id

        self._attr_available = hub.isConnected()

    def set_available(self, state):
        self._attr_available = state
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            # If desired, the name for the device could be different to the entity
            "name": self._device.name,
            "sw_version": self._device.firmware_version,
            "model": self._device.model,
            "manufacturer": self._device.manufacturer
        }
