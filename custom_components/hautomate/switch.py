import logging

from homeassistant.helpers.entity import ToggleEntity
from hautomate.enums import IntentState


_LOGGER = logging.getLogger(__name__)


class HautoIntent(ToggleEntity):
    """
    """

    def __init__(self, hauto_intent):
        self.hauto_intent = hauto_intent

        self.hauto_intent.pause = self._pause
        self.hauto_intent.unpause = self._unpause
        # self.hauto_intent.__call__ = self.__intent_call__

    # Internal methods

    async def _pause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.paused
        await self.async_update_ha_state()

    async def _unpause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.unpaused
        await self.async_update_ha_state()

    # async def __intent_call__(self, ctx, *a, **kw):
    #     _LOGGER.info(f'running... {ctx.event}')
    #     r = await self.hauto_intent.__runner__(ctx, *a, **kw)
    #     await self.async_update_ha_state()

    # ABC overrides

    @property
    def should_poll(self) -> bool:
        """ Return the polling requirement of the entity. """
        return False

    @property
    def unique_id(self):
        return self.hauto_intent._id

    @property
    def name(self) -> str:
        """ Return the name of the entity. """
        return f'intent_{self.hauto_intent._id}'

    # @property
    # def state(self) -> str:
    #     """ Return the state of the entity. """
    #     return self.hauto_intent._state.value.lower()

    @property
    def state_attributes(self) -> str:
        """ Return the data of the entity. """
        data = {
            'func': getattr(self.hauto_intent.func, '__name__', 'undefined'),
            'concurrency': self.hauto_intent.concurrency,
            'parent': getattr(self.hauto_intent._app, 'name', None),
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
        return self.hauto_intent._state == IntentState.ready

    # ...

    async def async_turn_on(self):
        """
        """
        await self._unpause()

    async def async_turn_off(self):
        """
        """
        await self._pause()

    async def async_toggle(self, **kwargs) -> None:
        """Toggle the entity."""
        if self.is_on:
            await self.async_turn_off(**kwargs)
        else:
            await self.async_turn_on(**kwargs)
