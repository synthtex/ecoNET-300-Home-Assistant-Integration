"""Platform econet300 switch integration."""

from homeassistant.components.switch import SwitchEntity


class BoilerSwitch(SwitchEntity):
    """Representation of a switch to control the boiler."""

    def __init__(self, hass, name, api):
        """Initialize the boiler switch."""
        self._name = name
        self._api = api
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the boiler on."""
        response = await self._api.set_param("BOILER_CONTROL", "1")
        if response and response["result"] == "OK":
            self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Turn the boiler off."""
        response = await self._api.set_param("BOILER_CONTROL", "0")
        if response and response["result"] == "OK":
            self._is_on = False
