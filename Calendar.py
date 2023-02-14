
from dataclasses import dataclass
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict, TypeVar


from my_types import Message
from sandbox.command.Command import Command, ParamOption

E = TypeVar("E", bound="Event")


@dataclass
class Event:
    start: str
    end: str
    location: str
    description: str


class Calendar:
    def __init__(self) -> None:
        self.command_get_events = self.get_events_commands()

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

    def get_events(self):

        service = self.get_service()
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items')
        if len(events) == 0:
            return 'No message was found in your calender, please add new one'
        else:
            print(events[0])
            return self.__print_events(events)

    def create_events(self, event: E):

        service = self.get_service()

        event = {
            # 'summary': 'Google I/O 2015',
            'location': event.description,
            'description': event.description,
            'start': {
                'dateTime': datetime.strptime(event.start, "%d/%m/%Y-%H:%M:%S").isoformat(),

            },
            'end': {
                'dateTime': datetime.strptime(event.end, "%d/%m/%Y %H:%M:%S").isoformat(),

            },
        }

        res = service.events().insert(calendarId='primary', body=event).execute()
        print(res)

        return "The event was create successfully"

    def get_events_commands(self):
        command = Command(self.get_events)
        command.add_command("when is my next event?")
        command.add_command("when is my nearest event?")
        command.add_command("when is my closet event?")
        command.add_command("when's my closet event?")
        command.add_command("what's my next event?")
        command.add_command("whats my next event?")

        return command

    def create_event_commands(self):
        command = Command(self.get_events)
        command.add_command(
            "please add event on $1 at $2 until $3. The event will place in $4. The description is $5.",
            {"$1": ParamOption(type="date", field_name="date", until="at")},
            {"$2": ParamOption(type="date",
                               field_name="date", until="until")},
            {"$3": ParamOption(
                type="date", field_name="date", until="the")},
            {"$4": ParamOption(type="str",
                               field_name="location", until="the")},
            {"$5": ParamOption(type="str",
                               field_name="description", until="end")},

        )

        return command

    def parse_message(self, content: str):
        if not content:
            return

        return self.command_get_events.execute(content)
