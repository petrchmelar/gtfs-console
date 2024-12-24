from typing import Sequence
import requests
from gtfsconsole.timetable import Timetable

from gtfsconsole.config import CONFIG


def export(timetables: Sequence[Timetable], prefix: str = "pt"):
    request_values = {
        "import_key": CONFIG.zivyobraz_import_key,
    }

    for timetable_idx, timetable in enumerate(timetables):
        request_values[f"{prefix}_{timetable_idx}_stop_name"] = timetable.stop_name
        request_values[f"{prefix}_{timetable_idx}_stop_id"] = timetable.stop_id
        for trip_idx, trip in enumerate(timetable.trips):
            request_values[f"{prefix}_{timetable_idx}_{trip_idx}_headsign"] = (
                trip.headsign
            )
            request_values[f"{prefix}_{timetable_idx}_{trip_idx}_short_name"] = (
                trip.short_name
            )
            request_values[f"{prefix}_{timetable_idx}_{trip_idx}_departure_time"] = (
                trip.departure_time
            )
            request_values[
                f"{prefix}_{timetable_idx}_{trip_idx}_wheelchair_accessible"
            ] = trip.wheelchair_accessible

    request_url = "http://in.zivyobraz.eu/?"
    requests.get(request_url, params=request_values)
