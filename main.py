import test.tester
import bundes.gui
from tkinter import *
import threading


def call_Tester():
    test.tester.Tester()

test_Thread = threading.Thread(target=call_Tester) #make Thread
test_Thread.daemon = True  # make as Daemon Thread
test_Thread.start()  # start Thread

root = Tk()
my_gui = bundes.gui.GUI(root)
root.mainloop()



