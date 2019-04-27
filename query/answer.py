#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from database.tables import Answer
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', quiz_id: int, info_id: int, correct: bool, commit=True) -> bool:
    try:
        session.add(Answer(quizId=quiz_id, infoId=info_id, correct=correct))

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_quiz_id(session: 'Session', quiz_id: int) -> List[Answer]:
    try:
        return session.query(Answer).filter(Answer.quizId == quiz_id)
    except NoResultFound as e:
        print(e)


def delete_by_quiz_id(session: 'Session', quiz_id: int, commit=True) -> bool:

    try:
        statement = Answer.__table__.delete().where(Answer.quizId == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    create(_session, 2, 1, False)
    create(_session, 2, 2, True)
    create(_session, 2, 3, True)
    create(_session, 2, 4, False)
    create(_session, 2, 5, False)

    # delete_by_quiz_id(_session, 2)

    result = get_by_quiz_id(_session, 2)
    [print(r.infoId) for r in result]
