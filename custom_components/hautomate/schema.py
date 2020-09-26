import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN, CONF_APPS_DIR


CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_APPS_DIR): cv.isdir})},
    extra=vol.ALLOW_EXTRA
)
