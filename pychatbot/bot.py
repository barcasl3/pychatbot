# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from wit import Wit
from api_config import WIT_API_KEY
from urlmatch import matching
import re
import random

from intents import INTENT_KOSZONTESKEZDES, INTENT_LEZARAS, INTENT_LEZARASELKOSZONES, INTENT_SZOLGALTATAS_RENDELES, INTENT_SZOLGALTATAS_INFORMACIO, INTENT_SZOLGALTATAS_AR, INTENT_NINCS
from database import get_szolgaltatas_ar, get_vps_ar, get_vps_adatok
import sablonok

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        client = Wit(WIT_API_KEY)
        resp = client.message(turn_context.activity.text)
        print(str(resp))

        best_intent = resp["intents"][0]["name"] if len(resp["intents"]) > 0 else "nincs"
        confidence = resp["intents"][0]["confidence"] if len(resp["intents"]) > 0 else -1.0

        print("Megállapított szándék: " + best_intent + " (Bizonyosság: " + str(confidence) + ")")
            
        if best_intent == INTENT_KOSZONTESKEZDES:
            await turn_context.send_activity(sablonok.koszontes[random.randint(0, len(sablonok.koszontes) - 1)])
        
        elif best_intent == INTENT_LEZARAS:
            await turn_context.send_activity(sablonok.koszontes[random.randint(0, len(sablonok.lezaras) - 1)])

        elif best_intent == INTENT_LEZARASELKOSZONES:
            await turn_context.send_activity(sablonok.lezaras_elkoszones[random.randint(0, len(sablonok.lezaras_elkoszones) - 1)])

        elif best_intent == INTENT_SZOLGALTATAS_INFORMACIO:
            szolgtipus = resp["entities"]["szolgaltatas_tipusa:szolgaltatas_tipusa"][0]["value"]
            if len(resp["entities"]) != 0:
                if szolgtipus == "vps":
                    #eroforras = resp["entities"]["vps_eroforras:vps_eroforras"][0]["value"]
                    csomag = resp["entities"]["vps_csomag:vps_csomag"][0]["value"] if "vps_csomag:vps_csomag" in resp["entities"] else "S"
                    vps_adatok = get_vps_adatok(csomag)
                    if vps_adatok['csomag_ara'] != -1:
                        await turn_context.send_activity(sablonok.szolginfo_vps[random.randint(0, len(sablonok.szolginfo_vps) - 1)].format(csomag, str(vps_adatok['vcpu_magok']), str(vps_adatok['ram']), str(vps_adatok['ssd']), str(vps_adatok['ipv4'])))
                        #await turn_context.send_activity("A VPS szolgáltatásunk " + csomag + " csomagja " + str(vps_adatok['vcpu_magok']) + " db vCPU maggal, " + str(vps_adatok['ram']) + " GB RAM-mal, " + str(vps_adatok['ssd']) + " GB nVME alapú SSD-tárhellyel és " + str(vps_adatok['ipv4']) + " db IPv4 címmel rendelkezik. Ezen felül minden VPS szerver tulajdonosa korlátlan adatforgalommal gazdálkodhat, a maximum 100/100 Mbps sávszélességű internetkapcsolatunkon. Lehetőség van saját ISO használatára is, de elérhető minden népszerűbb operációs rendszer. Szervereink DDoS védettek, így egy esetleges támadástól sem kell tartanod!")
                    else:
                        await turn_context.send_activity("Sajnos nem minden részletét sikerült felismernem a kérésednek. A VPS szolgáltatásaink részletes leírását megtekintheted a https://clans.hu/vps-standard oldalunkon.")
                    #if len(eroforras) != 0 and len(csomag) != 0:
                    #    await turn_context.send_activity("A VPS szolgáltatásunk " + csomag + " csomagja " GB " + eroforras + " erőforrással rendelkezik.")
                    #elif len(eroforras) != 0 and len(csomag) == 0:
                    #    await turn_context.send_activity("Különböző VPS csomagjaink különböző " + eroforras + " tulajdonságokkal rendelkeznek. Kérlek kérdésedben a csomagot is add meg, amelyikre kíváncsi vagy!")
                    #elif len(eroforras) == 0 and len(csomag) != 0:
                    #    await turn_context.send_activity("A(z) " + csomag + " csomagú VPS szolgáltatásunk részletes tulajdonságait a https://clans.hu/vps-standard oldalunkon megtekintheted.")      
                else:
                    rovidites = matching[szolgtipus] if szolgtipus in matching else ""
                    await turn_context.send_activity("Erről a játékszerverről bővebb információt a https://clans.hu/jatekszerverek/" + rovidites + " oldalunkon találsz.")
            else:
                await turn_context.send_activity("Sajnos nem sikerült megállapítanom, hogy pontosan melyik szolgáltatásunk iránt érdeklődsz. Próbáld újra, vagy tekintsd meg szolgáltatásainkat a weboldalunkon: https://www.clans.hu")

        elif best_intent == INTENT_SZOLGALTATAS_RENDELES:
            await turn_context.send_activity("Sajnos a megrendelések intézéséhez nem értek, így azt a weboldalunkon kell megtenned. Ne aggódj, nagyon egyszerű és gyors!")
            if len(resp["entities"]) != 0:
                szolgtipus = resp["entities"]["szolgaltatas_tipusa:szolgaltatas_tipusa"][0]["value"]
                if szolgtipus == "vps":
                    await turn_context.send_activity("A VPS szolgáltatás megrendeléséhez kérlek látogass el a https://clans.hu/vps-standard oldalunkra, ahol a megfelelő csomag kiválasztása után már indulhat is a megrendelés.")
                else:
                    rovidites = matching[szolgtipus] if szolgtipus in matching else ""
                    await turn_context.send_activity("A szolgáltatás megrendeléséhez kérlek látogass el a https://clans.hu/jatekszerverek/" + rovidites + " oldalunkra.")
            else:
                await turn_context.send_activity("Szolgáltatásaink megrendeléséhez látogass el a https://clans.hu/megrendeles oldalunkra.")
        
        elif best_intent == INTENT_SZOLGALTATAS_AR:
            if len(resp["entities"]) != 0:
                szolgtipus = resp["entities"]["szolgaltatas_tipusa:szolgaltatas_tipusa"][0]["value"]
                szolghosszkifejezes = resp["entities"]["szolgaltatas_hossza:szolgaltatas_hossza"][0]["value"] if "szolgaltatas_hossza:szolgaltatas_hossza" in resp["entities"] else "1 hónap"
                szolghossz = re.search("\d+", szolghosszkifejezes).group()
                slotkifejezes = re.search("\d+ (slot|férőhely|férő|hely)", turn_context.activity.text)
                szolgmeret = -1
                if(slotkifejezes != None):
                    szolgmeret = re.search("\d+", slotkifejezes.group()).group()
                if szolgtipus != "vps":
                    szolgaltatas_ara = get_szolgaltatas_ar(matching[szolgtipus] if szolgtipus in matching else "", int(szolghossz), int(szolgmeret))
                    ar_valid = True if szolgaltatas_ara != -1 else False
                    if(ar_valid):
                        await turn_context.send_activity(sablonok.szolgar_mindenmas[random.randint(0, len(sablonok.szolgar_mindenmas) - 1)].format(szolgmeret, szolgtipus, szolghossz, str(szolgaltatas_ara)))
                        #await turn_context.send_activity("Egy " + szolgmeret + " férőhelyes " + szolgtipus + " szolgáltatás " + szolghossz + " hónapra " + str(szolgaltatas_ara) + " Ft-ba kerül.")
                    else:
                        await turn_context.send_activity("Sajnálom, de nem sikerült felismernem minden részletet ahhoz, hogy meghatározzam az általad kért árat. Próbáld meg újra másképpen, vagy ellenőrizd az árainkat a www.clans.hu/jatekszerverek oldalunkon.")
                else:
                    vps_csomag = resp["entities"]["vps_csomag:vps_csomag"][0]["value"] if "vps_csomag:vps_csomag" in resp["entities"] else "S"
                    vps_ara = get_vps_ar(vps_csomag)

                    if(vps_ara != -1):
                        await turn_context.send_activity(sablonok.szolgar_vps[random.randint(0, len(sablonok.szolgar_vps) - 1)].format(vps_csomag, str(vps_ara)))
                        #await turn_context.send_activity("Egy " + vps_csomag + " csomagú VPS szolgáltatás ára havonta " + str(vps_ara) + " Ft.")
                    else:
                        await turn_context.send_activity("Sajnálom, de nem sikerült felismernem minden részletet ahhoz, hogy meghatározzam az általad kért árat. Próbáld meg újra másképpen, vagy ellenőrizd az árainkat a www.clans.hu/vps-standard oldalunkon.")
            else:
                await turn_context.send_activity("Sajnos nem sikerült megállapítanom, hogy milyen szolgáltatás árával kapcsolatban érdeklődsz. Kérlek, próbáld újra, vagy tekintsd meg árainkat a weboldalunkon!")
        #await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        elif best_intent == INTENT_NINCS:
            await turn_context.send_activity("Ebben a kérdésben sajnos nem tudok segíteni. Ha van már előfizetésed, kérlek látogass el Ügyféltámogatási felületünkre, ahol munkatársaim készséggel a rendelkezésedre állnak: https://webadmin.clans.hu/index.php?module=ugyfeltamogatas Ha még nincs előfizetésed, kérlek írj egy e-mailt az info@clans.hu címre, és segítünk!")

    # async def on_members_added_activity(
    #     self,
    #     members_added: ChannelAccount,
    #     turn_context: TurnContext
    # ):
    #     for member_added in members_added:
    #         if member_added.id != turn_context.activity.recipient.id:
    #             await turn_context.send_activity("Hello and welcome!")
