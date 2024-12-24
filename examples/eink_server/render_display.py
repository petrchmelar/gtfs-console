from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import imgkit
from gtfsconsole.timetable import Timetable, Trip, get_timetables
from gtfsconsole.app import update_feed_file
from gtfsconsole.config import CONFIG
from html2image import Html2Image
from gtfs_kit import read_feed


CHROME_PATH = "/usr/lib64/chromium-browser/headless_shell"

env = Environment(loader=FileSystemLoader("templates"))

if not CONFIG.feed_storage.exists():
    update_feed_file()

timetables = get_timetables(
    feed=read_feed(CONFIG.feed_storage, "km"),
    stop_names=["Šumavská"],
    stop_ids=[],
    number_of_trips=4,
)


# timetable = [
#     Timetable(
#         trips=[
#             Trip(
#                 headsign="Starý lískovec",
#                 short_name="6",
#                 departure_time="10:00",
#                 wheelchair_accessible=2,
#             ),
#             Trip(
#                 headsign="Ečerova",
#                 short_name="1",
#                 departure_time="10:10",
#                 wheelchair_accessible=1,
#             ),
#             Trip(
#                 headsign="Starý lískovec",
#                 short_name="6",
#                 departure_time="10:20",
#                 wheelchair_accessible=2,
#             ),
#         ],
#         stop_name="Šumavská",
#         stop_id="1",
#     ),
#     Timetable(
#         trips=[
#             Trip(
#                 headsign="Královo Pole",
#                 short_name="6",
#                 departure_time="10:00",
#                 wheelchair_accessible=2,
#             ),
#             Trip(
#                 headsign="Řeškovice",
#                 short_name="1",
#                 departure_time="10:10",
#                 wheelchair_accessible=1,
#             ),
#             Trip(
#                 headsign="Královo Pole",
#                 short_name="6",
#                 departure_time="10:20",
#                 wheelchair_accessible=2,
#             ),
#         ],
#         stop_name="Starý lískovec",
#         stop_id="2",
#     ),
# ]

template = env.get_template("display.html")
render_context = {
    "datetime": datetime.now().strftime("%H:%M"),
    "timetables": timetables,
}

with open("display.html", "w") as f:
    f.write(template.render(render_context))

hti = Html2Image(
    browser_executable=CHROME_PATH,
)

# hti.load_file("./templates/output.css")
# hti.load_file("./display.html")
# hti.screenshot_loaded_file(
#     file="display.html", output_file="display.png", size=(400, 300)
# )


hti.screenshot(
    html_str=template.render(render_context),
    css_str=open("./templates/output.css").read(),
    save_as="display.png",
    size=(400, 300),
)
