import requests
import pandas as pd
import json
import os
import traceback
from openpyxl import Workbook, load_workbook


# from miscellaneous import *


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method):
        self.headers[
            'embibe-token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTI4IDA3OjUzOjMyIFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.xGxczE-WOkmwPf85UQ3rSDKzuJCGkm793XK9wvU3EprMbgyfR9ybPgsYxBn22ujMEj7KA4l2wTDCWnbRb4ijng'
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, df):
        df1 = pd.read_csv("Prerequisite_home.csv")
        for ind in df.index:
            # if df["Exam"][ind] == "11th CBSE":
                # break

                learnmap_id = df["Learnmap_id"][ind]
                print("GETTING ALL PREREQUISITE FOR THIS LEARN PATH FROM HOME : ",learnmap_id,".......")
                format_refrence = df["Format_refrence"][ind]
                subject = df["Subject_tagged"][ind]
                try:
                    payload = {
                        'learnmap_id': learnmap_id,
                        'subject': subject

                    }
                    response1 = self.callAPI(
                        "https://preprodms.embibe.com/fiber_ms/chapter/prerequisites",
                        json.dumps(payload), 'POST')
                    # print(response1)
                    # print(response1.json())
                    print("\nGETTING TOPIC TITLE FOR ABOVE LEARN PATH  :\n")
                    # print(response1.json())
                    for item in response1.json():

                        title = item["title"]
                        print("TITLE: ",title)
                        concept_count = item["concept_count"]
                        learnpath_name = item["learnpath_name"]
                        df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                             df["Grade"][ind], df["Learnpath_name"][ind], title,
                                             format_refrence, learnpath_name,
                                             concept_count]
                        df1.to_csv("Prerequisite_home.csv", index=False)
                except Exception as e:
                    print(traceback.format_exc())
                    df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                         df["Grade"][ind], df["Learnpath_name"][ind], "", format_refrence, "", ""]

                    df1.to_csv("Prerequisite_home.csv", index=False)

            # else:
            #     continue


def prerequisite_home(df):
    src = Source()
    df1 = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade", "main_learnpath",
                                'Title', 'Format_refrence'
        , 'Topic_learnpath_name', "Concept_count"])
    df1.to_csv("Prerequisite_home.csv", index=False)

    src.main(df)

#
# df = pd.read_csv("positive_learn_results.csv")
# prerequisite_home(df)

# return_correct_sequence("6th CBSE", "CBSE")
