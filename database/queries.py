from typing import Dict, List
from database.tables import *
from uuid import uuid4
from hashlib import sha3_256


categories: List[Category] = list()
knowledge_base: List[KnowledgePairs] = list()
active_quizzes: List[ActiveQuiz] = list()
questions: List[Question] = list()
answers: List[Answer] = list()
users: List[User] = list()


def new_user(email: str, password: str) -> None:
    users.append(User(id=str(uuid4()), email=email, password_hash=sha3_256(password)))
