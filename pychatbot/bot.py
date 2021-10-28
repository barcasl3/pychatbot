# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from quntoken import tokenize
from emmorphpy import EmMorphPy
from purepospy import PurePOS

m = EmMorphPy()
p = PurePOS('/home/barcasl3/Downloads/emmorphpy-master/purepospy/purepospy/szeged.model')


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        szavak = []
        i = 0
        for tok in tokenize(turn_context.activity.text):
            szavak.append(tok.split('\t')[0])
            i += 1
        
        tokenized = ' '.join(szavak)
        print(tokenized)

        tagged = p.tag_sentence(tokenized)
        print(list(tagged))
            
        
        await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
