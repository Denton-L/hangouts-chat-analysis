#!/bin/python

import json

def parseTakeout(jsonFile):
    messages = []
    parsed = json.load(jsonFile)
    for conversation in parsed["conversation_state"]:
        senders = {i["id"]["chat_id"]: i["fallback_name"] for i in conversation["conversation_state"]["participant_data"]}
        for event in parsed["conversation_state"]["event"]:
            text = ""
            for segment in event["chat_message"]["message_content"]["segment"]:
                text += segment["text"]
            messages.append({
                    "timestamp": int(event["timestamp"]),
                    "sender": senders[event["self_event_state"]["user_id"]["chat_id"]],
                    "text": text
                    })
    return messages
