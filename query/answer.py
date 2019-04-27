#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from database.tables import Answer
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', quiz_id: int, info_id: int, question_index, correct: bool, commit=True) -> bool:
    try:
        session.add(Answer(quizId=quiz_id, infoId=info_id, questionIndex=question_index, correct=correct))

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


def get_answer_count(session: 'Session', quiz_id: int):
    correct_count: int = session.query(Answer).filter(Answer.correct is True, Answer.quizId == quiz_id).count()
    incorrect_count: int = session.query(Answer).filter(Answer.correct is False, Answer.quizId == quiz_id).count()

    return {"correct_count": correct_count, "incorrect_count": incorrect_count}

