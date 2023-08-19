# -*- coding: utf-8 -*-


!pip install requests

import requests
import pandas as pd
from .datagov_key import Searcher

import tkinter as tk
from tkinter import *
from pandastable import Table, TableModel

class MyApp(Searcher):
    def __init__(self, master,path):
        self.master = master
        master.title("OGD Data Fetcher")
        self.outpath = path
        self.lbl1 = Label(master,text='Access Government owned shareable data and information')
        self.lbl1.config(font=('helvetica', 20))
        self.lbl1.place(x=200, y=10)

        self.lbl2 = Label(master,text='Enter keyword to search \n (eg:"Pollution")')
        self.lbl2.config(font=('helvetica', 12))
        self.lbl2.place(x=300, y=100)

        self.key = Entry(master, width=20,font=('calibre',12,'normal'))
        self.key.place(x=500, y=110)

        self.lbl3 = Label(master,text='Enter Data format')
        self.lbl3.config(font=('helvetica', 12))
        self.lbl3.place(x=320, y=200)


        self.v = StringVar(master, "csv")
        self.values = {"JSON" : "json",
                  "CSV" : "csv",}
        i = 0
        for (text, value) in self.values.items():
          Radiobutton(master, text = text, variable = self.v,
          value = value).place(x=500+i, y=200)
          i+=60

        self.button1 = Button(master, text="Search", command=self.display_results)
        self.button1.place(x=480, y=300,height = 44, width = 127)


    def get_data(self):
      ##code to get data and display on new window
      try:
        choice = int(self.num.get())
        data = Searcher.getdata(self.results,self.form,choice)
        if self.form == 'json':
          df = pd.DataFrame.from_dict(data['records'])
        elif self.form == 'csv':
          df = pd.DataFrame([x.split(',') for x in (data.text).split('\n')[1:]], columns=[x for x in (data.text).split('\n')[0].split(',')])
        frame = Toplevel(self.master)
        self.table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        self.table.show()
        self.table.doExport(filename=self.outpath+"data.csv")
      except Exception as err:
        T = Label(self.master, text =err)
        T.config(font=('helvetica', 12),fg='red')
        T.place(x=690,y=500)


    def display_results(self):
      key = self.key.get()
      self.form = self.v.get()
      self.results = Searcher.search(key)
      if len(self.results) != 0:
        i = 0
        res=''
        for txt in self.results.keys():
          res += str(i) +'. '+ txt + '\n'
          i+=1
        for widgets in self.master.winfo_children():
          widgets.destroy()
        T = Text(self.master, height = 130, width = 190)
        T.pack()
        T.insert(tk.END, res)
        lbl = Label(self.master,text='Enter choice number ')
        lbl.config(font=('helvetica', 12))
        lbl.place(x=350,y=500)
        self.num = Entry(self.master, width=5,font=('calibre',12,'normal'))
        self.num.place(x=520,y=500)
        self.buttn = Button(self.master, text="Get Data", command=self.get_data)
        self.buttn.place(x=600,y=495,height = 34, width = 80)

      else:
        lbl = Label(self.master,text='No resources found. Try different key word')
        lbl.config(font=('helvetica', 12))
        lbl.place(x=420,y=400)

root = Tk()
path_to_save = 'C:/Users/Kavin/Downloads/'  #change the path
my_gui = MyApp(root,path_to_save)
root.geometry("1080x620")
root.mainloop()

