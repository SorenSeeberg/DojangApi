from database.tables import User
from database.db import SessionSingleton
from hashlib import sha3_256


class CustomException(Exception):

    def __call__(self, *args):
        return self.__class__(*(self.args + args))

    def __str__(self):
        return ': '.join(self.args)


class DuplicateEmailError(CustomException): pass


def create_user(session: 'Session', email: str, password: str, commit=True) -> bool:

    try:
        if email_exists(session, email):
            raise DuplicateEmailError("Email already exist")

        session.add(User(email=email, pwdHash=str(sha3_256(password.encode()).hexdigest())))

        if commit:
            session.commit()

        return True
    except DuplicateEmailError as e:
        print(f'DuplicateEmailError: {e}')
        return False


def get_user_by_email(session: 'Session', email: str):
    raise NotImplementedError


def get_user_by_id(session: 'Session', id: int):
    raise NotImplementedError


def update_user_password() -> bool:
    raise NotImplementedError


def update_user_confirmed() -> bool:
    raise NotImplementedError


def delete_user(session: 'Session') -> bool:
    raise NotImplementedError


def email_exists(session: 'Session', email: str) -> bool:
    result = session.query(User).filter(User.email == email).count()

    return True if result == 1 else False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    create_user(_session, "sorense@configit.com", "hallohallo234")
    create_user(_session, "soren.seeberg@gmail.com", "hallohallo234")


