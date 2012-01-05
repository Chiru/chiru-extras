from Tkinter import *

class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # method call counter
        self.pack()
        self.afterId = None
        root.bind('<KeyPress-a>', self.key_press)
        root.bind('<KeyRelease-a>', self.key_release)
        
    def key_press(self, event):
        if self.afterId != None:
            self.after_cancel( self.afterId )
            self.afterId = None
        else:
            print 'key pressed %s' % event.time

    def key_release(self, event):
        self.afterId = self.after_idle( self.process_release, event )

    def process_release(self, event):
        print 'key release %s' % event.time
        self.afterId = None

        
        
root = Tk()
root.geometry("400x30+0+0")
app1 = MyFrame(root)
root.mainloop()
