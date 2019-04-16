
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import INT, SMALLINT, BOOLEAN, VARCHAR, CHAR, NVARCHAR
from sqlalchemy import ForeignKey
from config import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)
meta = MetaData()

# Static Data Tables

INFO = Table(
    'Info', meta,
    Column('id', INT, primary_key=True),
    Column('key', NVARCHAR(TEXT_LENGTH)),
    Column('value', NVARCHAR(TEXT_LENGTH)),
    Column('categoryId', INT, ForeignKey('Category.id')),
    Column('beltId', SMALLINT, ForeignKey('Belt.id'))
)

CATEGORY = Table(
    'Category', meta,
    Column('id', SMALLINT, primary_key=True),
    Column('name', VARCHAR(LABEL_LENGTH))
)

BELT = Table(
    'Belt', meta,
    Column('id', SMALLINT, primary_key=True),
    Column('name', VARCHAR(LABEL_LENGTH))
)

# User Tables

USER = Table(
    'User', meta,
    Column('id', INT, primary_key=True),
    Column('email', VARCHAR(EMAIL_LENGTH), unique=True),
    Column('pwdHash', CHAR(PWD_HASH_LENGTH)),
    Column('confirmed', BOOLEAN, default=False),
)

# Quiz Tables

QUIZ = Table(
    'Quiz', meta,
    Column('id', CHAR(UUID_LENGTH), primary_key=True),
    Column('questionCount', SMALLINT),
    Column('currentQuestion', SMALLINT),
    Column('title', NVARCHAR(TITLE_LENGTH)),
    Column('timeStart', INT),
    Column('userId', INT, ForeignKey('User.id')),
    Column('beltMin', SMALLINT, ForeignKey('Belt.id'), default=1),
    Column('beltMax', SMALLINT, ForeignKey('Belt.id'), default=5)
)

QUESTION = Table(
    'Question', meta,
    Column('id', INT, primary_key=True),
    Column('text', NVARCHAR(TEXT_LENGTH)),
    Column('optionCount', SMALLINT),
    Column('quizId', CHAR(UUID_LENGTH), ForeignKey('Quiz.id')),
    Column('infoId', INT, ForeignKey('Info.id', ondelete="CASCADE")),
    Column('answerId', INT, ForeignKey('Answer.id', ondelete="CASCADE"))
)

OPTION = Table(
    'Option', meta,
    Column('id', INT, primary_key=True),
    Column('text', NVARCHAR(TEXT_LENGTH)),
    Column('questionId', INT, ForeignKey('Question.id', ondelete="CASCADE"))
)

ANSWER = Table(
    'Answer', meta,
    Column('id', INT, primary_key=True),
    Column('quizId', INT, ForeignKey('Quiz.id', ondelete="CASCADE")),
    Column('infoId', INT, ForeignKey('Info.id')),
    Column('correct', BOOLEAN)
)

RESULT = Table(
    'Result', meta,
    Column('id', INT, primary_key=True),
    Column('userId', INT, ForeignKey('User.id')),
    Column('correctCount', SMALLINT),
    Column('incorrectCount', SMALLINT),
    Column('timeSpent', INT),
    Column('beltMin', SMALLINT, ForeignKey('Belt.id'), default=1),
    Column('beltMax', SMALLINT, ForeignKey('Belt.id'), default=5)
)

# Junction Tables

QUIZ_CATEGORY = Table(
    'QuizCategory', meta,
    Column('id', INT, primary_key=True),
    Column('quizId', CHAR(UUID_LENGTH), ForeignKey('Quiz.id', ondelete="CASCADE")),
    Column('categoryId', INT, ForeignKey('Category.id', ondelete="CASCADE"))
)

RESULT_CATEGORY = Table(
    'ResultCategory', meta,
    Column('id', INT, primary_key=True),
    Column('resultId', INT, ForeignKey('Result.id', ondelete="CASCADE")),
    Column('categoryId', INT, ForeignKey('Category.id', ondelete="CASCADE"))
)

meta.create_all(engine)
