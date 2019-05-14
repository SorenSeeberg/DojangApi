#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from database.schemas import Answer
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', quiz_id: int, curriculum_id: int, question_index: int, correct: bool, commit=True) -> bool:
    try:
        session.add(Answer(quizId=quiz_id, curriculumId=curriculum_id, questionIndex=question_index, correct=correct))

        if commit:
            session.commit()
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_quiz_id(session: 'Session', quiz_id: int) -> List[Answer]:
    try:
        return session.query(Answer).filter(Answer.quizId == quiz_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_by_quiz_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        statement = Answer.__table__.delete().where(Answer.quizId == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_answer_count(session: 'Session', quiz_id: int) -> Dict:
    try:
        correct_count: int = session.query(Answer).filter(Answer.correct == True, Answer.quizId == quiz_id).count()
        incorrect_count: int = session.query(Answer).filter(Answer.correct == False, Answer.quizId == quiz_id).count()

        return {"correct_count": correct_count, "incorrect_count": incorrect_count}

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception
