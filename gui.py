import crawler
from tkinter import *
from tkinter import messagebox
import tkinter as tkinter1
import threading


root = Tk()
root.title('Bundesliga Vorhersage')

team_list=["A List wasn't loaded"]
def but1onClick():
    season.configure(text= "Loading, wait Please") #change the Season in the Text
    t1 = threading.Thread(target=crawling) #make Thread
    t1.daemon = True  # make as Daemon Thread
    t1.start()  # start

def crawling(): #
    crawler.crawling()
    team_list = crawler.team_list # Save the TeamList in List
    season.configure(text= crawler.liga[0]) #change the Season in the Text
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
        

def traning():
    return 0

# Set Labels
season = Label(root, text="Season : it wasn't loaded")
season.grid(row=1, column=1)
select_Team = Label(root, text="Choose two Teams")
select_Team.grid(row = 3, column = 1)
home_Team = Label(root, text="Home")
home_Team.grid(row = 3, column = 0)
away_Team = Label(root, text="Away")
away_Team.grid(row = 3, column = 2)
 
#set buttons
btn1 = Button(root, text="Crawling", command=but1onClick) # crawl
btn1.grid(row=0, column=1)
btn2 = Button(root, text="Training Start", command=traning, state=DISABLED)
btn2.grid(row=2, column=1)
vstext = Label(root, text="VS")
vstext.grid(row=4, column=1)
result_text = Label(root, text="Expected results")
result_text.grid(row=5, column=1)
result_team1 = Label(root, text="it wasn't trained")
result_team1.grid(row=5, column=0)
result_team2 = Label(root, text="it wasn't trained")
result_team2.grid(row=5, column=2)

# Create a Tkinter variable
tkvar1 = StringVar(root)
tkvar2 = StringVar(root)

# Dictionary with options
tkvar1.set("A List wasn't loaded") # set the default option
tkvar2.set("A List wasn't loaded") # set the default option

popupMenu1 = OptionMenu(root, tkvar1, *team_list)
popupMenu2 = OptionMenu(root, tkvar2, *team_list)
popupMenu1.grid(row = 4, column =0)
popupMenu2.grid(row = 4, column =2)

# on change dropdown value

def change_dropdown1(*args):
    print( tkvar1.get() )
def change_dropdown2(*args):
    print( tkvar2.get() )

# link function to change dropdown
tkvar1.trace('w', change_dropdown1)
tkvar2.trace('w', change_dropdown2)

root.mainloop()

