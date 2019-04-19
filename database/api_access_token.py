from database.tables import AccessToken
from database.db import SessionSingleton


def create(session: 'Session', user_id: int, commit=True) -> bool:
    try:
        session.add(AccessToken(userId=user_id))

        if commit:
            session.commit()
        return True
    except:
        return False


def create_access_token(user_id: int) -> None:

    _session: 'Session' = SessionSingleton().get_session()

    create(_session, user_id=user_id)
