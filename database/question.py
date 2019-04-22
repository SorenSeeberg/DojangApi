from database.tables import Question
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def create(session: 'Session', quiz_id: int, info_id: int, commit=True) -> bool:
    try:
        session.add(Question(quizId=quiz_id, infoId=info_id))

        if commit:
            session.commit()
        return True
    except IntegrityError as e:
        print(e)

    return False


def get_by_id(session: 'Session', question_id: int) -> Question:
    try:
        return session.query(Question).get(question_id)
    except NoResultFound as e:
        print(e)


def delete_by_quiz_id(session: 'Session', quiz_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.quizId == quiz_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


def delete_by_id(session: 'Session', question_id: int, commit=True) -> bool:
    try:
        statement = Question.__table__.delete().where(Question.id == question_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    question_row = create(_session, quiz_id=1, info_id=45)
