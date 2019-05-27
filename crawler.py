import requests  # import requests module
import time #import time module
import os
import csv

gameday = 1 # current gameday

# determine gameday by downloading current days data
def getGameday():
    f = open( 'currentGameday' +'.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    Url = 'https://www.openligadb.de/api/getmatchdata/bl1'
    data = requests.get(Url).json()
    wr.writerow([data[1]['Group']['GroupOrderID']])
    print('current gameday was loaded') 

# set current gameday 
def setGameday():
    global gameday
    t = open('currentGameday' +'.csv', 'r', encoding='utf-8')
    rdr = csv.reader(t)
    for line in rdr:
        """for Test
        gameday = int(line[0])
        """
        gameday = 33
    print('Gameday = '+str(gameday))
    
def crawling(year):
    if(os.path.isfile(str(year)+'.csv')): # if there is CSV File already, skip it
        return 
    f = open( str(year)+'.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    # crawling all matchdays
    for gameday in range(34): # total 34 Game
        url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(gameday+1) # set he URL
        data = requests.get(url).json()
        for game in range(len(data)):
            wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
             data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
        print(str(year)+'/day'+ str(gameday+1) + ' was loaded')
        
# crawl next days matches
def nxtMatch(year):
    if not(gameday == 34): # if season is over, don't crawl new Data
        f = open( 'nextGames' +'.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        nxtMatchUrl = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(year) +'/' + str(gameday+1)
        dataNxt = requests.get(nxtMatchUrl).json()
        for game in range(len(dataNxt)):
                wr.writerow([dataNxt[game]['MatchDateTime'],dataNxt[game]['Team1']['ShortName'],
                    dataNxt[game]['Team2']['ShortName']])
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
    team_list.sort()
    return team_list
