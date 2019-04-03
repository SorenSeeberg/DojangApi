from dataclasses import dataclass


@dataclass
class Category:
    id: str
    name: str


@dataclass
class KnowledgePairs:
    id: str
    langOne: str
    langTwo: str
    categoryId: str


@dataclass
class Option:
    id: str
    option: str
    question_id: str


@dataclass
class Question:
    id: str
    active_quiz_id: str
    question_number: int
    knowledge_pair_id: str


@dataclass
class ActiveQuiz:
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
