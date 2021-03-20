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
        crop = tracker.get_slot('crop')
        api_key = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b'
        loc = tracker.get_slot('location')
        
        
        if (crop=='rice'):
            current = requests.get('https://api.data.gov.in/resource/6e8e9a24-491d-4bcb-bdf4-bb0724cbb926?api-key={}&format=json&offset=0&limit=100&filters[state_ut]={}'.format(api_key,loc))
            print(current)
            msp_1=current.json()['records'][0]['kms_2016_17']
            msp_2=current.json()['records'][0]['kms_2017_18']
            msp_3=current.json()['records'][0]['kms_2018_19_']

            yr1=current.json()['field'][1]['name']
            yr2=current.json()['field'][2]['name']
            yr3=current.json()['field'][3]['name']

            response = """The msp for {} in the year {} was {}  \n The msp of {} in the year {} was {} \n The msp for {} in the year {} was {}  """.format(crop,yr1, msp_1,crop, yr2,msp_2,crop, yr3,msp_3)
            dispatcher.utter_message(text=response)
            return []

        elif (crop=='cotton'):
            current = requests.get('https://api.data.gov.in/resource/2962ee1b-4554-4c38-a8a7-953ecfeeb438?api-key={}&format=json&offset=0&limit=10&filters[state]={}'.format(api_key,loc))
            print(current)

            cmsp_11=current.json()['records'][0]['_2017_18___prod__as_per_cab_meeting_dt__18_6_19__qty__in_lakh_bales_']
            cmsp_12=current.json()['records'][0]['_2017_18___cci_purchases_under_msp__qty__in_lakh_bales_']
            cmsp_21=current.json()['records'][0]['prod__as_per_cab_meeting_dt__18_6_19__qty__in_lakh_bales_']
            cmsp_22=current.json()['records'][0]['_2018_19____cci_purchases_under_msp__qty__in_lakh_bales_']

            cyr1=current.json()['field'][3]['id']
            cyr2=current.json()['field'][7]['id']

            response = """The msp for {} in the year {} as per cab was {}  \n The msp for {} in the year {} as per cci was {} \n The msp for {} in the year {} as per cab was {}  \n The msp for {} in the year {} as per cci was {}""".format(crop,cyr1, cmsp_11,crop,cyr1,cmsp_12,crop,cyr2,cmsp_21,crop,cyr2,cmsp_22)
            dispatcher.utter_message(text=response)
            return []

        elif (crop=='jute'):
            current = requests.get('https://api.data.gov.in/resource/d6faf37c-13f3-4d9c-b06f-49e97ed9348e?api-key={}&format=json&offset=0&limit=10&filters[state]={}'.format(api_key,loc))
            print(current)

            jq1=current.json()['field'][1]['name']
            jm1=current.json()['field'][2]['name']
            jq2=current.json()['field'][3]['name']
            jm2=current.json()['field'][4]['name']


            jqty1=current.json()['records'][0]['crop_year_2017_18___quantity_procured_under_msp']
            jmsp1=current.json()['records'][0]['crop_year_2017_18___amount_disbursed']
            jqty2=current.json()['records'][0]['crop_year_2018_19___quantity_procured_under_msp']
            jmsp2=current.json()['records'][0]['crop_year_2018_19___amount_disbursed']

            response = """{} was {}  \n {} was {} \n {} was {} \n {} was {}""".format(jq1, jqty1,jm1,jmsp1, jq2,jqty2,jm2,jmsp2)

            dispatcher.utter_message(text=response)
            return[]


    
class ActionFertilizerConsumption(Action):

     def name(self) -> Text:
         return "action_get_fertilizers"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        loc = tracker.get_slot('location')
        api_key = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b'

        current = requests.get('https://api.data.gov.in/resource/1a800a9a-7c6e-42ba-b238-6ae1c17d5195?api-key={}&format=json&offset=0&limit=10&filters[state_u_t_]={}'.format(api_key,loc))
        print(current)

        fur=current.json()['records'][0]['urea']
        fdap=current.json()['records'][0]['dap']
        fmop=current.json()['records'][0]['mop']
        fcomplex=current.json()['records'][0]['complex']
        fssp=current.json()['records'][0]['ssp']
        ftot=current.json()['records'][0]['_total']

        response='''The urea used in {} in the year 2016-17 was {} \n The diammonium phosphate used in {} in the year 2016-17 was {} \n The potassium chloride used in {} in the year 2016-17 was {} \n The complex fertilizers used in {} in the year 2016-17 was {} \n The single superphosphate used in {} in the year 2016-17 was {} \n The total fertilizers used in {} in the year 2016-17 was {}'''.format(loc,fur,loc,fdap,loc,fmop,loc,fcomplex,loc,fssp,loc,ftot)







        dispatcher.utter_message(text=response)

        return []











        






