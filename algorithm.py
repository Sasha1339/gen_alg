from block import Block
import random
from parsers import *
from type_sign import TypeSign
from type_block import TypeBlock
from parameter_choice import ParameterChoice
import numexpr as ne


class Algorithm:
    _data_signs: List[Sign]
    _data_multiplier_original: List[Multiplier]
    _data_multiplier: List[Multiplier]
    _need_sensitivity: float
    _need_select: List[float]
    _blocks: List[List[Block]] = []
    _old_blocks: List[List[Block]] = []
    _count_blocks: int = 3
    _count_blocks_start: int = 3
    _count_individuals: int = 200
    _access_range: float
    _parameter_choice: ParameterChoice
    _current_work_individual: List[float] = []

    def __init__(self, file_name_signs: str, file_name_mult_orig: str, file_name_mult: str):
        self.set_data_compare()
        self._data_signs = get_signs(file_name_signs)
        self._data_multiplier_original = get_multiplier(file_name_mult_orig)
        self._data_multiplier = get_multiplier(file_name_mult)

    def set_data_compare(self):
        lines = open("resource/data_compare.json", 'r').read()
        lines = lines.replace('\n', '')
        data_lines = json.loads(lines)
        self._need_sensitivity = data_lines["need_sensitivity"]
        self._need_select = data_lines["need_select"]
        self._need_select.sort()
        self._parameter_choice = ParameterChoice[data_lines["choice_need"]]
        self._access_range = data_lines["access_range"]

    def build_individuals(self, number_iteration: int = 1):
        if number_iteration == 1:
            self.build_first_individuals()
        else:
            self._count_blocks = self._count_blocks_start + number_iteration - 1
            self._old_blocks = self._blocks
            self.build_new_generation_of_individuals()

    def build_first_individuals(self):
        for i in range(self._count_individuals):
            self._blocks.append([])
            for j in range(self._count_blocks_start):
                if j % 2 == 0:
                    self._blocks[i].append(random.choice(self._data_multiplier + self._data_multiplier_original))
                else:
                    self._blocks[i].append(random.choice(self._data_signs))
        return self._blocks

    def build_new_generation_of_individuals(self):
        list_signs: List[Block] = []
        list_multiplier: List[Block] = []
        for i in range(len(self._old_blocks)):
            for j in range(len(self._old_blocks[i])):
                if j % 2 == 0:
                    list_multiplier.append(self._old_blocks[i][j])
                else:
                    list_signs.append(self._old_blocks[i][j])
        self._blocks.clear()
        if len(list_multiplier) != 0:
            for i in range(self._count_individuals):
                self._blocks.append([])
                for j in range(self._count_blocks):
                    if j % 2 == 0:
                        element: Block = random.choice(list_multiplier)
                        self._blocks[i].append(element)
                    else:
                        element: Block = random.choice(list_signs)
                        self._blocks[i].append(element)


    def first_selection(self):
        indexes: List[int] = []
        if self._count_blocks % 2 == 0:
            for index in range(len(self._blocks)):
                if self._blocks[index][len(self._blocks[index]) - 1].get_type_sign() == TypeSign.DOUBLE:
                    indexes.append(index)
                if self._blocks[index][len(self._blocks[index]) - 1].get_type_sign() == TypeSign.SINGLE and \
                        self._blocks[index][len(self._blocks[index]) - 1].get_sign() != ")":
                    indexes.append(index)
        for index in range(len(self._blocks)):
            index_bracket_left: List[int] = []
            index_bracket_right: List[int] = []
            for i in range(len(self._blocks[index])):
                if self._blocks[index][i].get_type_block() == TypeBlock.SIGN:
                    if "(" in self._blocks[index][i].get_sign():
                        index_bracket_left.append(i)
                    elif ")" in self._blocks[index][i].get_sign():
                        index_bracket_right.append(i)
            for i in range(len(index_bracket_left)):
                if len(index_bracket_right) < len(index_bracket_left):
                    indexes.append(index)
                    break
                if index_bracket_left[i] > index_bracket_right[i]:
                    indexes.append(index)
                    break
        for index in range(len(self._blocks)):
            for i in range(len(self._blocks[index])):
                if self._blocks[index][i].get_type_block() == TypeBlock.MULTIPLIER:
                    if i > 0 and (not self.check_sign(self._blocks[index][i - 1].get_sign(),
                                                      self._blocks[index][i].get_accessed_left_sign()) and
                                  len(self._blocks[index][i].get_accessed_left_sign()) != 0):
                        indexes.append(index)
                        break
                    if i < (len(self._blocks[index]) - 1) and (
                            not self.check_sign(self._blocks[index][i + 1].get_sign(),
                                                self._blocks[index][i].get_accessed_right_sign()) and
                            len(self._blocks[index][i].get_accessed_right_sign()) != 0):
                        indexes.append(index)
                        break
        indexes.sort()
        while len(indexes) != 0:
            for index in indexes:
                self._blocks.pop(index)
                while index in indexes:
                    indexes.remove(index)
                for i in range(len(indexes)):
                    indexes[i] -= 1
                break
        return self._blocks

    def main_selection(self, change_access_range: int = 1):
        current_work_protection: List[float] = []
        results_individuals: List[List[Block]] = []
        for individual in self._blocks:
            expression: str = ""
            for element in individual:
                if element.get_type_block() == TypeBlock.MULTIPLIER:
                    expression += element.get_actual_value()
                else:
                    expression += element.get_sign()
            try:
                current_work_protection.append(float(ne.evaluate(expression)))
            except Exception as e:
                error: str = "error"
        for i in range(len(current_work_protection)):
            is_need_select: bool = True
            for cur_select in self._need_select:
                if current_work_protection[i] < cur_select * (1 - self._access_range / change_access_range):
                    is_need_select = False
                    break
            if current_work_protection[i] <= self._need_sensitivity * (1 + self._access_range / change_access_range) and is_need_select:
                results_individuals.append(self._blocks[i])
                self._current_work_individual.append(current_work_protection[i])
        self._blocks = results_individuals.copy()

    def sorted_individuals(self):
        if len(self._blocks) != 0:
            reference_value: float
            if self._parameter_choice == ParameterChoice.SELECT:
                reference_value = self._need_select[0]
            else:
                reference_value = self._need_sensitivity
            for i in range(len(self._current_work_individual) - 1):
                if abs(self._current_work_individual[i] - reference_value) > abs(self._current_work_individual[i+1] - reference_value):
                    value: float = self._current_work_individual[i]
                    self._current_work_individual[i] = self._current_work_individual[i+1]
                    self._current_work_individual[i + 1] = value
                    individual: List[Block] = self._blocks[i].copy()
                    self._blocks[i] = self._blocks[i+1].copy()
                    self._blocks[i+1] = individual
            self._current_work_individual.clear()
            count_individuals: int = len(self._blocks)
            if len(self._blocks) > 3:
                count_individuals = len(self._blocks) // 6
            result: List[List[Block]] = []
            for i in range(count_individuals):
                result.append(self._blocks[i])
            self._blocks = result.copy()
    def check_sign(self, sign: str, accessed_sign: List[str]):
        return sign in accessed_sign

    def setup(self):
        count_empty_individuals: int = 0
        count_blocks_iteration: int = 1
        while count_empty_individuals != 5:
            for i in range(100):
                self.build_individuals(count_blocks_iteration)
                self.first_selection()
                self.main_selection()
                self.sorted_individuals()
                if len(self._blocks) == 0:
                    count_empty_individuals += 1
                if count_empty_individuals == 3 or i % 3 == 0 and i != 0:
                    count_blocks_iteration += 1
                if len(self._blocks) == 2:
                    return self.get_result()
            return self.get_result()
        print("Необходимо применение другого вида защиты")
        return []


    def get_result(self):
        result: List[str] = []
        for individual in self._blocks:
            result_str: str = ""
            for i in range(len(individual)):
                if individual[i].get_type_block() == TypeBlock.MULTIPLIER:
                    result_str += individual[i].get_name_multiplier()
                else:
                    result_str += individual[i].get_sign()
            result.append(result_str)
        return result
