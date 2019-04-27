#!/usr/bin/python3
# -*- coding: utf-8 -*-

from uuid import uuid4
from database.tables import Quiz
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session',
           question_count: int,
           option_count: int,
           category_id: int,
           user_id: int,
           belt_min: int,
           belt_max: int,
           reverse_questions=False,
           commit=True) -> Quiz:

    quiz_row: Quiz = Quiz(
        token=str(uuid4()),
        questionCount=question_count,
        optionCount=option_count,
        currentQuestion=1,
        reverseQuestions=reverse_questions,
        categoryId=category_id,
        userId=user_id,
        beltMin=belt_min,
        beltMax=belt_max
    )

    session.add(quiz_row)

    if commit:
        session.commit()

    return quiz_row


def get_by_id(session: 'Session', quiz_id: int) -> Quiz:
    try:
        return session.query(Quiz).get(quiz_id)
    except NoResultFound as e:
        print(e)


def get_by_token(session: 'Session', token: str) -> Quiz:
    try:
        return session.query(Quiz).filter(Quiz.token == token).one()
    except NoResultFound as e:
        print(e)


def delete_by_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        # statement = Quiz.__table__.delete().where(Quiz.id == quiz_id)
        # session.execute(statement)

        session.delete(session.query(Quiz).get(quiz_id))

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    # quiz = create(session=_session, question_count=20, option_count=5, title='hello', user_id=1, belt_min=1, belt_max=5)

    # print(quiz.id, quiz.token)
    print(delete_by_id(_session, 1))
