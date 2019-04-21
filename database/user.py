from database.tables import User
from database.db import SessionSingleton
from hashlib import sha3_256
from exceptions import Exceptions
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.exc import IntegrityError


def hash_password(password) -> str:
    return str(sha3_256(password.encode()).hexdigest())


def create(session: 'Session', email: str, password: str, commit=True) -> User:
    try:
        if email_exists(session, email):
            raise Exceptions.DuplicateEmailError

        user_row = User(email=email, pwdHash=hash_password(password))
        session.add(user_row)

        if commit:
            session.commit()

        return user_row
    except Exceptions.DuplicateEmailError as e:
        print(e)
    except IntegrityError as e:
        print(e)


def create_admin(session: 'Session',
                 email: str = 'soren.seeberg@gmail.com',
                 password: str = 'hanadulsetmulighet',
                 commit=True) -> User:

    try:
        if email_exists(session, email):
            raise Exceptions.DuplicateEmailError

        user_row = User(email=email, pwdHash=hash_password(password), confirmed=True, enabled=True, administrator=True)
        session.add(user_row)

        if commit:
            session.commit()

        return user_row
    except Exceptions.DuplicateEmailError as e:
        print(e)
    except IntegrityError as e:
        print(e)


def get_by_email(session: 'Session', email: str) -> 'User':
    try:
        return session.query(User).filter(User.email == email).one()
    except MultipleResultsFound as e:
        print(e)
    except NoResultFound as e:
        print(e)


def get_by_id(session: 'Session', id: int) -> 'User':
    try:
        return session.query(User).get(id)
    except MultipleResultsFound as e:
        print(e)
    except NoResultFound as e:
        print(e)


def update_password(session: 'Session', email: str, new_password_value: str, commit=True) -> bool:
    user_row = get_by_email(session, email)

    if user_row:
        user_row.pwdHash = hash_password(new_password_value)

        if commit:
            session.commit()

        return True

    return False


def update_confirmed(session: 'Session', email: str, confirmed_value: bool, commit=True) -> bool:
    user_row = get_by_email(session, email)

    if user_row:
        user_row.confirmed = confirmed_value

        if commit:
            session.commit()

        return True

    return False


def delete(session: 'Session', email: str, commit=True) -> bool:
    user_row = get_by_email(session, email)

    if user_row:
        session.delete(user_row)

        if commit:
            session.commit()

        return True

    return False


def email_exists(session: 'Session', email: str) -> bool:
    result = session.query(User).filter(User.email == email).count()

    return False if result == 0 else True


def create_user_rows() -> None:
    _session: 'Session' = SessionSingleton().get_session()
    create_admin(_session, commit=False)
    create(_session, 'sorense@configit.com', '1234', commit=False)
    _session.commit()


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    # create(_session, "sorense@configit.com", "hallohallo234", commit=False)
    # create(_session, "soren.seeberg@gmail.com", "hallohallo234", commit=False)

    user_by_email: User = get_by_email(_session, "soren.seeberg@gmail.com")
    if user_by_email:
        print('\nUser by email')
        print(user_by_email.id, user_by_email.email)

    user_by_id: User = get_by_id(_session, 1)
    if user_by_id:
        print('\nUser by id')
        print(user_by_id.id, user_by_id.email)

    # print(update_confirmed(_session, 'soren.seeberg@gmail.com', confirmed_value=True, commit=False))
    # print(update_password(_session, 'soren.seeberg@gmail.com', 'fest2', commit=False))
    # _session.commit()
    # print(delete(_session, "soren.seeberg@gmail.com"))
