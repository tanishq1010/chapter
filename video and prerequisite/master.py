from goal_exam_extractor import goal_exam_grade_extractor
from home_data_extractor import home_data
import pandas as pd

from login_sign_up import *
from embibe_explainers_home import embibe_explainers_learn
from CG_embibe_explainers import *
from prerequisite_home import prerequisite_home
from prerequisite_CG import *


# from miscellaneous import *
# from home_data_continue_learning import home_data


def for_all_exam_goal(goal_exam_grade):
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam"][ind])
        signup_data = Signup()
        login_data = login(signup_data[0], "embibe1234")
        # child_data=add_user(signup_data[1],login_data[0])
        embibe_token = login_data[1]
        child_id = signup_data[1]
        home_data(child_id, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam"][ind],
                  goal_exam_grade["Goal"][ind], embibe_token)


if __name__ == '__main__':
    df_negative_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Title', 'Type', 'Format_refrence', 'Section_name', 'Subject',
                                                'Subject_tagged', 'Learnpath_name', 'Learnmap_id',"Chapter"])
    df_positive_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Title', 'Type', 'Format_refrence', 'Section_name', 'Subject',
                                                'Subject_tagged', 'Learnpath_name', 'Learnmap_id',"Chapter"])
    df_negative_results.to_csv("negative_learn_results.csv", index=False)
    df_positive_results.to_csv("positive_learn_results.csv", index=False)

    goal_exam_grade = goal_exam_grade_extractor()
    # df=pd.read_csv("goal_exams.csv")
    for_all_exam_goal(goal_exam_grade)

    df = pd.read_csv("positive_learn_results.csv")
    embibe_explainers_learn(df)

    CG_DB_Embibe_explainers(df)
    df12 = pd.read_csv("Embibe_explainers_videos.csv")
    df11 = pd.DataFrame(columns=df12.columns.values)
    df12 = pd.DataFrame(columns=df12.columns.values)
    df11.to_csv("Embibe_explainers_my_order.csv", index=False)
    df12.to_csv("Negative_Embibe_explainers_videos.csv")

    for ind in df.index:
        return_correct_sequence(df["Exam"][ind], df["Goal"][ind], df["Learnpath_name"][ind])
    
    


    prerequisite_home(df)
    prerequisite_cg(df)
    


    df12 = pd.read_csv("Prerequisite_CG.csv")
    df11 = pd.DataFrame(columns=df12.columns.values)
    df11.to_csv("Prerequisite_my_order.csv", index=False)

    for ind in df.index:
        sequence(df["Exam"][ind], df["Goal"][ind], df["Learnpath_name"][ind])







        
        # return_correct_sequence("11th CBSE", "CBSE",
        #                         "cbse--11th cbse--physics--heat and thermodynamics--kinetic theory")
        # return_correct_sequence(df["Exam"][ind], df["Goal"][ind], df["Learnpath_name"][ind])
        # break

    # list1 = [""] * len(df)
    # df["Video_sequence_matched"] = list1
    # for ind in df.index:
    #     goal=df["Goal"][ind]
    #     exam=df["Exam"][ind]
    #     main_learnpath=df["Learnpath_name"][ind]
    #     df1=pd.read_csv("Embibe_explainers_videos_home.csv")
    #     df2=pd.read_csv("Embibe_explainers_my_order.csv")
    #
    #     df1 = df1[df1['Goal'].str.contains(goal)]
    #     df1 = df1[df1['Exam'].str.contains(exam)]
    #     df1= df1[df1['main_learnpath'].str.contains(main_learnpath)]
    #
    #     df2 = df2[df2['Goal'].str.contains(goal)]
    #     df2 = df2[df2['Exam'].str.contains(exam)]
    #     df2 = df2[df2['main_learnpath'].str.contains(main_learnpath)]
    #
    #     if df1.equals(df2):
    #         df["Video_sequence_matched"][ind]="yes"
    #     else:
    #         df["Video_sequence_matched"][ind] = "no"
