from typing import Dict, List
from database.tables import *
from uuid import uuid4
from hashlib import sha3_256
import random

categories: List[Category] = list()
knowledge_base: List[KnowledgeKeyValue] = list()
active_quizzes: List[Quiz] = list()
questions: List[Question] = list()
answers: List[Answer] = list()
users: List[User] = list()
options: List[Option] = list()
quizzes: List[Quiz] = list()


def print_table(table: List) -> None:
    [print(row) for row in table]


def setup_categories():
    categories.extend([
        Category(id=1, name='farver'),
        Category(id=2, name='buildings')
    ])


def setup_knowledge_pairs():
    knowledge_base.extend([
        KnowledgeKeyValue(id=1, key='black', value='sort', category_id=1),
        KnowledgeKeyValue(id=2, key='white', value='hvid', category_id=1),
        KnowledgeKeyValue(id=3, key='red', value='rød', category_id=1),
        KnowledgeKeyValue(id=4, key='green', value='grøn', category_id=1),
        KnowledgeKeyValue(id=5, key='blue', value='blå', category_id=1),
        KnowledgeKeyValue(id=6, key='yellow', value='gul', category_id=1),
        KnowledgeKeyValue(id=7, key='house', value='hus', category_id=2),
        KnowledgeKeyValue(id=8, key='sky scraper', value='skyskraber', category_id=2),
        KnowledgeKeyValue(id=9, key='hut', value='hytte', category_id=2),
        KnowledgeKeyValue(id=10, key='farm', value='bondegård', category_id=2)
    ])


def pick_random_knowledge_pair_id(include_categories: List[int], used_ids: List[int]) -> KnowledgeKeyValue:
    return random.choice([k for k in knowledge_base if k.category_id in include_categories and k.id not in used_ids])


def pick_knowledge_pairs(pair_count: int, include_categories: List[int]) -> List[KnowledgeKeyValue]:
    pairs: List[KnowledgeKeyValue] = list()

    for x in range(pair_count):
        pairs.append(pick_random_knowledge_pair_id(
            include_categories=include_categories,
            used_ids=[p.id for p in pairs])
        )

    return pairs


def new_user(email: str, password: str) -> None:
    users.append(
        User(id=len(users) + 1, email=email, password_hash=sha3_256(password.encode()).hexdigest(), confirmed=True))


def new_question(quiz_id: str, included_category_ids: List[int], option_count: int) -> None:
    question_id: str = str(uuid4())

    _pairs: List[KnowledgeKeyValue] = pick_knowledge_pairs(option_count, included_category_ids)
    _options: List[Option] = [Option(id=str(uuid4()), question_id=question_id, option=option.value) for index, option in
                              enumerate(_pairs)]

    answer_index = random.randrange(option_count)

    _answer_pair: KnowledgeKeyValue = _pairs[answer_index]
    _answer_option: Option = _options[answer_index]

    options.extend(_options)

    questions.append(Question(
        id=question_id,
        quiz_id=quiz_id,
        option_count=option_count,
        knowledge_pair_id=_answer_pair.id,
        text=_answer_pair.key,
        answer_id=_answer_option.id)
    )


def new_quiz(question_count: int, option_count: int, included_category_ids: List[int]) -> None:
    quiz_id = str(uuid4())

    [new_question(quiz_id=quiz_id, included_category_ids=included_category_ids, option_count=option_count) for x in
     range(question_count)]
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
    new_user('soren.seeberg@gmail.com', 'abc1234')
    new_user('sorense@configit.com', 'ab134')

    quiz_id = 'quiz666'

    # new_question(quiz_id=quiz_id, included_category_ids=[1], option_count=5)
    new_quiz(question_count=20, option_count=4, included_category_ids=[1])
    # print_table(quizzes)
    # print_table(questions)
    # print_table(options)
    print_table(users)
    print(len(users[0].password_hash))
    print(len(quizzes[0].id))
