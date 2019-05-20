#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.exc import IntegrityError
from database.schemas import Curriculum
from sqlalchemy.orm.exc import NoResultFound
from data.import_data import extract_curriculum
from functools import lru_cache


def create_many(session: 'Session', curriculum: List[List], commit=True) -> bool:
    try:
        session.add_all([Curriculum(key=c[0], value=c[1], categoryId=c[2], levelId=c[3]) for c in curriculum])

        if commit:
            session.commit()
        return True

    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


@lru_cache(maxsize=512)
def get_by_id(session: 'Session', curriculum_id: int) -> Curriculum:
    try:
        return session.query(Curriculum).get(curriculum_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


@lru_cache(maxsize=512)
def get_by_level_and_category(session: 'Session', category_id: int, level_min: int, level_max: int) -> List[Curriculum]:
    try:
        if category_id == 0:
            return session.query(Curriculum).filter(Curriculum.levelId >= level_min,
                                                    Curriculum.levelId <= level_max)
        else:
            return session.query(Curriculum).filter(Curriculum.categoryId == category_id,
                                                    Curriculum.levelId >= level_min,
                                                    Curriculum.levelId <= level_max)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def setup(session: 'Session') -> None:
    """Populate curriculum table"""

    _curriculum = extract_curriculum()

    create_many(session, _curriculum, commit=False)
