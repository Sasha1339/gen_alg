import json
from typing import List
from sign import Sign
from multiplier import Multiplier


def get_multiplier(name_file) -> List[Multiplier]:
    result: List[Multiplier] = list()
    multipliers_str = open(name_file, 'r').read()
    multipliers_str = multipliers_str.replace('\n', '')
    data_multipliers = json.loads(multipliers_str)
    for multipliers_str in data_multipliers:
        result.append(Multiplier(multipliers_str["name"], multipliers_str["value"], multipliers_str["count_values"],
                                 multipliers_str["top_border"], multipliers_str["bottom_border"],
                                 multipliers_str["left_sign"], multipliers_str["right_sign"]))
    return result


def get_signs(name_file: str) -> List[Sign]:
    result: List[Sign] = list()
    signs_str = open(name_file, 'r').read()
    signs_str = signs_str.replace('\n', '')
    data_signs = json.loads(signs_str)
    for sign_str in data_signs:
        result.append(Sign(sign_str["sign"]))
    return result
