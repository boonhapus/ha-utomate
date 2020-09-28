import logging

from homeassistant.helpers.entity import ToggleEntity
from hautomate.enums import IntentState
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    hauto = hass.data[DOMAIN]
    _LOGGER.info(f'(switch) uhhh was it this easy? hauto={hauto}')


class HautoIntentEntity(ToggleEntity):
    """
    """

    def __init__(self, hauto_intent):
        self.hauto_intent = hauto_intent

        self.hauto_intent.pause = self._pause
        self.hauto_intent.unpause = self._unpause

    # Internal methods

    async def _pause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.paused
        await self.async_update_ha_state()

    async def _unpause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.unpaused
        await self.async_update_ha_state()

    # ABC overrides

    @property
    def should_poll(self) -> bool:
        """ Return the polling requirement of the entity. """
        return False

    # @property
    # def name(self) -> str:
    #     """ Return the name of the entity. """
    #     return self._name

    @property
    def state(self) -> str:
        """ Return the state of the entity. """
        return self.hauto_intent._state.value

    @property
    def state_attributes(self) -> str:
        """ Return the data of the entity. """
        data = {
            # 'parent': self.hauto_intent._app.name,
            'event': self.hauto_intent.event,
            'last_ran': self.hauto_intent.last_ran,
            'runs': self.hauto_intent.runs,
            'limit': self.hauto_intent.limit,
            'n_checks': len(self.hauto_intent.checks),
            'has_cooldown': self.hauto_intent.cooldown is not None,
        }
        return data

    @property
    def icon(self) -> str:
        """ Return icon. """
        return 'mdi:robot'

    @property
    def is_on(self) -> bool:
        """ Return True if entity is on. """
        raise self.hauto_intent._state not in (IntentState.paused, IntentState.cancelled)

    # ...

    async def async_turn_on(self):
        """
        """
        await self._unpause()

    async def async_turn_off(self):
        """
        """
        await self._pause()
