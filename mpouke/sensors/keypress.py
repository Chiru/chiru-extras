from Tkinter import *

class MyFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.go = False

        self.bind('<a>', self.showJudgments)
        self.bind('<KeyRelease-a>', self.makeChoice)
        self.pack(expand=YES, fill=BOTH)
        self.focus_force()

    def showJudgments(self, event=None):
        if self.go == False:
            self.go = True
            self.showJudgmentsA()
        else: 
            self.keepShowing()
            
    def keepShowing(self):
        print 'a key being pressed'

    def showJudgmentsA(self):
        print "key-press started"

    def makeChoice(self, event=None):
        print "choice made"
        self.go = False


mainw = Tk()
mainw.f = MyFrame(mainw)
mainw.f.grid()
mainw.mainloop()
