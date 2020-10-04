from hautomate.apis.homeassistant.events import HASS_EVENT_RECEIVE
from hautomate.context import Context
from hautomate.events import EVT_ANY
from hautomate.check import check
from hautomate.apis import trigger, homeassistant as hass
from hautomate.app import App


class HelloWorld(App):
    """
    Example app provided as part of the Custom Component.
    """
    @trigger.on(HASS_EVENT_RECEIVE, limit=1)
    async def first_event_only(self, ctx: Context):
        """
        Run on the first HomeAssistant event seen.
        """
        await hass.call_service(
            'persistent_notification',
            'create',
            {'title': '👋 from Hautomate! 🎉', 'message': 'Hello, world!'}
        )

    @trigger.on(EVT_ANY)
    @check(lambda ctx: ctx.event_data.get('frontend', False))
    async def echo(self, ctx: Context):
        """
        Echo all events that are manually fired into the hauto bus.
        """
        await hass.call_service(
            'persistent_notification',
            'create',
            {'title': '📣 echo from Hautomate! 🦇', 'message': f'{ctx.event}'}
        )


def setup(hauto):
    """ Setup apps. """
    return HelloWorld(hauto=hauto, name='example_app')
