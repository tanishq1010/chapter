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
            'Authorization'] = '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D'
        response = requests.request(method, url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, df):
        df1 = pd.read_csv("Prerequisite_CG.csv")
        for ind in df.index:
         # if df["Exam"][ind] == "11th CBSE":
            # break

            learnmap_id = df["Learnmap_id"][ind]
            print("GETTING ALL Topics FOR THIS LEARN PATH FROM CG : ", learnmap_id, "\n")
            format_refrence = df["Format_refrence"][ind]
            subject = df["Subject_tagged"][ind]
            learnpath_name1 = df["Learnpath_name"][ind]
            try:
                response1 = self.callAPI(
                    "https://content-demo.embibe.com/fiber_app/learning_maps/filters/" + str(learnmap_id),
                    "{}", 'GET')
                # print(response1)
                # print(response1.json())
                # print(response1.json()["Topic"])
                if response1.json()["Topic"] == []:
                    print("\t\tNO TOPICS FOR ABOVE LEARN PATH ID\n")
                    df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                         df["Grade"][ind], df["Learnpath_name"][ind], "",
                                         format_refrence, "",
                                         "", ""]
                else:
                    for topic in response1.json()["Topic"]:
                        print("\n")
                        print("\t\tFOR THIS TOPIC IN ABOVE LEARN PATH ID :", topic["name"])
                        learnpath_name = topic["learnpath_name"]
                        # print(learnpath_name)
                        response2 = self.callAPI(
                            "https://content-demo.embibe.com/learning_maps/prerequisite?format_reference=" + str(
                                format_refrence) + "&learnpath_name=" + str(learnpath_name),
                            "{}", 'GET')
                        # print(response2.json())
                        # print(response2.json()["prerequisite_learning_maps"])
                        if response2.json()["prerequisite_learning_maps"] != []:
                            print("\t\tGETTING ALL PREREQUISITES FOR TOPIC  :", topic["name"])
                            for item in response2.json()["prerequisite_learning_maps"]:
                                learnpath_name2 = (item["learnpath_name"])
                                LIST = []
                                LIST = learnpath_name2.split('--')
                                title = LIST[len(LIST) - 1]
                                sequence = item["sequence"]
                                i = int(0)
                                for count in item["concepts"]:
                                    i += 1
                                concept_count = i
                                df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                                     df["Grade"][ind], df["Learnpath_name"][ind], title,
                                                     format_refrence, learnpath_name2,
                                                     concept_count, sequence]
                                df1.to_csv("Prerequisite_CG.csv", index=False)

                        else:
                            print("\t\tNO PREREQUISITES FOR TOPIC  :", topic["name"], "\n")
                            df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                                 df["Grade"][ind], df["Learnpath_name"][ind], "",
                                                 format_refrence, learnpath_name,
                                                 "", ""]
                            df1.to_csv("Prerequisite_CG.csv", index=False)
            except Exception as e:
                print(traceback.format_exc())
                df1.loc[len(df1)] = [df["Child_ID"][ind], df["Exam"][ind], df["Goal"][ind],
                                     df["Grade"][ind], df["Learnpath_name"][ind], "",
                                     format_refrence, "",
                                     "", ""]
                df1.to_csv("Prerequisite_CG.csv", index=False)

            # else:
            #     continue


def sequence(exam, goal, learnpath_name):
    df11 = pd.read_csv("Prerequisite_my_order.csv")
    # column_name=df11.columns.values
    # df11=pd.DataFrame(columns=column_name)
    # df11.to_csv("Prerequisite_my_order.csv")
    # print(df11)
    df = pd.read_csv("Prerequisite_CG.csv")
    df = df[df['Goal'].str.contains(goal)]
    df = df[df['Exam'].str.contains(exam)]
    df = df[df['main_learnpath'].str.contains(learnpath_name)]
    # print(df)
    df.dropna(
        axis=0,
        how='any',
        thresh=None,
        subset=None,
        inplace=True
    )

    df.sort_values(by=['Sequence'], ascending=True,
                   inplace=True)
    # print(df)
    df.drop_duplicates(
        inplace=True)
    # print(df)
    df11 = pd.concat([df11, df])
    df11.to_csv("Prerequisite_my_order.csv", index=False)


def prerequisite_cg(df):
    src = Source()
    df1 = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade", "main_learnpath",
                                'Title', 'Format_refrence'
        , 'Topic_learnpath_name', "Concept_count", "Sequence"])
    df1.to_csv("Prerequisite_CG.csv", index=False)

    src.main(df)

# df = pd.read_csv("positive_learn_results.csv")
# prerequisite_cg(df)

# return_correct_sequence("6th CBSE", "CBSE")
# sequence("11th CBSE","CBSE","cbse--11th cbse--physics--mechanics--work, energy and power")
