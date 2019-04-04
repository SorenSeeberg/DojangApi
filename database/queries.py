from typing import Dict, List
from database.tables import *
from uuid import uuid4
from hashlib import sha3_256
import random

categories: List[Category] = list()
knowledge_base: List[KnowledgePair] = list()
active_quizzes: List[Quiz] = list()
questions: List[Question] = list()
answers: List[Answer] = list()
users: List[User] = list()


def setup_categories():
    categories.extend([
        Category(id=1, name='farver'),
        Category(id=2, name='buildings')
    ])


def setup_knowledge_pairs():
    knowledge_base.extend([
        KnowledgePair(id=1, langOne='black', langTwo='sort', categoryId=1),
        KnowledgePair(id=2, langOne='white', langTwo='hvid', categoryId=1),
        KnowledgePair(id=3, langOne='red', langTwo='sort', categoryId=1),
        KnowledgePair(id=4, langOne='green', langTwo='rød', categoryId=1),
        KnowledgePair(id=5, langOne='blue', langTwo='blå', categoryId=1),
        KnowledgePair(id=6, langOne='yellow', langTwo='gul', categoryId=1),
        KnowledgePair(id=7, langOne='house', langTwo='hus', categoryId=2),
        KnowledgePair(id=8, langOne='sky scraper', langTwo='skyskraber', categoryId=2),
        KnowledgePair(id=9, langOne='hut', langTwo='hytte', categoryId=2),
        KnowledgePair(id=10, langOne='farm', langTwo='bondegård', categoryId=2)
    ])


def pick_random_knowledge_pair_id(include_categories: List[int]) -> KnowledgePair:
    return random.choice(k for k in knowledge_base if k.categoryId in include_categories)


def new_user(email: str, password: str) -> None:
    users.append(User(id=str(uuid4()), email=email, password_hash=sha3_256(password.encode()).hexdigest()))


def new_quiz() -> None:
    pass


def new_question(quiz_id: str, included_category_ids: List[int], option_count: int) -> None:

    options: List[KnowledgePair] = [pick_random_knowledge_pair_id(included_category_ids) for x in range(option_count)]
    answer: KnowledgePair = random.choice(options)

    questions.append(Question(id=str(uuid4()), quiz_id=quiz_id, option_count=option_count, knowledge_pair_id=answer.id))


if __name__ == '__main__':
    setup_categories()
    setup_knowledge_pairs()
    new_user('soren.seeberg@gmail.com', 'abc1234')
    new_user('sorense@configit.com', 'ab134')

    [print(user) for user in users]
