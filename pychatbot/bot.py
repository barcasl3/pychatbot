# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from quntoken import tokenize
from wit import Wit
from api_config import WIT_API_KEY
from urlmatch import matching
import intents
import json

from intents import INTENT_KOSZONTESKEZDES, INTENT_LEZARAS, INTENT_LEZARASELKOSZONES, INTENT_SZOLGALTATAS_RENDELES, INTENT_SZOLGALTATAS_INFORMACIO

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        client = Wit(WIT_API_KEY)
        resp = client.message(turn_context.activity.text)
        print(str(resp))

        best_intent = resp["intents"][0]["name"]
        confidence = resp["intents"][0]["confidence"]

        print("Megállapított szándék: " + best_intent + " (Bizonyosság: " + str(confidence) + ")")
            
        if best_intent == INTENT_KOSZONTESKEZDES:
            await turn_context.send_activity("Szia! Én a Clans.hu chatbotja vagyok. Bár készítőim rengeteg dologra megtanítottak, azonban előfordulhat, hogy valamiben nem tudok segíteni. Ilyenkor ember kollégáimhoz irányítalak majd. Miben segíthetek?")
        
        elif best_intent == INTENT_LEZARAS:
            await turn_context.send_activity("Örülök, hogy segíthettem, segíthetek még valamiben?")

        elif best_intent == INTENT_LEZARASELKOSZONES:
            await turn_context.send_activity("Örülök, hogy segíthettem. További szép napot, szia!")

        elif best_intent == INTENT_SZOLGALTATAS_INFORMACIO:
            szolgtipus = resp["entities"]["szolgaltatas_tipusa:szolgaltatas_tipusa"][0]["value"]
            if len(resp["entities"]) != 0:
                if szolgtipus == "vps":
                    eroforras = resp["entities"]["vps_eroforras:vps_eroforras"][0]["value"]
                    csomag = resp["entities"]["vps_csomag:vps_csomag"][0]["value"]
                    if len(eroforras) != 0 and len(csomag) != 0:
                        await turn_context.send_activity("A(z) " + csomag + " csomagú VPS szolgáltatásunk 1 GB " + eroforras + " erőforrással rendelkezik.")
                    elif len(eroforras) != 0 and len(csomag) == 0:
                        await turn_context.send_activity("Különböző VPS csomagjaink különböző " + eroforras + " tulajdonságokkal rendelkeznek. Kérlek kérdésedben a csomagot is add meg, amelyikre kíváncsi vagy!")
                    elif len(eroforras) == 0 and len(csomag) != 0:
                        await turn_context.send_activity("A(z) " + csomag + " csomagú VPS szolgáltatásunk részletes tulajdonságait a https://clans.hu/vps-standard oldalunkon megtekintheted.")      
                else:
                    await turn_context.send_activity("Játékszervereinkről bővebb információt az oldalunkon találsz.")
            else:
                await turn_context.send_activity("Szolgáltatásainkról bővebb információt az oldalunkon találsz.")

        elif best_intent == INTENT_SZOLGALTATAS_RENDELES:
            await turn_context.send_activity("Sajnos a megrendelések intézéséhez nem értek, így azt a weboldalunkon kell megtenned. Ne aggódj, nagyon egyszerű és gyors!")
            if len(resp["entities"]) != 0:
                szolgtipus = resp["entities"]["szolgaltatas_tipusa:szolgaltatas_tipusa"][0]["value"]
                if szolgtipus == "vps":
                    await turn_context.send_activity("A VPS szolgáltatás megrendeléséhez kérlek látogass el a https://clans.hu/vps-standard oldalunkra, ahol a megfelelő csomag kiválasztása után már indulhat is a megrendelés.")
                
                elif szolgtipus == "teamspeak 3":
                    await turn_context.send_activity("A TeamSpeak 3 szolgáltatásunk megrendeléséhez kérlek látogass el a https://clans.hu/jatekszerverek/ts3 oldalunkra.")

                elif szolgtipus == "teamspeak 3 musicbot":
                    await turn_context.send_activity("A TeamSpeak 3 Musicbot szolgáltatásunk megrendeléséhez kérlek látogass el a https://clans.hu/jatekszerverek/ts3mb oldalunkra.")
                
                else:
                    await turn_context.send_activity("Játékszervereink megrendeléséhez kérlek látogass el a https://clans.hu/jatekszerverek oldalunkra, itt kiválaszthatod és megrendelheted a számodra megfelelő játékszervert.")
            else:
                await turn_context.send_activity("Szolgáltatásaink megrendeléséhez látogass el a https://clans.hu/megrendeles oldalunkra.")
        
        #await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
