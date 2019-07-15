import crawler
import csv
import os
import math
import ast
import numpy

class PoissionRegression:
    def __init__(self, startYear=0, startDay=0, endYear=0, endDay=0, nowYear=0):
        """
        Args:
            startYear (int): Start Year to predict. It is optional, Default value is 0.
            startDay (int): Start Matchday to predict. It is optional, Default value is 0.
            endYear (int): End Year to predict. It is optional, Default value is 0.
            endDay (int): End Matchday to predict. It is optional, Default value is 0.
            nowYear (int): now Leagyear to get teamlist. It is optional, Default value is 0. 
        """        
        self.startYear = startYear
        self.startDay = startDay
        self.endYear = endYear
        self.endDay = endDay
        self.nowYear = nowYear
        self.histo = []
        self.maxGoal = 0
        self.Data
        self.team_list = []


    def setDate(self, startYear, startDay, endYear, endDay, nowYear):
        """
        Args:
            startYear (int): Start Year to predict. 
            startDay (int): Start Matchday to predict. 
            endYear (int): End Year to predict. 
            endDay (int): End Matchday to predict. 
            nowYear (int): now Leagyear to get teamlist. 

        Returns:
            True if successful, False otherwise.

        """
        self.startYear = startYear
        self.startDay = startDay
        self.endYear = endYear
        self.endDay = endDay
        self.nowYear = nowYear
        return True

    def setData(self):
        if(self.startYear > self.endYear):
            return True
        if((self.startYear == self.endYear) & (self.startDay > self.endDay)):
            return True
        fileName = str(self.startDay)+"_"+str(self.startYear)+"_"+str(self.endDay)+"_"+str(self.endYear) + '.csv'
        if not(os.path.isfile(fileName)): # if there is CSV File already, skip it
             crawler.crawling(self.startYear, self.startDay,self.endYear, self.endDay)
        self.Data = fileName

    def poisson(actual, mean):
        return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)

    def function(self):
        k = open('team_list.txt', 'w')
        k.write("""{
        """)

        csvRead = csv.reader(open(self.Data))
        for row in csvRead:
            if row[1] not in self.team_list:
                self.team_list.append(row[1])
            if row[2] not in self.team_list:
                self.team_list.append(row[2])

        self.team_list.sort()

        for team in team_list:
            k.write("""	'%s': {'home_goals': 0, 'away_goals': 0, 'home_conceded': 0, 'away_conceded': 0,
                'home_games': 0, 'away_games': 0, 'alpha_h': 0, 'beta_h': 0, 'alpha_a': 0, 'beta_a': 0},
        """ % (team))

        k.write("}")
        k.close()

        s = open('team_list.txt', 'r').read()
        dict = ast.literal_eval(s)

        GAMES_PLAYED = 0
        WEEKS_WAIT = 4 # löschen
        TOTAL_VALUE = 0

        csvRead = csv.reader(open(self.Data))
        next(csvRead)

        for game in csvRead:
            home_team = game[1]
            away_team = game[2]
            home_goals = int(game[3])
            away_goals = int(game[4])
            home_win_prob = 0
            draw_win_prob = 0
            away_win_prob = 0
	
            curr_home_goals = 0
            curr_away_goals = 0
            avg_home_goals = 1
            avg_away_goals = 1
	
            team_bet = ''
            ev_bet = ''

            for key, value in dict.items():
                    curr_home_goals += dict[key]['home_goals']
                    curr_away_goals += dict[key]['away_goals']
		
                    if GAMES_PLAYED > (WEEKS_WAIT * 10):
                            avg_home_goals = curr_home_goals / (GAMES_PLAYED)
                            avg_away_goals = curr_away_goals / (GAMES_PLAYED)
                            
            if GAMES_PLAYED > (WEEKS_WAIT * 10):
                    home_team_a = (dict[home_team]['alpha_h'] + dict[home_team]['alpha_a']) / 2
                    away_team_a = (dict[away_team]['alpha_h'] + dict[away_team]['alpha_a']) / 2
		
                    home_team_d = (dict[home_team]['beta_h'] + dict[home_team]['beta_a']) / 2
                    away_team_d = (dict[away_team]['beta_h'] + dict[away_team]['beta_a']) / 2
		
                    home_team_exp = avg_home_goals * home_team_a * away_team_d #maximum likelyhood
                    away_team_exp = avg_away_goals * away_team_a * home_team_d

                    l = open('poisson.txt', 'w')
                    for i in range(10):
                            for j in range(10):
                                    prob = poisson(i, home_team_exp) * poisson(j, away_team_exp)
                                    l.write("Prob%s%s = %s\n" % (i, j, prob))
                    l.close()

                    
