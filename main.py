import pandas as pd
import traceback
import numpy as np

df1 = pd.read_csv("Chapter_Questions_1.csv")
df2 = pd.read_csv("Chapter_Questions_2.csv")
df3 = pd.read_csv("Chapter_Questions_3.csv")
df4 = pd.read_csv("Chapter_Questions_4.csv")
df5 = pd.read_csv("Chapter_Questions_5.csv")

df = pd.concat([df1, df2, df3, df4, df5])
df.replace('', np.nan, inplace=True)
# print(df)
df.to_csv("Chapter_Questions.csv", index=False)

df = pd.read_csv("Chapter_Questions.csv")
list1 = [""] * len(df)
df["Question_id"] = list1
for ind in df.index:
    var = (df["Question Id"][ind])
    try:
        var = (df["Question Id"][ind])
        # print(var)
        if var != "" and var != "NaN" and var != None and var != "error" and var != " " and var != "nan":
            print(var)
            df["Question_id"][ind] = int(var)
            # print(df["Question_id"][ind])
        else:
            print(var)
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            print("--------------------EXCEPT---------------------")
            df["Question_id"][ind] = ""
    except:
        print(var)
        print("------------------------------------------")
        df["Question_id"][ind] = ""

    # break
df.to_csv("Chapter_Questions.csv", index=False)

df = pd.read_csv("Question_bank.csv").drop_duplicates()
df1 = pd.read_csv("Chapter_Questions.csv").drop_duplicates()
df2 = pd.read_csv("Chapter_hygiene.csv").drop_duplicates()
#
# print(int(" "))
list1 = [""] * len(df)
df["question live"] = list1
for ind in df.index:

    # print(int(df["id"][ind]))
    df_new = df1.loc[df1["Question_id"] == int(df["id"][ind])]
    if len(df_new) > 0:
        df["question live"][ind] = "yes"
    else:
        df["question live"][ind] = "no"

df.to_csv("Question_bank.csv", index=False)

# list1 = [""] * len(df2)
# df2["Questions Live"] = list1
# for ind in df2.index:
#     flag = 0
#     df_new = df1.loc[df1["Exam"] == df2["Exam"][ind]]
#     if len(df_new) > 0:
#         df_new1 = df1.loc[df1["Goal"] == df2["Goal"][ind]]
#         if len(df_new1) > 0:
#             df_new2 = df1.loc[df1["Chapter"] == df2["Chapter Name"][ind]]
#             if len(df_new2) > 0:
#                 for ink in df_new2.index:
#                     if df_new2["Present in CG"][ink] == "no":
#                         flag = 1
#                         break
#                     else:
#                         continue
#                 if flag == 1:
#                     df2["Questions Live"][ind] = "no"
#                 else:
#                     df2["Questions Live"][ind] = "yes"
#             else:
#                 df2["Questions Live"][ind] = "Not found"
#         else:
#             df2["Questions Live"][ind] = "Not found"
#     else:
#         df2["Questions Live"][ind] = "Not found"
# df2.to_csv("Chapter_hygiene.csv", index=False)
