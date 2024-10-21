from sqlalchemy.inspection import inspect
from flask_sqlalchemy.model import Model
from . import db
from .history import add_history_row


def get_object_identifier(object: Model):
    return {
        "table": object.__class__.__tablename__,
        "id": getattr(object, inspect(object.__class__).primary_key[0].name),
    }


def get_object_data(object: Model):
    d = {**object.__dict__}
    d.pop("_sa_instance_state", None)
    return d


def get_object_identifier_and_data(object: Model):
    return get_object_identifier(object), get_object_data(object)


def add_row(object: Model, track_history=True) -> None:
    if track_history:
        object_identifier, object_data = get_object_identifier_and_data(object)
    db.session.add(object)
    db.session.commit()
    if track_history:
        add_history_row(object_identifier, object_data)


def save_row(object: Model, track_history=True) -> None:
    if track_history:
        object_identifier, object_data = get_object_identifier_and_data(object)
    db.session.commit()
    if track_history:
        add_history_row(object_identifier, object_data)


def merge_row(object: Model, track_history=True) -> None:
    if track_history:
        object_identifier, object_data = get_object_identifier_and_data(object)
    db.session.merge(object)
    db.session.commit()
    if track_history:
        add_history_row(object_identifier, object_data)


def delete_row(object: Model, track_history=True) -> None:
    if track_history:
        object_identifier, object_data = get_object_identifier(object), None
    db.session.delete(object)
    db.session.commit()
    if track_history:
        add_history_row(object_identifier, object_data)
