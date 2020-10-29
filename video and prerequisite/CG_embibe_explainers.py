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
        self.headers['Authorization'] = '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D'
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, df):
        df1 = pd.read_csv("Embibe_explainers_videos.csv")
        df2 = pd.read_csv("Negative_Embibe_explainers_videos.csv")
        for ind in df.index:
            # if df["Exam"][ind] == "11th CBSE":
              learnpath_name1 = df["Learnpath_name"][ind]
              print(df["Exam"][ind], "\t\t", df["Goal"][ind], "\t\t", df["Learnpath_name"][ind])
              format_refrence = df["Format_refrence"][ind]
              try:
                 response1 = self.callAPI(
                    "http://content-demo.embibe.com/learning_objects?where={%22status%22:%22Published%22}&lo_type=Video&lm_filter={%22format_reference%22:%22" + str(
                        format_refrence) + "%22,%22learnpath_name%22:{%22$regex%22:%22" + str(
                        learnpath_name1) + "%22}}&embed=true&max_results=100000",
                    '{}', 'GET')
                # print(response1)
                # print(response1.json())
                 for item in response1.json()["_items"]:
                    title = item["title"]
                    id = item["id"]
                    id = int(id)
                    try:
                      if item["content"]["key_attributes"]["type"] == "Topic Explainer" or item["content"]["key_attributes"][
                           "type"] == "Solved Problems asked in exams":
                       sequence = item["content"]["sequence"]
                       PRINT("\n")
                       print("SEQUENCE DICTIONARY :", sequence)
                       for inti in item["content"]["question_meta_tags"]:
                         for index in inti["learning_maps_data"]:
                            # if str(index["format_reference"]) == str(format_refrence):
                            #     print()
                            if index["format_reference"] == format_refrence:
                                learnpath_name = index["learnpath_name"]
                                code = index["code"]
                                # format_refrence = index["format_reference"]
                                # print(code)
                                try:
                                    sequence1 = sequence[code]
                                    print("FINDING THIS LM IN ABOVE SEQUENCE DICTIONARY", code)

                                    df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                                         df["Grade"][ind], learnpath_name1, title, format_refrence,
                                                         sequence1,
                                                         df["Subject_tagged"][ind], learnpath_name, id]
                                    df1 = df1.drop_duplicates()
                                    df1.to_csv("Embibe_explainers_videos.csv", index=False)
                                except Exception as e:
                                    # print(e)
                                    print("EXCEPTION DUE TO SEQUENCE NOT FOUND IN DICTIONARY :")
                                    print("CHAPTER LEARNPATH NAME :", learnpath_name1, "\n")
                                    print("LEARN PATH WHICH GAVE ERROR :", learnpath_name)
                                    print(traceback.format_exc())
                                    df2.loc[len(df2)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                                         df["Grade"][ind], learnpath_name1, title, format_refrence,
                                                         e,
                                                         df["Subject_tagged"][ind], learnpath_name, id]
                                    df2 = df2.drop_duplicates()
                                    df2.to_csv("Negative_Embibe_explainers_videos.csv", index=False)
                      else:
                        continue

                    except Exception as e:
                       print("SOME ERROR OCCURED WITH INTENT CONTENT QUESTION_META_TAG (SEQUENCE DICTIONARY) FOR THIS CHAPTER LEARN PATH :", learnpath_name1,"AND TITLE :",title)
                       print(traceback.format_exc())
                       df2.loc[len(df2)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                     df["Grade"][ind], learnpath_name1, "", format_refrence,
                                     e,
                                     df["Subject_tagged"][ind], "", ""]
                       df2 = df2.drop_duplicates()
                       df2.to_csv("Negative_Embibe_explainers_videos.csv", index=False)
              except Exception as e:
                  print("SOME ERROR WITH LEARN CHAPTER LEARN PATH AND API CALLING :",learnpath_name1)
                  print(traceback.format_exc())
                  df2.loc[len(df2)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                       df["Grade"][ind], learnpath_name1, "", format_refrence,
                                       e,
                                       df["Subject_tagged"][ind], "", ""]
                  df2 = df2.drop_duplicates()
                  df2.to_csv("Negative_Embibe_explainers_videos.csv", index=False)
            # else:
            #  continue


def return_correct_sequence(exam, goal, learnpath_name):
    df11 = pd.read_csv("Embibe_explainers_my_order.csv")
    df = pd.read_csv("Embibe_explainers_videos.csv")
    df = df[df['Goal'].str.contains(goal)]
    df = df[df['Exam'].str.contains(exam)]
    df = df[df['main_learnpath'].str.contains(learnpath_name)]


    df.sort_values(by=['Sequence'], ascending=True,
                   inplace=True)
    # del df['length of string']
    df.drop_duplicates(inplace=True)
    # df = pd.concat([df3, df])
    df11 = pd.concat([df11, df])
    df11.to_csv("Embibe_explainers_my_order.csv", index=False)


def CG_DB_Embibe_explainers(df):
    src = Source()
    if os.path.exists("Embibe_explainers_videos.csv"):
        print("file Embibe_explainers_videos.csv exists .....")
    else:
        print("making file Embibe_explainers_videos.csv .... ")
        df1 = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade", "main_learnpath",
                                    'Title', 'Format_refrence', 'Sequence', 'Subject'
            , 'Learnpath_name', "Video_ID"])
        df1.to_csv("Embibe_explainers_videos.csv", index=False)
        df12 = pd.read_csv("Embibe_explainers_videos.csv")
        df12 = pd.DataFrame(columns=df12.columns.values)
        df12.to_csv("Negative_Embibe_explainers_videos.csv", index=False)
        src.main(df)

# df = pd.read_csv("positive_learn_results.csv")
# CG_DB_Embibe_explainers(df)
#
# return_correct_sequence("11th CBSE", "CBSE", "cbse--11th cbse--physics--mechanics--work, energy and power")
