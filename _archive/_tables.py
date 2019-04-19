from dataclasses import dataclass


@dataclass
class Category:
    id: int  # PK
    name: str


@dataclass
class KnowledgeKeyValue:
    id: int  # PK
    key: str
    value: str
    category_id: int  # FK -> Category.id


@dataclass
class Option:
    id: str  # PK
    option: str
    question_id: str  # FK -> Question.id


@dataclass
class Question:
    id: str  # PK
    text: str
    option_count: int
    quiz_id: str  # FK -> Quiz.id
    knowledge_pair_id: int  # FK -> KnowledgePair.id
    answer_id: str  # FK -> Answer.id


@dataclass
class Quiz:
    id: str  # PK
    question_count: int
    current_question: int
    title: str
    created: int
    user_id: int  # FK -> User.id


@dataclass
class Answer:
    id: str  # PK
    knowledge_key_value_id: str  # FK -> KnowledgeKeyValue.id
    correct: bool


@dataclass
class User:
    id: int  # PK
    email: str  # Unique
    password_hash: str
    confirmed: bool


@dataclass
class Belt:
    id: int
    name: str


@dataclass
class QuizCategory:
    id: int
    quiz_id: str
    category_id: int
