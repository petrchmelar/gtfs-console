import os
from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import imgkit
from gtfsconsole.timetable import Timetable, Trip, get_timetables
from gtfsconsole.app import update_feed_file
from gtfsconsole.config import CONFIG
from html2image import Html2Image
from gtfs_kit import read_feed
import tempfile
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/display", response_class=Response)
def get_display():
    CHROME_PATH = CONFIG.browser_executable

    env = Environment(loader=FileSystemLoader("templates"))

    timetables = get_timetables(
        feed=read_feed(CONFIG.feed_storage, "km"),
        stop_names=["Šumavská"],
        stop_ids=[],
        number_of_trips=4,
    )

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
    try:
        hti.screenshot(
            html_str=template.render(render_context),
            css_str=open("./templates/output.css").read(),
            save_as="screenshot.png",
            size=(400, 300),
        )
        return Response(
            content=open("screenshot.png", "rb").read(), media_type="image/png"
        )
    finally:
        if os.path.exists("screenshot.png"):
            os.remove("screenshot.png")


if not CONFIG.feed_storage.exists():
    logging.info("Feed file does not exist, updating...")
    update_feed_file()
