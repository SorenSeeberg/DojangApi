from typing import List
from database.tables import Category
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', category_name: str, commit=True) -> bool:
    try:
        session.add(Category(name=category_name))

        if commit:
            session.commit()
        return True
    except:
        return False


def create_many(session: 'Session', category_names: List[str], commit=True) -> bool:
    try:
        session.add_all([Category(name=category_name) for category_name in category_names])

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_id(session: 'Session', id: int) -> Category:
    try:
        return session.query(Category).get(id)
    except NoResultFound as e:
        print(e)


category_names = ['Anatomi', 'Benteknikker', 'Bevægelse', 'Diverse', 'Håndteknikker', 'Kamp', 'Stande', 'Tal', 'Teori']


def create_category_rows() -> None:

    _session: 'Session' = SessionSingleton().get_session()

    create_many(_session, category_names)


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    print(get_by_id(_session, id=3).name)
