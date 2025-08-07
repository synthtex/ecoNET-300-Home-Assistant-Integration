"""Common code for econet300 integration."""
from datetime import timedelta
import logging

import async_timeout

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiError, AuthError, Econet300Api
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EconetDataCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, api: Econet300Api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=60),
        )
        self._api = api

    def has_data(self, key: str):
            """Check if the specified key exists in the data dictionary."""
            _LOGGER.debug("Key from has_data: %s", key)
            return key in self.data

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        _LOGGER.debug("Fetching data from API")

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(90):
                return await self._api.fetch_data()
        except AuthError as err:
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
