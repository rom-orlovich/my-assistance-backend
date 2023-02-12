
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict
from my_types import Message
from Event import Event
import types

from enum import Enum


class CalenderChatMode(Enum):
    GET_EVENTS = 1
    CREATE_EVENTS = 2


# start
# end
# location
# description
# summary


class CalenderChat:
    def __init__(self):
        self.is_active = False
        self.mode = None
        self.create_events_index = 0
        self.get_events_index = 0
        self.create_events_opt = {}
        self.get_events_opt = {}
        self.create_events_questions_list = [("When the event will start?", "start"),
                                             ("when the event will end?", "end"), ("Where the event will place?", "locations"), ("May you want add description?", "description")]
        self.wait_for_answer = False

    def manage_chat(self, content):
        self.get_create_event_questions(self)

    def check_next_index_valid(self):
        if self.create_events_index + 1 <= len(self.create_events_questions_list)-1:
            return False

    def check_pre_index_valid(self):
        if self.create_events_index - 1 >= 0:
            return False

    def get_create_events_response(self, content) -> None:
        if not self.wait_for_answer:
            return

        if self.mode is not CalenderChatMode.CREATE_EVENTS:
            return
        if not content:
            return
        self.create_events_opt[self.get_create_event_prop()] = content
        if self.create_events_index + 1 == len(self.create_events_questions_list):
            return
        self.create_events_index += 1
        self.wait_for_answer = False

    def get_create_event_question(self) -> str:
        return self.create_events_questions_list[self.create_events_index][0]

    def get_create_event_prop(self) -> str:
        return self.create_events_questions_list[self.create_events_index][1]

    def get_create_event_questions(self) -> str:
        if self.wait_for_answer:
            return
        if self.mode is not CalenderChatMode.CREATE_EVENTS:
            return

        if self.create_events_index < 0:
            return
        cur_question = self.create_events_questions_list[self.create_events_index][0]
        self.wait_for_answer = True
        return cur_question

    def toggle_activation(self, content: str) -> None:
        if "/calender" in content.lower():
            self.is_activate = True
        if "/calender/end" in content.lower():
            self.reset_calender_chat()

    def change_mode(self, content: str) -> None:
        if "/events/get" in content.lower():
            self.mode = CalenderChatMode.GET_EVENTS
        if "/events/create" in content.lower():
            self.mode = CalenderChatMode.CREATE_EVENTS
        else:
            self.mode = None

    def traverse_question(self, content: str):
        if 'back' in content.lower():
            if not self.check_pre_index_valid():
                return
            self.create_events_index -= 1
            self.wait_for_answer = False

        if 'next' in content.lower():
            if not self.check_next_index_valid():
                return
            self.create_events_index -= 1
            self.wait_for_answer = False

    def reset_calender_chat(self) -> None:
        self.is_active = False
        self.mode = None
        self.create_events_index = 0
        self.get_events_index = 0
        self.create_events_opt = {}
        self.get_events_opt = {}


class Calendar:
    def __init__(self) -> None:
        self.calender_chat = CalenderChat()

    def __print_events(self, events: Dict[str, any]):
        response = ""
        for event in events:
            for key, value in event.items():
                response += f'{key}:{value}'+"\n"
        return response

    def get_service(self):
        if 'credentials' not in session:
            return redirect('/auth/authorize')
        credentials = Credentials(
            **session.get("credentials"))
        service = build('calendar', 'v3', credentials=credentials)
        return service

    def get_events(self, query: List[str]):
        service = self.get_service()
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items')
        if len(events) == 0:
            return 'No message was found in your calender, please add new one'
        else:
            return self.__print_events(events)

    def create_events(self, query: List[str]):

        service = self.get_service()

        event = {
            # 'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': datetime.strptime("07/02/2023 16:00:00", "%d/%m/%Y %H:%M:%S").isoformat(),
                # 'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': datetime.strptime("07/02/2023 20:00:00", "%d/%m/%Y %H:%M:%S").isoformat(),
                # 'timeZone': 'America/Los_Angeles',
            },
        }

        res = service.events().insert(calendarId='primary', body=event).execute()
        print(res)

        return "The event was create successfully"

    def parse_message(self, content: str):
        if not content:
            return
        if "\calendar" not in content:
            return
        self.calender_chat.toggle_activation(content)

        # self.calender_chat["mode"] = True

        # if (self.calender_chat.get("mode")):
        #     pass

        # message_split = content.split("?")
        # endpoints = message_split[0]

        # query = message_split[1:] if len(message_split) > 1 else []

        # if END_POINTS.get("get_events") in endpoints:
        #     return self.get_events(query)
        # if END_POINTS.get("create_events") in endpoints:
        #     print("sss")
        #     return self.create_events(query)
