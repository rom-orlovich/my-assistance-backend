

from dataclasses import dataclass

import re
from symbol import parameters

from typing import Callable, Dict, TypeVar

from click import command


PO = TypeVar("PO", bound="ParamOption")


@dataclass
class ParamOption:
    field_name: str
    type: str
    until: str = None


class Command:
    def __init__(self, cb: Callable) -> None:
        self.words = {}
        self.parameters = {}
        self.cb = cb

    def add_command(self, content: str, parameters_opt: Dict[str, PO] = None):
        words = re.split(" |, ", content.lower())
        root_word = self.words

        for i, word in enumerate(words):

            if root_word.get(word):
                root_word = root_word[word]
            else:
                if parameters_opt:
                    if word.startswith("$"):
                        root_word[i] = parameters_opt[word]
                    else:
                        new_word = {}
                        root_word[word] = new_word
                        root_word = root_word[word]

        root_word["end"] = True

    def execute(self, content: str):
        words = re.split(" |, ", content)
        cur_word = self.words
        parameters = {}

        cur_parameter = None
        for i, word in enumerate(words):
            parameters_opt = cur_word.get(i)
            print(cur_word, parameters_opt)
            if parameters_opt:

                cur_parameter = parameters.get(
                    parameters_opt.field_name)
                if cur_parameter:
                    cur_parameter.append(word)
                else:
                    parameters[f'{parameters_opt.field_name}'] = [word]
            else:
                if cur_word.get(word):
                    cur_word = cur_word[word]
                else:
                    print(parameters)
                    return

        if cur_word.get("end"):
            if parameters:

                self.cb(parameters)
            else:
                self.cb()


if __name__ == "__main__":
    # command.add_command("please create new event on $1", {
    #                     "$1": ParamOption("date", "on", "date")})
    command = Command(lambda x: print("l"))

    command.add_command("please create new event on $1 at $2", {
                        "$1": ParamOption(field_name="date", until="at", type="date"), "$2": ParamOption(field_name="date", type="date")})

    command.execute("please create new event on 12/12/23 at 12:00")


# please create new event on $1
# please create new event on 25/02/23
