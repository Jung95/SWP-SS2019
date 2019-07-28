import crawler
from tkinter import *
import tkinter as tkinter1
import threading
import time
import csv
import os
import miniAlgo
import poisson

class GUI:
    def __init__(self, root):
        self.root = root
        # Global variables
        self.crawler = crawler.Crawler()
        self.minialgo = miniAlgo.Algorithmus()
        self.now = time.gmtime(time.time()) # set now
        self.year = self.now.tm_year # now year
        if(self.crawler.actualMatchday==1): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
            self.league_year = self.year - 1
        else:
            self.league_year = self.year
        self.isTrained = False

        self.statusIndc = 0

        # Option Lists
        self.start_Year_list = [str(self.league_year)]
        for self.year in range(1,10):
            self.start_Year_list.append(str(self.league_year-self.year))
        self.start_Match_list = [str(1)]
        for self.day in range(2,self.crawler.actualMatchday):
            self.start_Match_list.append(str(self.day))
        self.team_list=["No list loaded"]
        self.end_Year_list = [str(self.league_year)]
        self.end_Match_list = [str(34)]
         # Set Labels
        self.status = Label(root, text="Set a Start Date")
        self.status.grid(row=0, column=1)
        self.start_match_label = Label(root, text="Start Match")
        self.start_match_label.grid(row=2, column=0)
        self.end_match_label = Label(root, text="End Match")
        self.end_match_label.grid(row=2, column=2)
        self.start_year_label = Label(root, text="Start Year")
        self.start_year_label.grid(row=0, column=0)
        self.end_year_label = Label(root, text="End Year")
        self.end_year_label.grid(row=0, column=2)
        self.select_Team = Label(root, text="Choose two Teams")
        self.select_Team.grid(row = 5, column = 1)
        self.home_Team = Label(root, text="Home")
        self.home_Team.grid(row = 5, column = 0)
        self.away_Team = Label(root, text="Guest")
        self.away_Team.grid(row = 5, column = 2)
        self.vstext = Label(root, text="VS")
        self.vstext.grid(row=6, column=1)
        self.result_text = Label(root, text="Expected results")
        self.result_text.grid(row=7, column=1)
        self.result_team1 = Label(root, text="not trained")
        self.result_team1.grid(row=7, column=0)
        self.result_team2 = Label(root, text="not trained")
        self.result_team2.grid(row=7, column=2)


        #set buttons
        self.NextOrResetBtn = Button(root, text="Next", command=self.NextOrReset) # reset
        self.NextOrResetBtn.grid(row=1, column=1)
        self.crawlBtn = Button(root, text="Crawl", command=self.makeCrawlThread, state=DISABLED) # crawl
        self.crawlBtn.grid(row=2, column=1)
        self.startTrainBtn = Button(root, text="Start Training", command=self.traning, state=DISABLED)
        self.startTrainBtn.grid(row=4, column=1)


        # Create a Tkinter variable
        self.hometeamVar = StringVar(root) #home team
        self.guestteamVar = StringVar(root) #away team
        self.startYear = StringVar(root) #start year 
        self.endYear = StringVar(root) #end  year
        self.startMatch = StringVar(root) #start match day
        self.endMatch = StringVar(root) #end match day

        # Dictionary with options
        self.hometeamVar.set("No list loaded") # set the default option
        self.guestteamVar.set("No list loaded") # set the default option
        self.startYear.set(str(self.league_year)) # set the default option
        self.endYear.set(str(self.league_year)) # set the default option
        self.startMatch.set(str(1)) # set the default option
        if(self.crawler.actualMatchday==1):
            self.endMatch.set(str(34)) # set the default option
        else:
            self.endMatch.set(str(self.crawler.actualMatchday-1))

        self.homeTeamMenu = OptionMenu(root, self.hometeamVar, *self.team_list)
        self.geustTeamMenu = OptionMenu(root, self.guestteamVar, *self.team_list)
        self.homeTeamMenu.grid(row = 6, column =0)
        self.geustTeamMenu.grid(row = 6, column =2)
        self.homeTeamMenu.config(state="disabled")
        self.geustTeamMenu.config(state="disabled")
        self.startYearMenu = OptionMenu(root, self.startYear, *self.start_Year_list)
        self.startYearMenu.grid(row = 1, column =0)
        self.endYearMenu = OptionMenu(root, self.endYear, *self.end_Year_list)
        self.endYearMenu.grid(row = 1, column =2)

        self.startMatchMenu = OptionMenu(root, self.startMatch, *self.start_Match_list)
        self.startMatchMenu.grid(row = 3, column =0)
        self.endMatchMenu = OptionMenu(root, self.endMatch, *self.end_Match_list)
        self.endMatchMenu.grid(row = 3, column =2)
        self.endYearMenu.config(state="disabled")
        self.endMatchMenu.config(state="disabled")
        
    # link function to change dropdown
        self.hometeamVar.trace('w', self.change_dropdown1)
        self.guestteamVar.trace('w', self.change_dropdown2)
        self.startYear.trace('w', self.setStartMatchList)
        self.endYear.trace('w', self.setEndMatchList)
        # menu for selecting an algorithm 
        self.OPTIONS = [
            "Mini Algorithm", # add new algorithm names here
            "Poisson"
            ]
        self.algo = StringVar(root) 
        self.algo.set(self.OPTIONS[0]) # set the default option
        self.algoSelMenu = OptionMenu(root, self.algo, *self.OPTIONS)
        self.algoSelMenu.grid(row = 3, column = 1)
        self.algoSelMenu.config(state="disabled")
        # GUI start

        self.root.title('Bundesliga Prediction')
        # on change dropdown value
    def change_dropdown1(self, *args):
        self.TeamMenuChange(self.hometeamVar.get(), self.guestteamVar.get())
    def change_dropdown2(self, *args):
        self.TeamMenuChange(self.hometeamVar.get(), self.guestteamVar.get())
    def setStartMatchList(self, *args):
        self.startMatch.set(str(1)) # set the default option
        self.startMatchMenu['menu'].delete(0, 'end')
        if(int(self.startYear.get())==self.league_year):
            for x in range(1,self.crawler.actualMatchday):
                self.startMatchMenu['menu'].add_command(label=str(x), command=tkinter1._setit(self.startMatch, str(35-x)))   
        else:
            for x in range(1,35):
                self.startMatchMenu['menu'].add_command(label=str(x), command=tkinter1._setit(self.startMatch, str(x))) 
            
    def setEndMatchList(self, *args):
        #removed all
        self.endMatchMenu['menu'].delete(0, 'end')
        if(int(self.endYear.get())==self.league_year and self.crawler.actualMatchday != 1):
            self.endMatch.set(str(self.crawler.actualMatchday-1)) # set the default option
            if(self.startYear.get()==self.endYear.get()):
                for x in range(36-self.crawler.actualMatchday,35-int(self.startMatch.get())+1):
                    self.endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(self.endMatch, str(35-x)))    
            else:
                for x in range(36-self.crawler.actualMatchday,35):
                    self.endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(self.endMatch, str(35-x)))
        else:
            self.endMatch.set(str(34))
            if(self.startYear.get()==self.endYear.get()):
                for x in range(1,35-int(self.startMatch.get())+1):
                    self.endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(self.endMatch, str(35-x)))    
            else:
                for x in range(1,35):
                    self.endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(self.endMatch, str(35-x))) 

             


    def makeCrawlThread(self):
        self.NextOrResetBtn.config(state="disabled")
        self.crawlBtn.config(state="disabled")
        self.endMatchMenu.config(state="disabled")
        self.endYearMenu.config(state="disabled")
        self.status.configure(text= "Crawling, please wait") #change the Season in the Text
        t1 = threading.Thread(target=self.crawling) #make Thread
        t1.daemon = True  # make as Daemon Thread
        t1.start()  # start
    def NextOrReset(self):
        self.NextOrResetBtn.config(text="Reset")
        if self.statusIndc==0:  # if Next
            self.NextOrResetBtn.configure(text="Reset")
            self.endYearMenu.config(state="normal")
            self.endMatchMenu.config(state="normal")
            self.startYearMenu.config(state="disabled")
            self.startMatchMenu.config(state="disabled")
            self.crawlBtn.config(state="normal")
            self.status.configure(text= "Set a end date, and Crawl")
            # reset var and delete all old options
            self.endYearMenu['menu'].delete(0, 'end')
            for x in range(0,self.league_year-int(self.startYear.get())+1):
                self.endYearMenu['menu'].add_command(label=str(self.league_year-x), command=tkinter1._setit(self.endYear, str(self.league_year-x)))
            self.endYear.set(str(self.league_year))
            self.statusIndc=1
        elif self.statusIndc==1:  # if Reset
            self.NextOrResetBtn.configure(text="Next")
            self.endYearMenu.config(state="disabled")
            self.endMatchMenu.config(state="disabled")
            self.startYearMenu.config(state="normal")
            self.startMatchMenu.config(state="normal")
            self.crawlBtn.config(state="disabled")
            self.status.configure(text= "Set a start date")
            self.endYearMenu['menu'].delete(0, 'end')
            self.endMatchMenu['menu'].delete(0, 'end')
            self.endYearMenu['menu'].add_command(label=str(self.league_year), command=tkinter1._setit(str(self.league_year), str(self.league_year))) 
            self.endMatchMenu['menu'].add_command(label=str(34), command=tkinter1._setit(str(34), str(34)))
            self.statusIndc=0
    def TeamMenuChange(self,home, away):
        if not self.isTrained:
            return
        t2 = threading.Thread(target=self.startChoosnAlgo()) #make Thread
        t2.daemon = True  # make as Daemon Thread
        t2.start()

    def startChoosnAlgo(self):
        """ calls function of the choosen algorithm 

        args:
            home (sting): home team
            away (string): guest team
            
        """
        if(self.algo.get() == "Mini Algorithm"): # add more algorithm function calls here
            self.calcPrep()
        if(self.algo.get() == "Poisson"):
            model = poisson.fit_data(int(self.startYear.get()), int(self.startMatch.get()), int(self.endYear.get()), int(self.endMatch.get()))
            result = poisson.simulate_match(model, homeTeam = self.hometeamVar.get(), awayTeam = self.guestteamVar.get())
            self.result_team1.configure(text= str(result[0])+"%")
            self.result_text.configure(text= str(result[1])+"%")
            self.result_team2.configure(text= str(result[2])+"%")

    def calcPrep(self):
        """Creates histogram for training mini algorithm
        """
        self.minialgo.setDate(int(self.startYear.get()), int(self.startMatch.get()), int(self.endYear.get()), int(self.endMatch.get()), self.league_year)
        self.minialgo.setHisto()
        self.calc(self.hometeamVar.get(), self.guestteamVar.get())

    def calc(self, home, away):
        """Calcualte winning chances with minialgo

        args:
            home (string): home team
            away (string): guest team
        """
        if(home == "No list loaded" or away == "No list loaded"):
            return
        result = self.minialgo.predict(home, away)
        self.result_team1.configure(text= str(result[0])+"%")
        self.result_text.configure(text= str(result[1])+"%")
        self.result_team2.configure(text= str(result[2])+"%")
            
    def crawling(self):
        """Crawl selected game results and save team names in dropdown menues

        """
        self.crawler.crawling(int(self.startYear.get()),int(self.startMatch.get()),int(self.endYear.get()),int(self.endMatch.get()))

            
        team_list = self.crawler.get_team_list(self.league_year) # Save the TeamList in List

            # reset var and delete all old options
        self.hometeamVar.set(team_list[0])
        self.guestteamVar.set(team_list[1])
        self.homeTeamMenu['menu'].delete(0, 'end')
        self.geustTeamMenu['menu'].delete(0, 'end')
            #reload all teams
        for team in team_list:
            self.homeTeamMenu['menu'].add_command(label=team, command=tkinter1._setit(self.hometeamVar, team))
            self.geustTeamMenu['menu'].add_command(label=team, command=tkinter1._setit(self.guestteamVar, team))
        self.startTrainBtn.config(state="normal")
        self.algoSelMenu.config(state="normal")
        self.crawlBtn.config(state="disabled")
        self.startYearMenu.config(state="disabled")
        self.endYearMenu.config(state="disabled")
        self.startMatchMenu.config(state="disabled")
        self.endMatchMenu.config(state="disabled")
        self.status.configure(text= "Select Algo and Traning") 
            
    def traning(self):
        self.startTrainBtn.config(state="disabled")
        wasEnded = False
        self.isTrained = True
            
            # aktivate choosen algorithm
        self.startChoosnAlgo()
            
            # crawl teams for next matches
        self.crawler.nxtMatch(self.league_year)
            
            # put teams into lists

        if not(os.path.isfile('nextGames' + '.csv')):
            listHome = ['Season has ended', '-', '-', '-', '-', '-', '-', '-', '-'] # if no data initilise empty table
            listGuest = listHome
            wasEnded = True
        else:
            listHome = []
            listGuest = []
            f = open('nextGames' +'.csv', 'r', encoding='utf-8')
            rdr = csv.reader(f)
            for line in rdr:
                listHome.append(line[1])
                listGuest.append(line[2])

            # table for tomorrows machtes with winning chances
            if not wasEnded:
                nxtMtchs = Label(self.root, text='Next Matches')
                nxtMtchs.grid(row=0, column = 4)
                matchList = [0]*45
                for match in range(9):
                    if(self.algo.get() == "Mini Algorithm"):
                        result = self.minialgo.predict(listHome[match], listGuest[match])
                    if(self.algo.get() == "Poisson"):
                        result = [0]*3
                    Label(self.root, relief=RIDGE, text=listHome[match]).grid(row=1+match*2, column=3)
                    Label(self.root,relief=RIDGE, text=listGuest[match]).grid(row=1+match*2, column=5)
                    Label(self.root, text=str(result[0])+"%").grid(row=2+match*2, column=3)
                    Label(self.root, text=str(result[1])+"%").grid(row=2+match*2, column=4)
                    Label(self.root, text=str(result[2])+"%").grid(row=2+match*2, column=5)
                    Label(self.root, text='vs.').grid(row=1 + 2*match,column=4)
            else: 
                Label(self.root, text='season has ended').grid(row=2, column=4)
        self.homeTeamMenu.config(state="normal")
        self.geustTeamMenu.config(state="normal")            
       


