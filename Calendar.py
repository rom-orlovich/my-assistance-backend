
from flask import redirect, session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from typing import List
from my_types import Message
from Event import Event
import types
END_POINTS = {

    "create_events": "\calendar\events\create",
    "get_events": "\calendar\events\get"
}


class Calendar:

    def __print_events(self, events):
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
        # if len(query) == 0:
        #     return "Please provide valid parameter."

        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': datetime.strptime("07/02/2023 16:00:00", "%d/%m/%Y %H:%M:%S").isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': datetime.strptime("07/02/2023 20:00:00", "%d/%m/%Y %H:%M:%S").isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
        }
        # build_event = Event(query).event_normalize_opt
        # print(build_event)
        res = service.events().insert(calendarId='primary', body=event).execute()
        print(res)

        return "The event was create successfully"

    def parse_message(self, content: str):

        if not content:
            return
        if "\calendar" not in content:
            return
        message_split = content.split("?")
        endpoints = message_split[0]
        print(message_split)
        query = message_split[1:] if len(message_split) > 1 else []
        print(query)
        # print(endpoints, END_POINTS.get("get_events"))
        # print(END_POINTS.get("create_events") in endpoints)
        # print(query)
        if END_POINTS.get("get_events") in endpoints:
            return self.get_events(query)
        if END_POINTS.get("create_events") in endpoints:
            print("sss")
            return self.create_events(query)
