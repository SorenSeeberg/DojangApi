import random
from typing import List, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import ArgumentError
from database import db
from database import quiz
from database import question
from database import info
from database import option
from database import access_token
from database import user
from database import category


def _new_question(
        session: 'Session',
        quiz_id: int,
        category_id: int,
        question_number: int,
        option_count: int,
        level_min: int,
        level_max: int):

    info_rows = info.get_by_level_and_category(session, category_id, level_min, level_max)
    options_info: List['Info'] = random.sample(population=set(info_rows), k=option_count)
    answer_id: int = random.choice(options_info).id

    question_row: 'Question' = question.create(session, quiz_id, answer_id, question_number, commit=False)
    session.flush()
    [option.create(session, o.id, question_row.id, commit=False) for o in options_info]


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


def next_question(
        session: 'Session',
        email: str,
        access_token_string: str,
        quiz_token: str) -> Dict:
    if not access_token.validate_by_email(session, email, access_token_string):
        return {"responseCode": db.ResponseCodes.unauthorized_401}

    try:
        quiz_row: 'Quiz' = quiz.get_by_token(session, quiz_token)
        next_question_row: 'Question' = question.get_by_quiz_id_and_number(session, quiz_row.id,
                                                                           quiz_row.currentQuestion)

        next_question_info_row = info.get_by_id(session, next_question_row.infoId)
        option_rows: List['Option'] = option.get_by_question_id(session, next_question_row.id)
        option_dicts: List = [info.get_by_id(session, option_row.infoId).key for i, option_row in
                              enumerate(option_rows)]

        return {
            "responseCode": db.ResponseCodes.ok_200,
            "body": {
                "questionNumber": quiz_row.currentQuestion,
                "question": next_question_info_row.value,
                "options": option_dicts
            }
        }
    except AttributeError as e:
        print(e)
        return {"responseCode": db.ResponseCodes.not_found_404}
    except NoResultFound as e:
        print(e)
        return {"responseCode": db.ResponseCodes.not_found_404}


def answer_question():
    raise NotImplementedError


if __name__ == '__main__':
    _session = db.SessionSingleton().get_session()

    print(db.to_json(
        new_quiz(
            session=_session,
            access_token_string="99956412-a52d-4e8a-bb49-9c0405aebf2c",
            question_count=30,
            option_count=3,
            category_id=2,
            email="soren.seeberg@gmail.com",
            level_min=3,
            level_max=8)
    ))

    print(db.to_json(next_question(
        session=_session,
        email="soren.seeberg@gmail.com",
        access_token_string='99956412-a52d-4e8a-bb49-9c0405aebf2c',
        quiz_token='fc65ca62-f893-4e5d-9a9c-4edd1dba1cce'))
    )
