#!/bin/python

import json
import re
import time
import traceback

class Messages:

    messages = []

    def __init__(self, jsonFile=None, preParsed=None):
        if preParsed != None:
            self.messages = preParsed
        elif jsonFile != None:
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
                            self.messages.append({
                                    'timestamp': int(event['timestamp']) // 1000000,
                                    'conversationID': conversation['conversation_id']['id'],
                                    'sender': event['sender_id']['chat_id'],
                                    'text': text
                                    })
                    except:
                        print(event)
                        traceback.print_exc()
                        return

            for message in self.messages:
                message['sender'] = senders[message['sender']]

            self.messages.sort(key = lambda message: message['timestamp'])

    def toJSON(self, jsonFile):
        json.dump(self.message, jsonFile)

    def filterTimestamp(self, start=0, end=-1):
        if start < 0:
            start = int(time.time()) - start
        if end < 0:
            end = int(time.time()) - end
        return Messages(
                preParsed=[message for message in self.messages
                    if start <= message['timestamp'] and message['timestamp'] < end]
                )

    def filterConversationID(self, regexp):
        regex = re.compile(regexp)
        return Messages(
                preParsed=[message for message in self.messages
                    if regex.match(message['conversationID'])]
                )

    def filterSender(self, regexp):
        regex = re.compile(regexp)
        return Messages(
                preParsed=[message for message in self.messages
                    if regex.match(message['sender'])]
                )

    def filterText(self, regexp):
        regex = re.compile(regexp)
        return Messages(
                preParsed=[message for message in self.messages
                    if regex.match(message['text'])]
                )

    def slice(start, end):
        return Messages(preParsed=message[start:end])

    def count(self):
        return len(self.messages)

    def prettyPrint(self):
        for message in self.messages:
            print(
                    time.ctime(message['timestamp']),
                    '|',
                    message['conversationID'],
                    '|',
                    message['sender'].rjust(20),
                    '|',
                    message['text']
                )
