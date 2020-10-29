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
            'embibe-token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.QYI2fB25BRp4c8KNkHIKSOSYLvxARKIDGxJXstk5OMqmlZiQ-E2kult1tDHHKP7eNtNnh4-upBdjmFQeM8CkVw'
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, df):
        df1 = pd.read_csv("Embibe_explainers_videos_home.csv")
        for ind in df.index:
            # if df["Exam"][ind] == "11th CBSE":
                # break

                learnmap_id = df["Learnmap_id"][ind]
                # format_refrence = df["Format_refrence"][ind]
                print(df["Exam"][ind],"\t\t",df["Goal"][ind],"\t\t",df["Learnmap_id"][ind],"\n")
                try:
                    response1 = self.callAPI(
                        "https://preprodms.embibe.com/fiber_ms/v1/chapters/learning-objects?&learnMapId=" + str(
                            learnmap_id) + "&contentTypes=Video",
                        '{}', 'GET')
                    # print(response1)
                    # print(response1.json())
                    for item in response1.json():
                        if item["sectionName"] == "EMBIBE EXPLAINERS":
                            for item in item["sections"]:
                                for item in item["content"]:
                                    id = item["id"]
                                    title = item["title"]
                                    format_refrence = item["learning_map"]["format_reference"]
                                    print(title)
                                    topic_learnpath_name = item["learning_map"]["topic_learnpath_name"]
                                    df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                                         df["Grade"][ind], df["Learnpath_name"][ind], title,
                                                         format_refrence, topic_learnpath_name,
                                                         id]
                                    # df1 = df1.drop_duplicates()
                                    df1.to_csv("Embibe_explainers_videos_home.csv", index=False)
                except Exception as e:
                    print(traceback.format_exc())
                    df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                         df["Grade"][ind], df["Learnpath_name"][ind], "", "", "", ""]
                    # df1 = df1.drop_duplicates()
                    df1.to_csv("Embibe_explainers_videos_home.csv", index=False)
                print("\n")

            # else:
            #     continue


def embibe_explainers_learn(df):
    src = Source()
    df1 = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade", "main_learnpath",
                                'Title', 'Format_refrence'
        , 'Topic_learnpath_name', "Video_ID"])
    df1.to_csv("Embibe_explainers_videos_home.csv", index=False)
    src.main(df)

# df = pd.read_csv("positive_learn_results.csv")
# embibe_explainers_learn(df)

# return_correct_sequence("6th CBSE", "CBSE")
