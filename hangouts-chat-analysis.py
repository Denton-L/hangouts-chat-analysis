#!/bin/python

import itertools
import json
import re
import time
import traceback

def convertHangoutsJSON(jsonFile):
    messages = []
    senders = {}
    parsed = json.load(jsonFile)
    for conversation in parsed['conversation_state']:
        for person in conversation['conversation_state']['conversation']['participant_data']:
            if 'fallback_name' in person:
                senders[person['id']['chat_id']] = person['fallback_name']
            elif not person['id']['chat_id'] in senders:
                senders[person['id']['chat_id']] = person['id']['chat_id']

        for event in conversation['conversation_state']['event']:
            try:
                text = ''
                if ('chat_message' in event
                    and 'segment' in event['chat_message']['message_content']):

                    for segment in event['chat_message']['message_content']['segment']:
                        if 'text' in segment:
                            text += segment['text']
                        elif segment['type'] == 'LINE_BREAK':
                            text += '\n'
                    messages.append({
                            'timestamp': int(event['timestamp']) // 1000000,
                            'conversationID': conversation['conversation_id']['id'],
                            'sender': event['sender_id']['chat_id'],
                            'text': text
                            })
            except:
                print(event)
                traceback.print_exc()
                return

    for message in messages:
        message['sender'] = senders[message['sender']]

    messages.sort(key = lambda message: message['timestamp'])
    return messages

class Filter:

    def __init__(self, messages):
        self.iterator = iter(messages)

    def filterTimestamp(self, start=0, end=-1):
        if start < 0:
            start = int(time.time()) - start
        if end < 0:
            end = int(time.time()) - end
        self.iterator = filter(lambda message: start <= message['timestamp'] and message['timestamp'] < end, self.iterator)
        return self


    def filterConversationID(self, regexp):
        regex = re.compile(regexp)
        self.iterator = filter(lambda message: regex.match(message['conversationID']), self.iterator)
        return self

    def filterSender(self, regexp):
        regex = re.compile(regexp)
        self.iterator = filter(lambda message: regex.match(message['sender']), self.iterator)
        return self

    def filterText(self, regexp):
        regex = re.compile(regexp)
        self.iterator = filter(lambda message: regex.match(message['text']), self.iterator)
        return self

    def slice(self, start, end):
        self.iterator = itertools.islice(self.iterator, start, end)
        return self

    def count(self):
        return sum(1 for message in self.iterator)

    def print(self):
        for message in self.iterator:
            print(
                    time.ctime(message['timestamp']),
                    '|',
                    message['conversationID'],
                    '|',
                    message['sender'].rjust(20),
                    '|',
                    message['text']
                )
