import crawler
from tkinter import *
from tkinter import messagebox
import tkinter as tkinter1
import threading
import time
import csv
import os
import miniAlgo

now = time.gmtime(time.time()) # set now
year = now.tm_year # now year
mon = now.tm_mon #now month


    
if(mon<7): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
    league_year = year - 1
else:
    league_year = year
isTrained = False
minialgo = miniAlgo.Algorithmus(league_year)

root = Tk()
root.title('Bundesliga Prediction')
year_list = [str(league_year)]
for year in range(1,10):
    year_list.append(str(league_year-year))
team_list=["No list loaded"]

def but1onClick():
    season.configure(text= "Loading, please wait") #change the Season in the Text
    t1 = threading.Thread(target=crawling) #make Thread
    t1.daemon = True  # make as Daemon Thread
    t1.start()  # start

def dropdownChange(home, away):
    if not isTrained:
        return
    t2 = threading.Thread(target=calc(home,away)) #make Thread
    t2.daemon = True  # make as Daemon Thread
    t2.start()

def calc(home, away):
    if(home == "No list loaded" or away == "No list loaded"):
        return
    result = minialgo.predict(home, away)
    result_team1.configure(text= str(result[0])+"%")
    result_text.configure(text= str(result[1])+"%")
    result_team2.configure(text= str(result[2])+"%")
def crawling(): #
    start_year = int(tkvar3.get()) #set the Start year for Crawling
    for crawling_year in range(start_year, league_year+1): 
        crawler.crawling(crawling_year)
    team_list = crawler.get_team_list(league_year) # Save the TeamList in List
    season.configure(text= 'Bundesliga '+ str(league_year) + '/' + str(league_year+1)) #change the Season in the Text
    # reset var and delete all old options
    tkvar1.set(team_list[0])
    tkvar2.set(team_list[1])
    popupMenu1['menu'].delete(0, 'end')
    popupMenu2['menu'].delete(0, 'end')
    #reload all teams
    for team in team_list:
        popupMenu1['menu'].add_command(label=team, command=tkinter1._setit(tkvar1, team))
        popupMenu2['menu'].add_command(label=team, command=tkinter1._setit(tkvar2, team))
    btn2.config(state="normal")
    btn1.config(state="disabled")
    popupMenu3.config(state="disabled")
    

    
        
def traning():
    minialgo.setHisto()
    btn2.config(state="disabled")
    global isTrained
    isTrained = True
    calc(tkvar1.get(), tkvar2.get())
    
    crawler.getGameday()
    crawler.setGameday()
    # crawl teams for next matches
    crawler.nxtMatch(league_year)
    
    # put teams into lists
    """ for Test
    if not(os.path.isfile('nextGames' + '.csv')) or (crawler.gameday == 34):
                listHome = ['Season has ended', '-', '-', '-', '-', '-', '-', '-', '-'] # if no data initilise empty table
                listGuest = listHome
    else:
    """
    
    if True:
            listHome = []
            listGuest = []
            f = open('nextGames' +'.csv', 'r', encoding='utf-8')
            rdr = csv.reader(f)
            for line in rdr:
                listHome.append(line[1])
                listGuest.append(line[2])

    # table for tomorrows machtes
    nxtMtchs = Label(root, text='Next Matches')
    nxtMtchs.grid(row=7, column = 1)
    matchList = [0]*45
    for match in range(9):
        result = minialgo.predict(listHome[0], listGuest[0])
        Label(root, relief=RIDGE, text=listHome[match]).grid(row=8+match*2, column=0)
        Label(root,relief=RIDGE, text=listGuest[match]).grid(row=8+match*2, column=2)
        Label(root, text=str(result[0])+"%").grid(row=9+match*2, column=0)
        Label(root, text=str(result[1])+"%").grid(row=9+match*2, column=1)
        Label(root, text=str(result[2])+"%").grid(row=9+match*2, column=2)
        Label(root, text='vs.').grid(row=8 + 2*match,column=1)


    
# Set Labels
season = Label(root, text="Season : not loaded")
season.grid(row=1, column=1)
start_season = Label(root, text="Start season")
start_season.grid(row=1, column=0)
end_season = Label(root, text="End season")
end_season.grid(row=1, column=2)
now_season = Label(root, text=str(league_year))
now_season.grid(row=0, column=2)
select_Team = Label(root, text="Choose two Teams")
select_Team.grid(row = 3, column = 1)
home_Team = Label(root, text="Home")
home_Team.grid(row = 3, column = 0)
away_Team = Label(root, text="Guest")
away_Team.grid(row = 3, column = 2)


#set buttons
btn1 = Button(root, text="Crawler", command=but1onClick) # crawl
btn1.grid(row=0, column=1)
btn2 = Button(root, text="Start training", command=traning, state=DISABLED)
btn2.grid(row=2, column=1)
vstext = Label(root, text="VS")
vstext.grid(row=4, column=1)
result_text = Label(root, text="Expected results")
result_text.grid(row=5, column=1)
result_team1 = Label(root, text="not trained")
result_team1.grid(row=5, column=0)
result_team2 = Label(root, text="not trained")
result_team2.grid(row=5, column=2)


# Create a Tkinter variable
tkvar1 = StringVar(root)
tkvar2 = StringVar(root)
tkvar3 = StringVar(root)

# Dictionary with options
tkvar1.set("No list loaded") # set the default option
tkvar2.set("No list loaded") # set the default option
tkvar3.set(str(league_year)) # set the default option

popupMenu1 = OptionMenu(root, tkvar1, *team_list)
popupMenu2 = OptionMenu(root, tkvar2, *team_list)
popupMenu1.grid(row = 4, column =0)
popupMenu2.grid(row = 4, column =2)

popupMenu3 = OptionMenu(root, tkvar3, *year_list)
popupMenu3.grid(row = 0, column =0)

# on change dropdown value

def change_dropdown1(*args):
    dropdownChange(tkvar1.get(), tkvar2.get())
def change_dropdown2(*args):
    dropdownChange(tkvar1.get(), tkvar2.get())

# link function to change dropdown
tkvar1.trace('w', change_dropdown1)
tkvar2.trace('w', change_dropdown2)


root.mainloop()

