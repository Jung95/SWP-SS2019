import crawler
from tkinter import *
from tkinter import messagebox
import tkinter as tkinter1
import threading
import time
import csv
import os

now = time.gmtime(time.time()) # set now
year = now.tm_year # now year
mon = now.tm_mon #now month

if(mon<7): # if before start season, then  now month - 2 (for example now 4/2019, then liga18/19 -> url 2018, but not yet end the season, so url 2017 is loaded)
    league_year = year - 1
else:
    league_year = year

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
    return 0

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

# crawl teams for next matches
if not(os.path.isfile('nextGames' + '.csv')):
             listHome = ['Season has ended', '-', '-', '-', '-', '-', '-', '-', '-'] # if no data initilise empty table
             listGuest = listHome
else:
        listHome = []
        listGuest = []
f = open('nextGames' +'.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
        listHome.append(line[1])
        listGuest.append(line[2])
print(str(listHome))

# table for tomorrows machtes
nxtMtchs = Label(root, text='Next Matches')
nxtMtchs.grid(row=7, column = 1)

# initilise single grids
plyr1 = Label(root, relief=RIDGE, text=listHome[0])
plyr1.grid(row=8, column=0)
plyr2 = Label(root,relief=RIDGE, text=listGuest[0])
plyr2.grid(row=8, column=2)
plyr3 = Label(root, relief=RIDGE, text=listHome[1])
plyr3.grid(row=9, column=0)
plyr4 = Label(root, relief=RIDGE, text=listGuest[1])
plyr4.grid(row=9, column=2)
plyr5 = Label(root,relief=RIDGE, text=listHome[2])
plyr5.grid(row=10, column=0)
plyr6 = Label(root, relief=RIDGE,text=listGuest[2])
plyr6.grid(row=10, column=2)
plyr7 = Label(root,relief=RIDGE, text=listHome[3])
plyr7.grid(row=11, column=0)
plyr8 = Label(root, relief=RIDGE, text=listGuest[3])
plyr8.grid(row=11, column=2)
plyr9 = Label(root,relief=RIDGE, text=listHome[4])
plyr9.grid(row=12, column=0)
plyr10 = Label(root,relief=RIDGE, text=listGuest[4])
plyr10.grid(row=12, column=2)
plyr11 = Label(root,relief=RIDGE, text=listHome[5])
plyr11.grid(row=13, column=0)
plyr12 = Label(root,relief=RIDGE, text=listGuest[5])
plyr12.grid(row=13, column=2)
plyr13 = Label(root, relief=RIDGE,text=listHome[6])
plyr13.grid(row=14, column=0)
plyr14 = Label(root, relief=RIDGE,text=listGuest[6])
plyr14.grid(row=14, column=2)
plyr15 = Label(root,relief=RIDGE, text=listHome[7])
plyr15.grid(row=15, column=0)
plyr16 = Label(root,relief=RIDGE, text=listGuest[7])
plyr16.grid(row=15, column=2)
plyr17 = Label(root, relief=RIDGE,text=listHome[8])
plyr17.grid(row=16, column=0)
plyr18 = Label(root, relief=RIDGE,text=listGuest[8])
plyr18.grid(row=16, column=2)

# vs. between the two teams
cnt = 8
for v in range(1,10):
    Label(root, text='vs.').grid(row=cnt,column=1)
    cnt = cnt + 1


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
    print( tkvar1.get() )
def change_dropdown2(*args):
    print( tkvar2.get() )

# link function to change dropdown
tkvar1.trace('w', change_dropdown1)
tkvar2.trace('w', change_dropdown2)


root.mainloop()

