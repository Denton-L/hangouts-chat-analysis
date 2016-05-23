#!/bin/python

import json

def parseTakeout(jsonFile):
    messages = []
    parsed = json.load(jsonFile)
    for conversation in parsed['conversation_state']:
        senders = {
                i['id']['chat_id']:
                    i['fallback_name'] if 'fallback_name' in i else i['id']['chat_id']
                for i in conversation['conversation_state']['conversation']['participant_data']
                }
        for event in conversation['conversation_state']['event']:
            try:
                text = ''
                if 'chat_message' in event and 'segment' in event['chat_message']['message_content']:
                    for segment in event['chat_message']['message_content']['segment']:
                        if 'text' in segment:
                            text += segment['text']
                        elif segment['type'] == 'LINE_BREAK':
                            text += '\n'
                        else:
                            print(segment)
                    messages.append({
                            'timestamp': int(event['timestamp']),
                            'conversationId': conversation['conversation_id']['id'],
                            'sender': senders[event['self_event_state']['user_id']['chat_id']],
                            'text': text
                            })
            except:
                print(event)
                return
    return messages
