from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Dict, List, TypeVar, Union

T = TypeVar("T", bound="Word")
WD = TypeVar("WD", bound="WordsDict")


class Word:
    value: str
    is_exist: bool
    field_type: str or None
    field_name: str or None
    next_words: List[T]
    next_words_len: int

    def __init__(self, next_words: Dict[str, T], field_name: Union[str, None], field_type: Union[str, None], ) -> None:
        self.next_words = next_words
        self.field_name = field_name
        self.field_type = field_type
        self.is_exist = False

        self.next_words_len = len(next_words)

    def change_is_exist(self):
        self.is_exist = True

    def convert_next_words_to_str(self) -> str:
        return " ".join(list(map(lambda x: x.value, self.next_words)))

    def convert_next_words_to_date(self, format: str = "%d/%m/%y,%H:%M:%S") -> None or str:
        next_words_str = self.convert_next_words_to_str()
        try:
            return datetime.strptime(next_words_str, format).isoformat()
        except ValueError:
            return None

    def convert_parameters(self):
        if self.field_type == "str":
            return self.convert_next_words_to_str()
        if self.field_type == "int":
            return int(self.next_words[0].value)
        if self.field_type == "date":
            return self.convert_next_words_to_date()
        else:
            return list(map(lambda x: x.value, self.next_words))

    def get_parameters(self):
        if not self.field_type:
            return None
        next_words_len = len(self.next_words)
        if not next_words_len:
            return None
        return self.convert_parameters()


class WordsDict:

    def __init__(self, words_dict: Dict[str, Word]) -> None:

        self.words_dict = words_dict

    def check_all_words_is_exist_prop(self) -> bool:

        for key, value in self.words_dict.items():
            if not value.is_exist:
                return False
            for next_word in value.next_words:
                if not next_word.is_exist:
                    return False

        return True

    def map_parameters(self, content: str) -> Dict[str, str]:
        content_words_list = re.split(" |, ", content.lower())
        for word in content_words_list:
            words_match = self.words_dict.get(word)
            if not words_match:
                pass

    def is_content_valid(self, content: str) -> bool:
        """
        Args:
            content (str): The command text content. 
        Returns:
            bool: True if all the words are exist in the command, otherwise False.
        """
        content_words_list = re.split(" |, ", content.lower())
        for i, word in enumerate(content_words_list):
            words_match = self.words_dict.get(word)
            if not words_match:
                continue
            words_match.change_is_exist()
            words_next_list = words_match.next_words
            words_next_list_len = len(words_next_list)
            if not words_next_list_len:
                continue
            else:
                if words_next_list_len + i > len(content_words_list)-1:
                    return False
                for j, next_word in enumerate(words_next_list):
                    if content_words_list[i+j+1] == next_word:
                        next_word.change_is_exist()

        return self.check_all_words_is_exist_prop()


if __name__ == "__main__":
    pass
