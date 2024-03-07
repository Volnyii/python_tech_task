from urllib.parse import parse_qs
from enum import Enum

"""
Задача №1
Получить из url: https://google.ru/?wmid=242&clickid=92c84d0f8c034531ace41792bd8bcc05&Mookid=zoSIq0bZhDXE
значение параметра clickid
"""


class StringsEnum(Enum):
    URL_TEST = "https://google.ru/?wmid=242&clickid=92c84d0f8c034531ace41792bd8bcc05&Mookid=zoSIq0bZhDXE"


class ParametersEnum(Enum):
    CLICKID = "clickid"


class StringParser:
    """String parser"""

    def __init__(self, input_string: StringsEnum):
        self.__input_string = input_string.value
        self.__json_from_input_string = self.__get_json_from_input_string

    @staticmethod
    def __print_log_text(parameter: str, parameter_value: str):
        print(f"Value {parameter} = {parameter_value}")

    @property
    def __get_json_from_input_string(self) -> dict[str]:
        return parse_qs(self.__input_string)

    def get_param_list(self, arg_value: ParametersEnum):
        arg_value = arg_value.value
        param_value = self.__json_from_input_string[arg_value][0]
        self.__print_log_text(arg_value, param_value)


if __name__ == "__main__":
    (StringParser(StringsEnum.URL_TEST)
     .get_param_list(ParametersEnum.CLICKID))
