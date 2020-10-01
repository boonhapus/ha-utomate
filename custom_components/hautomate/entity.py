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

    def _pause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.paused

        # prefer .write_ha_state() here because the state has already
        # been updated. there's no need to schedule/update yet again.
        self.async_write_ha_state()

    def _unpause(self):
        """ TODO """
        self.hauto_intent._state = IntentState.ready

        # prefer .write_ha_state() here because the state has already
        # been updated. there's no need to schedule/update yet again.
        self.async_write_ha_state()

    #

    @property
    def device_state_attributes(self):
        attr = {}
        attr['intent_state'] = self.hauto_intent._state.value
        attr['func'] = getattr(self.hauto_intent.func, '__name__', 'undefined')
        attr['concurrency'] = self.hauto_intent.concurrency
        attr['parent'] = getattr(self.hauto_intent._app, 'name', None)
        attr['event'] = self.hauto_intent.event
        attr['last_ran'] = self.hauto_intent.last_ran
        attr['runs'] = self.hauto_intent.runs
        attr['limit'] = self.hauto_intent.limit
        attr['n_checks'] = len(self.hauto_intent.checks)
        attr['has_cooldown'] = self.hauto_intent.cooldown is not None
        return attr
