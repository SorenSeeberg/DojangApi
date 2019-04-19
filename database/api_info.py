from typing import List
from database.tables import Info
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create_many(session: 'Session', infos: List[List], commit=True) -> bool:
    try:
        session.add_all([Info(key=info[0], value=info[1], categoryId=info[2], beltId=info[3]) for info in infos])

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_id(session: 'Session', id: int) -> Info:
    try:
        return session.query(Info).get(id)
    except NoResultFound as e:
        print(e)


def create_info_rows() -> None:
    _infos = [
        ['Agwison', 'Runding mellem tommel- og pegefinger', 5, 1],
        ['Anpalmok hechyomakki', 'Adskille blokering m. indersiden af underarm', 5, 1],
        ['Gyottari-seogi', 'Hjælpestand', 7, 1]
    ]

    _session: 'Session' = SessionSingleton().get_session()

    create_many(_session, _infos)


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    print(get_by_id(_session, id=3).key)
