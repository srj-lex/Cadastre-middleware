from random import randint, choice
from time import sleep
from typing import Final

from flask import Flask


POSSIBLE_RESULTS: Final[tuple[str]] = ("true", "false")


app = Flask(__name__)


@app.route(
    "/cadastre",
    methods=[
        "GET",
    ],
)
def emulator():
    sleep_duration = randint(0, 3)
    response = {"result": choice(POSSIBLE_RESULTS)}
    sleep(sleep_duration)
    return (response, 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
