

# start
# end
# location
# description
# summary

from sandbox.Questionnaire import Questionnaire


ADD_EVENTS_QUESTIONNAIRE = [
    {"question": "When the event will start?", "answer": "", "field": "start"},
    {"question": "when the event will end?", "answer": "", "field:": "end"},
    {"question:": "Where the event will place?",
        "answer": "", "field": "locations"},
    {"question": "May you want add description?",
        "answer": "", "field": "description"},
    {"question": "Enter 'events/create/submit' to confirm", "answer": "", "field": ''}
]


class CalenderChat():
    def __init__(self):
        self.create_events = Questionnaire(ADD_EVENTS_QUESTIONNAIRE)
        self.get_events = Questionnaire([])
        self.cur_questionnaire = None
        self.result = {}

    def manage_commands(self, content: str):
        self.active(content)
        self.transverse(content)
        self.end(content)

    def conversation(self, content: str):
        if self.cur_questionnaire is None:
            return
        conversation = self.cur_questionnaire.conversation(content)
        if conversation:
            return conversation

    def submit_results(self, content: str):
        if self.cur_questionnaire.end(content):
            return self.cur_questionnaire.create_answers_results()

    def active(self, content: str):
        if "/events/get" in content.lower():
            self.cur_questionnaire.reset_all()
            self.cur_questionnaire = self.get_events
        elif "/events/create" in content.lower():
            self.cur_questionnaire.reset_all()
            self.cur_questionnaire = self.create_events

    def transverse(self, content: str):
        if "/back" in content.lower():
            self.cur_questionnaire.back()

        elif "/next" in content.lower():
            self.cur_questionnaire = self.cur_questionnaire.next()

    def end(self, content: str):
        if "/events/end" in content.lower():
            self.cur_questionnaire = None
