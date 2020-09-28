"""
Hautomate. A task automation library focused on home automation.

For more details about this component, please refer to
https://github.com/boonhapus/Hautomate/example/custom_components/README.md
"""
import logging

from hautomate.apis.homeassistant.events import HASS_EVENT_RECEIVE
from hautomate.settings import HautoConfig
# from hautomate.context import Context
# from hautomate.events import EVT_INTENT_SUBSCRIBE
from hautomate import Hautomate

from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.const import MATCH_ALL, SERVICE_RELOAD, EVENT_TIME_CHANGED
# from homeassistant.core import Event

from .switch import HautoIntentEntity
from .schema import CONFIG_SCHEMA
from .const import DOMAIN, CONF_APPS_DIR


_LOGGER = logging.getLogger(__name__)
PLATFORMS = ['switch']


# async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
#     hauto = hass.data[DOMAIN]
#     _LOGGER.info(f'(__init__) uhhh was it this easy? hauto={hauto}')


async def async_setup(hass, config):
    """ """
    component = EntityComponent(_LOGGER, DOMAIN, hass)

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
    await hauto.start()
    _LOGGER.info(f'setup {len(hauto.apps)} apps!')

    # register Intents
    for app in hauto.apps:
        _LOGGER.info(f'adding {len(app.intents)} from {app}!')
        await component.async_add_entities([HautoIntentEntity(i) for i in app.intents])

    # ----------------------------------------------------------------------------------

    async def _stop_start(event):
        """ Handle reload service calls. """
        _LOGGER.debug('stopping hautomate')
        await hauto.stop()
        _LOGGER.debug('successfully stopped, restarting hautomate')
        await hauto.start()
        _LOGGER.debug('hautomate is up and ready for use!')

    async def _fire_event(event):
        """ Hook Home-Assistant events into the Hauto Bus. """
        if event.event_type in (EVENT_TIME_CHANGED, ):
            return

        await hauto.bus.fire(
            HASS_EVENT_RECEIVE,
            parent=hauto.apis.homeassistant,
            hass_event=event
        )

    # async def _create_intent_switch(ctx: Context):
    #     """ TODO """
    #     intent = ctx.event_data['created_intent']
    #     async_add_entities([HautoIntentEntity(intent)])

    # ----------------------------------------------------------------------------------

    # register services
    hass.services.async_register(DOMAIN, SERVICE_RELOAD, _stop_start)

    # listen to HASS events
    hass.bus.async_listen(MATCH_ALL, _fire_event)

    # listen to hauto events
    # hauto.bus.subscribe(EVT_APP_LOAD, _create_app_entity)
    # hauto.bus.subscribe(EVT_APP_UNLOAD, _remove_app_entity)
    # hauto.bus.subscribe(EVT_INTENT_SUBSCRIBE, _create_intent_switch)

    return True
