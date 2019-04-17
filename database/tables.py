from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import INT, SMALLINT, BOOLEAN, VARCHAR, CHAR, NVARCHAR, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import *

Base = declarative_base()
meta = MetaData()

# Static Data Tables

# INFO = Table(
#     'Info', meta,
#     Column('id', INT, primary_key=True),
#     Column('key', NVARCHAR(TEXT_LENGTH)),
#     Column('value', NVARCHAR(TEXT_LENGTH)),
#     Column('categoryId', INT, ForeignKey('Category.id')),
#     Column('beltId', SMALLINT, ForeignKey('Belt.id'))
# )


class Category(Base):
    __tablename__ = "Category"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(LABEL_LENGTH))


class Belt(Base):
    __tablename__ = "Belt"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(LABEL_LENGTH))


# User Tables


class User(Base):
    __tablename__ = "User"

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(EMAIL_LENGTH), unique=True)
    pwdHash = Column(CHAR(PWD_HASH_LENGTH))
    confirmed = Column(BOOLEAN, default=False)


# Quiz Tables

class Quiz(Base):
    __tablename__ = "Quiz"

    id = Column(CHAR(UUID_LENGTH), primary_key=True),
    questionCount = Column(SMALLINT),
    currentQuestion = Column(SMALLINT),
    title = Column(NVARCHAR(TITLE_LENGTH)),
    timeStart = Column(INT),
    userId = Column(INT, ForeignKey('User.id')),
    beltMin = Column(SMALLINT, ForeignKey('Belt.id'), default=1),
    beltMax = Column(SMALLINT, ForeignKey('Belt.id'), default=5)


class Question(Base):
    __tablename__ = "Question"

    id = Column(INT, primary_key=True),
    text = Column(NVARCHAR(TEXT_LENGTH)),
    optionCount = Column(SMALLINT),
    quizId = Column(CHAR(UUID_LENGTH), ForeignKey('Quiz.id')),
    infoId = Column(INT, ForeignKey('Info.id', ondelete="CASCADE")),
    answerId = Column(INT, ForeignKey('Answer.id', ondelete="CASCADE"))


# OPTION = Table(
#     'Option', meta,
#     Column('id', INT, primary_key=True),
#     Column('text', NVARCHAR(TEXT_LENGTH)),
#     Column('questionId', INT, ForeignKey('Question.id', ondelete="CASCADE"))
# )
#
# ANSWER = Table(
#     'Answer', meta,
#     Column('id', INT, primary_key=True),
#     Column('quizId', INT, ForeignKey('Quiz.id', ondelete="CASCADE")),
#     Column('infoId', INT, ForeignKey('Info.id')),
#     Column('correct', BOOLEAN)
# )
#
# RESULT = Table(
#     'Result', meta,
#     Column('id', INT, primary_key=True),
#     Column('userId', INT, ForeignKey('User.id')),
#     Column('correctCount', SMALLINT),
#     Column('incorrectCount', SMALLINT),
#     Column('timeSpent', INT),
#     Column('beltMin', SMALLINT, ForeignKey('Belt.id'), default=1),
#     Column('beltMax', SMALLINT, ForeignKey('Belt.id'), default=5)
# )

# Junction Tables

# QUIZ_CATEGORY = Table(
#     'QuizCategory', meta,
#     Column('id', INT, primary_key=True),
#     Column('quizId', CHAR(UUID_LENGTH), ForeignKey('Quiz.id', ondelete="CASCADE")),
#     Column('categoryId', INT, ForeignKey('Category.id', ondelete="CASCADE"))
# )
#
# RESULT_CATEGORY = Table(
#     'ResultCategory', meta,
#     Column('id', INT, primary_key=True),
#     Column('resultId', INT, ForeignKey('Result.id', ondelete="CASCADE")),
#     Column('categoryId', INT, ForeignKey('Category.id', ondelete="CASCADE"))
# )

# Database Init

if __name__ == '__main__':
    engine = create_engine(DB_CONNECTION_STRING, echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # insert_user = USER.insert()
    # insert_user.execute(email="soren.seeberg@gmail.com", pwdHash="abcd"*16)
