"""
Hautomate. A task automation library focused on home automation.

For more details about this component, please refer to
https://github.com/boonhapus/Hautomate/example/custom_components/README.md
"""
import logging
import pathlib

from hautomate.settings import HautoConfig
from hautomate import Hautomate

from homeassistant.helpers import discovery
from homeassistant.const import SERVICE_RELOAD
from homeassistant.core import ServiceCall

from .schema import CONFIG_SCHEMA
from .const import DOMAIN, CONF_APPS_DIR


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """ Setup the hautomate component from configuration.yaml """
    apps_dir = config[DOMAIN][CONF_APPS_DIR]

    if apps_dir == 'hello_world':
        apps_dir = pathlib.Path(__file__).parent / 'hello_world'

    cfg_data = {
        'apps_dir': apps_dir,
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
    hauto = Hautomate(cfg)
    hass.data[DOMAIN] = {
        'hauto': hauto,
        'switch_platform': None,  # see switch.py
        'sensor_platform': None   # see sensor.py
    }

    # ----------------------------------------------------------------------------------

    async def _stop_start(call: ServiceCall):
        """ Handle reload service calls. """
        _LOGGER.debug('stopping hautomate')
        await hauto.stop()
        _LOGGER.debug('successfully stopped, restarting hautomate')
        await hauto.start()
        _LOGGER.debug('hautomate is up and ready for use!')

    async def _fire_event(call: ServiceCall):
        """ Provide a service to fire an event on Hautomate bus. """
        event = call.data.get('event', None)
        data = call.data.get('data', {})

        if event is None:
            raise TypeError('an event must be provided!')

        if not isinstance(data, dict):
            raise TypeError('service call data is not a valid json mapping!')

        data['frontend'] = True
        data['from_user_id'] = call.context.user_id
        await hauto.bus.fire(event.upper(), parent=hauto.apis.homeassistant, **data)

    # ----------------------------------------------------------------------------------

    # register services
    hass.services.async_register(DOMAIN, SERVICE_RELOAD, _stop_start)
    hass.services.async_register(DOMAIN, 'fire', _fire_event)
    discovery.load_platform(hass, 'switch', DOMAIN, {}, config)
    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    return True
