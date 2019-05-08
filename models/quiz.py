#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import ArgumentError
from exceptions import Exceptions
import response_codes
from database import db
from query import access_token, category, option, info, question, quiz, answer, result
from query import validate_input_data
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


def _clean_up_quiz(session: 'Session', quiz_token: str, access_token_string: str, commit=True) -> bool:
    """ Deleting a quiz, including associated questions, options and answers """

    if not access_token.validate(session, access_token_string):
        raise Exceptions.Unauthorized

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        quiz.delete_by_token(session, quiz_token, commit=False)
        question.delete_by_quiz_id(session, quiz_row.id, commit=False)
        option.delete_by_quiz_id(session, quiz_row.id, commit=False)

        if commit:
            session.commit()

        return True

    except Exceptions.Unauthorized as e:
        print(e)

    except NoResultFound:
        print('NoResultFound: Quiz not found')

    except Exception as e:
        print(e)

    return False


def new_quiz(
        session: 'Session',
        access_token_string: str,
        data: Dict) -> Dict:

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    input_schema = {
        "questionCount": [int, True],
        "optionCount": [int, True],
        "categoryId": [int, True],
        "levelMin": [int, True],
        "levelMax": [int, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    question_count: int = data.get('questionCount')
    option_count: int = data.get('optionCount')
    category_id: int = data.get('categoryId')
    level_min: int = data.get('levelMin')
    level_max: int = data.get('levelMax')

    """ Creates new quiz with associated questions and options """
    user_id: int = access_token.get_user_id_by_token(session=session, access_token=access_token_string)

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
            ResponseKeys.status: response_codes.ResponseCodes.created_201,
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
        return {ResponseKeys.status: response_codes.ResponseCodes.internal_server_error_500}


def get_quiz(session: 'Session', access_token_string: str, quiz_token: str) -> Dict:
    """ Get a quiz by access token """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "title": category.get_by_id(session, quiz_row.categoryId).name,
                "quizToken": quiz_row.token,
                "complete": quiz_row.complete,
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


def get_current_question(
        session: 'Session',
        access_token_string: str,
        quiz_token: str) -> Dict:
    """ Returns the current question with associated options and quiz info """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        if not quiz_row:
            raise NoResultFound

        """ Checking if the quiz has been completed """
        if quiz_row.complete:
            raise Exceptions.QuizCompleteError

        next_question_row: 'Question' = question.get_by_quiz_id_and_index(session,
                                                                          quiz_row.id,
                                                                          quiz_row.currentQuestion)

        next_question_info_row = info.get_by_id(session, next_question_row.infoId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

        options = [{
            "index": row.optionIndex,
            "text": info.get_by_id(session, row.infoId).key} for row in option_rows]

        return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "questionIndex": quiz_row.currentQuestion,
                "question": next_question_info_row.value,
                "options": options
            }
        }

    except Exceptions.QuizCompleteError:
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404,
                'message': 'No more questions. Quiz has been completed.'}

    except AttributeError:
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404,
                'message': 'Quiz not found'}

    except NoResultFound:
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404,
                'message': 'Quiz not found'}


def answer_question(session: 'Session',
                    access_token_string: str,
                    quiz_token: str,
                    data: Dict) -> Dict:
    """ Accepts an answer and advances the quiz. The correctness of the question is returned """

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    input_schema = {
        "optionIndex": [int, True],
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    option_index: int = data.get('optionIndex')

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        if not quiz_row:
            raise NoResultFound

    except NoResultFound:
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404,
                'message': 'Quizzen kunne ikke findes'}

    """ Checking if the quiz has been completed """
    if quiz_row.complete:
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404,
                'message': 'Quizzen er afsluttet.'}

    question_row: 'Question' = question.get_by_quiz_id_and_index(session, quiz_row.id, quiz_row.currentQuestion)
    option_row: 'Option' = option.get_by_question_id_and_index(session, question_row.id, option_index)

    """ Creating answer row  """
    answer.create(session=session,
                  quiz_id=quiz_row.id,
                  info_id=option_row.infoId,
                  question_index=quiz_row.currentQuestion,
                  correct=question_row.infoId == option_row.infoId,
                  commit=False
                  )

    """ Advancing or concluding quiz """
    if quiz_row.currentQuestion + 1 < quiz_row.questionCount:
        quiz_row.currentQuestion += 1

    else:
        answer_count: Dict = answer.get_answer_count(session, quiz_row.id)
        result.create(session,
                      user_id=quiz_row.userId,
                      quiz_token=quiz_row.token,
                      correct_count=answer_count.get('correct_count', -1),
                      incorrect_count=answer_count.get('incorrect_count', -1),
                      time_spent=int(time.time()) - quiz_row.timeStart,
                      belt_min=quiz_row.beltMin,
                      belt_max=quiz_row.beltMax,
                      commit=False
                      )
        quiz_row.complete = True

    session.commit()

    """ returns the answer result. Was it right or wrong? """
    if not question_row.infoId == option_row.infoId:
        return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
                ResponseKeys.body:
                    {
                        'answer': False,
                        'text': f'Svaret er forkert\n'
                        f'Du har svaret: {info.get_by_id(session, option_row.infoId).key}\n'
                        f'Det rigtige svar er: {info.get_by_id(session, question_row.infoId).key}'
                    }
                }

    return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body:
                {
                    'answer': True,
                    'text': 'Svaret er korrekt'
                }
            }


def _new_quiz(session):
    print(db.to_json(
        new_quiz(
            session=session,
            access_token_string=config.DEBUG_ACCESS_TOKEN,
            data={
                'questionCount': 10,
                'optionCount': 3,
                'categoryId': 2,
                'levelMin': 3,
                'levelMax': 8
            }
        )
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
        data={
            'optionIndex': random.randrange(3)
        }
    )
    ))


def _get_quiz(session):
    print(db.to_json(get_quiz(
        session=session,
        access_token_string=config.DEBUG_ACCESS_TOKEN,
        quiz_token=config.DEBUG_QUIZ_TOKEN))
    )


def _delete_quiz(session):
    print(db.to_json(_clean_up_quiz(
        session=session,
        quiz_token=config.DEBUG_QUIZ_TOKEN,
        access_token_string=config.DEBUG_ACCESS_TOKEN))
    )


if __name__ == '__main__':
    _session = db.SessionSingleton().get_session()

    # for x in range(100):
    #     _new_quiz(_session)

    _new_quiz(_session)
    # _get_quiz(_session)
    # _current_question(_session)
    # _answer_question(_session)
    # _delete_quiz(_session)
