#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from uuid import uuid4
from sqlalchemy import MetaData, Column
from sqlalchemy import SMALLINT, INT, BOOLEAN, VARCHAR, CHAR, NVARCHAR
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config import *

Base = declarative_base()
meta = MetaData()


# Static Data Tables

class Curriculum(Base):
    __tablename__ = "Curriculum"

    id = Column(INT, primary_key=True)
    key = Column(NVARCHAR(TEXT_LENGTH))
    value = Column(NVARCHAR(TEXT_LENGTH))
    categoryId = Column(INT, ForeignKey('Category.id'))
    levelId = Column(INT, ForeignKey('Level.id'))


class Category(Base):
    __tablename__ = "Category"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(LABEL_LENGTH))


class Level(Base):
    __tablename__ = "Level"

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(LABEL_LENGTH))


# User Tables

class User(Base):
    __tablename__ = "User"

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(EMAIL_LENGTH), unique=True, nullable=False)
    pwdHash = Column(CHAR(PWD_HASH_LENGTH), nullable=False)
    confirmed = Column(BOOLEAN, default=False)
    enabled = Column(BOOLEAN, default=False)
    administrator = Column(BOOLEAN, default=False)


class AccessToken(Base):
    __tablename__ = "AccessToken"

    id = Column(INT, primary_key=True)
    userId = Column(INT, ForeignKey('User.id'), nullable=False)
    token = Column(CHAR(UUID_LENGTH), default=str(uuid4()), unique=True, nullable=False)
    createdAt = Column(INT, default=int(time.time()))


class VerificationToken(Base):
    __tablename__ = "VerificationToken"

    id = Column(INT, primary_key=True)
    userId = Column(INT, ForeignKey('User.id'), nullable=False)
    token = Column(CHAR(UUID_LENGTH), default=str(uuid4()), unique=True, nullable=False)
    createdAt = Column(INT, default=int(time.time()))


# Quiz Tables

class Quiz(Base):
    __tablename__ = "Quiz"

    id = Column(INT, primary_key=True)
    token = Column(CHAR(UUID_LENGTH), default=str(uuid4()), unique=True)
    complete = Column(BOOLEAN, default=False)
    questionCount = Column(INT)
    optionCount = Column(INT)
    currentQuestion = Column(INT)
    reverseQuestions = Column(BOOLEAN, default=False)
    categoryId = Column(INT)
    timeStart = Column(INT)
    userId = Column(INT, ForeignKey('User.id'))
    levelMin = Column(INT, ForeignKey('Level.id'))
    levelMax = Column(INT, ForeignKey('Level.id'))


class Question(Base):
    __tablename__ = "Question"

    id = Column(INT, primary_key=True)
    quizId = Column(INT, ForeignKey('Quiz.id', ondelete="CASCADE"))
    curriculumId = Column(INT, ForeignKey('Curriculum.id'))
    questionIndex = Column(SMALLINT)


class Option(Base):
    __tablename__ = "Option"

    id = Column(INT, primary_key=True)
    curriculumId = Column(INT, ForeignKey('Curriculum.id'))
    quizId = Column(INT, ForeignKey('Quiz.id', ondelete="CASCADE"))
    questionId = Column(INT, ForeignKey('Question.id', ondelete="CASCADE"))
    optionIndex = Column(INT)


class Answer(Base):
    __tablename__ = "Answer"

    id = Column(INT, primary_key=True)
    quizId = Column(INT, ForeignKey('Quiz.id', ondelete="CASCADE"))
    curriculumId = Column(INT, ForeignKey('Curriculum.id'))
    questionIndex = Column(INT)
    correct = Column(BOOLEAN)


class Result(Base):
    __tablename__ = "Result"

    id = Column(INT, primary_key=True)
    quizToken = Column(CHAR(UUID_LENGTH), unique=True)
    userId = Column(INT, ForeignKey('User.id'))
    correctCount = Column(INT)
    incorrectCount = Column(INT)
    timeSpent = Column(INT)
    levelMin = Column(INT, ForeignKey('Level.id'), default=1)
    levelMax = Column(INT, ForeignKey('Level.id'), default=5)


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

def setup(engine) -> None:
    Base.metadata.create_all(engine)

