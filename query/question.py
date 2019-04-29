#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import Question
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def create(session: 'Session', quiz_id: int, info_id: int, question_index: int, commit=True) -> Question:
    try:
        question_row: Question = Question(quizId=quiz_id, infoId=info_id, questionIndex=question_index)
        session.add(question_row)

        if commit:
            session.commit()
        return question_row
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', question_id: int) -> Question:
    try:
        return session.query(Question).get(question_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_by_quiz_id_and_index(session: 'Session', quiz_id: int, question_index: int) -> Question:
    try:
        return session.query(Question).filter(Question.quizId == quiz_id, Question.questionIndex == question_index).one()
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_quiz_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.quizId == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_id(session: 'Session', question_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.id == question_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception
