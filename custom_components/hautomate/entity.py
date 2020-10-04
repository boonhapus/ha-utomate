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
        intent = self.hauto_intent
        fn_name = (
            getattr(intent.func, '__qualname__', None)
            or getattr(intent.func, '__name__', None)
            or str(intent.func)
        )

        attr = {
            'event': intent.event,
            'func': fn_name,
            'concurrency': intent.concurrency,
            'n_checks': len(intent.checks),
            'has_cooldown': intent.cooldown is not None,
            'intent_state': intent._state.value,
            'app': getattr(intent._app, 'name', None),
            'last_ran': intent.last_ran,
            'runs': intent.runs,
            'limit': intent.limit
        }

        return attr
