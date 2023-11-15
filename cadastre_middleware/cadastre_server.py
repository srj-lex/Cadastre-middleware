import os
from typing import Final
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_swagger_ui import get_swaggerui_blueprint
import requests

from database import (
    db,
    Requests,
    write_data_to_db,
    get_result_by_id,
    get_history,
)


load_dotenv()

USER: Final[str] = os.getenv("POSTGRES_USER", "postgres_user")
PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "my_password")
POSTGRE_DB: Final[str] = os.getenv("POSTGRES_DB", "postgres")

HOST: Final[str] = os.getenv("DB_HOST", "localhost")
PORT: Final[int] = os.getenv("DB_PORT", 5432)

URL_OF_CAD_SERV: Final[
    str
] = "ext_server:5050/cadastre"
ERR_RESPONSE: Final[dict] = {"err": "invalid params, please, try again"}
EMPTY_RESULT: Final[dict] = {"err": "cadastre number is not found"}


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{POSTGRE_DB}"
db.init_app(app)

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
admin = Admin(app, name="admin panel", template_mode="bootstrap3")


class AdminPanel(ModelView):
    can_create = False


admin.add_view(AdminPanel(Requests, db.session))


SWAGGER_URL = "/swagger/"
API_URL = "/static/swagger.yml"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Cadastre API"}
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


def params_validator(data: dict) -> bool:
    valid_list = ["cadastre_number", "longitude", "latitude"]
    return valid_list == list(data.keys())


@app.route(
    "/ping",
    methods=[
        "GET",
    ],
)
def ping() -> Response:
    return ("online", 200)


@app.route(
    "/query",
    methods=[
        "GET",
    ],
)
def query() -> Response:
    data = request.args
    if params_validator(data):
        res = requests.get(URL_OF_CAD_SERV, params=data)
        id = uuid4()
        result = res.json().get("result")
        write_data_to_db(id=id, data=data, result=result)
        response = {"id": id}
        return (response, 201)
    return (ERR_RESPONSE, 400)


@app.route(
    "/result",
    methods=[
        "GET",
    ],
)
def result() -> Response:
    uuid = request.args.get("id", "invalid")
    if len(uuid) != 36:
        return (ERR_RESPONSE, 400)

    response = get_result_by_id(uuid)
    if response is None:
        return (ERR_RESPONSE, 400)
    return (response, 200)


@app.route(
    "/history",
    methods=[
        "GET",
    ],
)
def history() -> Response:
    cadastre_number = request.args.get("cadastre_number", None)
    if cadastre_number and not cadastre_number.isdigit():
        return (ERR_RESPONSE, 400)
    response = get_history(cadastre_number)
    if not response:
        return (EMPTY_RESULT, 404)
    return (response, 200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.debug = True
    app.run(host="0.0.0.0", port=5000)
