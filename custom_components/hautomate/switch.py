import asyncio
import logging

from hautomate.apis.homeassistant.events import HASS_EVENT_RECEIVE
from hautomate.context import Context
from hautomate.events import EVT_INTENT_SUBSCRIBE, EVT_INTENT_END, EVT_STOP
from hautomate.intent import Intent
from hautomate.util.async_ import safe_sync
from hautomate.enums import IntentState

from homeassistant.helpers import entity_platform
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import MATCH_ALL, EVENT_TIME_CHANGED, EVENT_STATE_CHANGED
from homeassistant.core import Event

from .entity import HautoIntentEntity
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ Setup the hauto platform. """
    if discovery_info is None:
        return

    platform = entity_platform.current_platform.get()
    hass.data[DOMAIN]['entity_platform'] = platform
    hauto = hass.data[DOMAIN]['hauto']

    await hauto.start()

    entities = [HautoIntentSwitch(intent) for app in hauto.apps for intent in app.intents]
    async_add_entities(entities)
    _LOGGER.info(f'setup {len(hauto.apps)} apps!')

    # ----------------------------------------------------------------------------------

    @safe_sync
    def _create_intent_switch(ctx: Context):
        """ On INTENT_SUBSCRIBE, create a new HautoIntentSwitch. """
        intent = ctx.event_data['created_intent']

        if intent._app is not None or intent.func.__name__ == '<lambda>':
            entity = HautoIntentSwitch(intent)
            async_add_entities([entity])
            _LOGGER.info(f'added entity ({entity.entity_id}) for intent: {intent}')

    @safe_sync
    async def _update_intent(ctx: Context):
        """ On INTENT_END, run an update on the HautoIntentSwitch. """
        intent = ctx.event_data['ended_intent']
        entity = platform.entities.get(f'switch.hauto_intent_{intent._id}')

        if entity is None:
            return

        entity.async_write_ha_state()

    async def _remove_intent_switch(ctx: Context):
        """ On HAUTO_STOP, remove all the entities we've thus created. """
        if not platform.entities:
            return

        await asyncio.gather(*[
            platform.async_remove_entity(entity_id)
            for entity_id in platform.entities
        ])

    async def _hook_event(event: Event):
        """ Hook Home-Assistant events into the Hauto Bus. """
        if event.event_type in (EVENT_TIME_CHANGED, ):
            return

        # short-circuit our own updates, which would filter back into
        # hautomate and possibly create an infinite loop...
        if (
            event.event_type == EVENT_STATE_CHANGED
            and event.data['entity_id'].startswith('switch.hauto_intent_')
        ):
            return

        await hauto.bus.fire(
            HASS_EVENT_RECEIVE,
            parent=hauto.apis.homeassistant,
            hass_event=event
        )

    # ----------------------------------------------------------------------------------

    # listen to hauto events in HASS
    # - create Entities once a new INTENT exists
    # - update Entities once an INTENT runs
    # - remove Entities once we STOP
    hauto.bus.subscribe(EVT_INTENT_SUBSCRIBE, _create_intent_switch)
    hauto.bus.subscribe(EVT_INTENT_END, _update_intent)
    hauto.bus.subscribe(EVT_STOP, _remove_intent_switch)

    # listen to HASS events in Hautomate
    # - forward all HASS events into the hautomate event bus
    #   NOTE: not to confuse this with directly firing an event into the bus!
    hass.bus.async_listen(MATCH_ALL, _hook_event)


class HautoIntentSwitch(HautoIntentEntity, SwitchEntity):
    """
    A switch which represents an active Intent.
    """
    def __init__(self, hauto_intent: Intent):
        super().__init__(hauto_intent)
        self.entity_id = f'switch.hauto_intent_{hauto_intent._id}'

    @property
    def state(self) -> str:
        """ Return the state of the switch. """
        return 'on' if self.hauto_intent._state == IntentState.ready else 'off'

    @property
    def name(self):
        """ Return the name of the switch. """
        parent = self.hauto_intent._app
        func = self.hauto_intent.func.__name__

        if parent is None:
            return f'UnboundIntent {func}'

        return f'Intent {parent.name}.{func}'

    @property
    def is_on(self) -> bool:
        """ Return True if entity is on. """
        return self.hauto_intent._state == IntentState.ready

    async def async_turn_on(self):
        """
        Turn the IntentEntitySwtich on.

        This will run the internal unpause callback during a single
        iteration of the event loop.
        """
        self._unpause()

    async def async_turn_off(self):
        """
        Turn the IntentEntitySwtich off.

        This will run the internal pause callback during a single
        iteration of the event loop.
        """
        self._pause()
