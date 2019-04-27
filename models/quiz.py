#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import ArgumentError

import response_codes
from database import db
from query import access_token, category, option, info, question, quiz, answer, result
import config
from response_codes import ResponseKeys


def _new_question(
        session: 'Session',
        quiz_id: int,
        category_id: int,
        question_number: int,
        option_count: int,
        level_min: int,
        level_max: int):

    """ Creates a question with answer options. Not committed to db """

    info_rows = info.get_by_level_and_category(session, category_id, level_min, level_max)
    options_info: List['Info'] = random.sample(population=set(info_rows), k=option_count)
    answer_id: int = random.choice(options_info).id

    question_row: 'Question' = question.create(session, quiz_id, answer_id, question_number, commit=False)
    session.flush()
    [option.create(session, o.id, question_row.quizId, question_row.id, i, commit=False) for i, o in
     enumerate(options_info)]


def new_quiz(
        session: 'Session',
        access_token_string: str,
        question_count: int,
        option_count: int,
        category_id: int,
        level_min: int,
        level_max: int) -> Dict:

    """ Creates new quiz with associated questions and options """

    user_id: int = access_token.get_user_id_by_token(session=session, access_token=access_token_string)

    try:
        if not access_token.validate(session, access_token_string):
            return {ResponseKeys.response_code: response_codes.ResponseCodes.unauthorized_401}

    except ArgumentError as e:
        print(e)
        return {ResponseKeys.response_code: response_codes.ResponseCodes.bad_request_400}

    try:
        quiz_row: 'Quiz' = quiz.create(
            session=session,
            question_count=question_count,
            option_count=option_count,
            category_id=category_id,
            user_id=user_id,
            belt_min=level_min,
            belt_max=level_max,
            commit=False
        )

        session.flush()

        [_new_question(session, quiz_row.id, category_id, i, option_count, level_min, level_max) for i in
         range(question_count)]

        session.commit()

        return {
            ResponseKeys.response_code: response_codes.ResponseCodes.created_201,
            ResponseKeys.body: {
                "title": category.get_by_id(session, quiz_row.categoryId).name,
                "quizToken": quiz_row.token,
                "totalQuestions": quiz_row.questionCount,
                "currentQuestion": quiz_row.currentQuestion,
                "optionCount": quiz_row.optionCount,
                "levelMin": quiz_row.beltMin,
                "levelMax": quiz_row.beltMax,
            }
        }

    except ArgumentError as e:
        print(e)
        return {ResponseKeys.response_code: response_codes.ResponseCodes.internal_server_error_500}


def get_quiz(session: 'Session', quiz_token: str, access_token_string: str) -> Dict:

    """ Get a quiz by access token """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.response_code: response_codes.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        return {
            ResponseKeys.response_code: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "title": category.get_by_id(session, quiz_row.categoryId).name,
                "quizToken": quiz_row.token,
                "totalQuestions": quiz_row.questionCount,
                "currentQuestion": quiz_row.currentQuestion,
                "optionCount": quiz_row.optionCount,
                "levelMin": quiz_row.beltMin,
                "levelMax": quiz_row.beltMax,
            }
        }

    except ArgumentError as e:
        print(e)
        return {"responseCode": response_codes.ResponseCodes.not_found_404}


def delete_quiz(session: 'Session', quiz_token: str, access_token_string: str) -> Dict:

    """ Deleting a quiz, including associated questions, options and answers """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.response_code: response_codes.ResponseCodes.unauthorized_401}

    quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

    quiz.delete_by_token(session, quiz_token, commit=False)
    question.delete_by_quiz_id(session, quiz_row.id, commit=False)
    option.delete_by_quiz_id(session, quiz_row.id, commit=False)

    session.commit()

    return dict()


