#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from database.tables import Option
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', info_id: int, quiz_id: int, question_id: int, option_index: int, commit=True) -> bool:
    try:
        session.add(Option(infoId=info_id, quizId=quiz_id, questionId=question_id, optionIndex=option_index))

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_question_id(session: 'Session', question_id: int) -> List[Option]:
    try:
        return session.query(Option).filter(Option.questionId == question_id)
    except NoResultFound as e:
        print(e)


def get_by_question_id_and_index(session: 'Session', question_id: int, option_index: int) -> Option:
    try:
        return session.query(Option).filter(Option.questionId == question_id, Option.optionIndex == option_index).one()
    except NoResultFound as e:
        print(e)


def delete_by_quiz_id(session: 'Session', quest_id: int, commit=True) -> bool:
    try:
        statement = Option.__table__.delete().where(Option.quizId == quest_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


def delete_by_question_id(session: 'Session', question_id: int, commit=True) -> bool:
    try:
        statement = Option.__table__.delete().where(Option.questionId == question_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    from database import db

    _session = db.SessionSingleton().get_session()
    create(_session, 3, 1, 1, 1)
