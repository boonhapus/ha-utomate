import asyncio
import logging

# from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import entity_platform
from hautomate.context import Context
from hautomate.events import EVT_STOP

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ Setup the hauto platform. """
    if discovery_info is None:
        return

    platform = entity_platform.current_platform.get()
    hass.data[DOMAIN]['sensor_platform'] = platform
    hauto = hass.data[DOMAIN]['hauto']

    async def _remove_user_created_sensors(ctx: Context):
        """ On HAUTO_STOP, remove all the entities we've thus created. """
        if not platform.entities:
            return

        await asyncio.gather(*[
            platform.async_remove_entity(entity_id)
            for entity_id in platform.entities
        ])

    # listen to hauto events in HASS
    # - remove Sensors once we STOP
    hauto.bus.subscribe(EVT_STOP, _remove_user_created_sensors)