def get_current_question(
        session: 'Session',
        access_token_string: str,
        quiz_token: str) -> Dict:

    """ Returns the current question with associated options and quiz info """

    if not access_token.validate(session, access_token_string):
        return {"responseCode": response_codes.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
        next_question_row: 'Question' = question.get_by_quiz_id_and_index(session,
                                                                          quiz_row.id,
                                                                          quiz_row.currentQuestion)

        next_question_info_row = info.get_by_id(session, next_question_row.infoId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

        options = [{
            "index": row.optionIndex,
            "text": info.get_by_id(session, row.infoId).key} for row in option_rows]

        return {
            ResponseKeys.response_code: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "questionIndex": quiz_row.currentQuestion,
                "question": next_question_info_row.value,
                "options": options
            }
        }
    except AttributeError as e:
        print(e)
        return {ResponseKeys.response_code: response_codes.ResponseCodes.not_found_404}
    except NoResultFound as e:
        print(e)
        return {ResponseKeys.response_code: response_codes.ResponseCodes.not_found_404}


def answer_question(session: 'Session',
                    access_token_string: str,
                    quiz_token: str,
                    option_index: int) -> Dict:

    """ Accepts an answer and advances the quiz. The correctness of the question is returned """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.response_code: response_codes.ResponseCodes.unauthorized_401}

    quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
    question_row: 'Question' = question.get_by_quiz_id_and_index(session, quiz_row.id, quiz_row.currentQuestion)
    option_row: 'Option' = option.get_by_question_id_and_index(session, question_row.id, option_index)

    if quiz_row.currentQuestion < quiz_row.questionCount:
        answer.create(session=session,
                      quiz_id=quiz_row.id,
                      info_id=option_row.infoId,
                      question_index=quiz_row.currentQuestion,
                      correct=question_row.infoId == option_row.infoId,
                      commit=False
                      )
        quiz_row.currentQuestion += 1
        session.commit()
    else:
        answer_count: Dict = answer.get_answer_count(session, quiz_row.id)
        result.create(session,
                      user_id=quiz_row.userId,
                      correct_count=answer_count.get('correct_count', -1),
                      incorrect_count=answer_count.get('incorrect_count', -1),
                      time_spent=int(time.time()) - quiz_row.timeStart,
                      belt_min=quiz_row.beltMin,
                      belt_max=quiz_row.beltMax,
                      )
        delete_quiz(session=session,
                    quiz_token=quiz_row.token,
                    access_token_string=access_token_string
                    )

    if question_row.infoId == option_row.infoId:

        return {ResponseKeys.response_code: response_codes.ResponseCodes.ok_200,
                ResponseKeys.body:
                    {
                        'answer': True,
                        'text': 'Svaret er korrekt'
                    }
                }
    else:
        return {ResponseKeys.response_code: response_codes.ResponseCodes.ok_200,
                ResponseKeys.body:
                    {
                        'answer': False,
                        'text': f'Svaret er forkert\n'
                        f'Du har svaret: {info.get_by_id(session, option_row.infoId).key}\n'
                        f'Det rigtige svar er: {info.get_by_id(session, question_row.infoId).key}'
                    }
                }


def _new_quiz(session):
    print(db.to_json(
        new_quiz(
            session=session,
            access_token_string=config.DEBUG_ACCESS_TOKEN,
            question_count=10,
            option_count=3,
            category_id=2,
            level_min=3,
            level_max=8)
    ))


def _current_question(session):
    print(db.to_json(get_current_question(
        session=session,
        access_token_string=config.DEBUG_ACCESS_TOKEN,
        quiz_token=config.DEBUG_QUIZ_TOKEN))
    )


def _answer_question(session):
    print(db.to_json(answer_question(
        session=session,
        access_token_string=config.DEBUG_ACCESS_TOKEN,
        quiz_token=config.DEBUG_QUIZ_TOKEN,
        option_index=random.randrange(3)))
    )


def _get_quiz(session):
    print(db.to_json(get_quiz(
        session=session,
        quiz_token=config.DEBUG_QUIZ_TOKEN,
        access_token_string=config.DEBUG_ACCESS_TOKEN))
    )


if __name__ == '__main__':
    _session = db.SessionSingleton().get_session()
    # _new_quiz(_session)
    # _get_quiz(_session)
    _current_question(_session)
    # _answer_question(_session)
