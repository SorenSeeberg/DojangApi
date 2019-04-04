from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str


@dataclass
class KnowledgePair:
    id: int
    langOne: str
    langTwo: str
    categoryId: int


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


@dataclass
class Quiz:
    id: str
    total_question_count: int
    current_question_index: int
    title: str
    created: int
    userId: str


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
