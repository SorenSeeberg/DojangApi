from dataclasses import dataclass
from typing import List
from uuid import uuid4


@dataclass
class Answer:
    id: str
    text: str


@dataclass
class Question:
    id: str
    text: str
    answers: List[Answer]


def new_answer() -> Answer:
    return Answer(id=str(uuid4()), text='Hello answer')


def new_question(num_answers: int):
    return Question(id=str(uuid4()), text='Hello questiond', answers=[new_answer() for x in range(num_answers)])


def validate_question():
    pass


def new_question_range(num_questions: int, num_answers) -> List[Question]:
    return [new_question(num_answers) for x in range(num_questions)]


if __name__ == '__main__':
    questions = new_question_range(10, 5)
    pass
