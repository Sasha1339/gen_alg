from type_block import TypeBlock
from type_sign import TypeSign
from typing import List


class Block:
    _type_block: TypeBlock

    def get_type_block(self):
        return self._type_block

    def get_type_sign(self) -> TypeSign:
        pass

    def get_sign(self) -> str:
        pass

    def get_accessed_left_sign(self) -> List[str]:
        pass

    def get_accessed_right_sign(self) -> List[str]:
        pass

    def get_actual_value(self) -> str:
        pass

    def get_name_multiplier(self) -> str:
        pass