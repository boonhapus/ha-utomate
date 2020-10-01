import logging

from hautomate.apis.homeassistant.events import HASS_EVENT_RECEIVE
from hautomate.events import EVT_INTENT_SUBSCRIBE, EVT_INTENT_END
from hautomate.util.async_ import safe_sync
from hautomate.enums import IntentState

from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import MATCH_ALL, EVENT_TIME_CHANGED

from .entity import HautoIntentEntity
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ """
    if discovery_info is None:
        return

    component = EntityComponent(_LOGGER, DOMAIN, hass)  # used to update HautoIntentEntity
    hauto = hass.data[DOMAIN]

    await hauto.start()

    intents = [intent for app in hauto.apps for intent in app.intents]
    async_add_entities([HautoIntentSwitch(i) for i in intents])
    _LOGGER.info(f'setup {len(hauto.apps)} apps!')

    # ----------------------------------------------------------------------------------

    @safe_sync
    def _create_intent_switch(ctx):
        """ TODO """
        intent = ctx.event_data['created_intent']

        if intent._app is not None or intent.func.__name__ == '<lambda>':
            async_add_entities([HautoIntentSwitch(intent)])
            _LOGGER.info(f'added intent: {intent}')

    async def _update_intent(ctx):
        """ TODO """
        intent = ctx.event_data['ended_intent']
        entity_id = f'hautomate.intent_{intent._id}'
        entity = component.get_entity(entity_id)  # TODO can this be replaced ?

        if entity is None:
            return

        await entity.async_update_ha_state()

    async def _hook_event(event):
        """ Hook Home-Assistant events into the Hauto Bus. """
        if event.event_type in (EVENT_TIME_CHANGED, ):
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
    hauto.bus.subscribe(EVT_INTENT_SUBSCRIBE, _create_intent_switch)
    hauto.bus.subscribe(EVT_INTENT_END, _update_intent)

    # listen to HASS events in Hautomate
    # - forward all HASS events into the hautomate event bus
    #   NOTE: not to confuse this with directly firing an event into the bus!
    hass.bus.async_listen(MATCH_ALL, _hook_event)


class HautoIntentSwitch(HautoIntentEntity, SwitchEntity):
    """
    """
    def __init__(self, hauto_intent):
        super().__init__(hauto_intent)
        self.entity_id = f'switch.intent_{hauto_intent._id}'

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
        """ """
        self._unpause()

    async def async_turn_off(self):
        """ """
        self._pause()
