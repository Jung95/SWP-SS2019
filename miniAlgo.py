import crawler
import os
import csv

class Algorithmus:
    def __init__(self, year):
        self.year = year
        self.histo = []
        self.maxGoal = 0



    def setHisto(self):
        
        if not(os.path.isfile(str(self.year)+'.csv')): # if there is CSV File already, skip it
             crawler.crawling(self.year)
        result = 0
        f = open(str(self.year) +'.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            if (int(line[3])> result):
                result = int(line[3])
            if (int(line[4])> result):
                result = int(line[4])           
        self.maxGoal = result
        team_list = crawler.get_team_list(self.year)
        home = {}
        away = {}
        for team in team_list:
            home[team] = [0]*(self.maxGoal+1)
            away[team] = [0]*(self.maxGoal+1)
        self.histo = [home, away]

        f = open(str(self.year) +'.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            self.histo[0][line[1]][int(line[3])]+=1
            self.histo[1][line[2]][int(line[4])]+=1

    def predict(self, home, away): #result[0] is home  1 is draw 2 is away
        result = [0]*3
        for home_goal in range(int(self.maxGoal)+1):
            for away_goal in range(int(self.maxGoal)+1):
                if(home_goal==away_goal):
                    result[1] += self.histo[0][home][home_goal]*self.histo[1][away][away_goal]
                if(home_goal>away_goal):
                    result[0] += self.histo[0][home][home_goal]*self.histo[1][away][away_goal]
                if(home_goal<away_goal):
                    result[2] += self.histo[0][home][home_goal]*self.histo[1][away][away_goal]
        total = result[0]+result[1]+result[2]
        result[0]= round(result[0]/total*100,2)
        result[1]= round(result[1]/total*100,2)
        result[2]= round(result[2]/total*100,2)          
        return result



