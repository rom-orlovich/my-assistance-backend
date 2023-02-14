
from dataclasses import dataclass
from symbol import parameters
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict
from lib.date_utils import DateUtils


from services.chat.lib.chat_types import Event
from services.chat.lib.command import Command, ParamOption


class Calendar:
    def __init__(self) -> None:
        self.command_get_closet_event = self.get_my_closet_event()
        self.command_create_events = self.create_event_commands()
        self.date_util = DateUtils()

    def get_date_event(self, event, type: str):
        date_dict = (event.get(type))
        date_str = date_dict.get("dateTime")
        return date_str

    def create_event_dict(self, parameters: Event):
        date_util = DateUtils()
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

    def get_service(self):
        if 'credentials' not in session:
            return redirect('/auth/authorize')
        credentials = Credentials(
            **session.get("credentials"))
        service = build('calendar', 'v3', credentials=credentials)
        return service

    def create_events(self, event: Event):
        service = self.get_service()
        event = self. create_event_dict(event)
        res = service.events().insert(calendarId='primary', body=event).execute()
        return "The event was create successfully"

    def create_event_commands(self):
        parameters_options = {
            "$start": ParamOption("start", "$start"),
            "$end": ParamOption("end", "$end"),
            "$location": ParamOption("location", "$location"),
            "$summary": ParamOption("summary", "$summary")
        }

        command = Command(self.create_events, parameters_options)
        command.add_command(
            "please add a new event that its summary is $summary. The event will begin on $start and end on $end and his location will place in $location")
        command.add_command(
            "please create a new event that will start on $start and end on $end and will place in $location")
        return command

    def get_events(self):
        service = self.get_service()
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items')
        if len(events) == 0:
            return []
        else:

            return events

    def get_closet_event(self):
        events = self.get_events()

        if len(events):
            event = events[0]
            start_date, start_time = self.date_util.get_date_and_time(
                self.get_date_event(event, "start"))
            end_date, end_time = self.date_util.get_date_and_time(
                self.get_date_event(event, "end"))

            return f'Your next event is on {start_date} at {start_time} and end on {end_date} at {end_time}'
        else:
            return "No event was found"

    def get_my_closet_event(self):
        command = Command(self.get_closet_event)
        command.add_command("when is my next event?")
        command.add_command("when is my nearest event?")
        command.add_command("when is my closet event?")
        command.add_command("when's my closet event?")
        command.add_command("what's my next event?")
        command.add_command("what is my next event?")
        command.add_command("whats my next event?")
        return command

    def parse_message(self, content: str):
        if not content:
            return

        res = self.command_get_closet_event.execute(content)
        if res:
            return res

        res = self.command_create_events.execute(content)
        if res:
            return res
        return None


# calendar = Calendar()
