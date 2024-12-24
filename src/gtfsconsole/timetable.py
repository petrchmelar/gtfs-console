from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from gtfs_kit import Feed
import gtfs_kit as gk
import logging


@dataclass
class Trip:
    headsign: str
    short_name: str
    departure_time: str
    wheelchair_accessible: int

    def __str__(self):
        return f"{self.short_name} - {self.headsign} - {self.departure_time}"


@dataclass
class Timetable:
    trips: list[Trip]
    stop_name: str
    stop_id: str

    def __str__(self):
        return f"{self.stop_name}\n" + "\n".join([str(trip) for trip in self.trips])


def get_stops(feed: Feed) -> list[tuple[str, str]]:
    stops_df = gk.get_stops(feed)
    stops_df = stops_df[stops_df["stop_id"].notna() & stops_df["stop_name"].notna()]
    return list(zip(stops_df["stop_id"], stops_df["stop_name"]))


def get_timetables(
    feed: Feed,
    stop_names: list[str],
    stop_ids: list[str],
    from_datetime: datetime | None = None,
    number_of_trips: int = 10,
) -> list[Timetable]:
    if from_datetime is None:
        from_datetime = datetime.now()

    from_date = from_datetime.strftime("%Y%m%d")
    from_time = from_datetime.strftime("%H:%M:%S")

    logging.info(
        f"Getting timetable for names {stop_names} and ids {stop_ids} at {from_time}"
    )

    logging.info(f"Getting stops")
    stops_df = gk.get_stops(feed)
    logging.info(f"Got {len(stops_df)} stops")

    logging.info(f"Getting routes")
    routes_df = gk.get_routes(feed)
    logging.info(f"Got {len(routes_df)} routes")

    logging.info(f"Filtering stops by names and ids")
    stop_dfs = []

    # Filter in for loops to keep order
    for stop_name in stop_names:
        stop_dfs.append(stops_df[stops_df["stop_name"] == stop_name])
    for stop_id in stop_ids:
        stop_dfs.append(stops_df[stops_df["stop_id"] == stop_id])

    stops_df = pd.concat(stop_dfs)
    logging.info(f"Filtered {len(stops_df)} stops")

    timetables = []
    for stop in stops_df.itertuples():
        logging.info(f"Building timetable for {stop.stop_name}")
        timetable_df = gk.build_stop_timetable(feed, stop.stop_id, [from_date])
        timetable_df = timetable_df[
            pd.to_timedelta(timetable_df["departure_time"]) > from_time
        ]
        timetable_df = timetable_df.head(number_of_trips)
        timetable_df = timetable_df.merge(
            routes_df[["route_id", "route_short_name"]], on="route_id"
        )

        trips = []
        for timetable_row in timetable_df.itertuples():
            trips.append(
                Trip(
                    headsign=timetable_row.trip_headsign,
                    short_name=timetable_row.route_short_name,
                    departure_time=timetable_row.departure_time,
                    wheelchair_accessible=timetable_row.wheelchair_accessible,
                )
            )

        timetables.append(
            Timetable(trips=trips, stop_name=stop.stop_name, stop_id=stop.stop_id)
        )

    return timetables
