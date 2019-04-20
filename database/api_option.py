from typing import List
from database.tables import Option
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def create(session: 'Session', text: str, question_id: int, commit=True) -> bool:
    try:
        session.add(Option(text=text, questionId=question_id))

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


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    # create(_session, 'one', 2)
    # create(_session, 'two', 2)
    # create(_session, 'three', 2)
    # create(_session, 'four', 2)

    result = get_by_question_id(_session, 2)
    [print(r.text) for r in result]
