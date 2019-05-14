#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from database.schemas import Quiz


def create(session: 'Session',
           question_count: int,
           option_count: int,
           category_id: int,
           user_id: int,
           level_min: int,
           level_max: int,
           reverse_questions=False,
           commit=True) -> Quiz:

    try:
        quiz_row: Quiz = Quiz(
            token=str(uuid4()),
            questionCount=question_count,
            optionCount=option_count,
            currentQuestion=1,
            reverseQuestions=reverse_questions,
            categoryId=category_id,
            userId=user_id,
            levelMin=level_min,
            levelMax=level_max
        )

        session.add(quiz_row)

        if commit:
            session.commit()

        return quiz_row
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', quiz_id: int) -> Quiz:
    try:
        return session.query(Quiz).get(quiz_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_by_token(session: 'Session', token: str) -> Quiz:
    try:
        return session.query(Quiz).filter(Quiz.token == token).one()
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        statement = Quiz.__table__.delete().where(Quiz.id == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_token(session: 'Session', quiz_token: str, commit=True) -> bool:
    try:
        statement = Quiz.__table__.delete().where(Quiz.token == quiz_token)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception
