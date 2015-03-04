#!/usr/bin/python
# -*- coding: utf-8 -*-
########################################################################################################################
# Joe's Python Experimente - wxPython Test mit Python2
#-----------------------------------------------------------------------------------------------------------------------
# \file       Py2wxTest.py
# \creation   2015-03-04, Joe Merten
#-----------------------------------------------------------------------------------------------------------------------
# Basierend auf Beispielcode von Jan Bodnar, ZetCode wxPython Tutorial, http://zetcode.com/wxpython/gdi
# Prerequisites: install wxpython: sudo apt-get install python-wxgtk2.8
#
# Fazit:
# - sobald app.MainLoop() läuft, reagiert das Skript nicht mehr auf Signale
# - Multithreading habe ich nicht zusammen mit Python2 & wxPython getestet
# - Utf-8 (auch Codepoints >64k) kommen sauber bis zu GUI durch, egal ob im Source als Stringliteral oder via Kommandozeile übergeben
########################################################################################################################

import sys
import signal
import time
import wx


class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(250, 150))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.Show()

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        #bmp = wx.Bitmap('/tmp/Vistra-St10.png')
        #dc.DrawBitmap(bmp, 0, 0, True)
        dc.DrawLine(50, 60, 190, 60)
        dc.SetBrush(wx.Brush('#c56c00'))
        dc.DrawRectangle(10, 15, 90, 60)


def signalHandler(signum, frame):
    print('Signal handler called with signal', signum)

def setSignalHandlers():
    signal.signal(signal.SIGALRM, signalHandler)
    signal.signal(signal.SIGUSR1, signalHandler)
    signal.signal(signal.SIGUSR2, signalHandler)


if __name__ == '__main__':
    setSignalHandlers()
    #while True: time.sleep(1)
    app = wx.App()
    title = 'Hello 𝘑𝘰𝘦 😎'
    if len(sys.argv) >=2: title += " (" + sys.argv[1] + ")"
    Example(None, title)
    app.MainLoop()
