import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf
import math
import csv

# fileName = str(startDay)+"_"+str(startYear)+"_"+str(endDay)+"_"+str(endYear) + '.csv'

a= "1_2018_34_2018.csv"

# create csv data with header
with open(a,newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('file.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Datum','HomeTeam','AwayTeam','HomeGoals','AwayGoals'])
    w.writerows(data)
data = pd.read_csv('file.csv')

# print(data.head())

# write file.csv in pd dataframe
goal_model_data = pd.concat([data[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
                    columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
                    data[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
                    columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])

#fit data into a poisson distribution    
poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data, 
                        family=sm.families.Poisson()).fit()

poisson_model.predict(pd.DataFrame(data={'team': 'VfB Stuttgart', 'opponent': 'FC Bayern',
                                       'home':1},index=[1]))
    
poisson_model.predict(pd.DataFrame(data={'team': 'FC Bayern', 'opponent': 'VfB Stuttgart',
                                       'home':0},index=[1]))

    
    
def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
    home_goals_avg = foot_model.predict(pd.DataFrame(
            data={'team': homeTeam, 'opponent': awayTeam,'home':1}, index=[1])).values[0]
    
    away_goals_avg = foot_model.predict(pd.DataFrame(
            data={'team': awayTeam, 'opponent': homeTeam,'home':0}, index=[1])).values[0]
    
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))
    
    
    
vfbstu_bayern = simulate_match(poisson_model, 'VfB Stuttgart', 'FC Bayern', max_goals=3)


# Stuttgart win
stuwin = np.sum(np.triu(vfbstu_bayern, -1))
# draw
stubaydraw = np.sum(np.diag(vfbstu_bayern))
# Bayern win
bayernwin = np.sum(np.triu(vfbstu_bayern, 1))


