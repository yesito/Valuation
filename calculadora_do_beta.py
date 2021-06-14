# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:48:29 2021

@author: lucab
"""

import yfinance as yf
import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.offsetbox import AnchoredText
import sys
from datetime import datetime

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000

def main():
    share_code = input("input the share code that you desire to use: ").upper()
    inicio = input("input the beginning of the period you wish to analyse (yyyy-mm-dd) Attention!!! remember that the beginning of the period you want to analyse must contain the closing data of the previous month, therefore, for example, instead of using 2020-01-01 while analysing 2020-2021, use: 2019-12-01, as the program will choose the closing date: 2019-12-31. ")
    inicio = inicio.strip()
    final = input("input the end of the period you wish to analyse (yyyy-mm-dd). For example, if you are analysing 2020-2021, use 2021-12-31 as last possible closing day (the program will know when the market wasn't operating). ")
    final = final.strip()
    share_code = share_code.strip()
    dado_acao_dia = data(share_code,inicio,final)
    print(dado_acao_dia)
    dado_acao_mes = monthly_close_prices(dado_acao_dia)
    print(dado_acao_mes)
    market_code = input("input the market code that you desire to use: ").upper()
    market_code = market_code.strip()
    dado_mercado_dia = data(market_code,inicio,final)
    dado_mercado_mes = monthly_close_prices(dado_mercado_dia)
    retornos_mensaiss = monthly_return(dado_acao_mes)
    retornos_mensaism = monthly_return(dado_mercado_mes)
    B2 = calculate_B2(retornos_mensaiss,retornos_mensaism)
    B1 = calculate_B1(B2,retornos_mensaiss,retornos_mensaism)
    R2 = calculate_R2(retornos_mensaiss,retornos_mensaism,B2)
    trust = calculate_trust(retornos_mensaiss,retornos_mensaism)
    curva = plot_curve(B1,B2,retornos_mensaiss, retornos_mensaism,share_code, market_code,R2,trust)
       
    flag = True
    while flag == True:
        answer = input("do you wish to export your regression in PNG? (Answer Yes or No) ") .lower()
        answer = answer.strip()
        if answer == "yes":
            plt.savefig('plot.png', dpi=800)
            print("file sucssessfully exported!")
            flag = False
        elif answer == "no":
            flag = False
        else:
            print("invalid input")
            flag = True
    
    plt.show()
    
    
    flag = True
    while flag == True:
        answer2 = input("Do you wish to make another Regression? (Answer Yes or No) ") .lower()
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
                        
    
def data(code,inicio,final):
    prices = yf.download(code,start = inicio,end = final )
    prices = prices.dropna()
    close_prices = prices.drop(columns = ["Open", "High","Low", "Adj Close", "Volume"])
    return close_prices
    
def monthly_close_prices(data):
    index = data.index
    index2 = index.tolist()
    str_index = []
    for i in range(0, len(index2),1):
        str_index += [index2[i].strftime("%d-%m-%Y")]
    z =0   
    lst=[]
    for i in range(len(str_index)-1,-1,-1):
        if z != int(str_index[i][3] + str_index[i][4]):
            lst += [str_index[i]]
        z = int(str_index[i][3] + str_index[i][4])
    ilist = []
    for i in range(0,len(str_index),1):
        for j in range(0,len(lst),1):
            if str_index[i] == lst[j]:
                ilist += [i]
    close_prices = []
    for i in range (0,len(ilist),1):
        close_prices += [data.iloc[int(ilist[i]),0]]
    return close_prices
    

def monthly_return(data):
    lst = []
    for i in range(0,len(data)-1,1):
        retorno = ((data[i+1] - data[i])/(data[i]))*100
        lst += [retorno]
    return lst

def calculate_B2(retornos_mensaiss,retornos_mensaism):
    X = retornos_mensaism
    Y = retornos_mensaiss
    xm = np.average(X)
    ym = np.average(Y)
    #somatorio
    z = 0
    w = 0
    for i in range(0,len(X),1):
        z += (X[i] - xm)*(Y[i] - ym)
        w += ((X[i] - xm)*(X[i] - xm))
    
    B2 = z/w
    B1 = (ym - (B2*xm))
    
    return B2

def calculate_B1(B2,retornos_s,retornos_m):
    X = retornos_m
    Y = retornos_s
    xm = np.average(X)
    ym = np.average(Y)
    B1 = (ym - (B2*xm))
    return B1

 
def calculate_R2(retornos_s,retornos_m,B2):
    R2 = (B2*B2)*(var(retornos_m)/var(retornos_s))
    return R2

def calculate_trust(retornos_s,retornos_m):
    return None






def plot_curve(B1,B2,retornos_s,retornos_m, share_code, market_code,R2,trust):
    y = []
    def f(x,B1,B2):
        return B2*x + B1
    x = linspace(-15,15,100)
    y = zeros(len(x))
    for i in range(0,len(x),1):
        y[i] += f(x[i],B1,B2)
    p1 = plt.plot(x,y,"r-",)
    p2 = plt.scatter(retornos_m,retornos_s, s=2)
    plt.xlabel("Retorno Mensal " + str(share_code) + " (%)")
    plt.ylabel("Retorno Mensal " + str(market_code) + " (%)")
    plt.legend([str(round(B2,3)) + "*x" + " + " + str(round(B1,3))])
    a = -12
    plt.annotate("R² = " + str((round(R2*100, 5))) + "%", xy = (-3,a-3))
    # (PARA O FUTURO) plt.annotate("intervalo de confiança para B  = ", xy = (-3, a))
    plt.title("Regressão entre os retornos mensais de " + str(share_code) + " e " + str(market_code) + " (2016-2021)")
    
    return None
    

    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
    

