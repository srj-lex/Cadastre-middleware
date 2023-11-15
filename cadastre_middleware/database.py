from datetime import datetime
from typing import Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, desc, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


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
        result=bool(result),
    )

    db.session.add(obj)
    db.session.commit()


def get_result_by_id(id: str) -> Union[dict, None]:
    request = db.session.get(Requests, id)
    if request is not None:
        result = {
            "cadastre_number": request.cadastre_number,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "result": request.result,
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
            "result": i.result,
        }
        for i in data
    ]
    return result
