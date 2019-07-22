import crawler
import csv
import os
import math
import ast
import numpy

#class PoissionRegression:
#    def __init__(self, startYear=0, startDay=0, endYear=0, endDay=0, nowYear=0):
#        """
#        Args:
#            startYear (int): Start Year to predict. It is optional, Default value is 0.
#            startDay (int): Start Matchday to predict. It is optional, Default value is 0.
#            endYear (int): End Year to predict. It is optional, Default value is 0.
#            endDay (int): End Matchday to predict. It is optional, Default value is 0.
#            nowYear (int): now Leagyear to get teamlist. It is optional, Default value is 0. 
#        """        
#        self.startYear = startYear
#        self.startDay = startDay
#        self.endYear = endYear
#        self.endDay = endDay
#        self.nowYear = nowYear
#        self.histo = []
#        self.maxGoal = 0
#        self.Data
#        self.team_list = []


#    def setDate(self, startYear, startDay, endYear, endDay, nowYear):
#        """
#        Args:
#            startYear (int): Start Year to predict. 
#            startDay (int): Start Matchday to predict. 
#            endYear (int): End Year to predict. 
#            endDay (int): End Matchday to predict. 
#            nowYear (int): now Leagyear to get teamlist. 
#
#        Returns:
#            True if successful, False otherwise.

#        """
#        self.startYear = startYear
#        self.startDay = startDay
#        self.endYear = endYear
#        self.endDay = endDay
#        self.nowYear = nowYear
#        return True

#    def setData(self):
#        """sets CSV file as self.Data

#        """
	
#        if(self.startYear > self.endYear):
#            return True
#        if((self.startYear == self.endYear) & (self.startDay > self.endDay)):
#            return True
#        fileName = str(self.startDay)+"_"+str(self.startYear)+"_"+str(self.endDay)+"_"+str(self.endYear) + '.csv'
#        if not(os.path.isfile(fileName)): # if there is CSV File already, skip it
#             crawler.crawling(self.startYear, self.startDay,self.endYear, self.endDay)
#        self.Data = "1_2018_2_2018.csv" #fileName replaced by dummy

def poisson(actual, mean):
    """calculates die poission distributed probability
    Args:
    actual(int): the number of goals for which the probability is calculated
    mean(float): the likelyhood for a team's goals

    Returns:
    The probability of making "actual" goals

    """
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)

# data = '1_2018_2_2018.csv'
def function(data):
    """calculates the poission probablilites and saves them in a txt file

    """
    team_list = []
    
    # create a txt file
    k = open('team_list.txt', 'w')
    k.write("""{
    """)
    
    csvRead = csv.reader(open(data))
        
    # create a list with all team names
    for row in csvRead:
        if row[1] not in team_list:
            team_list.append(row[1])
        if row[2] not in team_list:
            team_list.append(row[2])

    team_list.sort()

    # add dummies for all values for all teams in the txt file
    for team in team_list:
            k.write("""	"%s": {'home_goals': 0, 'away_goals': 0, 'home_conceded': 0, 'away_conceded': 0, 'home_games': 0,
                    'away_games': 0, 'alpha_h': 0, 'beta_h': 0, 'alpha_a': 0, 'beta_a': 0},
    """ % (team))
    k.write("}")
    k.close()

    # erstelle txt für predictions
    r = open('prediction.txt', 'w')
    r.write("""{
    """)

    # erstelle ein Dictonary um Updates in der txt zu speichern
    s = open('team_list.txt', 'r').read()
    dict = ast.literal_eval(s)

    GAMES_PLAYED = 0
    WEEKS_WAIT = 4 # löschen
    TOTAL_VALUE = 0

    csvRead = csv.reader(open(data))
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

                # Mittelwert der erzielten Tore
                if GAMES_PLAYED > (WEEKS_WAIT * 10):
                        avg_home_goals = curr_home_goals / (GAMES_PLAYED)
                        avg_away_goals = curr_away_goals / (GAMES_PLAYED)
                            
        if GAMES_PLAYED > (WEEKS_WAIT * 1):
                #attack rate
                home_team_a = (dict[home_team]['alpha_h'] + dict[home_team]['alpha_a']) / 2
                away_team_a = (dict[away_team]['alpha_h'] + dict[away_team]['alpha_a']) / 2

                #defense rate
                home_team_d = (dict[home_team]['beta_h'] + dict[home_team]['beta_a']) / 2
                away_team_d = (dict[away_team]['beta_h'] + dict[away_team]['beta_a']) / 2

                #maximum likelyhood
                home_team_exp = avg_home_goals * home_team_a * away_team_d 
                away_team_exp = avg_away_goals * away_team_a * home_team_d

                # Wahrscheinlichkeiten für alle Torkonstellationen
                l = open('poisson.txt', 'w')
                for i in range(10):
                        for j in range(10):
                                prob = poisson(i, home_team_exp) * poisson(j, away_team_exp)
                                l.write("Prob%s%s = %s\n" % (i, j, prob))
                l.close()

                # Wahrscheinlichkeiten für home win, Unentschieden, away win
                with open('poisson.txt') as f:
                        for line in f:
				
                                home_goals_m = int(line.split(' = ')[0][4])
                                away_goals_m = int(line.split(' = ')[0][5])
				
                                prob = float(line.split(' = ')[1])
				
                                if home_goals_m > away_goals_m:
                                        home_win_prob += prob
                                elif home_goals_m == away_goals_m:
                                        draw_win_prob += prob
                                elif home_goals_m < away_goals_m:
                                        away_win_prob += prob

                highestEV = max(away_win_prob, draw_win_prob, home_win_prob)
		
                if (home_win_prob == highestEV) and (home_win_prob > 0):
                        team_bet = home_team
                        ev_bet = home_win_prob
				
                elif (draw_win_prob == highestEV) and (draw_win_prob > 0):
                        team_bet = 'Draw'
                        ev_bet = draw_win_prob
                elif (away_win_prob == highestEV) and (away_win_prob > 0):
                        team_bet = away_team
                        ev_bet = away_win_prob
		
                if (team_bet != '') and (ev_bet != ''):
                        printout = "For " + str(home_team) + " vs." + str(away_team) + " bet on " + str(team_bet) + " (Probability =" + str(ev_bet) + ") \n"
                        r.write(printout)
                        #print ("For", home_team, "vs.", away_team, "bet on '%s' (Probability = %s)" % (team_bet, ev_bet))

	# UPDATE VARIABLES AFTER MATCH HAS BEEN PLAYED
        dict[home_team]['home_goals'] += home_goals
        dict[home_team]['home_conceded'] += away_goals
        dict[home_team]['home_games'] += 1
	
        dict[away_team]['away_goals'] += away_goals
        dict[away_team]['away_conceded'] += home_goals
        dict[away_team]['away_games'] += 1
	
        GAMES_PLAYED += 1
	
        # CREATE FACTORS
        if GAMES_PLAYED > (WEEKS_WAIT * 10):
                for key, value in dict.items():
                        alpha_h = (dict[key]['home_goals'] / dict[key]['home_games']) / avg_home_goals
                        beta_h = (dict[key]['home_conceded'] / dict[key]['home_games']) / avg_away_goals

                        alpha_a = (dict[key]['away_goals'] / dict[key]['away_games']) / avg_away_goals
                        beta_a = (dict[key]['away_conceded'] / dict[key]['away_games']) / avg_home_goals

                        dict[key]['alpha_h'] = alpha_h
                        dict[key]['beta_h'] = beta_h
                        dict[key]['alpha_a'] = alpha_a
                        dict[key]['beta_a'] = beta_a
    r.close()

		    
