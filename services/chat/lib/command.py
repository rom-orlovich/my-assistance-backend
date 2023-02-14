

from ast import Param
from dataclasses import dataclass, field
from datetime import datetime

import re
from symbol import parameters

from typing import Callable, Dict, List, Tuple, TypeVar, Union

from click import command

from lib.date_utils import DateUtils
from services.chat.lib.chat_types import ParamOption, ParamsLocations


class Command:
    """
        Command is class that its core is a Trie words data structure. 
        If sentence will match the command the callback will execute with the parameters if they exist.
    """

    def __init__(self, cb: Callable, parameters_metadata: Dict[str, ParamOption] = None) -> None:
        """
        Args:
            cb (Callable): A callback that will execute when one of the commands are match.
            parameters_metadata (Dict[str, ParamOption], optional):Meta data about the parameter that may include in the command. Defaults to None.
        """
        self.words = {}
        self.parameters_metadata = parameters_metadata
        self.cb = cb

    def split_sentence_to_words(self, sentence: str, regex_delimiter: str = " |, |\. ") -> List[str]:
        """
        Args:
            sentence (str): The sentences.
            regex_delimiter (str, optional): How to split the sentences Defaults to " |, |\. ".

        Returns:
            _type_: List of the non empty words from the sentence.
        """
        return list(filter(None, re.split(regex_delimiter, sentence.lower())))

    def get_token_parameter(self, word: str) -> Union[Tuple[ParamOption, str], None]:
        """
        Args:
            word (str): word to analyze if it is token.
        Returns:
            Union[Tuple[ParamOption, str], None]: The key and the value of the token.
        """
        parameters_opt = self.parameters_metadata.get(word)
        if word.startswith("$") and parameters_opt:
            key = f'{word[0]}'
            token = {**parameters_opt}

            return token, key
        return None

    def add_command(self, command: str) -> None:
        """ 
        Use Trie algorithm.
        Words that already exist in the Trie node, will attach to the next node.
        Also, the methods analyze where node the token will be placed.

        Args:
            command (str): a sentence that will execute the cb. 
        """
        words = self.split_sentence_to_words(command)

        root_word = self.words
        for word in words:

            # If the word is exist move to the next node of word.
            if root_word.get(word):
                root_word = root_word[word]
            else:
                new_word = {}
                key = word

                # Check if there is parameters_metadata
                if self.parameters_metadata:
                    token = self.get_token_parameter(word)
                    if token:
                        new_word, key = token

                # Add new word the the node the current key(word).
                root_word[key] = new_word

                # Move root_word to the next node.
                root_word = root_word[key]

        # The last word in the command marks its end indictor to true.
        root_word["end"] = True

    # Add list of commands.
    def add_commands(self, commands: List[str]) -> None:
        for command in commands:
            self.add_command(command)

    def get_parameters(self, words: List[str], params_indexes: List[ParamsLocations]) -> Union[Dict, None]:
        """
        Slice the values of the parameters by their start and end position relative to the words list and generate a parameter dict. 

        Args:
            words (List[str]): A List of the words from the command.
            params_indexes (List[ParamsLocations]): A indexes list of where the parameter's value is start and end relative to the words list.   
        Returns:
            Union[Dict, None]: If the command has parameters_metadata the method will return the a dict from the extracted parameters value. 
        """
        if not self.parameters_metadata:
            return
        parameters = {}
        for param_indexes in params_indexes:
            metadata = self.parameters_metadata.get(param_indexes.token)
            param_value = words[param_indexes.min:param_indexes.max]
            parameters[metadata.field_name] = " ".join(param_value)
        return parameters

    def execute(self, command: str) -> any:
        """ 
        Loop over the provided command words and check if the current command is match the the any sequence of words in the Trie data structure.
        If it does the command will execute the callback. 

        Args:
            command (str): The command that the method will check if it match to any sequence of words in the Trie data structure.

        Returns:
            _type_: The result of the function.
        """
        words = self.split_sentence_to_words(command)
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

        # Append the last parameter index start index until the end of the words list.
        # This block only happen when the last word that match the command is parameter.
        if cur_param_name:
            params_indexes.append(
                ParamsLocations(cur_param_name, startIndex, len(words)))

        parameters = self.get_parameters(words, params_indexes)
        res = None

        # If the last word has the indicator end, the sentence match to the command and the callback will execute.
        if cur_word.get("end"):
            if parameters:
                res = self.cb(parameters)
            else:
                res = self.cb()

        return res
