import crawler
import os
import csv

def maxGoal(year):#return max goal
    result = 0
    f = open(str(year) +'.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        if (int(line[3])> result):
            result = int(line[3])
        if (int(line[4])> result):
            result = int(line[4])           
    return result 

def getHisto(year):
    maxGoals = maxGoal(year)
    team_list = crawler.get_team_list(year)
    home = {}
    away = {}
    for team in team_list:
        home[team] = [0]*(maxGoals+1)
        away[team] = [0]*(maxGoals+1)
    histo = [home, away]

    f = open(str(year) +'.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        histo[0][line[1]][int(line[3])]+=1
        histo[1][line[2]][int(line[4])]+=1
    return histo

def algo(home, away, year): #result[0] is home  1 is draw 2 is away
    result = [0]*3
    histo = getHisto(year)
    for home_goal in range(maxGoal(year)+1):
        for away_goal in range(maxGoal(year)+1):
            if(home_goal==away_goal):
                result[1] += histo[0][home][home_goal]*histo[1][away][away_goal]
            if(home_goal>away_goal):
                result[0] += histo[0][home][home_goal]*histo[1][away][away_goal]
            if(home_goal<away_goal):
                result[2] += histo[0][home][home_goal]*histo[1][away][away_goal]
    total = result[0]+result[1]+result[2]
    result[0]= round(result[0]/total*100,2)
    result[1]= round(result[1]/total*100,2)
    result[2]= round(result[2]/total*100,2)          
    return result


