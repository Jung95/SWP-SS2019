import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+'/bundes')
import miniAlgo
import crawler
import gui
import csv
from datetime import datetime
import requests  # import requests module
import time #import time module
import urllib.request
import json
from tkinter import *

class Tester:
    """
    It tests all functions of the main-programm
    """
    def __init__(self):
        self.test_startYear = 2018
        self.test_startDay = 1
        self.test_endYear= 2018
        self.test_endDay = 2
        self.test_nowYear = 2019
        self.miniAlgo = miniAlgo.Algorithmus()
        self.crawler = crawler.Crawler()
        
        self.test_crawler_set_actualMatchday()
        self.test_crawler_crawling()
        self.test_crawler_nxtMatch()
        self.test_crawler_get_team_list()
        self.test_miniAlgo_setDate()
        self.test_miniAlgo_setHisto()
        self.test_miniAlgo_predict()
        self.test_gui()



    def test_crawler_set_actualMatchday(self):
        """It tests set_actualMatchday Function of crawler.
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("crawler actualMatchday set Test:")
        url = 'https://www.openligadb.de/api/getmatchdata/bl1'
        opener = urllib.request.urlopen(url)
        data = json.load(opener)

        match1 = data[0]['Group']
        groupID = match1['GroupOrderID']
        lastmatch = data[0]['MatchDateTime']
        now = datetime.today().isoformat()
        result = True 
        for x in range(1, 9):
            match1 = data[x]['Group']
            if match1['GroupOrderID'] != groupID:
                result = False
            else: 
                pass 
        if result==False:
            print('Error : unexpected Matchday diffrence')
        else:
            print("actualMatchday set Okay")
        self.crawler.set_actualMatchday()
        return result

    def test_crawler_crawling(self):
        '''
        This methods tests if the current csv data has the expected length.
        The length correspodens with the number of matches in this time period.
        
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        
        '''
        print("--------------------------")
        print("crawling Test:")
        self.crawler.crawling(self.test_startYear, self.test_startDay, self.test_endYear, self.test_endDay)  
        expectedLines = ((34-self.test_startDay+1) + (self.test_endYear-self.test_startYear-1)*34 + self.test_endDay)*9
        
        filename = str(self.test_startDay) + '_' + str(self.test_startYear) + '_' + str(self.test_endDay) + '_' + str(self.test_endYear) + '.csv'
        f = open(filename, 'r', encoding='utf-8', newline='')
        rdr = csv.reader(f)
        value = len(list(rdr))
        if value == expectedLines:
            print ('Found all Matches')
            print ('crawling Okay')
            return True
        else:
            print('Found '+ str(value) + ' of ' + str(expectedLines) + ' Matches')
            print ('crawling Error')
            return False

    def test_crawler_nxtMatch(self):
        """It tests nxtMatch Function of crawler.
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("crawler get next Match Test:")
        self.crawler.actualMatchday = 1
        self.crawler.nxtMatch(2018)
        sample_listHome=['Hannover 96', 'TSG 1899 Hoffenheim', 'Bayer Leverkusen', 'Eintracht Frankfurt', 'FC Augsburg', '1. FC Nürnberg', 'VfB Stuttgart', 'RB Leipzig', 'FC Schalke 04']
        sample_listGuest=['Borussia Dortmund', 'SC Freiburg', 'VfL Wolfsburg', 'Werder Bremen', 'Borussia Mönchengladbach', '1. FSV Mainz 05', 'FC Bayern', 'Fortuna Düsseldorf', 'Hertha BSC']

        listHome = []
        listGuest = []
        f = open('nextGames' +'.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            listHome.append(line[1])
            listGuest.append(line[2])
        if(listHome== sample_listHome and listGuest == sample_listGuest ):
            print("next Match get Okay")
            return True
        else:
            print("next Match get Error")
            return False

    def test_crawler_get_team_list(self):
        """It tests get_team_list Function of crawler.
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("crawler get teamlist Test:")
        nowYear_team_list = ['1. FC Köln', '1. FC Union Berlin', '1. FSV Mainz 05', 'Bayer Leverkusen', 'Borussia Dortmund', 'Borussia Mönchengladbach', 'Eintracht Frankfurt', 'FC Augsburg', 'FC Bayern', 'FC Schalke 04', 'Fortuna Düsseldorf', 'Hertha BSC', 'RB Leipzig', 'SC Freiburg', 'SC Paderborn 07', 'TSG 1899 Hoffenheim', 'VfL Wolfsburg', 'Werder Bremen']

        if self.crawler.get_team_list(self.test_nowYear)==nowYear_team_list:
            print("teamlist get Okay")
            return True
        else:
            print("teamlist get error")
            return False
        
    def test_miniAlgo_setDate(self):
        """Test for right setting of variables
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        result = True
        print("--------------------------")
        print("miniAlgo setDate Test:")
        self.miniAlgo.setDate(self.test_startYear,self.test_startDay,self.test_endYear,self.test_endDay, self.test_nowYear)
        if self.miniAlgo.startYear==self.test_startYear: print("startYear set Okay")
        else: 
            print("startYear set Error")
            result= False
        if self.miniAlgo.startDay==self.test_startDay: print("startDay set Okay")
        else: 
            print("startDay set Error")
            result= False        
        if self.miniAlgo.endYear==self.test_endYear: print("endYear set Okay")
        else: 
            print("endYear set Error")
            result= False  
        if self.miniAlgo.endDay==self.test_endDay: print("endDay set Okay")
        else: 
            print("endDay set Error")
            result= False  
        if self.miniAlgo.nowYear==self.test_nowYear: print("nowYear set Okay")
        else: 
            print("nowYear set Error")
            result= False  
        return result
    
    def test_miniAlgo_setHisto(self):
        """It tests setHisto Function of miniAlgo.
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("miniAlgo setHisto Test:")
        sample_histo=[{'1. FC Köln': [0, 0, 0, 0], '1. FC Union Berlin': [0, 0, 0, 0], '1. FSV Mainz 05': [0, 0, 0, 0], 'Bayer Leverkusen': [0, 1, 0, 0], 'Borussia Dortmund': [0, 0, 0, 1], 'Borussia Mönchengladbach': [1, 0, 0, 0], 'Eintracht Frankfurt': [1, 0, 0, 0], 'FC Augsburg': [0, 1, 0, 0], 'FC Bayern': [0, 1, 0, 0], 'FC Schalke 04': [1, 0, 0, 0], 'Fortuna Düsseldorf': [0, 1, 0, 0], 'Hertha BSC': [0, 0, 0, 0], 'RB Leipzig': [1, 0, 0, 0], 'SC Freiburg': [1, 0, 0, 0], 'SC Paderborn 07': [0, 0, 0, 0], 'TSG 1899 Hoffenheim': [1, 0, 0, 0], 'VfL Wolfsburg': [0, 1, 0, 0], 'Werder Bremen': [0, 0, 0, 0]}, {'1. FC Köln': [0, 0, 0, 0], '1. FC Union Berlin': [0, 0, 0, 0], '1. FSV Mainz 05': [0, 0, 0, 0], 'Bayer Leverkusen': [1, 0, 0, 0], 'Borussia Dortmund': [0, 0, 0, 0], 'Borussia Mönchengladbach': [1, 0, 0, 0], 'Eintracht Frankfurt': [0, 1, 0, 0], 'FC Augsburg': [1, 0, 0, 0], 'FC Bayern': [0, 0, 0, 0], 'FC Schalke 04': [1, 0, 0, 0], 'Fortuna Düsseldorf': [1, 0, 0, 0], 'Hertha BSC': [0, 1, 0, 0], 'RB Leipzig': [0, 1, 0, 0], 'SC Freiburg': [0, 1, 0, 0], 'SC Paderborn 07': [0, 0, 0, 0], 'TSG 1899 Hoffenheim': [1, 0, 0, 0], 'VfL Wolfsburg': [0, 1, 0, 0], 'Werder Bremen': [0, 1, 0, 0]}]
        self.miniAlgo.setHisto()
        if(self.miniAlgo.maxGoal==3):
            print("max goal Okay")
        else:
            print("max goal Error")
        if(self.miniAlgo.histo==sample_histo):
            print("histo set Okay")
        else:
            print("histo set Error")
        
    def test_miniAlgo_predict(self):
        """It tests predict Function of miniAlgo.
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("miniAlgo predict Test:")
        if(self.miniAlgo.predict('Bayer Leverkusen', 'RB Leipzig')==[0.0, 100.0, 0.0]):
            print("predict Okay")
        else:
            print("predict Error")
    
    def test_gui(self):
        """It tests GUI with invoke() function.  
            Args: 
            
            return: 
                bool: True if successful, false otherwise
        """
        print("--------------------------")
        print("GUI Test:")
        root = Tk()
        testGUI = gui.GUI(root)
        if(testGUI.statusIndc == 0):
            print('GUI is running')
        testGUI.startYear.set(str(2018))
        testGUI.startMatch.set(str(1)) 
        testGUI.NextOrResetBtn.invoke()
        if(testGUI.statusIndc==1):
            print('Next Button Okay ')
        else:
            print('Next Button error')
        testGUI.endYear.set(str(2018))   
        testGUI.endMatch.set(str(2))

        testGUI.crawlBtn.invoke()
        if(testGUI.status.cget("text")=='Crawling, please wait'):
            print('Crawl Button Okay')
        else:
            print('Crawl Button error')
        testGUI.crawling()
        if(testGUI.status.cget("text")== "Select Algo and Traning"):
            print('Crawling Okay in GUI')
        else:
            print('Crawling error in GUI')
        testGUI.startTrainBtn.invoke()
        if(testGUI.isTrained== True):
            print('Traing button Okay')
        else:
            print('Traing button  error')        
         
tester = Tester()
