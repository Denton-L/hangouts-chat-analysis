#!/bin/python

import json
import traceback

def parseTakeout(jsonFile):
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
                if 'chat_message' in event and 'segment' in event['chat_message']['message_content']:
                    for segment in event['chat_message']['message_content']['segment']:
                        if 'text' in segment:
                            text += segment['text']
                        elif segment['type'] == 'LINE_BREAK':
                            text += '\n'
                    messages.append({
                            'timestamp': int(event['timestamp']),
                            'conversationId': conversation['conversation_id']['id'],
                            'sender': event['sender_id']['chat_id'],
                            'text': text
                            })
            except:
                print(event)
                traceback.print_exc()
                return

    for message in messages:
        message["sender"] = senders[message["sender"]]

    messages.sort(key = lambda message: message["timestamp"])
    return messages
