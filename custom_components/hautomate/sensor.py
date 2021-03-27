import logging

# from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import entity_platform

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ Setup the hauto platform. """
    if discovery_info is None:
        return

    platform = entity_platform.current_platform.get()
    hass.data[DOMAIN]['sensor_platform'] = platform
