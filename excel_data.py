import pandas as pd
import os
def DataStore(name,mobile_number,land,quantity,aadharno):
    if os.path.isfile("user_data.xlsx"):
        df=pd.read_excel("user_data.xlsx")
        df=df.append(pd.DataFrame([[name,mobile_number,land,quantity,aadharno]],
            columns=["name","mobile_number","land_area","quantity_alloted","aadhar_no"]))
        df.to_excel("user_data.xlsx",index=False)
    else:
        df=pd.DataFrame([[name,mobile_number,land,quantity,aadharno]],
        columns=["name","mobile_number","land_area","quantity_alloted","aadhar_no"])
        df.to_excel("user_data.xlsx",index=False)
        return []

