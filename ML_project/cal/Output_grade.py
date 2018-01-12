import csv
import sys
import pandas as pd

#with open ("AIML_2017_Leaderboard.csv", 'r') as parse_file:
#    sentences = parse_file.readlines()

#for sentence in sentences:
#    print (sentence.split(','))

leaderboard = pd.read_csv("AIML_2017_Leaderboard.csv")
score_file = pd.read_csv("AIML_2017_ML.csv");

#print(leaderboard, score)


for i in leaderboard['student_ID']:
    score_str = ""
    score = 0
    score_file_index = (score_file.index[score_file['student_ID']==i].tolist())
    leaderboard_index = (leaderboard.index[leaderboard['student_ID']==i].tolist())

    #Documentaion
    Documentation_str = "Documentation Score: " + str(score_file.iloc[score_file_index[0]]['Documentation_score'])
    Documentation_score = score_file.iloc[score_file_index[0]]['Documentation_score']
    if(score_file.iloc[score_file_index[0]]['code']=="-1"):
        Documentation_score *= 0.85 
        Documentation_str += " x 0.85 = " + str(Documentation_score) + "(Late for one day)"
    Documentation_str += "\n"

    #Public Score
    Public_str = "Public Score: " + str(score_file.iloc[score_file_index[0]]['Public_score']) + "\n"
    Public_score = score_file.iloc[score_file_index[0]]['Public_score']
    Public_str += "Public Leaderboard score: " + str(leaderboard.iloc[leaderboard_index[0]]['Public Score']) + "\n"
    if(leaderboard.iloc[leaderboard_index[0]]['Public Reproduce']!=0):
        Public_str += "Public Reproduce score: " + str(leaderboard.iloc[leaderboard_index[0]]['Public Reproduce']) + "\n"
        if(leaderboard.iloc[leaderboard_index[0]]['Public Reproduce'] - leaderboard.iloc[leaderboard_index[0]]['Public Score'] < -0.02):
            Public_str += "Public Reproduce score (Double check): " + str(leaderboard.iloc[leaderboard_index[0]]['Double run']) + "\n"
    else:
        Public_str += "Reproduce Error: " + str(leaderboard.iloc[leaderboard_index[0]]['Error Message']) + "\n"

    #Private Score
    Private_str = "Private Score: " + str(score_file.iloc[score_file_index[0]]['Private_score']) + "\n"
    Private_score = score_file.iloc[score_file_index[0]]['Private_score']
    Private_str += "Private Leaderboard score: " + str(leaderboard.iloc[leaderboard_index[0]]['Private Score']) + "\n"

    #Rank 
    Rank_str = "Rank Score: " + str(score_file.iloc[score_file_index[0]]['Rank']) + "\n"
    Rank_score = score_file.iloc[score_file_index[0]]['Rank']

    score = Documentation_score + Public_score + Private_score + Rank_score
    score_str = Documentation_str + Public_str + Private_str + Rank_str + "\nTotal Score: " + str(score) + "\n"

    document_name = i + ".txt"
    with open(document_name, 'w') as grading_file:
        grading_file.writelines(score_str)

