from hautomate.enums import IntentState

from homeassistant.helpers.entity import Entity


class HautoIntentEntity(Entity):
    """
    """
    entity_registry_enabled_default = True
    icon = 'mdi:robot'
    should_poll = False

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
        self.hauto_intent._state = IntentState.ready
        await self.async_update_ha_state()
