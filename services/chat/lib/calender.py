

from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

from lib.date_utils import DateUtils


from services.chat.lib.chat_types import Event
from services.chat.lib.command import Command, ParamOption


class Calendar:
    """
       Calender is class that manage the calender operations of the user.
       The operations execute by various predefined commands.    
    """

    def __init__(self) -> None:
        self.command_get_closet_event = self.get_my_closet_event()
        self.command_create_events = self.create_event_commands()
        self.date_util = DateUtils()

    # Extract the date value from the event calender api response.
    def get_date_event(self, event, type: str):
        date_dict = (event.get(type))
        date_str = date_dict.get("dateTime")
        return date_str

    # Transform the event parameters to match the current form of the calender's create event request.
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
        """
        Extract the login user's credentials from the session.
        The service use them in order to access to calender api. 
        """
        if 'credentials' not in session:
            return redirect('/auth/authorize')
        credentials = Credentials(
            **session.get("credentials"))
        service = build('calendar', 'v3', credentials=credentials)
        return service

    # A query to create a new event in the user's calender.
    def create_event(self, event: Event):
        service = self.get_service()
        event = self. create_event_dict(event)
        res = service.events().insert(calendarId='primary', body=event).execute()
        return "The event was create successfully"

   # Initial the command instance with sentences and parameter that will execute the     create_event method.
    def create_event_commands(self):
        parameters_options = {
            "$start": ParamOption("start", "$start"),
            "$end": ParamOption("end", "$end"),
            "$location": ParamOption("location", "$location"),
            "$summary": ParamOption("summary", "$summary")
        }
        commands = ["please add a new event that its summary is $summary. The event will begin on $start and end on $end and his location will place in $location",
                    "please create a new event that will start on $start and end on $end and will place in $location",
                    "add a new event that will begin on $start and end on $end and his summary is $summary",
                    "a $summary on $start - $end in $location"
                    ]
        command = Command(self.create_event, parameters_options)
        command.add_commands(commands)
        return command

    # A query to get event from the user's calender.
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

    # Extract from the events the first event which is the nearest event.
    # Return a message that describe when the event will happen.
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
            return "No event was found."

    # Initial the command instance with sentences and parameter that will execute the     get_closet_event method.
    def get_my_closet_event(self):
        command = Command(self.get_closet_event)
        commands = ["when is my next event?", "when is my nearest event?",
                    "when is my closet event?",
                    "when's my closet event?",
                    "what's my next event?",
                    "what is my next event?",
                    "whats my next event?"]
        command.add_commands(commands)
        return command

  # Parse message and execute the command.
  # If the execution was successful, return the result.
    def parse_message(self, content: str):
        if not content:
            return
        result = self.command_get_closet_event.execute(content)
        if result:
            return result
        result = self.command_create_events.execute(content)
        if result:
            return result
        return None
