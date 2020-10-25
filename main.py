import  pandas as pd
import traceback

df1=pd.read_csv("Chapter_Questions_1.csv")
df2=pd.read_csv("Chapter_Questions_2.csv")
df3=pd.read_csv("Chapter_Questions_3.csv")
df4=pd.read_csv("Chapter_Questions_4.csv")
df5=pd.read_csv("Chapter_Questions_5.csv")

df=pd.concat([df1,df2,df3,df4,df5])
df.to_csv("Chapter_Questions.csv",index=False)

df=pd.read_csv("Question_bank.csv").drop_duplicates()
df1 = pd.read_csv("Chapter_Questions.csv").drop_duplicates()
df2 = pd.read_csv("Chapter_hygiene.csv").drop_duplicates()

# print(int(" "))
list1 = [""] * len(df1)
df1["Present in CG"] = list1
for ind in df1.index:
 try:
    print(int(df1["Question Id"][ind]))
    df_new = df.loc[df["id"] == int(df1["Question Id"][ind])]
    if len(df_new) > 0:
        df1["Present in CG"][ind] = "yes"
    else:
        df1["Present in CG"][ind] = "no"
 except Exception as e:
     print(traceback.format_exc())
     df1["Present in CG"][ind] = ""
df1.to_csv("Chapter_Questions.csv", index=False)

list1 = [""] * len(df2)
df2["Questions Live"] = list1
for ind in df2.index:
    flag = 0
    df_new = df1.loc[df1["Exam"] == df2["Exam"][ind]]
    if len(df_new) > 0:
        df_new1 = df1.loc[df1["Goal"] == df2["Goal"][ind]]
        if len(df_new1) > 0:
            df_new2 = df1.loc[df1["Chapter"] == df2["Chapter Name"][ind]]
            if len(df_new2) > 0:
                for ink in df_new2.index:
                    if df_new2["Present in CG"][ink] == "no":
                        flag = 1
                        break
                    else:
                        continue
                if flag == 1:
                    df2["Questions Live"][ind] = "no"
                else:
                    df2["Questions Live"][ind] = "yes"
            else:
                df2["Questions Live"][ind] = "Not found"
        else:
            df2["Questions Live"][ind] = "Not found"
    else:
        df2["Questions Live"][ind] = "Not found"
df2.to_csv("Chapter_hygiene.csv", index=False)
