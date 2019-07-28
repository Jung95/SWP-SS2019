import pandas as pd
import numpy as np
from scipy.stats import poisson
import statsmodels.api as sm
import statsmodels.formula.api as smf
import csv

def fit_data(startYear, startMatch, endYear, endMatch):
    """

    fits the given data into an poisson distribution and creates an regression model
    
    Input:
        csv file with the collected data
    Args:
        startYear (int): Start Year of the Data which will be fited. 
        startMatch (int): Start Match of the Data which will be fited. 
        endYear (int): End Year of the Data which will be fited. 
        endMatch (int): End Matchday of the Data which will be fited. 
    Returns:
        csv file with the prepared data 
        Poisson regression model of the data

    """
    filename = str(startMatch) + '_' + str(startYear) + '_' + str(endMatch) + '_' + str(endYear) + '.csv'
    
    with open(filename, newline='') as f:
        r = csv.reader(f)
        data = [line for line in r]
        
    with open('poissonfile.csv','w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['Date','HomeTeam','AwayTeam','HomeGoals','AwayGoals'])
        w.writerows(data)
    data = pd.read_csv('poissonfile.csv')
    
    goal_model_data = pd.concat([data[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
                    columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
                    data[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
                    columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])
   
    poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data, 
                        family=sm.families.Poisson()).fit()
    return poisson_model

    
def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    """
    
    computes the probabilitys of the chance to win against the other team by the given datafram
    
    Args:
        foot_model (pdDataFrame): conditioned dataframe of the trainingdata. 
        homeTeam (str): Hometeam to predict. 
        awayTeam (str): Guestteam to predict. 
        max_goals (int): maxmimum scored goals recorded in the dataframe 
    Returns:
        list of the probabilitys in this order: (homewins, draw, guestwins)

    """
    home_goals_avg = foot_model.predict(pd.DataFrame(
            data={'team': homeTeam, 'opponent': awayTeam,'home':1}, index=[1])).values[0]
    
    away_goals_avg = foot_model.predict(pd.DataFrame(
            data={'team': awayTeam, 'opponent': homeTeam,'home':0}, index=[1])).values[0]
    
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    
    result = [0]*3
    abc = (np.outer(np.array(team_pred[0]), np.array(team_pred[1])))
    result[0] = round(np.sum(np.tril(abc, -1))*100, 2)
    result[1] = round(np.sum(np.diag(abc))*100, 2)
    result[2] = round(np.sum(np.triu(abc, 1))*100, 2)
    
    return result
    
      

# =============================================================================
#   # Example   
#    poisson_model.predict(pd.DataFrame(data={'team': 'VfB Stuttgart', 'opponent': 'FC Bayern',
#                                           'home':1},index=[1]))
#        
#    poisson_model.predict(pd.DataFrame(data={'team': 'FC Bayern', 'opponent': 'VfB Stuttgart',
#                                           'home':0},index=[1]))
#  
#   vfbstu_bayern = simulate_match(poisson_model, 'VfB Stuttgart', 'FC Bayern')
#   # Stuttgart win
#   stuwin = np.sum(np.tril(vfbstu_bayern, -1))
#   # draw
#   stubaydraw = np.sum(np.diag(vfbstu_bayern))
#   # Bayern win
#   bayernwin = np.sum(np.tril(vfbstu_bayern, 1))
# =============================================================================
