#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.exc import IntegrityError
from database.schemas import Info
from sqlalchemy.orm.exc import NoResultFound
from data.import_data import extract_info


def create_many(session: 'Session', infos: List[List], commit=True) -> bool:
    try:
        session.add_all([Info(key=info[0], value=info[1], categoryId=info[2], beltId=info[3]) for info in infos])

        if commit:
            session.commit()
        return True

    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', info_id: int) -> Info:
    try:
        return session.query(Info).get(info_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_by_level_and_category(session: 'Session', category_id: int, level_min: int, level_max: int) -> List[Info]:
    try:
        return session.query(Info).filter(Info.categoryId == category_id, Info.beltId >= level_min,
                                          Info.beltId <= level_max)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def setup(session: 'Session') -> None:
    """Populate Info table"""

    _infos = extract_info()

    create_many(session, _infos, commit=False)
