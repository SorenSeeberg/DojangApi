from uuid import uuid4
from database.tables import AccessToken
from database.tables import User
from database.user import get_by_email
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def get_by_user_id_and_token(session, user_id: int, access_token: str) -> AccessToken:
    try:
        return session.query(AccessToken).filter(AccessToken.userId == user_id, AccessToken.token == access_token).one()
    except NoResultFound as e:
        print(e)


def create(session: 'Session', user_id: int, commit=True) -> str:
    token = str(uuid4())
    session.add(AccessToken(userId=user_id, token=token))

    if commit:
        session.commit()

    return token


def create_access_token(user_id: int) -> None:
    _session: 'Session' = SessionSingleton().get_session()

    create(_session, user_id=user_id)


def validate_by_id(session: 'Session', user_id: int, access_token: str) -> bool:
    try:
        session.query(AccessToken).filter(AccessToken.userId == user_id, AccessToken.token == access_token).one()
        return True
    except NoResultFound as e:
        print(e)

    return False


def validate_by_email(session: 'Session', email: str, access_token: str) -> bool:
    user: User = get_by_email(session, email)

    if not user:
        return False

    return validate_by_id(session, user.id, access_token)


def delete(session: 'Session', user_id: int, access_token: str, commit=True) -> bool:
    access_token: AccessToken = get_by_user_id_and_token(session, user_id, access_token)

    if access_token:
        session.delete(access_token)

        if commit:
            session.commit()

        return True

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
