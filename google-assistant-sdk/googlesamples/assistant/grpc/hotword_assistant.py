#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import json
import os.path
import time
import threading

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType


class HotwordAssistant(object):

    def __init__(self, device_model_id, creds_path=os.path.join(
        os.path.expanduser('~/.config'),
        'google-oauthlib-tool',
        'credentials.json'
    )):
        with open(creds_path, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            self.assistant = Assistant(credentials, device_model_id)

    def __enter__(self):
        return self

    def stop(self):
        self.assistant.__exit__(None, None, None)
        # self.assistant.stop_conversation()

    def assist(self):
        for event in self.assistant.start():

            if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
                print('Hotword detected')
                # Stopping in a separate thread to prevent blocking the main thread.
                threading.Thread(target=self.stop).start()
                return

            print(event)

            if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and not event.args['with_follow_on_turn']):
                print()
            if event.type == EventType.ON_DEVICE_ACTION:
                for command, params in event.actions:
                    print('Do command', command, 'with params', str(params))

                if command == "com.example.commands.BlinkLight":
                    number = int(params['number'])
                    for i in range(int(number)):
                        print('Device is blinking.')
                        time.sleep(1)

                if command == "com.example.commands.ShowImages":
                    query = params['query']
                    print('Query is ', query)


def main():
    assistant = HotwordAssistant()
    assistant.assist()


if __name__ == '__main__':
    main()
