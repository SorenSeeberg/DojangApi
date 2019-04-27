#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import ArgumentError
from database import db
from query import access_token, category, option, info, question, quiz, user, answer, result
import config


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
        email: str,
        level_min: int,
        level_max: int) -> Dict:
    user_id: int = user.get_by_email(session, email).id
    print(user_id)

    try:
        if not access_token.validate_by_id(session, user_id, access_token_string):
            return {"responseCode": db.ResponseCodes.unauthorized_401}

    except ArgumentError as e:
        print(e)
        return {"responseCode": db.ResponseCodes.bad_request_400}

    try:
        quiz_row: 'Quiz' = quiz.create(
            session,
            question_count,
            option_count,
            category_id,
            user_id,
            level_min,
            level_max,
            commit=False
        )

        session.flush()

        [_new_question(session, quiz_row.id, category_id, i, option_count, level_min, level_max) for i in
         range(1, question_count + 1)]

        session.commit()

        return {
            "responseCode": db.ResponseCodes.created_201,
            "body": {
                "title": category.get_by_id(session, quiz_row.categoryId).name,
                "quizToken": quiz_row.token,
                "totalQuestions": quiz_row.questionCount,
                "optionCount": quiz_row.optionCount,
                "levelMin": quiz_row.beltMin,
                "levelMax": quiz_row.beltMax,
            }
        }

    except ArgumentError as e:
        print(e)
        return {"responseCode": db.ResponseCodes.internal_server_error_500}


def delete_quiz(session: 'Session', quiz_token: str) -> Dict:
    """
    Deleting a quiz, including associated questions, options and answers
    """

    quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)

    quiz.delete_by_token(session, quiz_token, commit=False)
    question.delete_by_quiz_id(session, quiz_row.id, commit=False)
    option.delete_by_quiz_id(session, quiz_row.id, commit=False)

    session.commit()

    return dict()


def current_question(
        session: 'Session',
        email: str,
        access_token_string: str,
        quiz_token: str) -> Dict:
    if not access_token.validate_by_email(session, email, access_token_string):
        return {"responseCode": db.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
        next_question_row: 'Question' = question.get_by_quiz_id_and_index(session,
                                                                          quiz_row.id,
                                                                          quiz_row.currentQuestion)

        next_question_info_row = info.get_by_id(session, next_question_row.infoId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)

        options = [{"index": row.optionIndex, "text": info.get_by_id(session, row.infoId).key} for row in option_rows]

        return {
            "responseCode": db.ResponseCodes.ok_200,
            "body": {
                "questionIndex": quiz_row.currentQuestion,
                "question": next_question_info_row.value,
                "options": options
            }
        }
    except AttributeError as e:
        print(e)
        return {"responseCode": db.ResponseCodes.not_found_404}
    except NoResultFound as e:
        print(e)
        return {"responseCode": db.ResponseCodes.not_found_404}


def answer_question(session: 'Session',
                    email: str,
                    access_token_string: str,
                    quiz_token: str,
                    option_index: int) -> Dict:
    if not access_token.validate_by_email(session, email, access_token_string):
        return {"responseCode": db.ResponseCodes.unauthorized_401}

    quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
    question_row: 'Question' = question.get_by_quiz_id_and_index(session, quiz_row.id, quiz_row.currentQuestion)
    option_row: 'Option' = option.get_by_question_id_and_index(session, question_row.id, option_index)

    # TODO : fix if currentQuestion becomes zero indexed
    if quiz_row.currentQuestion < quiz_row.questionCount - 1:
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
        delete_quiz(session, quiz_row.token)

    if question_row.infoId == option_row.infoId:

        return {'responseCode': db.ResponseCodes.ok_200,
                'body':
                    {
                        'answer': True,
                        'text': 'Svaret er korrekt'
                    }
                }
    else:
        return {'responseCode': db.ResponseCodes.ok_200,
                'body':
                    {
                        'answer': False,
                        'text': f'Svaret er forkert\n'
                        f'Du har svaret: {info.get_by_id(session, option_row.infoId).key}\n'
                        f'Det rigtige svar er: {info.get_by_id(session, question_row.infoId).key}'
                    }
                }


if __name__ == '__main__':
    _session = db.SessionSingleton().get_session()

    # print(db.to_json(
    #     new_quiz(
    #         session=_session,
    #         access_token_string=config.DEBUG_ACCESS_TOKEN,
    #         question_count=10,
    #         option_count=3,
    #         category_id=2,
    #         email=config.DEBUG_EMAIL,
    #         level_min=3,
    #         level_max=8)
    # ))

    print(db.to_json(current_question(
        session=_session,
        email=config.DEBUG_EMAIL,
        access_token_string=config.DEBUG_ACCESS_TOKEN,
        quiz_token=config.DEBUG_QUIZ_TOKEN))
    )

    print(db.to_json(answer_question(
        session=_session,
        email=config.DEBUG_EMAIL,
        access_token_string=config.DEBUG_ACCESS_TOKEN,
        quiz_token=config.DEBUG_QUIZ_TOKEN,
        option_index=random.randrange(3)))
    )
