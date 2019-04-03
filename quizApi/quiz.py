from dataclasses import dataclass
from uuid import uuid4
from typing import List
# from quizApi.question import Question


@dataclass
class Quiz:
    id: str
    title: str
    total_questions: int
    current_question: int
    question_ids: List[int]


def new_quiz(title: str, total_questions: int) -> Quiz:
    return Quiz(id=str(uuid4()), title=title, total_questions=total_questions, current_question=0, question_ids=[])


def abort_quiz(id: str) -> bool:
    try:
        print(f'Aborting quiz {id}')
        return True
    except:
        return False


def conclude_quiz():
    pass


def advance_quiz(quiz_id: str, next_question_id: str) -> "Question":
    print(f'Advancing quiz {quiz_id}, {next_question_id}')
    pass
