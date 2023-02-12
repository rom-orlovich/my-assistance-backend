from dataclasses import dataclass
from typing import List


@dataclass
class QuestionAnswer:
    question: str
    answer: str
    field: str


class Questionnaire:
    def __init__(self, questionnaire: List[QuestionAnswer]) -> None:
        self.questionnaire = questionnaire

        self.reset_state()

    def reset_state(self):
        self.mode = False
        self.wait_for_answer = False
        self.cur_index = 0

    def reset_all_answer(self):
        for questionAnswer in self.questionnaire:
            questionAnswer.answer = ""

    def reset_all(self):
        self.reset_all_answer()
        self.reset_state()

    def end(self):
        last_index = len(self.questionnaire)-1
        if self.cur_index == last_index:
            if self.get_answer(last_index) == "submit":
                return True

    def reset_answer(self, index: int):
        self.questionnaire[index].answer = ""

    def index_valid(self, index: int):
        if 0 < index < len(self.questionnaire):
            return True
        else:
            return False

    def add_question(self, question: str, field: str):
        self.questionnaire.append(
            {"question": question, "answer": "", "field": field})

    def add_answer(self, answer: str, index: int):
        if self.index_valid(index):
            self.questionnaire[index][answer] = answer

            return True
        else:
            return False

    def get_answer(self, index: int):
        return self.questionnaire[index].answer

    def get_question(self, index: int):
        return self.questionnaire[index].question

    def quest_cur_question(self):
        self.wait_for_answer = True
        return self.get_question(self.cur_index)

    def response_cur_question(self, answer: str):
        if self.add_answer(answer, self.cur_index):
            self.next()

    def conversation(self, answer: str):
        if self.wait_for_answer:
            self.response_cur_question(answer)
        else:
            return self.quest_cur_question()

    def back(self):
        if not self.index_valid(self.cur_index - 1):
            return
        self.cur_index -= 1
        self.wait_for_answer = False

    def next(self):
        if not self.index_valid(self.cur_index + 1):
            return
        self.cur_index += 1
        self.wait_for_answer = False

    def create_answers_results(self):
        results = {}
        for questionAnswer in self.questionnaire[:-1]:
            results[questionAnswer.field] = questionAnswer.answer

        return results
