from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str


@dataclass
class KnowledgePair:
    id: int
    lang_one: str
    lang_two: str
    category_id: int


@dataclass
class Option:
    id: str
    option: str
    question_id: str


@dataclass
class Question:
    id: str
    quiz_id: str
    option_count: int
    knowledge_pair_id: int
    text: str
    answer_id: str


@dataclass
class Quiz:
    id: str
    question_count: int
    current_question: int
    title: str
    created: int
    user_id: int


@dataclass
class Answer:
    id: str
    knowledgeId: str
    correct: bool


@dataclass
class User:
    id: str
    email: str
    password_hash: str
