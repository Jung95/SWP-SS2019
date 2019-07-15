import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf
import csv

# fileName = str(startDay)+"_"+str(startYear)+"_"+str(endDay)+"_"+str(endYear) + '.csv'

a= "1_2018_34_2018.csv"

with open(a,newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('file.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Datum','HomeTeam','AwayTeam','HomeGoals','AwayGoals'])
    w.writerows(data)
data = pd.read_csv('file.csv')

print(data.head())

goal_model_data = pd.concat([data[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
            columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
           data[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
            columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])

poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data, 
                        family=sm.families.Poisson()).fit()

poisson_model.predict(pd.DataFrame(data={'team': 'VfB Stuttgart', 'opponent': 'FC Bayern',
                                       'home':1},index=[1]))
