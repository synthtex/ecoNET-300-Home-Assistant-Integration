"""Module provides a events implementation from econet300 module."""

import logging

from homeassistant.components.logbook import LOGBOOK_ENTRY_MESSAGE
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@callback
def sync_econet_alarms(hass, entity_id, alarms):
    """Log alarms fetched from the boiler system to Home Assistant."""
    _LOGGER.info("Logging boiler error from econet300 to Home Assistant: %s", alarms)
    if not alarms:
        _LOGGER.info("No alarms to log from the econet300.")
        return

    _LOGGER.info("Logging boiler from econet300 alarms to Home Assistant: %s", alarms)

    for alarm in alarms:
        hass.bus.fire(
            LOGBOOK_ENTRY_MESSAGE,
            {
                ATTR_ENTITY_ID: entity_id,
                "message": f"Boiler Alarm: {alarm}",
                "name": "Boiler",
                "domain": DOMAIN,
            },
        )
