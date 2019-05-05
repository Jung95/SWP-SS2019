import requests  # import requests module
import time #import time module
import json #import json module

def crawling():
    now = time.gmtime(time.time()) # set now
    year = now.tm_year # now year
    mon = now.tm_mon #now month

    if(mon<7): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
        league_year = year - 2
    else:
        league_year = year - 1

    result = {}
    # crawling all matchday
    league_result = []
    for gameday in range(34): # total 34 Game
        url = 'https://www.openligadb.de/api/getmatchdata/bl1/' + str(league_year) +'/' + str(gameday+1) # set he URL
        data = requests.get(url).json()
        day_result = []
        for game in range(len(data)):
            day = {}
            day['Datum'] = data[game]['MatchDateTime']
            day['Heimverein'] = data[game]['Team1']['TeamName']
            day['Gastverein']= data[game]['Team2']['TeamName']
            day['ToreHeim'] =  str(data[game]['MatchResults'][1]['PointsTeam1'])
            day['ToreGast']=  str(data[game]['MatchResults'][1]['PointsTeam2'])
            day_result.append(day)
        league_result.append(day_result)
        print('day'+ str(gameday+1) + ' was loaded')
    result['LeagueResult'] = league_result

    team_list = []
    url = 'https://www.openligadb.de/api/getavailableteams/bl1/' + str(league_year) # set he URL
    teams = requests.get(url).json()
    # crawling all Teams
    for num in range(len(teams)):
        team_list.append(teams[num]['TeamName'])
        
    result['TeamList'] = team_list
    result['year'] = 'Bundesliga '+ str(league_year) + '/' + str(league_year+1)
    jons_result = json.dumps(result, indent=4)
    
    return jons_result

