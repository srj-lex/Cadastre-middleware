from datetime import datetime
import os
from typing import Final, Union
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import Integer, String, DateTime, desc, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


load_dotenv()

USER: Final[str] = os.getenv("POSTGRES_USER", "postgres_user")
PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "my_password")
POSTGRE_DB: Final[str] = os.getenv("POSTGRES_DB", "postgres")

HOST: Final[str] = os.getenv("DB_HOST", "localhost")
PORT: Final[int] = os.getenv("DB_PORT", 5432)

URL_OF_CAD_SERV: Final[str] = "http://127.0.0.1:5050/cadastre"
ERR_RESPONSE: Final[dict] = {"err": "invalid params, please, try again"}
EMPTY_RESULT: Final[dict] = {"err": "cadastre number is not found"}


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{POSTGRE_DB}"
db.init_app(app)


class Requests(db.Model):
    __table_name__ = "requests_to_API"

    request_id: Mapped[str] = mapped_column(
        String, nullable=False, primary_key=True
    )
    cadastre_number: Mapped[int] = mapped_column(Integer, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    date_of_request: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now()
    )
    result: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return (
            f"<cadastre_number - {self.cadastre_number},"
            f" result - {self.result},"
            f" date_of_request - {self.date_of_request}>"
        )


def write_data_to_db(id: str, data: dict, result: str) -> None:
    obj = Requests(
        request_id=id,
        cadastre_number=data.get("cadastre_number"),
        longitude=data.get("longitude"),
        latitude=data.get("latitude"),
        result=bool(result)
    )

    db.session.add(obj)
    db.session.commit()


def get_result_by_id(id: str) -> Union[dict, None]:
    request = (
        db.session.query(Requests).get(id)
    )
    if request is not None:
        result = {
            "cadastre_number": request.cadastre_number,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "result": request.result
        }
        return result
    return request


def get_history(cadastre_number: str) -> dict:
    if cadastre_number:
        data = (
            db.session.query(Requests)
            .filter(Requests.cadastre_number == cadastre_number)
            .order_by(desc(Requests.date_of_request))
        )
    else:
        data = (
            db.session.query(Requests)
            .order_by(desc(Requests.date_of_request))
            .all()
        )

    result = [
        {
            "cadastre_number": i.cadastre_number,
            "longitude": i.longitude,
            "latitude": i.latitude,
            "result": i.result
        }

        for i in data
    ]
    return result


def params_validator(data: dict) -> bool:
    valid_list = ["cadastre_number", "longitude", "latitude"]
    return valid_list == list(data.keys())


@app.route("/query", methods=["GET", ])
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


@app.route("/result", methods=["GET", ])
def result() -> Response:
    uuid = request.args.get("id", "invalid")
    if len(uuid) != 36:
        return (ERR_RESPONSE, 400)

    response = get_result_by_id(uuid)
    if response is None:
        return (ERR_RESPONSE, 400)
    return (response, 200)


@app.route("/ping", methods=["GET", ])
def ping() -> Response:
    return ("online", 200)


@app.route("/history", methods=["GET", ])
def history() -> Response:
    cadastre_number = request.args.get("cadastre_number", None)
    if cadastre_number and not cadastre_number.isdigit():
        return (ERR_RESPONSE, 400)
    response = get_history(cadastre_number)
    if not response:
        return (EMPTY_RESULT, 400)
    return (response, 200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.debug = True
    app.run(port=5000)
