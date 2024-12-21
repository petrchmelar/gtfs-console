from fnmatch import fnmatch
from typing import Annotated
from config import CONFIG
from timetable import get_timetables, get_stops
from gtfs_kit import read_feed
import logging
from datetime import datetime
from zivyobraz_exporter import export

logging.basicConfig(level=logging.INFO)

import typer

app = typer.Typer()


@app.command()
def list_stops(pattern: str = "*"):
    if not CONFIG.feed_storage.exists():
        raise FileNotFoundError(f"Feed file {CONFIG.feed_storage} does not exist")

    feed = read_feed(CONFIG.feed_storage, dist_units="km")
    stops = get_stops(feed)
    for code, name in stops:
        if fnmatch(name, pattern):
            print(f"{code} - {name}")


@app.command()
def update_feed_file():
    urllib.request.urlretrieve(CONFIG.feed_url, CONFIG.feed_storage)
    print(f"Feed file {CONFIG.feed_storage} updated")


@app.command()
def timetable(
    stop_ids: Annotated[list[str] | None, typer.Option(help="Stop IDs")] = None,
    stop_names: Annotated[list[str] | None, typer.Option(help="Stop names")] = None,
    from_datetime: Annotated[
        datetime | None, typer.Option(help="From datetime")
    ] = None,
    number_of_trips: Annotated[int, typer.Option(help="Number of trips")] = 4,
    export_zivyobraz: Annotated[
        bool, typer.Option(help="Export to Zivy obraz")
    ] = False,
    prefix: Annotated[str, typer.Option(help="Prefix for Zivy obraz")] = "pt",
):
    if stop_ids is None and stop_names is None:
        raise ValueError("Either stop_id or stop_name must be provided")

    if stop_ids is None:
        stop_ids = []
    if stop_names is None:
        stop_names = []

    if not CONFIG.feed_storage.exists():
        raise FileNotFoundError(f"Feed file {CONFIG.feed_storage} does not exist")

    feed = read_feed(CONFIG.feed_storage, dist_units="km")
    timetables = get_timetables(
        feed=feed,
        stop_names=stop_names,
        stop_ids=stop_ids,
        from_datetime=from_datetime,
        number_of_trips=number_of_trips,
    )
    print(timetables)

    if export_zivyobraz:
        export(timetables, prefix)


if __name__ == "__main__":
    app()


# # feed = read_feed("data", "km")
# # timetables = get_timetables(feed, "Šumavská")

# timetables = [
#     Timetable(
#         trips=[
#             Trip(headsign="Šumavská", short_name="1", arrival_time=datetime.now() + timedelta(minutes=10)),
#             Trip(headsign="Šumavská", short_name="6", arrival_time=datetime.now() + timedelta(minutes=20)),
#             Trip(headsign="Šumavská", short_name="1", arrival_time=datetime.now() + timedelta(minutes=30)),
#         ],
#         stop_name="Šumavská"
#     ),
#     Timetable(
#         trips=[
#             Trip(headsign="Šumavská", short_name="1", arrival_time=datetime.now() + timedelta(minutes=5)),
#             Trip(headsign="Šumavská", short_name="6", arrival_time=datetime.now() + timedelta(minutes=15)),
#             Trip(headsign="Šumavská", short_name="1", arrival_time=datetime.now() + timedelta(minutes=25)),
#         ],
#         stop_name="Šumavská"
#     )
# ]


# def st_timetable(timetables: Sequence[Timetable]):
#     tables = []
#     for timetable in timetables:
#         values = list(zip(*[[trip.short_name, trip.headsign, trip.arrival_time] for trip in timetable.trips]))
#         tables.append(go.Table(
#             header=dict(values=['Short name', 'Headsign', 'Arrival time'], line_color="black", fill_color="white", font=dict(color="black")),
#             cells=dict(values=values, line_color="black", fill_color="white", font=dict(color="black")),
#         ))

#     fig = make_subplots(rows=len(timetables), specs=[[{"type": "table"}], [{"type": "table"}]], horizontal_spacing=0.0)
#     for i, table in enumerate(tables, start=1):
#         fig.add_trace(table, row=i, col=1)

#     fig.update_layout(
#         width=400,
#         height=300,
#     )

#     env = Environment(loader=FileSystemLoader('.'))
#     template = env.get_template('sign.html')
#     html = template.render(timetables=timetables)
#     with open("sign.html", "w") as f:
#         f.write(html)
#     st.html(html)

#     imgkit.from_string(html, "out.jpg", options={"width": 400, "height": 300})


# st.sidebar.success("Select a demo above.")
# st.title("Timetable for Šumavská")
# st_timetable(timetables)
