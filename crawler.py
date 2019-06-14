import requests  # import requests module
import time #import time module
import os
import csv
import actualMatchday
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
# use alternative actualMatchday() 
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
                    data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
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
    team_list = []
    url = 'https://www.openligadb.de/api/getavailableteams/bl1/' + str(year) # set he URL
    teams = requests.get(url).json()
    for num in range(len(teams)):
        team_list.append(teams[num]['ShortName'])
    team_list.sort()
    return team_list

