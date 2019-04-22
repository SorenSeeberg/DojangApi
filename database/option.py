from typing import List
from database.tables import Option
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', info_id: int, question_id: int, commit=True) -> bool:
    try:
        session.add(Option(infoId=info_id, questionId=question_id))

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


def delete_by_quiz_id(session: 'Session', question_id: int, commit=True) -> bool:

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
    _session: 'Session' = SessionSingleton().get_session()

    create(_session, 1, 2)
    create(_session, 2, 2)
    create(_session, 3, 2)
    create(_session, 4, 2)

    result = get_by_question_id(_session, 2)
    [print(r.infoId) for r in result]
