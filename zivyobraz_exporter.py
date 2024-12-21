from dataclasses import asdict
from typing import Sequence
import streamlit as st
import pandas as pd
import numpy as np
from timetable import get_timetables, get_stops, Timetable, Trip
from gtfs_kit import read_feed
import logging
from datetime import datetime, timedelta

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image
import imgkit

import requests

from config import CONFIG


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

    request_url = "http://in.zivyobraz.eu/?"
    requests.get(request_url, params=request_values)
