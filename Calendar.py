
from dataclasses import dataclass
from symbol import parameters
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict, TypeVar


from my_types import Message
from sandbox.command.Command import Command, DateUtil, ParamOption, TypeOption

E = TypeVar("E", bound="Event")


@dataclass
class Event:
    start: str
    end: str
    location: str
    summary: str
    # description: str


class Calendar:
    def __init__(self) -> None:
        self.command_get_events = self.get_events_commands()
        self.command_create_events = self.create_event_commands()

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

    def create_events(self, event: Event):

        service = self.get_service()
        event = self. create_event_dict(event)
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

    def create_event_dict(self, parameters: Event):
        print(parameters)
        # timeZone = pytz.timezone("Europe/London")
        # dt = datetime.datetime.utcnow()
        # local_dt = timeZone.localize(dt, is_dst=None)
        date_util = DateUtil()

        event = {
            'summary': parameters.get("summary"),
            'location': parameters.get("location"),
            # 'description': event.description,
            'start': {
                'dateTime':  date_util.convert(parameters.get("start")).isoformat(),
                "timeZone": "Israel"},
            'end': {
                'dateTime': date_util.convert(parameters.get("end")).isoformat(),
                "timeZone": "Israel"

            },
        }

        return event

    def create_event_commands(self):
        parameters_options = {
            "$start": ParamOption("start", TypeOption("date"), "$start"),
            "$end": ParamOption("end", TypeOption("date"), "$end"),
            "$location": ParamOption("location", TypeOption("str"), "$location"),
            "$summary": ParamOption("summary", TypeOption("str"), "$summary")
        }
        command = Command(self.create_events, parameters_options)
        command.add_command(
            "please add a new event that its summary is $summary. The event will begin in $start and end in $end and his location will place in $location")
        command.add_command(
            "please create a new event that will start in $start and end in $end and will place in $location")

        return command

    def parse_message(self, content: str):
        if not content:
            return

        res = self.command_get_events.execute(content)
        res = self.command_create_events.execute(content)
        return res
