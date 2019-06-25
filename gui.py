import crawler
from tkinter import *
from tkinter import messagebox
import tkinter as tkinter1
import threading
import time
import csv
import os
import miniAlgo
import tester

# Global variables
now = time.gmtime(time.time()) # set now
year = now.tm_year # now year
mon = now.tm_mon #now month
if(mon<7): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
    league_year = year - 1
else:
    league_year = year
isTrained = False
minialgo = miniAlgo.Algorithmus()

# Option Lists
year_list = [str(league_year)]
for year in range(1,10):
    year_list.append(str(league_year-year))
day_list = [str(1)]
for day in range(2,35):
    day_list.append(str(day))
team_list=["No list loaded"]

# GUI start
root = Tk()
root.title('Bundesliga Prediction')

def makeCrawlThread():
    season.configure(text= "Loading, please wait") #change the Season in the Text
    t1 = threading.Thread(target=crawling) #make Thread
    t1.daemon = True  # make as Daemon Thread
    t1.start()  # start

def TeamMenuChange(home, away):
    if not isTrained:
        return
    t2 = threading.Thread(target=startChoosnAlgo()) #make Thread
    t2.daemon = True  # make as Daemon Thread
    t2.start()

def startChoosnAlgo():
    """ calls function of the choosen algorithm 

    args:
        home (sting): home team
        away (string): guest team
    
    """
    if(algo.get() == "Mini Algorithm"): # add more algorithm function calls here
        calcPrep()

def calcPrep():
    """Creates histogram for training mini algorithm
    """
    minialgo.setDate(int(startYear.get()), int(startMatch.get()), int(endYear.get()), int(endMatch.get()), league_year)
    minialgo.setHisto()
    calc(hometeamVar.get(), guestteamVar.get())

def calc(home, away):
    """Calcualte winning chances with minialgo

    args:
        home (string): home team
        away (string): guest team
    """
    if(home == "No list loaded" or away == "No list loaded"):
        return
    print(home)
    print(away)
    result = minialgo.predict(home, away)
    result_team1.configure(text= str(result[0])+"%")
    result_text.configure(text= str(result[1])+"%")
    result_team2.configure(text= str(result[2])+"%")
    
def crawling():
    """Crawl selected game results and save team names in dropdown menues

    """
    crawler.crawling(int(startYear.get()),int(startMatch.get()),int(endYear.get()),int(endMatch.get()))
    tester.crawlTest(int(startYear.get()),int(startMatch.get()),int(endYear.get()),int(endMatch.get()))
    
    team_list = crawler.get_team_list(league_year) # Save the TeamList in List
    season.configure(text= 'Bundesliga '+ str(league_year) + '/' + str(league_year+1)) #change the Season in the Text
    # reset var and delete all old options
    hometeamVar.set(team_list[0])
    guestteamVar.set(team_list[1])
    homeTeamMenu['menu'].delete(0, 'end')
    geustTeamMenu['menu'].delete(0, 'end')
    #reload all teams
    for team in team_list:
        homeTeamMenu['menu'].add_command(label=team, command=tkinter1._setit(hometeamVar, team))
        geustTeamMenu['menu'].add_command(label=team, command=tkinter1._setit(guestteamVar, team))
    startTrainBtn.config(state="normal")
    crwalBtn.config(state="disabled")
    startYearMenu.config(state="disabled")
    endYearMenu.config(state="disabled")
    startMatchMenu.config(state="disabled")
    endMatchMenu.config(state="disabled")
       
