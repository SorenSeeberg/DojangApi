#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import Result
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session',
           user_id: int,
           correct_count: int,
           incorrect_count: int,
           time_spent: int,
           belt_min: int,
           belt_max: int,
           commit=True) -> bool:
    try:
        session.add(Result(userId=user_id,
                           correctCount=correct_count,
                           incorrectCount=incorrect_count,
                           timeSpent=time_spent,
                           beltMin=belt_min,
                           beltMax=belt_max)
                    )

        if commit:
            session.commit()
        return True
    except:
        return False


def get_by_id(session: 'Session', result_id: int) -> Result:
    try:
        return session.query(Result).get(result_id)
    except NoResultFound as e:
        print(e)
