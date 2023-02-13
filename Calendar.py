
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict, TypeVar
from sandbox.CalenderChat import CalenderChat

from my_types import Message
from sandbox.Event import Event
import types

from enum import Enum


class Calendar:
    def __init__(self) -> None:
        self.chat_manager = CalenderChat()

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

    def manage_commands(self, content: str, query: TypeVar("T", dict)):
        if "/events/get/submit" in content:
            return self.get_events(query)
        elif "/events/create/submit" in content:
            return self.create_events(query)

    def parse_message(self, content: str):
        if not content:
            return
        if "\calendar" not in content:
            return
        # if self.chat_manager.manage_commands(content):
        #     pass
        # conversation = self.chat_manager.conversation()
        # if conversation:
        #     return conversation
        # results = self.chat_manager.submit_results()
        # if results:
        #     pass

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
