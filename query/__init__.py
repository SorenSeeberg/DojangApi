from typing import Dict


def validate_input_data(data: Dict, validation_scheme: Dict) -> bool:
    for key, value in validation_scheme.items():
        value_type = value[0]
        required: bool = value[1]

        if required:
            if key not in data:
                print('Required field missing:', key)
                return False

        if key in data:
            if not isinstance(data.get(key), value_type):
                print(f'Value of {key} is of type {type(data.get(key))}. Expected {value_type}')
                return False

    return True
