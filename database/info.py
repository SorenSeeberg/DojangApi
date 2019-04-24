from typing import List
from database.tables import Info
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound
from data.import_data import extract_info


def create_many(session: 'Session', infos: List[List], commit=True) -> bool:
    try:
        session.add_all([Info(key=info[0], value=info[1], categoryId=info[2], beltId=info[3]) for info in infos])

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_id(session: 'Session', info_id: int) -> Info:
    try:
        return session.query(Info).get(info_id)
    except NoResultFound as e:
        print(e)


def get_by_level_and_category(session: 'Session', category_id: int, level_min: int, level_max: int) -> List[Info]:
    try:
        return session.query(Info).filter(Info.categoryId == category_id, Info.beltId >= level_min,
                                          Info.beltId <= level_max)
    except NoResultFound as e:
        print(e)


def create_info_rows() -> None:
    """Populate Info table"""
    _infos = extract_info()
    _session: 'Session' = SessionSingleton().get_session()

    create_many(_session, _infos)


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    # print(get_by_id(_session, info_id=3).key)

    [print(row.key, row.value) for row in get_by_level_and_category(_session, 1, 5, 7)]
