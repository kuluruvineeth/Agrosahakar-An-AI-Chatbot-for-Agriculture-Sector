# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests


class ActionCheckPrice(Action):

    def name(self) -> Text:
        return "action_get_price"

    def run(self, dispatcher, tracker, domain):
        api_key = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b'
        loc = tracker.get_slot('location')
        current = requests.get('https://api.data.gov.in/resource/6e8e9a24-491d-4bcb-bdf4-bb0724cbb926?api-key={}&format=json&offset=0&limit=100&filters[state_ut]={}'.format(api_key,loc))

        print(current)
        msp_1=current.json()['records'][0]['kms_2016_17']
        msp_2=current.json()['records'][0]['kms_2017_18']
        msp_3=current.json()['records'][0]['kms_2018_19_']

        yr1=current.json()['field'][1]['name']
        yr2=current.json()['field'][2]['name']
        yr3=current.json()['field'][3]['name']

        response = """The msp for rice in the year {} was {}  \n The msp of rice in the year {} was {} \n The msp for rice in the year {} was {}  """.format(yr1, msp_1, yr2,msp_2, yr3,msp_3)
        dispatcher.utter_message(text=response)
        return []






