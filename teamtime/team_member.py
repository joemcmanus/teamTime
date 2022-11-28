from datetime import datetime
from typing import List

from pytz import timezone


class TeamMember:
    def __init__(self, csv_row: List):
        self.name = csv_row[0]
        self.timezone = csv_row[1]
        self.time = _get_current_formatted_time(self.timezone)
        self.city = csv_row[2].strip()
        self._geo_location = None

    @property
    def _location(self):
        # This import is slow. Only import it if you need it.
        from geopy.geocoders import Nominatim

        if self._geo_location is None:
            geolocator = Nominatim(user_agent="teamTime")
            self._geo_location = geolocator.geocode(self.city)

        return self._geo_location

    @property
    def latitude(self) -> float:
        return self._location.latitude

    @property
    def longitude(self) -> float:
        return self._location.longitude


def _get_current_formatted_time(time_zone: str, format_: str = "%Y-%m-%d %H:%M") -> str:
    return datetime.now(timezone(time_zone)).strftime(format_)
