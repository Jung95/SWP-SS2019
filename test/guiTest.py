import sys
import os
import getBundes
from tkinter import *
import gui

root = Tk()
testGUI = gui.GUI(root)
if(testGUI.statusIndc == 0):
    print('GUI is running')
testGUI.startYear.set(str(2018))
testGUI.startMatch.set(str(1)) 
testGUI.NextOrResetBtn.invoke()
if(testGUI.statusIndc==1):
    print('Okay in Next Btn')
else:
    print('error in Next Btn')
testGUI.endYear.set(str(2018))   
testGUI.endMatch.set(str(1))

testGUI.crawlBtn.invoke()
if(testGUI.status.cget("text")=='Crawling, please wait'):
    print('Okay in Crawl Btn')
else:
    print('error in Crawl Btn')
testGUI.crawling()
if(testGUI.status.cget("text")== "Select Algo and Traning"):
    print('Okay in Crawling ')
else:
    print('error in Crawling')
testGUI.startTrainBtn.invoke()
if(testGUI.isTrained== True):
    print('Okay in Traing')
else:
    print('error in Traing')
