# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:20:54 2020

@author: lucab
"""

import pdftotext
from datetime import datetime
import pandas as pd
import sys

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000

#print("Welcome! This app is intended to get financial data from companies in trimestral relatories (PDF)")
#print("and tranform this information into Data Frames, being able to export them as CSV files.")
#print("\n")
#print("To start, please:")

def main():
    
    
    
    filename = "ITRweg1T2019" #insert only the file name whithout the extension
    filename = filename.strip()
    filename += ".pdf" 
    folderpath = "C:\\Users\\lucab\\OneDrive\\A&M\\DemonstrativosFinanceiros\\PDF\\weg2019" #insert the folder path where the pdf is:
    folderpath = folderpath.strip()
    pages = [6] #input the number of the pages in which the tablesheet is (list): 
    filepath = folderpath + "\\" + filename
    
    listofpagetxt = read(filepath, pages)
    #print(listofpagetxt)
    pagelsts = txtorganizerinlst(listofpagetxt)
    #print(pagelsts)
    table = cleanheaderandfooter(pagelsts)
    print(table)
    perioddirty = perio(pagelsts)
    label = extractlabel(table)
    code =  extractcode(table)
    period = cleanperiod(perioddirty)
    values = extractvalues(table)
    print(values)
    #print(len(values),len(code),len(label))
    dictionary = createdict(label, code, period, values)
    #print(dictionary)
    dataframe = createdataframe(dictionary)
    
    
    print (dataframe)
    flag = True
    while flag == True:
        answer = input("do you wish to export your Data in a CSV format? (Answer Yes or No) ") .lower()
        answer = answer.strip()
        if answer == "yes":
            exportcsv(dataframe)
            print("file sucssessfully exported!")
            flag = False
        elif answer == "no":
            flag = False
        else:
            print("invalid input")
            flag = True
   
    
    flag = True
    while flag == True:
        answer2 = input("Do you wish to make another Data Frame? (Answer Yes or No) ") .lower()
        answer2 = answer2.strip()
        if answer2 == "yes":
            flag = False
            main()
        elif answer2 == "no":
            while flag == True:
                answer3 = input("Do you wish to exit? (Answer Yes or No) ") .lower()
                answer3 = answer3.strip()
                if answer3 == "yes":
                    flag == False
                    sys.exit()
                elif answer3 == "no":
                    flag == False
                    main()
                else:
                    print("invalid input")
                    flag == True
        else:
            print("invalid input")
            flag = True
                        
        
        
    
def read(filepath,pages):

    listofpagen = []
    listofpagetxt = []
    with open (filepath, "rb") as infile:
        pdfread = pdftotext.PDF(infile)
        for i in range (0,len(pages),1):
            page = pages[i]
            listofpagen += [page]
            
        for i in range (0,len(listofpagen),1):
            pagetext = pdfread[listofpagen[i]-1]
            listofpagetxt += [pagetext.split("\n")]
            
        return listofpagetxt
                
def txtorganizerinlst(listofpagetxt):
    pagelsts = []
    for i in range (0,len(listofpagetxt),1):
        pagelnlst = []
        for j in range(0,len(listofpagetxt[i]),1):
            linelst = listofpagetxt[i][j].split()
            if linelst != []:
                pagelnlst += [linelst]
        pagelsts += pagelnlst
    
    return pagelsts

def cleanheaderandfooter(pagelsts):
    table = []
    for i in range (0,len(pagelsts),1):
        try:
            new = ""
            test = pagelsts[i][0]
            for j in range(0,len(test),1):
                if test[j] != ".":
                    new += test [j]
            int(new)
        except:
            pass
        else:
            table += [pagelsts[i]]
    return table


    
def perio(pagelsts):
    period = []
    for i in range (0,len(pagelsts),1):
        for j in range(0,len(pagelsts[i]),1):
            test = ""
            if len(pagelsts[i][j]) == 10:
                for l in range (0,len(pagelsts[i][j]),1):
                    if pagelsts[i][j][l] != "/":
                        test += pagelsts[i][j][l]
                try:
                    int(test)
                except:
                    pass
                else:
                    if pagelsts[i] not in period:
                        period += [pagelsts[i]]
                        
                        
    
    return period

    
def extractlabel(table):
    x = 0
    for j in range(len(table[1])-1,-1,-1):
        valued = table[1][j]
        valuelst = valued.split(".")
        value = ""
        for h in range(0,len(valuelst),1):
            value += str(valuelst[h])
        try:
            value = int(value)
        except:
            break
        else:
            x += 1
    
    lst = []
    for i in range (0, len(table),1):
        label = ""
        for j in range(1,len(table[i])-x,1):
            label += " " + table[i][j]
        lst += [label.strip()]
    return lst

def extractcode(table):
    lst = []
    for i in range(0,len(table),1):
        lst += [table[i][0]]
    return lst
    
def cleanperiod(period):
    lst = []
    for i in range(0,len(period),1):
        for j in range (0,len(period[i]),1):
            test = ""
            for l in range (0, len(period[i][j]),1):
                if period[i][j][l] != "/":
                    test += period[i][j][l]
            try:
                int(test)
            except:
                pass
            else:
                if period[i][j] not in lst and len(period[i][j]) == 10:
                    lst += [period[i][j]]
    
    lstdt = []
    for i in range(0,len(lst),1):
        date = lst[i]
        date_object = datetime.strptime(date, "%d/%m/%Y")
        lstdt += [date_object]
    lstdts = sorted(lstdt)
    
    lst = []
    for i in range(0,len(lstdts),1):
        date = lstdts[i]
        new = date.strftime("%d/%m/%Y")
        lst += [new]
        
    if len(lst) == 2:
        return [lst[1],lst[0]]
    elif len(lst) == 4:
        return [lst[3],lst[1]]
    else:
        #print ("No period could be identified correctly")
        return None
    
    
def extractvalues(table):
    values = []
    for i in range (0, len(table),1):
        nested = []
        nestedinv = []
        for j in range(len(table[i])-1,-1,-1):
            valued = table[i][j]
            valuelst = valued.split(".")
            value = ""
            for h in range(0,len(valuelst),1):
                    value += str(valuelst[h])
            try:
                value = int(value)
            except:
                valued = table[i][j]
                valuelst = valued.split(",")
                value = ""
                h = 0
                for h in range(0,len(valuelst),1):
                    value += str(valuelst[h])
                try:
                    value = int(value)
                except:
                    break
                else:
                    nested += [table[i][j]]
            else:
                nested += [table[i][j]]
        for i in range(len(nested)-1,-1,-1):
            nestedinv += [nested[i]]
        values += [nestedinv]
    
        
    return values
    
def createdict(label, code, period, values):
    dictionary2 = {}  
    
    if period != None:
        for i in range(0,len(period),1):
            dictionary1 = {}
            for j in range(0, len(label),1):
                try:
                    dictionary1[code[j],label[j]] = values[j][i]
                except:
                    dictionary1[code[j],label[j]] = None
            dictionary2[period[i]] = dictionary1
        return dictionary2 
    else:
        dictionary1 = {}
        for i in range(0,len(values[1]),1):
            dictionary1 = {}
            for j in range(0,len(label),1):
                try:
                    dictionary1[code[j],label[j]] = values[j][i]
                except:
                    dictionary1[code[j],label[j]] = None
            dictionary2[i] = dictionary1
        return dictionary2
def createdataframe(dictionary):
    frame = pd.DataFrame(dictionary)
    return frame

def exportcsv(dataframe):
    folderpath = input("where do you want to export your .csv file (enter a folder path): ")
    folderpath = folderpath.strip()
    filename = input("how do you want to name your file? ")
    filename = filename.strip()
    filename += ".csv"
    filepath = folderpath + "\\" + filename
    csv = dataframe.to_csv(path_or_buf = filepath, encoding = "utf-8" )
    
    return csv
    



    
            
            

        

    
    
    
    
if __name__ == "__main__":
    main()
    