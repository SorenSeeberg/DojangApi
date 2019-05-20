#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.exc import IntegrityError
from database.schemas import Level
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', level_name: str, commit=True) -> bool:
    try:
        session.add(Level(name=level_name))

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def create_many(session: 'Session', level_names: List[str], commit=True) -> bool:
    try:
        session.add_all([Level(name=level_name) for level_name in level_names])

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', id: int) -> Level:
    try:
        return session.query(Level).get(id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_names(session: 'Session') -> List[str]:
    # todo : these should be pulled from database at some point
    return LEVEL_NAMES


LEVEL_NAMES = ["10. kup", "9. kup", "8. kup", "7. kup", "6. kup", "5. kup", "4. kup", "3. kup", "2. kup", "1. kup",
               "1. dan", "2. dan", "3. dan", "4. dan", "5. dan", "6. dan"]


def setup(session: 'Session') -> None:
    """Populate the Level table"""

    create_many(session, LEVEL_NAMES, commit=False)
