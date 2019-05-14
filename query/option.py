#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.exc import IntegrityError
from database.schemas import Option
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', curriculum_id: int, quiz_id: int, question_id: int, option_index: int, commit=True) -> bool:
    try:
        session.add(Option(curriculumId=curriculum_id, quizId=quiz_id, questionId=question_id, optionIndex=option_index))

        if commit:
            session.commit()
        return True
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_question_id(session: 'Session', question_id: int) -> List[Option]:
    try:
        return session.query(Option).filter(Option.questionId == question_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


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

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_question_id(session: 'Session', question_id: int, commit=True) -> bool:
    try:
        statement = Option.__table__.delete().where(Option.questionId == question_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception
