"""
Hautomate. A task automation library focused on home automation.

For more details about this component, please refer to
https://github.com/boonhapus/Hautomate/example/custom_components/README.md
"""
import logging

from hautomate.settings import HautoConfig
from hautomate import Hautomate

from homeassistant.helpers import discovery
from homeassistant.const import SERVICE_RELOAD

from .schema import CONFIG_SCHEMA
from .const import DOMAIN, CONF_APPS_DIR


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """ """
    cfg_data = {
        'apps_dir': config[DOMAIN][CONF_APPS_DIR],
        'latitude': hass.config.latitude,
        'longitude': hass.config.longitude,
        'elevation': hass.config.elevation,
        'timezone': hass.config.time_zone,
        'api_configs': {
            'homeassistant': {
                'feed': 'custom_component',
                'hass_interface': hass
            }
        }
    }

    cfg = HautoConfig(**cfg_data)
    hass.data[DOMAIN] = hauto = Hautomate(cfg)

    # ----------------------------------------------------------------------------------

    async def _stop_start(call):
        """ Handle reload service calls. """
        _LOGGER.debug('stopping hautomate')
        await hauto.stop()
        _LOGGER.debug('successfully stopped, restarting hautomate')
        await hauto.start()
        _LOGGER.debug('hautomate is up and ready for use!')

    async def _fire_event(call):
        """ Provide a service to fire an event on Hautomate bus. """
        await hauto.bus.fire(
            call.data['event'].upper(),
            parent=hauto.apis.homeassistant,
            **call.data['data']
        )

    # ----------------------------------------------------------------------------------

    # register services
    hass.services.async_register(DOMAIN, SERVICE_RELOAD, _stop_start)
    hass.services.async_register(DOMAIN, 'fire', _fire_event)
    discovery.load_platform(hass, 'switch', DOMAIN, {}, config)
    return True
