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
from query import category, option, curriculum, question, quiz, result, level
from query import answer as query_answer
from query import validate_input_data
from response_codes import ResponseKeys


def _create_question(
        session: 'Session',
        quiz_id: int,
        category_id: int,
        question_index: int,
        option_count: int,
        level_min: int,
        level_max: int,
        question_count: int,
        used_ids: List[int]):
    """ Creates a question with answer options. Not committed to db """

    curriculum_ids = list()
    attempts = 0

    if category_id == 0:
        while not curriculum_ids:
            if attempts == 20:
                return False
            category_id = random.randrange(1, category.count()+1)
            curriculum_rows = curriculum.get_by_level_and_category(session, category_id, level_min, level_max)
            curriculum_ids: List[int] = [row.id for row in curriculum_rows]
            attempts += 1
    else:
        curriculum_rows = curriculum.get_by_level_and_category(session, category_id, level_min, level_max)
        curriculum_ids: List[int] = [row.id for row in curriculum_rows]

    if len(curriculum_ids) >= option_count:
        option_ids: List[int] = random.sample(population=set(curriculum_ids), k=option_count)
    else:
        option_ids: List[int] = [random.choice(curriculum_ids) for i in range(option_count)]

    answer_id = -1

    if len(curriculum_ids) < question_count:
        answer_id = random.choice(option_ids)
    else:
        while answer_id in used_ids or answer_id == -1:
            answer_id = random.choice(option_ids)

    used_ids.append(answer_id)

    question_row: 'Question' = question.create(session, quiz_id, answer_id, question_index, commit=False)
    session.flush()
    [option.create(session, o, question_row.quizId, question_row.id, i, commit=False) for i, o in
     enumerate(option_ids)]

    return True


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

    if level_min >= level_max-1:
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400,
                ResponseKeys.message: 'Der skal være større afstand mellem største og mindste grad'}

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

        used_ids: List[int] = list()

        for i in range(1, question_count+1):
            result = _create_question(session,
                                      quiz_row.id,
                                      category_id, i,
                                      option_count,
                                      level_min,
                                      level_max,
                                      question_count,
                                      used_ids)

            if not result:
                session.rollback()
                return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400,
                        ResponseKeys.message: 'Kunne ikke oprette quizzen'}

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

        if not quiz_row.complete:
            next_question_cur_row = curriculum.get_by_id(session, next_question_row.curriculumId)
            option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

            options = [{
                "index": row.optionIndex,
                "option": curriculum.get_by_id(session, row.curriculumId).key} for row in option_rows]

            current_question = {
                    "index": quiz_row.currentQuestion,
                    "question": next_question_cur_row.value,
                    "options": options
                }

        else:
            options = list()
            current_question = {
                "index": -1,
                "question": '',
                "options": options
            }

        if quiz_row.categoryId == 0:
            title = 'Fuld Pensum'
        else:
            title = category.get_by_id(session, quiz_row.categoryId).name

        return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                "title": title,
                "quizToken": quiz_row.token,
                "complete": quiz_row.complete,
                "totalQuestions": quiz_row.questionCount,
                "currentQuestionIndex": quiz_row.currentQuestion,
                "optionCount": quiz_row.optionCount,
                "levelMin": quiz_row.levelMin,
                "levelMax": quiz_row.levelMax,
                "currentQuestion": current_question
            }
        }

    except ArgumentError as e:
        print(e)
        return {"responseCode": response_codes.ResponseCodes.not_found_404}


@lru_cache()
def get_configuration(session: 'Session') -> Dict:
    """ Get quiz configuration options """

    categories = list(category.get(session))
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
    # TODO : move into database
    raise NotImplementedError


def get_result(session: 'Session', quiz_token: str) -> Dict:

    quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
    result_row: 'Result' = result.get_by_quiz_token(session, quiz_token)
    answer_rows = query_answer.get_by_quiz_id(session, quiz_row.id)
    percentage_correct: int = int(result_row.correctCount / (result_row.correctCount + result_row.incorrectCount) * 100)

    if quiz_row.categoryId == 0:
        category_name: str = 'Fuld Pensum'
    else:
        category_name: str = category.get_by_id(session, quiz_row.categoryId).name

    return {
            ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body: {
                'categoryName': category_name,
                'quizToken': quiz_row.token,
                'percentageCorrect': percentage_correct,
                'timeSpent': result_row.timeSpent,
                'answers': [{'text': curriculum.get_by_id(session, a.curriculumId).key, 'correct': a.correct} for a in answer_rows]
            }
        }


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
    if quiz_row.currentQuestion == quiz_row.questionCount:
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
    else:
        quiz_row.currentQuestion += 1

    session.commit()

    """ returns the answer result. Was it right or wrong? """
    if not question_row.curriculumId == option_row.curriculumId:
        return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
                ResponseKeys.body:
                    {
                        'answer': False,
                        'text': f'<p>Du har svaret: <b>{curriculum.get_by_id(session, option_row.curriculumId).key}</b><p>'
                        f'<p>Det rigtige svar er: <b>{curriculum.get_by_id(session, question_row.curriculumId).key}</b><p>'
                    }
                }

    return {ResponseKeys.status: response_codes.ResponseCodes.ok_200,
            ResponseKeys.body:
                {
                    'answer': True,
                    'text': '<p>Svaret er korrekt<p>'
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

