#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import Question
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def create(session: 'Session', quiz_id: int, info_id: int, question_number: int, commit=True) -> Question:
    try:
        question_row: Question = Question(quizId=quiz_id, infoId=info_id, questionNumber=question_number)
        session.add(question_row)

        if commit:
            session.commit()
        return question_row
    except IntegrityError as e:
        print(e)


def get_by_id(session: 'Session', question_id: int) -> Question:
    try:
        return session.query(Question).get(question_id)
    except NoResultFound as e:
        print(e)


def get_by_quiz_id_and_number(session: 'Session', quiz_id: int, question_number: int) -> Question:
    try:
        return session.query(Question).filter(Question.quizId == quiz_id, Question.questionNumber == question_number).one()
    except NoResultFound as e:
        print(e)


def delete_by_quiz_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.quizId == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


def delete_by_id(session: 'Session', question_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.id == question_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    _question_row = create(_session, quiz_id=1, info_id=45)