def traning():
    startTrainBtn.config(state="disabled")
    global isTrained
    wasEnded = False
    isTrained = True
    
    # aktivate choosen algorithm
    startChoosnAlgo()
    
    # crawl teams for next matches
    crawler.nxtMatch(league_year)
    
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
        nxtMtchs = Label(root, text='Next Matches')
        nxtMtchs.grid(row=7, column = 1)
        matchList = [0]*45
        for match in range(9):
            result = minialgo.predict(listHome[match], listGuest[match])
            Label(root, relief=RIDGE, text=listHome[match]).grid(row=8+match*2, column=0)
            Label(root,relief=RIDGE, text=listGuest[match]).grid(row=8+match*2, column=2)
            Label(root, text=str(result[0])+"%").grid(row=9+match*2, column=0)
            Label(root, text=str(result[1])+"%").grid(row=9+match*2, column=1)
            Label(root, text=str(result[2])+"%").grid(row=9+match*2, column=2)
            Label(root, text='vs.').grid(row=8 + 2*match,column=1)
    else: 
        Label(root, text='season has ended').grid(row= 9, column=1)
    
# Set Labels
season = Label(root, text="Season : not loaded")
season.grid(row=1, column=1)
start_season = Label(root, text="Start Match")
start_season.grid(row=2, column=0)
end_season = Label(root, text="End Match")
end_season.grid(row=2, column=2)
select_Team = Label(root, text="Choose two Teams")
select_Team.grid(row = 3, column = 1)
home_Team = Label(root, text="Home")
home_Team.grid(row = 3, column = 0)
away_Team = Label(root, text="Guest")
away_Team.grid(row = 3, column = 2)


#set buttons
crwalBtn = Button(root, text="Crawler", command=makeCrawlThread) # crawl
crwalBtn.grid(row=0, column=1)
startTrainBtn = Button(root, text="Start Training", command=traning, state=DISABLED)
startTrainBtn.grid(row=2, column=1)
vstext = Label(root, text="VS")
vstext.grid(row=4, column=1)
result_text = Label(root, text="Expected results")
result_text.grid(row=5, column=1)
result_team1 = Label(root, text="not trained")
result_team1.grid(row=5, column=0)
result_team2 = Label(root, text="not trained")
result_team2.grid(row=5, column=2)

# Create a Tkinter variable
hometeamVar = StringVar(root) #home team
guestteamVar = StringVar(root) #away team
startYear = StringVar(root) #start year 
endYear = StringVar(root) #end  year
startMatch = StringVar(root) #start match day
endMatch = StringVar(root) #end match day

# Dictionary with options
hometeamVar.set("No list loaded") # set the default option
guestteamVar.set("No list loaded") # set the default option
startYear.set(str(league_year)) # set the default option
endYear.set(str(league_year)) # set the default option
startMatch.set(str(1)) # set the default option
endMatch.set(str(34)) # set the default option

homeTeamMenu = OptionMenu(root, hometeamVar, *team_list)
geustTeamMenu = OptionMenu(root, guestteamVar, *team_list)
homeTeamMenu.grid(row = 4, column =0)
geustTeamMenu.grid(row = 4, column =2)

startYearMenu = OptionMenu(root, startYear, *year_list)
startYearMenu.grid(row = 0, column =0)
endYearMenu = OptionMenu(root, endYear, *year_list)
endYearMenu.grid(row = 0, column =2)

startMatchMenu = OptionMenu(root, startMatch, *day_list)
startMatchMenu.grid(row = 1, column =0)
endMatchMenu = OptionMenu(root, endMatch, *day_list)
endMatchMenu.grid(row = 1, column =2)

# on change dropdown value
def change_dropdown1(*args):
    TeamMenuChange(hometeamVar.get(), guestteamVar.get())
def change_dropdown2(*args):
    TeamMenuChange(hometeamVar.get(), guestteamVar.get())

# link function to change dropdown
hometeamVar.trace('w', change_dropdown1)
guestteamVar.trace('w', change_dropdown2)

# menu for selecting an algorithm 
OPTIONS = [
    "Mini Algorithm", # add new algorithm names here
    ]
algo = StringVar(root) 
algo.set(OPTIONS[0]) # set the default option
algoSelMenu = OptionMenu(root, algo, *OPTIONS)
algoSelMenu.grid(row = 3, column = 1)



root.mainloop()

