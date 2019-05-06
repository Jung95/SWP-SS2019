import requests  # import requests module
import time #import time module
import os
import csv

team_list=[]
liga = []
def crawling():
    now = time.gmtime(time.time()) # set now
    year = now.tm_year # now year
    mon = now.tm_mon #now month

    if(mon<7): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
        league_year = year - 2
    else:
        league_year = year - 1

    url = 'https://www.openligadb.de/api/getavailableteams/bl1/' + str(league_year) # set he URL
    teams = requests.get(url).json()
    # crawling all Teams
    for num in range(len(teams)):
        team_list.append(teams[num]['TeamName'])
    liga.append('Bundesliga '+ str(league_year) + '/' + str(league_year+1))

    if(os.path.isfile(str(league_year)+'.csv')): # if there is CSV File already, skip it
        return 

    f = open( str(league_year)+'.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    # crawling all matchday
    for gameday in range(34): # total 34 Game
        url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(league_year) +'/' + str(gameday+1) # set he URL
        data = requests.get(url).json()
        for game in range(len(data)):
            wr.writerow([data[game]['MatchDateTime'],data[game]['Team1']['ShortName'],
             data[game]['Team2']['ShortName'], data[game]['MatchResults'][1]['PointsTeam1'], data[game]['MatchResults'][1]['PointsTeam2']])
        print('day'+ str(gameday+1) + ' was loaded')