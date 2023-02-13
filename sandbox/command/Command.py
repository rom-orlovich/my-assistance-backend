from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Self

import re

from WordsDict import WordsDict


class Command:
    def __init__(self, words_to_active: WordsDict, words_parameters_to_cb: WordsDict, cb: Callable([Any], Any)) -> None:
        self.words_to_active = words_to_active
        self.words_parameters_to_cb = words_parameters_to_cb
        self.cb = cb
