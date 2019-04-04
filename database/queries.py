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
options: List[Option] = list()
quizzes: List[Quiz] = list()


def setup_categories():
    categories.extend([
        Category(id=1, name='farver'),
        Category(id=2, name='buildings')
    ])


def setup_knowledge_pairs():
    knowledge_base.extend([
        KnowledgePair(id=1, lang_one='black', lang_two='sort', category_id=1),
        KnowledgePair(id=2, lang_one='white', lang_two='hvid', category_id=1),
        KnowledgePair(id=3, lang_one='red', lang_two='rød', category_id=1),
        KnowledgePair(id=4, lang_one='green', lang_two='grøn', category_id=1),
        KnowledgePair(id=5, lang_one='blue', lang_two='blå', category_id=1),
        KnowledgePair(id=6, lang_one='yellow', lang_two='gul', category_id=1),
        KnowledgePair(id=7, lang_one='house', lang_two='hus', category_id=2),
        KnowledgePair(id=8, lang_one='sky scraper', lang_two='skyskraber', category_id=2),
        KnowledgePair(id=9, lang_one='hut', lang_two='hytte', category_id=2),
        KnowledgePair(id=10, lang_one='farm', lang_two='bondegård', category_id=2)
    ])


def pick_random_knowledge_pair_id(include_categories: List[int], used_ids: List[int]) -> KnowledgePair:
    return random.choice([k for k in knowledge_base if k.category_id in include_categories and k.id not in used_ids])


def pick_knowledge_pairs(pair_count: int, include_categories: List[int]) -> List[KnowledgePair]:
    pairs: List[KnowledgePair] = list()

    for x in range(pair_count):
        pairs.append(pick_random_knowledge_pair_id(
            include_categories=include_categories,
            used_ids=[p.id for p in pairs])
        )

    return pairs


def new_user(email: str, password: str) -> None:
    users.append(User(id=str(uuid4()), email=email, password_hash=sha3_256(password.encode()).hexdigest()))


def new_question(quiz_id: str, included_category_ids: List[int], option_count: int) -> None:

    question_id: str = str(uuid4())

    _pairs: List[KnowledgePair] = pick_knowledge_pairs(option_count, included_category_ids)
    _options: List[Option] = [Option(id=str(uuid4()), question_id=question_id, option=option.lang_two) for index, option in enumerate(_pairs)]

    answer_index = random.randrange(option_count)

    _answer_pair: KnowledgePair = _pairs[answer_index]
    _answer_option: Option = _options[answer_index]

    options.extend(_options)

    questions.append(Question(
        id=question_id,
        quiz_id=quiz_id,
        option_count=option_count,
        knowledge_pair_id=_answer_pair.id,
        text=_answer_pair.lang_one,
        answer_id=_answer_option.id)
    )


def new_quiz(question_count: int, option_count: int, included_category_ids: List[int]) -> None:
    quiz_id = str(uuid4())

    [new_question(quiz_id=quiz_id, included_category_ids=included_category_ids, option_count=option_count) for x in range(question_count)]
    quizzes.append(Quiz(
        id=quiz_id,
        question_count=question_count,
        current_question=1,
        created=1234,
        title='colors',
        user_id=1)
    )


if __name__ == '__main__':
    setup_categories()
    setup_knowledge_pairs()
    # new_user('soren.seeberg@gmail.com', 'abc1234')
    # new_user('sorense@configit.com', 'ab134')
    #
    # [print(user) for user in users]

    quiz_id = 'quiz666'

    # new_question(quiz_id=quiz_id, included_category_ids=[1], option_count=5)
    new_quiz(question_count=20, option_count=4, included_category_ids=[1])
    [print(quiz) for quiz in quizzes]
    [print(question) for question in questions]
    [print(option) for option in options]
