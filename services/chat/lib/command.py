

from ast import Param
from dataclasses import dataclass, field
from datetime import datetime

import re
from symbol import parameters

from typing import Callable, Dict, List, TypeVar

from click import command

from lib.date_utils import DateUtils
from lib.my_types import ParamOption, ParamsLocations


class Command:
    def __init__(self, cb: Callable, parameters_metadata: Dict[str, ParamOption] = None) -> None:
        self.words = {}
        self.parameters_metadata = parameters_metadata
        self.cb = cb

    def add_command(self, command: str):
        words = list(filter(None, re.split(" |, |\. ", command.lower())))

        root_word = self.words

        for i, word in enumerate(words):
            if root_word.get(word):
                root_word = root_word[word]
            else:
                new_word = {}
                key = word
                if self.parameters_metadata:
                    parameters_opt = self.parameters_metadata.get(word)
                    if word.startswith("$") and parameters_opt:
                        key = f'{word[0]}'
                        new_word = {"index": i, **parameters_opt}

                root_word[key] = new_word
                root_word = root_word[key]

        root_word["end"] = True

    def add_commands(self, commands: List[str]):
        for command in commands:
            self.add_command(command)

    def get_parameters(self, words: List[str], params_indexes: List[ParamsLocations]):
        if not self.parameters_metadata:
            return

        parameters = {}
        for param_indexes in params_indexes:
            metadata = self.parameters_metadata.get(param_indexes.token)
            param_value = words[param_indexes.min:param_indexes.max]
            parameters[metadata.field_name] = " ".join(param_value)
        return parameters

    def execute(self, command: str):
        words = list(filter(None, re.split(" |, |\. ", command.lower())))
        cur_word = self.words

        params_indexes: List[ParamsLocations] = []
        startIndex = None
        endIndex = None
        cur_param_name = None

        for i, word in enumerate(words):
            word_command = cur_word.get(word)
            cur_param = cur_word.get("$")
            # If there there is corresponded word is continue to next word.
            if word_command:
                cur_word = cur_word[word]

            # If the position of the last parameter is known, check where is the end input of that parameter.
                if startIndex and not endIndex:
                    endIndex = i
                    params_indexes.append(
                        ParamsLocations(cur_param_name, startIndex, endIndex))
                    endIndex = None
                    startIndex = None
                    cur_param_name = None

         # Check where is the first position of parameter location and save its index and his name.
            if not startIndex and cur_param:
                startIndex = i
                cur_word = cur_word["$"]
                cur_param_name = cur_param.get("token")

        if cur_param_name:
            params_indexes.append(
                ParamsLocations(cur_param_name, startIndex, len(words)))

        self.words.get(cur_param_name) or self.words.get(word)
        parameters = self.get_parameters(words, params_indexes)

        res = None
        if cur_word.get("end"):

            if parameters:
                res = self.cb(parameters)
            else:
                res = self.cb()

        return res
