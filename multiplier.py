from block import Block
from typing import List
from type_block import TypeBlock


class Multiplier(Block):
    _type_block: TypeBlock = TypeBlock.MULTIPLIER
    _name: str
    _left_sign: List[str]
    _right_sign: List[str]
    _value: str
    _step: float
    _top_border: float
    _bottom_border: float

    def __init__(self, name: str, value: str, count_values: int, top_border: float = 0.0,
                 bottom_border: float = 0.0, left_sign: List[str] = list, right_sign: List[str] = list):
        self._name = name
        self._value = value
        if top_border == 0.0 and bottom_border == 0.0:
            self._top_border = float(value)
            self._bottom_border = float(value)
        else:
            self._top_border = top_border
            self._bottom_border = bottom_border
        self.set_step(count_values)
        self._left_sign = left_sign
        self._right_sign = right_sign

    def get_name_multiplier(self) -> str:
        return self._name

    def get_actual_value(self) -> str:
        return self._value

    def set_step(self, count_values: int):
        self._step = (self._top_border - self._bottom_border) / (count_values - 1.0)

    def get_more_actual_value(self) -> str:
        if float(self._value) + self._step <= self._top_border:
            self._value = str(float(self._value) + self._step)
        else:
            self._value = str(self._top_border)
        return self._value

    def get_small_actual_value(self) -> str:
        if float(self._value) - self._step >= self._bottom_border:
            self._value = str(float(self._value) - self._step)
        else:
            self._value = str(self._bottom_border)
        return self._value

    def get_accessed_left_sign(self) -> List[str]:
        return self._left_sign

    def get_accessed_right_sign(self) -> List[str]:
        return self._right_sign
