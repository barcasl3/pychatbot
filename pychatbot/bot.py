# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from quntoken import tokenize
from wit import Wit
from api_config import WIT_API_KEY
import intents
import json

from intents import INTENT_KOSZONTESKEZDES, INTENT_LEZARAS, INTENT_LEZARASELKOSZONES

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        client = Wit(WIT_API_KEY)
        resp = client.message(turn_context.activity.text)

        best_intent = resp["intents"][0]["name"]
        confidence = resp["intents"][0]["confidence"]

        print("Megállapított szándék: " + best_intent + " (Bizonyosság: " + str(confidence) + ")")
            
        if best_intent == INTENT_KOSZONTESKEZDES:
            await turn_context.send_activity("Szia! Miben segíthetek?")
        
        elif best_intent == INTENT_LEZARAS:
            await turn_context.send_activity("Örülök, hogy segíthettem, segíthetek még valamiben?")

        elif best_intent == INTENT_LEZARASELKOSZONES:
            await turn_context.send_activity("Örülök, hogy segíthettem. További szép napot, szia!")
        
        #await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
