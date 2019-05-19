#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time
from functools import lru_cache
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import ArgumentError
from exceptions import Exceptions
import response_codes
from database import db
from query import category, option, curriculum, question, quiz, result, level
from query import answer as query_answer
from query import validate_input_data
import config
from response_codes import ResponseKeys


def _create_question(
        session: 'Session',
        quiz_id: int,
        category_id: int,
        question_number: int,
        option_count: int,
        level_min: int,
        level_max: int):
    """ Creates a question with answer options. Not committed to db """

    curriculum_rows = curriculum.get_by_level_and_category(session, category_id, level_min, level_max)
    options_curriculum: List['Curriculum'] = random.sample(population=set(curriculum_rows), k=option_count)
    answer_id: int = random.choice(options_curriculum).id

    question_row: 'Question' = question.create(session, quiz_id, answer_id, question_number, commit=False)
    session.flush()
    [option.create(session, o.id, question_row.quizId, question_row.id, i, commit=False) for i, o in
     enumerate(options_curriculum)]


def create(session: 'Session', user_id: int, data: Dict) -> Dict:
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
    try:
        quiz_row: 'Quiz' = quiz.create(
            session=session,
            question_count=question_count,
            option_count=option_count,
            category_id=category_id,
            user_id=user_id,
            level_min=level_min,
            level_max=level_max,
            commit=False
        )

        session.flush()

        [_create_question(session, quiz_row.id, category_id, i, option_count, level_min, level_max) for i in
         range(question_count)]

        session.commit()

        quiz_row = get(session, quiz_row.token)

        return {
            ResponseKeys.status: response_codes.ResponseCodes.created_201,
            ResponseKeys.body: quiz_row.get('body', {})
        }

    except ArgumentError as e:
        print(e)
        return {ResponseKeys.status: response_codes.ResponseCodes.internal_server_error_500}


def get(session: 'Session', quiz_token: str) -> Dict:
    """ Get a quiz by access token """

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

        next_question_row: 'Question' = question.get_by_quiz_id_and_index(session,
                                                                          quiz_row.id,
                                                                          quiz_row.currentQuestion)

        next_question_cur_row = curriculum.get_by_id(session, next_question_row.curriculumId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

        options = [{
            "index": row.optionIndex,
            "option": curriculum.get_by_id(session, row.curriculumId).key} for row in option_rows]

        return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "title": category.get_by_id(session, quiz_row.categoryId).name,
                "quizToken": quiz_row.token,
                "complete": quiz_row.complete,
                "totalQuestions": quiz_row.questionCount,
                "currentQuestionIndex": quiz_row.currentQuestion,
                "optionCount": quiz_row.optionCount,
                "levelMin": quiz_row.levelMin,
                "levelMax": quiz_row.levelMax,
                "currentQuestion": {
                    "index": quiz_row.currentQuestion,
                    "question": next_question_cur_row.value,
                    "options": options
                }
            }
        }

    except ArgumentError as e:
        print(e)
        return {"responseCode": response_codes.ResponseCodes.not_found_404}


@lru_cache()
def get_configuration(session: 'Session') -> Dict:
    """ Get quiz configuration options """

    categories = list(category.get_categories(session))
    categories.insert(0, "Fuld pensum")
    levels = level.get_names(session)

    return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "categories": categories,
                "levelMin": levels,
                "levelMax": levels,
                "questionCount": [10, 25, 50],
                "optionCount": [3, 4, 5],
                "timeLimit": [0, 10, 15, 20, 30],
                "displayNames": {
                    "categories": 'Kategorier',
                    "levelMax": "Højeste bælte",
                    "levelMin": "Laveste bælte",
                    "questionCount": "Antal spørgsmål",
                    "optionCount": "Antal svarmuligheder",
                    "timeLimit": "Tidsgrænse i minutter"
                }
            }
            }


def get_predefined_configurations() -> Dict:
    # todo : move into database
    raise NotImplementedError


def get_current_question(session: 'Session', quiz_token: str) -> Dict:
    """ Returns the current question with associated options and quiz info """

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

        next_question_cur_row = curriculum.get_by_id(session, next_question_row.curriculumId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

        options = [{
            "optionIndex": row.optionIndex,
            "option": curriculum.get_by_id(session, row.curriculumId).key} for row in option_rows]

        return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "questionIndex": quiz_row.currentQuestion,
                "question": next_question_cur_row.value,
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


def get_result() -> Dict:
    raise NotImplementedError


def get_results() -> Dict:
    raise NotImplementedError


def answer(session: 'Session', quiz_token: str, data: Dict) -> Dict:
    """ Accepts an answer and advances the quiz. The correctness of the question is returned """

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
    query_answer.create(session=session,
                        quiz_id=quiz_row.id,
                        curriculum_id=option_row.curriculumId,
                        question_index=quiz_row.currentQuestion,
                        correct=question_row.curriculumId == option_row.curriculumId,
                        commit=False
                        )

    """ Advancing or concluding quiz """
    if quiz_row.currentQuestion + 1 < quiz_row.questionCount:
        quiz_row.currentQuestion += 1

    else:
        answer_count: Dict = query_answer.get_answer_count(session, quiz_row.id)
        result.create(session,
                      user_id=quiz_row.userId,
                      quiz_token=quiz_row.token,
                      correct_count=answer_count.get('correct_count', -1),
                      incorrect_count=answer_count.get('incorrect_count', -1),
                      time_spent=int(time.time()) - quiz_row.timeStart,
                      level_min=quiz_row.levelMin,
                      level_max=quiz_row.levelMax,
                      commit=False
                      )
        quiz_row.complete = True

    session.commit()

    """ returns the answer result. Was it right or wrong? """
    if not question_row.curriculumId == option_row.curriculumId:
        return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
                ResponseKeys.body:
                    {
                        'answer': False,
                        'text': f'Svaret er forkert\n'
                        f'Du har svaret: {curriculum.get_by_id(session, option_row.curriculumId).key}\n'
                        f'Det rigtige svar er: {curriculum.get_by_id(session, question_row.curriculumId).key}'
                    }
                }

    return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body:
                {
                    'answer': True,
                    'text': 'Svaret er korrekt'
                }
            }


def delete(session: 'Session', quiz_token: str, commit=True) -> bool:
    """ Deleting a quiz, including associated questions, options and answers """

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


def _new_quiz(session):
    print(db.to_json(
        create(
            session=session,
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
        quiz_token=config.DEBUG_QUIZ_TOKEN))
    )


def _answer_question(session):
    print(db.to_json(answer(
        session=session,
        quiz_token=config.DEBUG_QUIZ_TOKEN,
        data={
            'optionIndex': random.randrange(3)
        }
    )
    ))


def _get_quiz(session):
    print(db.to_json(get(
        session=session,
        quiz_token=config.DEBUG_QUIZ_TOKEN))
    )


def _delete_quiz(session):
    print(db.to_json(delete(
        session=session,
        quiz_token=config.DEBUG_QUIZ_TOKEN))
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
