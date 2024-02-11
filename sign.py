from block import Block
from type_sign import TypeSign
from direction_sign import DirectionSign
from type_block import TypeBlock


class Sign(Block):
    _type_block: TypeBlock = TypeBlock.SIGN
    _sign: str
    _type_sign: TypeSign
    _direction_sign: DirectionSign

    def __init__(self, sign: str):
        self._sign = sign
        if len(sign) == 1:
            self._type_sign = TypeSign.SINGLE
        else:
            self._type_sign = TypeSign.DOUBLE
        if "(" in sign:
            self._direction_sign = DirectionSign.LEFT
        elif ")" in sign:
            self._direction_sign = DirectionSign.RIGHT
        else:
            self._direction_sign = DirectionSign.UNREGISTERED

    def get_type_sign(self) -> TypeSign:
        return self._type_sign

    def get_direction_sign(self) -> DirectionSign:
        return self._direction_sign

    def get_sign(self) -> str:
        return self._sign
