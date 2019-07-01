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
statusIndc = 0

# Option Lists
start_Year_list = [str(league_year)]
for year in range(1,10):
    start_Year_list.append(str(league_year-year))
start_Match_list = [str(1)]
for day in range(2,35):
    start_Match_list.append(str(day))
team_list=["No list loaded"]
end_Year_list = [str(league_year)]
end_Match_list = [str(34)]

# GUI start
root = Tk()
root.title('Bundesliga Prediction')

def makeCrawlThread():
    NextOrResetBtn.config(state="disabled")
    crawlBtn.config(state="disabled")
    endMatchMenu.config(state="disabled")
    endYearMenu.config(state="disabled")
    status.configure(text= "Crawling, please wait") #change the Season in the Text
    t1 = threading.Thread(target=crawling) #make Thread
    t1.daemon = True  # make as Daemon Thread
    t1.start()  # start
def NextOrReset():
    NextOrResetBtn.config(text="Reset")
    global end_Year_list
    global end_Match_list
    global statusIndc
    global league_year
    global year
    global startYear
    global endYearMenu
    if statusIndc==0:  # if Next
        NextOrResetBtn.configure(text="Reset")
        endYearMenu.config(state="normal")
        endMatchMenu.config(state="normal")
        startYearMenu.config(state="disabled")
        startMatchMenu.config(state="disabled")
        crawlBtn.config(state="normal")
        status.configure(text= "Set a end date, and Crawl")
        # reset var and delete all old options
        for x in range(1,league_year-int(startYear.get())+1):
            endYearMenu['menu'].add_command(label=str(league_year-x), command=tkinter1._setit(endYear, str(league_year-x)))
        endYear.set(str(league_year))
        statusIndc=1
    elif statusIndc==1:  # if Reset
        NextOrResetBtn.configure(text="Next")
        endYearMenu.config(state="disabled")
        endMatchMenu.config(state="disabled")
        startYearMenu.config(state="normal")
        startMatchMenu.config(state="normal")
        crawlBtn.config(state="disabled")
        status.configure(text= "Set a start date")
        endYearMenu['menu'].delete(0, 'end')
        endMatchMenu['menu'].delete(0, 'end')
        endYearMenu['menu'].add_command(label=str(league_year), command=tkinter1._setit(str(league_year), str(league_year))) 
        endMatchMenu['menu'].add_command(label=str(34), command=tkinter1._setit(str(34), str(34)))
        statusIndc=0
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
    algoSelMenu.config(state="normal")
    crawlBtn.config(state="disabled")
    startYearMenu.config(state="disabled")
    endYearMenu.config(state="disabled")
    startMatchMenu.config(state="disabled")
    endMatchMenu.config(state="disabled")
    status.configure(text= "Select Algo and Traning") 
       
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
        nxtMtchs.grid(row=0, column = 4)
        matchList = [0]*45
        for match in range(9):
            result = minialgo.predict(listHome[match], listGuest[match])
            Label(root, relief=RIDGE, text=listHome[match]).grid(row=1+match*2, column=3)
            Label(root,relief=RIDGE, text=listGuest[match]).grid(row=1+match*2, column=5)
            Label(root, text=str(result[0])+"%").grid(row=2+match*2, column=3)
            Label(root, text=str(result[1])+"%").grid(row=2+match*2, column=4)
            Label(root, text=str(result[2])+"%").grid(row=2+match*2, column=5)
            Label(root, text='vs.').grid(row=1 + 2*match,column=4)
    else: 
        Label(root, text='season has ended').grid(row=2, column=4)
    
# Set Labels
status = Label(root, text="Set a Start Date")
status.grid(row=0, column=1)
start_match_label = Label(root, text="Start Match")
start_match_label.grid(row=2, column=0)
end_match_label = Label(root, text="End Match")
end_match_label.grid(row=2, column=2)
start_year_label = Label(root, text="Start Year")
start_year_label.grid(row=0, column=0)
end_year_label = Label(root, text="End Year")
end_year_label.grid(row=0, column=2)
select_Team = Label(root, text="Choose two Teams")
select_Team.grid(row = 5, column = 1)
home_Team = Label(root, text="Home")
home_Team.grid(row = 5, column = 0)
away_Team = Label(root, text="Guest")
away_Team.grid(row = 5, column = 2)
vstext = Label(root, text="VS")
vstext.grid(row=6, column=1)
result_text = Label(root, text="Expected results")
result_text.grid(row=7, column=1)
result_team1 = Label(root, text="not trained")
result_team1.grid(row=7, column=0)
result_team2 = Label(root, text="not trained")
result_team2.grid(row=7, column=2)


#set buttons
NextOrResetBtn = Button(root, text="Next", command=NextOrReset) # reset
NextOrResetBtn.grid(row=1, column=1)
crawlBtn = Button(root, text="Crawl", command=makeCrawlThread, state=DISABLED) # crawl
crawlBtn.grid(row=2, column=1)
startTrainBtn = Button(root, text="Start Training", command=traning, state=DISABLED)
startTrainBtn.grid(row=4, column=1)


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
homeTeamMenu.grid(row = 6, column =0)
geustTeamMenu.grid(row = 6, column =2)

startYearMenu = OptionMenu(root, startYear, *start_Year_list)
startYearMenu.grid(row = 1, column =0)
endYearMenu = OptionMenu(root, endYear, *end_Year_list)
endYearMenu.grid(row = 1, column =2)

startMatchMenu = OptionMenu(root, startMatch, *start_Match_list)
startMatchMenu.grid(row = 3, column =0)
endMatchMenu = OptionMenu(root, endMatch, *end_Match_list)
endMatchMenu.grid(row = 3, column =2)
endYearMenu.config(state="disabled")
endMatchMenu.config(state="disabled")
# on change dropdown value
def change_dropdown1(*args):
    TeamMenuChange(hometeamVar.get(), guestteamVar.get())
def change_dropdown2(*args):
    TeamMenuChange(hometeamVar.get(), guestteamVar.get())
def setEndMatchList(*args):
    global startYear
    global startMatch
    global endYear
    global endMatch
    global endMatchMenu
    #removed all
    endMatchMenu['menu'].delete(0, 'end')
    if(startYear.get()==endYear.get()):
        for x in range(1,35-int(startMatch.get())+1):
            endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(endMatch, str(35-x)))    
    else:
        for x in range(1,35):
            endMatchMenu['menu'].add_command(label=str(35-x), command=tkinter1._setit(endMatch, str(35-x))) 

# link function to change dropdown
hometeamVar.trace('w', change_dropdown1)
guestteamVar.trace('w', change_dropdown2)
endYear.trace('w', setEndMatchList)
# menu for selecting an algorithm 
OPTIONS = [
    "Mini Algorithm", # add new algorithm names here
    ]
algo = StringVar(root) 
algo.set(OPTIONS[0]) # set the default option
algoSelMenu = OptionMenu(root, algo, *OPTIONS)
algoSelMenu.grid(row = 3, column = 1)
algoSelMenu.config(state="disabled")


root.mainloop()

