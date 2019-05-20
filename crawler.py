import requests  # import requests module
import time #import time module
import os
import csv

def crawling(year):
    if(os.path.isfile(str(year)+'.csv')): # if there is CSV File already, skip it
        return 
    f = open( str(year)+'.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    # crawling all matchday
    for gameday in range(34): # total 34 Game
        url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(gameday+1) # set he URL
        data = requests.get(url).json()
        for game in range(len(data)):
            wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
             data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
        print(str(year)+'/day'+ str(gameday+1) + ' was loaded')

def get_team_list(year):
    if not(os.path.isfile(str(year)+'.csv')): # if there is not CSV File , crawl it
        crawling(year)
    team_list = []
    f = open(str(year) +'.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        if line[1] in team_list:
            pass
        else:
            team_list.append(line[1])
    return team_list