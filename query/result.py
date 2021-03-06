#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy.exc import IntegrityError
from database.schemas import Result
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session',
           user_id: int,
           quiz_token: str,
           correct_count: int,
           incorrect_count: int,
           time_spent: int,
           level_min: int,
           level_max: int,
           commit=True) -> bool:
    try:
        session.add(Result(userId=user_id,
                           quizToken=quiz_token,
                           correctCount=correct_count,
                           incorrectCount=incorrect_count,
                           timeSpent=time_spent,
                           levelMin=level_min,
                           levelMax=level_max)
                    )

        if commit:
            session.commit()
        return True

    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_id(session: 'Session', result_id: int) -> Result:
    try:
        return session.query(Result).get(result_id)
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_by_quiz_token(session: 'Session', token: str) -> Result:
    try:
        return session.query(Result).filter(Result.quizToken == token).one()
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def get_last_user_results(session: 'Session', user_id: int) -> List[Result]:

    return session.query(Result).filter(Result.userId == user_id).order_by(Result.id.desc()).limit(5)
