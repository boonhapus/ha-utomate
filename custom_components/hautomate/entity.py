from typing import Dict, Any

from hautomate.util.async_ import safe_sync
from hautomate.intent import Intent
from hautomate.enums import IntentState

from homeassistant.helpers.entity import Entity


class HautoIntentEntity(Entity):
    """
    Representation of a hauto Intent in hass.
    """
    entity_registry_enabled_default = True
    icon = 'mdi:robot'
    should_poll = False

    def __init__(self, hauto_intent: Intent):
        self.hauto_intent = hauto_intent

        # monkey-patch the Intent's post init state-changing methods
        self.hauto_intent.unpause = self._unpause
        self.hauto_intent.cancel = self._cancel
        self.hauto_intent.pause = self._pause

    # Internal methods

    @safe_sync
    def _cancel(self):
        """
        Implement Intent.cancel & write state in hass.
        """
        self.hauto_intent._state = IntentState.cancelled

        # prefer .write_ha_state() here because the state has already
        # been updated. there's no need to schedule/update yet again.
        self.async_write_ha_state()

    @safe_sync
    def _pause(self):
        """
        Implement Intent.pause & write state in hass.
        """
        self.hauto_intent._state = IntentState.paused

        # prefer .write_ha_state() here because the state has already
        # been updated. there's no need to schedule/update yet again.
        self.async_write_ha_state()

    @safe_sync
    def _unpause(self):
        """
        Implement Intent.unpause & write state in hass.
        """
        self.hauto_intent._state = IntentState.ready

        # prefer .write_ha_state() here because the state has already
        # been updated. there's no need to schedule/update yet again.
        self.async_write_ha_state()

    #

    @property
    def available(self) -> bool:
        """ Return whether or not the Intent is available. """
        return self.hauto_intent._state != IntentState.cancelled

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        """ Return additional information about an Intent. """
        attr = {}
        attr['event'] = self.hauto_intent.event
        attr['func'] = getattr(self.hauto_intent.func, '__name__', 'undefined')
        attr['concurrency'] = self.hauto_intent.concurrency
        attr['n_checks'] = len(self.hauto_intent.checks)
        attr['has_cooldown'] = self.hauto_intent.cooldown is not None
        attr['intent_state'] = self.hauto_intent._state.value
        attr['app'] = getattr(self.hauto_intent._app, 'name', None)
        attr['last_ran'] = self.hauto_intent.last_ran
        attr['runs'] = self.hauto_intent.runs
        attr['limit'] = self.hauto_intent.limit
        return attr
