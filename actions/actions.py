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

from typing import Any, Text, Dict, List,Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import EventType
from utils.fertilizer import fertilizer_dic
import pickle
import os
import time
import pandas as pd
import numpy as np
from tabulate import tabulate

import requests
import subprocess
from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player

# from excel_data import DataStore

crop_recommendation_model_path = 'RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = 'b8e63e97d870d37437a1bf6a70f3de3f'
    current=requests.get("http://api.openweathermap.org/data/2.5/weather?appid={}&q={}".format(api_key,city_name))

    temperature=current.json()['main']['humidity']
    humidity=current.json()['main']['temp']





    temperature = round((temperature - 273.15), 2)
    return temperature, humidity



# class ActionSaveData(Action):
#     def name(self) -> Text:
#         return "action_save_data"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         DataStore(tracker.get_slot("nitrogen"),
#             tracker.get_slot("phosphorous"),
#             tracker.get_slot("potassium"),
#             tracker.get_slot("crop"))
#         dispatcher.utter_message(text="Data noted")

#         return []





class ActionCheckPrice(Action):

    def name(self) -> Text:
        return "action_get_price"

    def run(self, dispatcher, tracker, domain):
        crop = tracker.get_slot('crop')
        print(crop)
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

            table_rice = [["Rice",msp_1,yr1],["Rice",msp_2,yr2],["Rice",msp_3,yr3]]
            header_rice=[" Crop"," Procurement(as per KMS) "," Year "]
            response=tabulate(table_rice, header_rice, tablefmt="plain")




            





            dispatcher.utter_message(text=response)
            language = 'en'
            audio = gTTS(text=response, lang=language, slow=False)
            audio.save("rice.mp3")
            os.system("rice.mp3")
            time.sleep(18000)

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
        language = 'en'
        audio = gTTS(text=response, lang=language, slow=False)
        audio.save("anything.mp3")
        os.system("anything.mp3")
        time.sleep(34000)   

        return []


# class FertilizerRecommendation(FormAction):
#     def name(self) -> Text:
#         return "fertilizer_info"
#     @staticmethod
#     def required_slots(tracker: "Tracker") -> List[Text]:
#         return ["nitrogen","phosphorous","potassium","crop"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
#         return {
#         "nitrogen":[self.from_text()],
#         "phosphorous":[self.from_text()],
#         "potassium":[self.from_text()],
#         "crop":[self.from_text()]
#         }

#     def submit(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text, Any],
#     ) -> List[EventType]:

#         dispatcher.utter_message("Here are the information that you provided.\nNitrogen: {0},\nPhosphorous: {1},\nPotassium: {2},\ncrop: {3}".format(
#         tracker.get_slot("nitrogen"),
#         tracker.get_slot("phosphorous"),
#         tracker.get_slot("potassium"),
#         tracker.get_slot("crop")
#         ))
#         return []

class ActionFertilizerRecommendation(Action):
    def name(self) -> Text:
        return "action_ferti_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        crop_name = tracker.get_slot('crop')
        N = tracker.get_slot('nitrogen')
        P = tracker.get_slot('phosphorous')
        K = tracker.get_slot('potassium')
        print(crop_name)
        N1 = N.split("_", 1)
        print(int(N1[1]))
        P1 = P.split("_", 1)
        print(int(P1[1]))
        K1 = K.split("_", 1)
        print(int(K1[1]))
        # ph = float(request.form['ph'])

        df = pd.read_csv('fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - int(N1[1])
        p = pr - int(P1[1])
        k = kr - int(K1[1])
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

        response = (fertilizer_dic[key])
        dispatcher.utter_message(text=response)

        

        return []


class ActionCropRecommendation(Action):
    def name(self) -> Text:
        return "action_crop_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        crop_name = tracker.get_slot('crop')
        N = tracker.get_slot('nitrogen')
        P = tracker.get_slot('phosphorous')
        K = tracker.get_slot('potassium')
        print(crop_name)
        N1 = N.split("_", 1)
        print(int(N1[1]))
        P1 = P.split("_", 1)
        print(int(P1[1]))
        K1 = K.split("_", 1)
        print(int(K1[1]))
        # ph = float(request.form['ph'])

        ph = tracker.get_slot('ph')
        rainfall = tracker.get_slot('rainfall')
        ph1 = ph.split("_", 1)
        print(float(ph1[1]))
        rainfall1 = rainfall.split("_", 1)
        print(float(rainfall1[1]))


        city = tracker.get_slot("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            print(temperature)
            print(humidity)
            data = np.array([[int(N1[1]), int(P1[1]), int(K1[1]), temperature, humidity, float(ph1[1]), float(rainfall1[1])]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            print(final_prediction)



        response = """The crop recommended to grow according to our prediction is {}""".format(final_prediction)


        
        dispatcher.utter_message(text=response)

        

        return []














        






