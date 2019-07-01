import requests  # import requests module
import time #import time module
import os
import csv
import urllib.request
import json
from datetime import datetime

# determine gameday by downloading current days data

# set current gameday 
def actualMatchday():
    ''' 
    Method needs an Internet access
    Data based on 'https://www.openligadb.de/api/getmatchdata/bl1'
        
    Returns: 
        - actualMatchday() returns an int which correspodend with the actual matchday of the Bundesliga
        - in case that the matchday is over but the url not updated still returns the actual matchday
        - if the season is over it returns 35
        - or an Error Message when the Matchdays of the matches differs
    '''
    
    url = 'https://www.openligadb.de/api/getmatchdata/bl1'
    opener = urllib.request.urlopen(url)
    data = json.load(opener)

    match1 = data[0]['Group']
    groupID = match1['GroupOrderID']
    lastmatch = data[0]['MatchDateTime']
    now = datetime.today().isoformat()
    
    for x in range(1, 9):
        match1 = data[x]['Group']
        if match1['GroupOrderID'] != groupID:
            print('unexpected Matchday diffrence')
            return False
        else: 
            if lastmatch < data[x]['MatchDateTime']:
                lastmatch = data[x]['MatchDateTime']
            else:
                continue        
    if lastmatch < now:
        return groupID + 1
    else:
        return groupID



def crawling(startYear, startDay, endYear, endDay):
    fileName = str(startDay)+"_"+str(startYear)+"_"+str(endDay)+"_"+str(endYear) + '.csv'
    if(os.path.isfile(fileName)): # if there is CSV File already, skip it
        return 
    f = open( fileName, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    # crawling all matchdays
    for year in range(startYear, endYear+1):
        # If same start year and end yaer.
        if (year == startYear and endYear == startYear):
            for day in range(startDay, endDay+1):
                url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(day) # set he URL
                data = requests.get(url).json()
                for game in range(len(data)):
                    wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
                    data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'],
                                 data[game]['MatchResults'][1]['PointsTeam2']])
                print(str(year)+'/day'+ str(day) + ' was loaded')        
        # If same year and start yaer.
        elif (year == startYear):
            for day in range(startDay, 35):
                url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(day) # set he URL
                data = requests.get(url).json()
                for game in range(len(data)):
                    wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
                    data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
                print(str(year)+'/day'+ str(day) + ' was loaded')
        # If same year and end yaer.
        elif (year == endYear):
            for day in range(1, endDay+1):
                url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(day) # set he URL
                data = requests.get(url).json()
                for game in range(len(data)):
                    wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
                    data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
                print(str(year)+'/day'+ str(day) + ' was loaded')
        else:
            for day in range(1, 35):
                url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(day) # set he URL
                data = requests.get(url).json()
                for game in range(len(data)):
                    wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
                    data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
                print(str(year)+'/day'+ str(day) + ' was loaded')    
        
# crawl next days matches
def nxtMatch(year):
    gameday= actualMatchday()
    if not(gameday == 35): # if season is over, don't crawl new Data
        f = open( 'nextGames' +'.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        nxtMatchUrl = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(gameday+1)
        dataNxt = requests.get(nxtMatchUrl).json()
        for game in range(len(dataNxt)):
                wr.writerow([dataNxt[game]['MatchDateTime'],dataNxt[game]['Team1']['ShortName'],
                    dataNxt[game]['Team2']['ShortName']])
        print(str(year)+'/day'+ str(gameday+1) + ' was loaded')   


def get_team_list(year):
    team_list = []
    url = 'https://www.openligadb.de/api/getavailableteams/bl1/' + str(year) # set he URL
    teams = requests.get(url).json()
    for num in range(len(teams)):
        team_list.append(teams[num]['ShortName'])
    team_list.sort()
    return team_list
