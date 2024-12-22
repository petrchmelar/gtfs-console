from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import imgkit

env = Environment(loader=FileSystemLoader("examples/eink_server/templates"))

template = env.get_template("display.html")

render_context = {"datetime": datetime.now().strftime("%H:%M")}

imgkit.from_string(
    template.render(render_context),
    "examples/eink_server/display.png",
    options={"width": 400, "height": 300},
)
