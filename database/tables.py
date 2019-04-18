from sqlalchemy import create_engine, MetaData, Column
from sqlalchemy import INT, SMALLINT, BOOLEAN, VARCHAR, CHAR, NVARCHAR
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config import *
from database.db import EngineSingleton

Base = declarative_base()
meta = MetaData()


# Static Data Tables

class Info(Base):
    __tablename__ = "Info"

    id = Column(INT, primary_key=True)
    key = Column(NVARCHAR(TEXT_LENGTH))
    value = Column(NVARCHAR(TEXT_LENGTH))
    categoryId = Column(INT, ForeignKey('Category.id'))
    beltId = Column(SMALLINT, ForeignKey('Belt.id'))


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

    id = Column(CHAR(UUID_LENGTH), primary_key=True)
    questionCount = Column(SMALLINT)
    currentQuestion = Column(SMALLINT)
    title = Column(NVARCHAR(TITLE_LENGTH))
    timeStart = Column(INT)
    userId = Column(INT, ForeignKey('User.id'))
    beltMin = Column(SMALLINT, ForeignKey('Belt.id'), default=1)
    beltMax = Column(SMALLINT, ForeignKey('Belt.id'), default=5)


class Question(Base):
    __tablename__ = "Question"

    id = Column(INT, primary_key=True)
    text = Column(NVARCHAR(TEXT_LENGTH))
    optionCount = Column(SMALLINT)
    quizId = Column(CHAR(UUID_LENGTH), ForeignKey('Quiz.id'))
    infoId = Column(INT, ForeignKey('Info.id', ondelete="CASCADE"))
    answerId = Column(INT, ForeignKey('Answer.id', ondelete="CASCADE"))


class Option(Base):
    __tablename__ = "Option"

    id = Column(INT, primary_key=True)
    text = Column(NVARCHAR(TEXT_LENGTH))
    questionId = Column(INT, ForeignKey('Question.id', ondelete="CASCADE"))


class Answer(Base):
    __tablename__ = "Answer"

    id = Column(INT, primary_key=True)
    quizId = Column(INT, ForeignKey('Quiz.id', ondelete="CASCADE"))
    infoId = Column(INT, ForeignKey('Info.id'))
    correct = Column(BOOLEAN)


class Result(Base):
    __tablename__ = "Result"

    id = Column(INT, primary_key=True)
    userId = Column(INT, ForeignKey('User.id'))
    correctCount = Column(SMALLINT)
    incorrectCount = Column(SMALLINT)
    timeSpent = Column(INT)
    beltMin = Column(INT, ForeignKey('Belt.id'), default=1)
    beltMax = Column(INT, ForeignKey('Belt.id'), default=5)


# Junction Tables

class QuizCategory(Base):
    __tablename__ = "QuizCategory"

    id = Column(INT, primary_key=True)
    quizId = Column(CHAR(UUID_LENGTH), ForeignKey('Quiz.id', ondelete="CASCADE"))
    categoryId = Column(INT, ForeignKey('Category.id', ondelete="CASCADE"))


class ResultCategory(Base):
    __tablename__ = "ResultCategory"

    id = Column(INT, primary_key=True)
    resultId = Column(INT, ForeignKey('Result.id', ondelete="CASCADE"))
    categoryId = Column(INT, ForeignKey('Category.id', ondelete="CASCADE"))


# Database Tables Init

if __name__ == '__main__':
    engine = EngineSingleton().get_engine()
    Base.metadata.create_all(engine)

