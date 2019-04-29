#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.exc import IntegrityError
from database.tables import Belt
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', belt_name: str, commit=True) -> bool:
    try:
        session.add(Belt(name=belt_name))

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def create_many(session: 'Session', belt_names: List[str], commit=True) -> bool:
    try:
        session.add_all([Belt(name=belt_name) for belt_name in belt_names])

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', id: int) -> Belt:
    try:
        return session.query(Belt).get(id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


BELT_NAMES = ["10. kup", "9. kup", "8. kup", "7. kup", "6. kup", "5. kup", "4. kup", "3. kup", "2. kup", "1. kup",
              "1. dan", "2. dan", "3. dan", "4. dan", "5. dan", "6. dan", "Teori"]


def setup(session: 'Session') -> None:
    """Populate the Belt table"""

    create_many(session, BELT_NAMES, commit=False)
