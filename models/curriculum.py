from typing import Dict

from query import validate_input_data, category
from response_codes import ResponseKeys, ResponseCodes
from query import curriculum, level
from database.test_session import get_session


def get(session: 'Session', data: Dict) -> Dict:

    input_schema = {
        "categoryId": [int, True],
        "levelMin": [int, True],
        "levelMax": [int, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    category_id: int = data.get('categoryId', -1)
    level_min: int = data.get('levelMin', -1)
    level_max: int = data.get('levelMax', -1)

    level_labels = level.get_names(session)
    category_labels = category.get(session)

    # Out of bounds validation checks
    if category_id < 0 or category_id - 1 > len(category_labels):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    if level_min - 1 < 0 or level_min - 1 > len(level_labels):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    if level_max - 1 < 0 or level_max - 1 > len(level_labels):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    curriculum_rows = curriculum.get_by_level_and_category(session, category_id, level_min, level_max)

    return_data = [[row.key, row.value, level_labels[row.levelId - 1]] for row in curriculum_rows]

    if category_id == 0:
        category_label = 'Fuld Pensum'
    else:
        category_label = category_labels[category_id - 1]

    return {ResponseKeys.status: ResponseCodes.ok_200,
            ResponseKeys.body: {
                    'levelLabels': level_labels,
                    'categoryLabels': ['Fuld pensum'] + category_labels,
                    'levelMinLabel': level_labels[level_min - 1],
                    'levelMaxLabel': level_labels[level_max - 1],
                    'categoryLabel': category_label,
                    'data': return_data
                }
            }


def update() -> Dict:
    raise NotImplementedError


if __name__ == '__main__':
    session = get_session()

    result = get(session, {'categoryId': 0, 'levelMin': 1, 'levelMax': 3})
    print(result.get('status'))
    print(result.get('body').get('categoryLabel'))
    print('done')

