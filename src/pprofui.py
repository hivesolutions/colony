#!/usr/bin/env python
# Python Profiler User Interface
# By Brent Burley, 2004, erburley@charter.net
# This software is placed into the public domain

#Reduced font size, added horizontal scroll bars: Drew Gulino, 2005
#Added support for python 2.5, thanks to David Ross, 2007 

from Tkinter import *
import sys, string, re, cStringIO, pstats
skip_re = re.compile(r'(Ordered by|List reduced|^\s*$)')
func_re = re.compile(r'(<?\w+>?:\d+\([^()]+(?:\(\))?\))')
def ignore(e): return "break"

class Profile(Frame):
    def __init__(self, filename, parent=None):
        # main frame
        Frame.__init__(self, parent)
        font = ('Courier', 9)

        # create '_callers' listbox
        f = Frame(self)
        f.pack(expand=YES, fill=BOTH)
        vscroll = Scrollbar(f, orient=VERTICAL)
        hscroll = Scrollbar(f, orient=HORIZONTAL)
        self._callers = Listbox(f, yscrollcommand=vscroll.set, xscrollcommand=hscroll.set,font=font)
        hscroll.config(command=self._callers.xview)
        hscroll.pack(side=BOTTOM, fill=BOTH)
        vscroll.configure(command=self._callers.yview)
        vscroll.pack(side=RIGHT, fill=BOTH)        
        self._callers.pack(side=RIGHT, expand=YES, fill=BOTH)
        self._callers.bind('<Button-1>',
                           lambda e, s=self: s.choose(e, s._callers))
        self._callers.bind('<ButtonRelease-1>', ignore)
        self._callers.bind('<B1-Motion>', ignore)

        # create '_callees' listbox
        f = Frame(self)
        f.pack(expand=YES, fill=BOTH)
        vscroll = Scrollbar(f, orient=VERTICAL)
        hscroll = Scrollbar(f, orient=HORIZONTAL)
        self._callees = Listbox(f, yscrollcommand=vscroll.set, xscrollcommand=hscroll.set, font=font)
        hscroll.config(command=self._callees.xview)
        hscroll.pack(side=BOTTOM, fill=BOTH)
        vscroll.configure(command=self._callees.yview)
        vscroll.pack(side=RIGHT, fill=BOTH)        
        self._callees.pack(side=RIGHT, expand=YES, fill=BOTH)
        self._callees.bind('<Button-1>', 
                           lambda e, s=self: s.choose(e, s._callees))
        self._callees.bind('<ButtonRelease-1>', ignore)
        self._callees.bind('<B1-Motion>', ignore)

        # button frame
        f = Frame(self)

        # list all
        self._listall = Button(f, text='List All', command=self.listall)
        self._listall.pack(side=LEFT)

        # create sort menu
        f.pack(expand=NO, fill=X)
        self._sorted = Button(f)
        self._sorted.pack(side=LEFT)
        self._sortMenu = m = Menu(self, tearoff=0)
        self._sorted.bind("<Button-1>", self.popupSortMenu)
        opts = 'time cumulative calls file line module name nfl pcalls stdname'
        for o in string.split(opts):
            m.add_command(label=o,
                          command=lambda s=self,o=o: s.sort(o))

        # close button
        self._close = Button(f, text="Close", command=self.quit)
        self._close.pack(side=RIGHT)

        # load stats
        self.setFilename(filename)

    def setFilename(self, filename):
        self._stream = cStringIO.StringIO()
        try:
            self._stats = stats = pstats.Stats(filename, stream=self._stream)
        except TypeError:
            self._stats = stats = pstats.Stats(filename)
#        stats.strip_dirs()
        self.sort('cumulative')

    def listall(self):
        self._callees.delete(0,END)
        self.setStats(self._callers, self._stats.print_stats)

    def popupSortMenu(self, e):
        self._sortMenu.tk_popup(e.x_root, e.y_root)
        return "break"

    def sort(self, type):
        self._stats.sort_stats(type)
        self._sorted['text'] = 'sort: ' + type
        self._callees.delete(0,END)
        self._callees.insert(END, 'Click on an entry display callers/callees')
        self.setStats(self._callers, self._stats.print_stats)

    def setStats(self, list, func, *args):
        list.delete(0,END)
        self._stream.reset()
        self._stream.truncate()
        sys.stdout = self._stream
        apply(func, args)
        for l in string.split(sys.stdout.getvalue(), '\n'):
            if skip_re.search(l): continue
            list.insert(END, l)
        sys.stdout = sys.__stdout__

    def choose(self, e, list):
        text = list.get(list.nearest(e.y))
        try: fn = func_re.findall(text)[-1]
        except IndexError: return
        fn = re.escape(fn)
        self.setStats(self._callees, self._stats.print_callees, fn)
        self.setStats(self._callers, self._stats.print_callers, fn)
        return "break"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: pprofui.py <stats file>'
        sys.exit(1)
    stats = sys.argv[1]

    top = Tk()
    p = Profile(stats, top)
    p.master.title('Python Profile: ' + stats)
    p.pack(expand=YES, fill=BOTH)
    top.geometry('800x600+200+200')
    mainloop()
