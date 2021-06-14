# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:57:44 2021

@author: lucab
"""
import calculadora_do_beta as beta
import sgs
import conversor_pdf_df as cv

def main():
    
    share_code = "WEGE3.SA"
    inicio = "2018-12-01" #input the beginning of the period you wish to analyse (yyyy-mm-dd) Attention!!! remember that the beginning of the period you want to analyse must contain the closing data of the previous month, therefore, for example, instead of using 2020-01-01 while analysing 2020-2021, use: 2019-12-01, as the program will choose the closing date: 2019-12-31.
    inicio = inicio.strip()
    final = "2019-12-31" #input the end of the period you wish to analyse (yyyy-mm-dd). For example, if you are analysing 2020-2021, use 2021-12-31 as last possible closing day (the program will know when the market wasn't operating).
    final = final.strip()
    share_code = share_code.strip()
    dado_acao = beta.data(share_code,inicio,final)
    market_code = "^BVSP"
    market_code = market_code.strip()
    dado_mercado = beta.data(market_code,inicio,final)
    B = Beta(dado_acao, dado_mercado)
    RiskFree_CDI = risk_free(inicio, final)
    ExpectedRiskPremium = expected_risk_premium(inicio,final,market_code)
    expected_return = cost_of_equity(ExpectedRiskPremium,RiskFree_CDI,B) 
    
    #print(expected_return, RiskFree_CDI,  ExpectedRiskPremium, B  )
    
    #Until here informations were nescessary to calculate cost of equity
    #-------------------------------------------------------------------------------------------
    #Use anualaccounts if you are investiganting by trimester or only accesaccounts if anual DFP`s or consolidated.
    
    folderpath = "C:\\Users\\lucab\\OneDrive\\A&M\\DemonstrativosFinanceiros\\PDF\\wege" #insert the folder path where the pdf is:
    _1t = "ITRweg1T2019"
    _2t = "ITRweg2T2019"
    _3t = "ITRweg3T2019"
    _4t = "ITRweg4T2019"
    _4t18 = "ITRweg4T2018"
    
    lst4t = []
     

    operational_income4t = accessaccount(_4t,folderpath,[19],(19,0))
    lease_expense4t = accessaccount(_4t,folderpath, [22],(0,0))
    interest_expense4t =accessaccount(_4t,folderpath, [22],(1,0))
    lst4t += [operational_income4t, lease_expense4t, interest_expense4t]
    
    
    interest_c_r = interest_coverage_ratio(lst4t)
    default_sp = default_spread(interest_c_r)
    

    ebit4t = accessaccount(_4t,folderpath, [19],(15,0))
    tax4t = accessaccount(_4t,folderpath, [19],(16,0))
    ebit4tb = accessaccount(_4t18,folderpath, [19],(15,0))
    tax4tb = accessaccount(_4t18,folderpath, [19],(16,0))
    
    m_t_r = marginal_tax_rate(ebit4t,ebit4tb,tax4t,tax4tb)
    after_tax_cost_debt = after_tax_cost_of_debt(m_t_r,RiskFree_CDI,default_sp)
    
    n_a4t = accessaccount(_4t,folderpath, [19],(25,0))
    ll4t = accessaccount(_4t,folderpath, [19],(19,0))
    p_mes = beta.data(share_code,"2019-12-01","2019-12-31")
    
    e_mv = e_market_value(share_code,n_a4t,ll4t,p_mes)
    
    
    mv = accessaccount(_4t,folderpath,[17],(0,0))
    
    mv_debt_ = mv_debt(mv)
    
    #print(accounts)
    #print(interest_c_r)
    #print (default_sp)
    #print(m_t_r)
    #print(after_tax_cost_debt)
    #print(e_mv)
    #print(mv_debt_)
    
    D = mv_debt_/(mv_debt_ + e_mv)
    E = e_mv/(e_mv + mv_debt_)
     
    WACC = expected_return*E + after_tax_cost_debt*D
    print(WACC)
    
   
    
def Beta(dado_acao_dia, dado_mercado_dia):
    ac = beta.monthly_close_prices(dado_acao_dia)
    ar = beta.monthly_return(ac)
    mc = beta.monthly_close_prices(dado_mercado_dia)
    mr = beta.monthly_return(mc)
    B = beta.calculate_B2(mr,ar)
    return B


def risk_free(inicio,final):
    ts = sgs.time_serie(4389, inicio, final)
    tsv = ts.iloc[-1]
    return tsv

def expected_risk_premium(inicio,final,market_code):
    dado_mercado_dia = beta.data(market_code,inicio,final)
    mc = beta.monthly_close_prices(dado_mercado_dia)
    mr = beta.monthly_return(mc)
    retorno_total = 1
    for i in range(0, len(mr),1):
        retorno_total = retorno_total*(1+(mr[i]/100))
    return (retorno_total*100) - 100

def cost_of_equity(retorno_total, tsv, beta):
    expected_return = tsv + (beta*retorno_total)
    return expected_return

def import_PDF_to_DF(filepath,pages):
    
    listofpagetxt = cv.read(filepath, pages)
    pagelsts = cv.txtorganizerinlst(listofpagetxt)
    table = cv.cleanheaderandfooter(pagelsts)
    perioddirty = cv.perio(pagelsts)
    label = cv.extractlabel(table)
    code =  cv.extractcode(table)
    period = cv.cleanperiod(perioddirty)
    values = cv.extractvalues(table)
    dictionary = cv.createdict(label, code, period, values)
    dataframe = cv.createdataframe(dictionary)
    
    return dataframe

def accessaccount(filename, folderpath, pages,iposition):
    filename = filename.strip()
    filename += ".pdf" 
    folderpath = folderpath.strip()
    filepath = folderpath + "\\" + filename
    df = import_PDF_to_DF(filepath, pages)
    accountd = df.iloc[iposition]
    accountlst = accountd.split(".")
    account = ""
    for i in range(0,len(accountlst),1):
        account += str(accountlst[i])
    try:
        account = int(account)
    except:
        account = ""
        accountd = df.iloc[iposition]
        lst = []
        lst += accountd
        for i in range(0,len(lst),1):
            if lst[i] == ",":
                lst[i] = "."
            else:
                pass
        for i in range(0,len(lst),1):
            account += lst[i]
        try:
            account == int(account)
        except:
            try:
                account == float(account)
            except: 
                print(account)
            else:
                return account
    else:
        return account

def anualaccounts(lst1t,lst2t,lst3t,lst4t):

    lsty = [lst1t,lst2t,lst3t,lst4t]
    operational_incomey = lsty [0][0] + lsty[1][0] + lsty[2][0] + lsty[3][0]
    lease_expensey = lsty [0][1] + lsty[1][1] + lsty[2][1] + lsty[3][1]
    interest_expensey = lsty [0][2] + lsty[1][2] + lsty[2][2] + lsty[3][2]


    lst = [operational_incomey,lease_expensey,interest_expensey]
    return lst

def interest_coverage_ratio(lst):
    Interest_coverage_r = (lst[0] + (-1*lst[1])) / ((-1*lst[2]) + (-1*lst[1]))
    return Interest_coverage_r
    
def default_spread(i_c_r): #in percentage
    if i_c_r >12.5:
        rating = ["AAA",(0.35)]
    elif i_c_r <= 12.5 and i_c_r > 9.5:
        rating = ["AA",(0.5)]
    elif i_c_r <= 9.5 and i_c_r > 7.5:
        rating = ["A+",(0.7)]
    elif i_c_r <= 7.5 and i_c_r > 6:
        rating = ["A",(0.85)]
    elif i_c_r <= 6 and i_c_r > 4.5:
        rating = ["A-",(1)]
    elif i_c_r <= 4.5 and i_c_r > 4:
        rating = ["BBB",(1.5)]
    elif i_c_r <= 4 and i_c_r > 3.5:
        rating = ["BB+",(2)]
    elif i_c_r <= 3.5 and i_c_r > 3:
        rating = ["BB",(2.5)]
    elif i_c_r <= 3 and i_c_r > 2.5:
        rating = ["B+",(3.25)]
    elif i_c_r <= 2.5 and i_c_r > 2:
        rating = ["B",(4)]
    elif i_c_r <= 2 and i_c_r > 1.5:
        rating = ["B-",(6)]
    elif i_c_r <= 1.5 and i_c_r > 1.25:
        rating = ["CCC",(8)]
    elif i_c_r <= 1.25 and i_c_r > 0.8:
        rating = ["CC",(10)]
    elif i_c_r <= 0.8 and i_c_r > 0.5:
        rating = ["C",(12)]
    elif i_c_r <= 0.5:
        rating = ["D",(20)]
    return rating
def marginal_tax_rate(ebit4t,ebit4tb, tax4t, tax4tb): #used effective as marginal tax rate.

    ebity =  ebit4t 
    taxy = tax4t
    
    taxy = taxy*-1
    
    mg_tx_r = (taxy - tax4tb)/((ebity- ebit4tb)*100)
    return mg_tx_r

def after_tax_cost_of_debt(mg_tx_r,RiskFree_CDI,default_sp):
    default_sp = default_sp[1]
    atcd = (((RiskFree_CDI + default_sp)/100)*(1-(mg_tx_r/100)))*100
    return atcd

def e_market_value(share_code,n_a4t,ll4t,p_mes):

    n_a = float(ll4t)/float(n_a4t)
    p_f_mes = beta.monthly_close_prices(p_mes)
    
    return n_a*p_f_mes[0]

def mv_debt(mv):
    return mv
    
if __name__ == "__main__":
    main()
    
    