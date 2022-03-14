import dash_bootstrap_components as dbc
from dash import html
import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def formatter_2_decimals(x):
	return "{:.2f}".format(x)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def uf_show_msg(sContent):
    mag= tk.messagebox.showwarning("warning ", sContent)			



def uf_is_empty(sValue):

    if isinstance(sValue, list) :
        if len(sValue) == 0:
            sValue = None

    if sValue is not None and not isinstance(sValue, str):
        sValue = str(sValue)
    
    if sValue is not None and sValue != "" and len(sValue)>0 :    
        return False
    else:
        return True    