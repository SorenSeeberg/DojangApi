#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from database.schemas import Category
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', category_name: str, commit=True) -> bool:
    try:
        session.add(Category(name=category_name))

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def create_many(session: 'Session', category_names: List[str], commit=True) -> bool:
    try:
        session.add_all([Category(name=category_name) for category_name in category_names])

        if commit:
            session.commit()
        return True
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_by_id(session: 'Session', id: int) -> Category:
    try:
        return session.query(Category).get(id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_categories(session: 'Session') -> List[str]:
    return CATEGORY_NAMES


CATEGORY_NAMES = ['Anatomi', 'Benteknikker', 'Bevægelse', 'Diverse', 'Håndteknikker', 'Kamp', 'Stande', 'Tal', 'Teori']


def setup(session: 'Session') -> None:
    """ Populate the category names """

    create_many(session, CATEGORY_NAMES, commit=False)

