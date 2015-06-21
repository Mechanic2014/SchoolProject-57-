from html.parser import HTMLParser
import urllib.request as req
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
from selenium import webdriver

def GoodBanks(N):
    GBanksBID = [[], [], [], []]#cost of dollar that you sale to bank   - index = 2/needed - max from B
    GBanksASK = [[], [], [], []]#cost of dollar that bank sales to  you - index = 3/needed - min from A
    NewNB = []
    NewNA = []
    
    for i in range(len(N)):
        if N[i][2] != "None/',":
            NewNB.append(N[i])

    for i in range(len(N)):
        if N[i][3] != "None/',":
            NewNA.append(N[i])
    
    A = NewNA
    B = NewNB
    A.sort(key=lambda x: x[3])
    B.sort(key=lambda x: x[2])
    B.reverse()
    
    for i in range(len(B)):
        if 1 <= int(B[i][1]) <= 1000 and GBanksBID[0].__len__() < 5:
            GBanksBID[0].append(B[i])
        elif 1001 <= int(B[i][1]) <= 5000 and GBanksBID[1].__len__() < 5:
            GBanksBID[1].append(B[i])
        elif 5001 <= int(B[i][1]) <= 10000 and GBanksBID[2].__len__() < 5:
            GBanksBID[2].append(B[i])
        elif 10001 <= int(B[i][1]) and GBanksBID[3].__len__() < 5:
            GBanksBID[3].append(B[i])
        elif GBanksBID[0].__len__() == 5 and GBanksBID[1].__len__() == 5 and GBanksBID[2].__len__() == 5 and GBanksBID[3].__len__() == 5 :
            break
    
    for i in range(len(A)):
        if 1 <=int(A[i][1]) <= 1000 and GBanksASK[0].__len__() < 5:
            GBanksASK[0].append(A[i])
        elif 1001 <= int(A[i][1]) <= 5000 and GBanksASK[1].__len__() < 5:
            GBanksASK[1].append(A[i])
        elif 5001 <= int(A[i][1])<= 10000 and GBanksASK[2].__len__() < 5:
            GBanksASK[2].append(A[i])
        elif 10001 <= int(A[i][1]) and GBanksASK[3].__len__() < 5:
            GBanksASK[3].append(A[i])
        elif GBanksASK[0].__len__() == 5 and GBanksASK[1].__len__() == 5 and GBanksASK[2].__len__() == 5 and GBanksASK[3].__len__() == 5 :
            break
    if len(GBanksBID) == 0 or len(GBanksASK) == 0:
        print("Good Banks Error: No Banks")

    return (GBanksBID, GBanksASK)




def Print_Good_Banks(GBanksBID, GBanksASK):
    File = open("/home/consta/Desktop/Programing/SchoolProject/Archive/MS.txt", "a")
    File.write("Basket B, Good BID banks - good to sale your money to them, ")
    File.write(time.ctime(time.time()))
    File.write(":")
    File.write("\n")
    for i in GBanksBID[1]:
        File.write(",".join(i))
        File.write("\n")
    File.write("Basket B, Good ASK banks - good to buy your money from them, ")
    File.write(time.ctime(time.time()))
    File.write(":")
    File.write("\n")
    for i in GBanksASK[1]:
        File.write(",".join(i))
        File.write("\n")
url = "http://quote.rbc.ru/cash/#!/?sortf=BID&sortd=DESC&city=1&currency=3&summa=&period=60&pagerLimiter=600&pageNumber=1"



class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
                self.CurrSt_tag = tag
                self.CurrSt_tagAttrs = attrs
                if self.CurrSt_tag == "tr" and len(self.CurrSt_tagAttrs) >= 1 and len(self.CurrSt_tagAttrs[0]) >= 2 and self.CurrSt_tagAttrs[0][0] == "title" and self.CurrSt_tagAttrs[0][1] != None:
                        Name.append(self.CurrSt_tagAttrs[0][1])
                if self.CurrSt_tag == "input" and len(self.CurrSt_tagAttrs) >= 2 and self.CurrSt_tagAttrs[0][0] == "id" and self.CurrSt_tagAttrs[1][0] == "type" and self.CurrSt_tagAttrs[1][1] == "checkbox":
                        ID.append(self.CurrSt_tagAttrs[0][1])
                if self.CurrSt_tag == "a" and len(self.CurrSt_tagAttrs) == 3 and self.CurrSt_tagAttrs[0] == ('href', '#') and self.CurrSt_tagAttrs[1] == ('target', '_blank') and self.CurrSt_tagAttrs[2][1][38:41] == "BID":
                        BID.append(self.CurrSt_tagAttrs[2][1][42:49])
                if self.CurrSt_tag == "a" and len(self.CurrSt_tagAttrs) == 3 and self.CurrSt_tagAttrs[0] == ('href', '#') and self.CurrSt_tagAttrs[1] == ('target', '_blank') and self.CurrSt_tagAttrs[2][1][38:41] == "ASK":
                        ASK.append(self.CurrSt_tagAttrs[2][1][42:49])#PurchasingCost
        def handle_data(self, data):
                self.CurrSt_tag = self.get_starttag_text()
                if self.CurrSt_tag != None and self.CurrSt_tag[0:10] == "<td class=" and self.CurrSt_tag[11:14] == "kom":
                        Commission.append(data)#Commission
                if self.CurrSt_tag != None and self.CurrSt_tag[0:10] == "<td class=" and self.CurrSt_tag[11:14] == "sum":
                        Volume.append(data)#Volume
                if self.CurrSt_tag != None and self.CurrSt_tag[0:10] == "<td class=" and self.CurrSt_tag[11:15] == "time":
                        TM.append(data)
                if self.CurrSt_tag != None and self.CurrSt_tag[0:9] == "<span id=" and self.CurrSt_tag[10:17] == "address" and self.CurrSt_tag[19:24] == "class"and self.CurrSt_tag[26:32] == "hidden":
                        Address.append(data)

def Get_Best_BID_Cost(N):
    Sort_N_array_BID = N[:]
    Sort_N_array_BID.sort(key=lambda x: x[2])
    Sort_N_array_BID.reverse()
    A = 0
    B = 0
    C = 0
    D = 0
    for i in range(len(Sort_N_array_BID)):
        if Sort_N_array_BID[i][2] != "None/',":
            if 1 <= int(Sort_N_array_BID[i][1]) <= 1000 and A == 0:
                A = float(Sort_N_array_BID[i][2])
            elif 1001 <= int(Sort_N_array_BID[i][1]) <= 5000 and B == 0:
                B = float(Sort_N_array_BID[i][2])
            elif 5001 <= int(Sort_N_array_BID[i][1]) <= 10000 and C == 0:
                C = float(Sort_N_array_BID[i][2])
            elif 10001 <= int(Sort_N_array_BID[i][1]) and D == 0:
                D = float(Sort_N_array_BID[i][2])
            elif A != 0 and B != 0 and C != 0 and D != 0 :
                break
    return [A, B, C, D]

def Get_Best_ASK_Cost(N):
    Sort_N_array_ASK = N[:]
    Sort_N_array_ASK.sort(key=lambda x: x[3])
    A = 0
    B = 0
    C = 0
    D = 0
    for i in range(len(Sort_N_array_ASK)):
        if Sort_N_array_ASK[i][3] != "None/',":
            if 1 <= int(Sort_N_array_ASK[i][1]) <= 1000 and A == 0:
                A = float(Sort_N_array_ASK[i][3])
            elif 1001 <= int(Sort_N_array_ASK[i][1]) <= 5000 and B == 0:
                B = float(Sort_N_array_ASK[i][3])
            elif 5001 <= int(Sort_N_array_ASK[i][1]) <= 10000 and C == 0:
                C = float(Sort_N_array_ASK[i][3])
            elif 10001 <= int(Sort_N_array_ASK[i][1]) and D == 0:
                D = float(Sort_N_array_ASK[i][3])
            elif A != 0 and B != 0 and C != 0 and D != 0 :
                break
    return [A, B, C, D]

def Get_N_array(ID, Volume, BID, ASK, Name, Commission, Address, TM):
    TM = TM[2:]
    NumberOfID = ID.__len__()                               #NumberOfId = how much deals I get
    N = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(NumberOfID)]
    for i in range(NumberOfID):                             #small arrs that conists of Name of Bank,Id,salecost,buycost,last time upload(TM),Commission(Y/N)
        N[i][0] = ID[i]         #uniq number for the exect deal 
    for i in range(NumberOfID):
        N[i][1] = Volume[i]     #max cost of sale(volume of sale)
    for i in range(NumberOfID):
        N[i][2] = BID[i]        #cost of sale to banks
    for i in range(NumberOfID):
        N[i][3] = ASK[i]        #cost of buying from banks
    for i in range(NumberOfID):
        N[i][4] = Name[i]       #name of the bank
    for i in range(NumberOfID):
        N[i][5] = Commission[i] #commission of that bank
    for i in range(NumberOfID):
        N[i][6] = Address[i]
    for i in range(NumberOfID):
        N[i][7] = TM[i]
    return N

def Get_Spread_Arrays(NumberOfID, N):
    Spread_A_Value = []
    Spread_B_Value = []
    Spread_C_Value = []
    Spread_D_Value = []
    for i in range(NumberOfID):
        p = int(N[i][1])
        if N[i][2] != "None/'," and N[i][3] != "None/',":
            t = float(N[i][3]) - float(N[i][2])
            if 1 <= p <= 1000:
                Spread_A_Value.append(t)
            elif 1001 <= p <= 5000:
                Spread_B_Value.append(t)
            elif 5001 <= p <= 10000:
                Spread_C_Value.append(t)
            elif 10001 <= p:
                Spread_D_Value.append(t)
    
    Spread_A_Value.sort()
    Spread_B_Value.sort()
    Spread_C_Value.sort()
    Spread_D_Value.sort()
    
    return (Spread_A_Value, Spread_B_Value, Spread_C_Value, Spread_D_Value)

def Get_Med_Max_Min_Spread_Time_Arr(Spread_Time_A, Spread_Time_B, Spread_Time_C, Spread_Time_D, Spread_A_Value, Spread_B_Value, Spread_C_Value, Spread_D_Value):
    v = datetime.datetime.now()
    if Spread_A_Value.__len__() != 0 :
        MedianSprA = Spread_A_Value[len(Spread_A_Value) // 2]
        MinSprA = Spread_A_Value[len(Spread_A_Value) // 10]
        MaxSprA = Spread_A_Value[len(Spread_A_Value)*9 // 10]
        Spread_Time_A = Spread_Time_A[1:]
        Spread_Time_A.append([MedianSprA, MaxSprA, MinSprA, v])
    else:
        Spread_Time_A = Spread_Time_A[1:]
        Spread_Time_A.append([0, 0, 0, v])

    if Spread_B_Value.__len__() != 0:
        MedianSprB = Spread_B_Value[len(Spread_B_Value) // 2]
        MinSprB = Spread_B_Value[len(Spread_B_Value) // 10]
        MaxSprB = Spread_B_Value[len(Spread_B_Value)*9 // 10]
        Spread_Time_B = Spread_Time_B[1:]
        Spread_Time_B.append([MedianSprB, MaxSprB, MinSprB, v])
    else:
        Spread_Time_B = Spread_Time_B[1:]
        Spread_Time_B.append([0, 0, 0, v])
        
    if Spread_C_Value.__len__() != 0: 
        MedianSprC = Spread_C_Value[len(Spread_C_Value) // 2]
        MinSprC = Spread_C_Value[len(Spread_C_Value) // 10]
        MaxSprC = Spread_C_Value[len(Spread_C_Value)*9 // 10]
        Spread_Time_C = Spread_Time_C[1:]
        Spread_Time_C.append([MedianSprC, MaxSprC, MinSprC, v])
    else:
        Spread_Time_C = Spread_Time_C[1:]
        Spread_Time_C.append([0, 0, 0, v])

    if Spread_D_Value.__len__() != 0:
        MedianSprD = Spread_D_Value[len(Spread_D_Value) // 2]
        MinSprD = Spread_D_Value[len(Spread_D_Value) // 10]
        MaxSprD = Spread_D_Value[len(Spread_D_Value)*9 // 10]
        Spread_Time_D = Spread_Time_D[1:]
        Spread_Time_D.append([MedianSprD, MaxSprD, MinSprD, v])
    else:
        Spread_Time_D = Spread_Time_D[1:]
        Spread_Time_D.append([0, 0, 0, v])

    return (Spread_Time_A, Spread_Time_B, Spread_Time_C, Spread_Time_D)

def Print_Spread_Plot(BasketName, Spread_Time_X):
    if os.path.isfile('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + 'plot.jpg'):
           os.remove('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + 'plot.jpg')
    y1 =  [Spread_Time_X[i][0] for i in range(Spread_Time_X.__len__())]#median Spread
    y2 =  [Spread_Time_X[i][1] for i in range(Spread_Time_X.__len__())]#Max Spread
    y3 =  [Spread_Time_X[i][2] for i in range(Spread_Time_X.__len__())]#Min Spread
    x =  [Spread_Time_X[i][3] for i in range(Spread_Time_X.__len__())]#Current time
    plt.figure(BasketName)
    plt.ylim(0., 4.0)
    for i in range(1, y1.__len__()):
        [Cord_x_1, Cord_x_2, Cord_y_1, Cord_y_2, Cord_y_3, Cord_y_4, Cord_y_5, Cord_y_6] = [x[i-1], x[i], y1[i-1], y1[i], y2[i-1], y2[i], y3[i-1], y3[i]]

        if Cord_y_1 != 0 and Cord_y_2 != 0 and Cord_y_3 != 0 and Cord_y_4 != 0 and Cord_y_5 != 0 and Cord_y_6 != 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "g:", [Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "k.")#Median
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "r-", [Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "k.")#Max
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_5, Cord_y_6], "b-", [Cord_x_1, Cord_x_2], [Cord_y_5, Cord_y_6], "k.")#Min
        elif Cord_y_1 != 0 and Cord_y_2 == 0 and Cord_y_3 != 0 and Cord_y_4 == 0 and Cord_y_5 != 0 and Cord_y_6 == 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "w:", Cord_x_2, Cord_y_2, "w.", Cord_x_1, Cord_y_1, "k.")#Median
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "w-", Cord_x_2, Cord_y_4, "w.", Cord_x_1, Cord_y_3, "k.")#Max
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_5, Cord_y_6], "w-", Cord_x_2, Cord_y_6, "w.", Cord_x_1, Cord_y_5, "k.")#Min
        elif Cord_y_1 == 0 and Cord_y_2 != 0 and Cord_y_3 == 0 and Cord_y_4 != 0 and Cord_y_5 == 0 and Cord_y_6 != 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "w:", Cord_x_1, Cord_y_1, "w.")#Median
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "w-", Cord_x_1, Cord_y_3, "w.")#Max
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_5, Cord_y_6], "w-", Cord_x_1, Cord_y_5, "w.")#MinA  
    plt.gcf().autofmt_xdate()
    plt.savefig('/home/consta/Desktop/Programing/SchoolProject/PlotPics/'+ BasketName +'_plot.jpg')

def Print_BID_ASK_Plot(BasketName, Cost_Time_X):
    if os.path.isfile('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_BID/ASK_plot.jpg'):
           os.remove('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_BID/ASK_plot.jpg')
    y1 =  [Cost_Time_X[i][0] for i in range(Cost_Time_X.__len__())]#BID cost
    y2 =  [Cost_Time_X[i][1] for i in range(Cost_Time_X.__len__())]#ASK cost
    x =  [Cost_Time_X[i][2] for i in range(Cost_Time_X.__len__())]
    plt.figure(BasketName + "_BID/ASK_plot")
    plt.ylim(52., 56.)
    for i in range(1, y1.__len__()):
        [Cord_x_1, Cord_x_2, Cord_y_1, Cord_y_2, Cord_y_3, Cord_y_4] = [x[i-1], x[i], y1[i-1], y1[i], y2[i-1], y2[i]]
        if Cord_y_1 != 0 and Cord_y_2 != 0 and Cord_y_3 != 0 and Cord_y_4 != 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "b-", [Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "k.")#BID
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "r-", [Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "k.")#ASK
        elif Cord_y_1 != 0 and Cord_y_2 == 0 and Cord_y_3 != 0 and Cord_y_4 == 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "w-", Cord_x_2, Cord_y_2, "w.", Cord_x_1, Cord_y_1, "k.")#BID
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "w-", Cord_x_2, Cord_y_4, "w.", Cord_x_1, Cord_y_3, "k.")#ASK
        elif Cord_y_1 == 0 and Cord_y_2 != 0 and Cord_y_3 == 0 and Cord_y_4 != 0:
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_1, Cord_y_2], "w-", Cord_x_1, Cord_y_1, "w.")#BID
            plt.plot([Cord_x_1, Cord_x_2], [Cord_y_3, Cord_y_4], "w-", Cord_x_1, Cord_y_3, "w.")#ASk 
    plt.gcf().autofmt_xdate()
    plt.savefig('/home/consta/Desktop/Programing/SchoolProject/PlotPics/'+ BasketName +'_BID_ASK_plot.jpg')

def Make_Start_Plot(BasketName, Spread_Time_X):
    plt.figure(BasketName)
    
    y1 =  [Spread_Time_X[i][0] for i in range(Spread_Time_X.__len__())]
    y2 =  [Spread_Time_X[i][1] for i in range(Spread_Time_X.__len__())]
    y3 =  [Spread_Time_X[i][2] for i in range(Spread_Time_X.__len__())]
    x =  [Spread_Time_X[i][3] for i in range(Spread_Time_X.__len__())]

    plt.plot(x, y1, "w-", x, y1, "w.")#MedianA
    plt.plot(x, y2, "w-", x, y2, "w.")#MaxA
    plt.plot(x, y3, "w-", x, y3, "w.")#MinA
    plt.savefig('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_plot.jpg')

def Make_Start_BID_ASK_plot(BasketName, Cost_Time_X):
    plt.figure(BasketName + "_BID/ASK_plot")

    y1 = [Cost_Time_X[i][0] for i in range(len(Cost_Time_X))]
    y2 = [Cost_Time_X[i][1] for i in range(len(Cost_Time_X))]
    x = [Cost_Time_X[i][2] for i in range(len(Cost_Time_X))]

    plt.plot(x, y1, "w-", x, y1, "w.")#BID
    plt.plot(x, y2, "w-", x, y2, "w.")#ASK
    plt.savefig('/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_BID_ASK_plot.jpg')

def Get_BID_ASK_cost(N, Cost_Time_A, Cost_Time_B, Cost_Time_C, Cost_Time_D):
    v = datetime.datetime.now()

    [Best_A_BID, Best_B_BID, Best_C_BID, Best_D_BID] = Get_Best_BID_Cost(N)

    [Best_A_ASK, Best_B_ASK, Best_C_ASK, Best_D_ASK] = Get_Best_ASK_Cost(N)

    print(str(time.ctime(time.time())),"#", Best_A_BID, " # ",Best_B_BID, " # ",Best_C_BID, " # ",Best_D_BID, " # ",Best_A_ASK, " # ",Best_B_ASK, " # ",Best_C_ASK, " # ",Best_D_ASK)
    Cost_Time_A = Cost_Time_A[1:]
    Cost_Time_B = Cost_Time_B[1:]
    Cost_Time_C = Cost_Time_C[1:]
    Cost_Time_D = Cost_Time_D[1:]

    Cost_Time_A.append([Best_A_BID, Best_A_ASK, v])
    Cost_Time_B.append([Best_B_BID, Best_B_ASK, v])
    Cost_Time_C.append([Best_C_BID, Best_C_ASK, v])
    Cost_Time_D.append([Best_D_BID, Best_D_ASK, v])

    return (Cost_Time_A, Cost_Time_B, Cost_Time_C, Cost_Time_D)

def Make_HTML_page(BasketName, GBanksBID, GBanksASK):
    HTMLpage = open("/home/consta/Desktop/Programing/SchoolProject/" + BasketName + "_HTMLpage.html", "w")
    text_part_1 = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    table, th, td {
        border: 1px solid black;
    }
    h3 {
        margin-bottom: -2px; /* Отрицательный отступ между заголовком и текстом */
        margin-top: 0%;
    }

    </style>
    </head>
    <body>

    <table>
    <tr>
        <td colspan="1" width="270">Време последнего обновления:<br>"""
    #Here we will put time and date of last update
    text_part_1_2 = str(time.ctime(time.time()))
    text_part_2 = """</td>
        <td colspan="2"><i><h3><b>Сумма к обмену</b></h3>"""
    #Here we will put prise for the exect basket(depends on basket name)
    if BasketName == "Basket_A":
        text_part_2_3 = "от 1$ до 1000$"
    if BasketName == "Basket_B":
        text_part_2_3 = "от 1001$ до 5000$"
    if BasketName == "Basket_C":
        text_part_2_3 = "от 5001$ до 10000$"
    if BasketName == "Basket_D":
        text_part_2_3 = "от 10001$"

    text_part_3 = """</i></td>
    </tr>
    <tr>
        <td colspan="2">График маржи баков</td>
        <td colspan="2" height="30"><h3><i><b>Лучшие курсы покупки:</b></i></h3></td>
    </tr>
    <tr>
        <td colspan="2" ><img src="""
    #Here we will put spread plot file name : "/home/consta/Desktop/Programing/SchoolProject/PlotPics/Basket_A_plot.jpg"
    
    text_part_3_4 = '"/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_plot.jpg"'
    
    text_part_4 = """alt="Spread Plot" width="550" ></td>
        <td>"""
    #here we will put banksASK in HTML format
    if BasketName == "Basket_A":
        HTML_Good_BID_Banks = ""
        for i in range(len(GBanksBID[0])):
            HTML_Good_BID_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksBID[0][i][2]) + " " + "Цена продажи: " + str(GBanksBID[0][i][3]) + "<br>" + str(GBanksBID[0][i][4]) + "<br>" + str(GBanksBID[0][i][6]) + "<br>" + "<br>"
    
    if BasketName == "Basket_B":
        HTML_Good_BID_Banks = ""
        for i in range(len(GBanksBID[1])):
            HTML_Good_BID_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksBID[1][i][2]) + " " + "Цена продажи: " + str(GBanksBID[1][i][3]) + "<br>" + str(GBanksBID[1][i][4]) + "<br>" + str(GBanksBID[1][i][6]) + "<br>" + "<br>"

    if BasketName == "Basket_C":
        HTML_Good_BID_Banks = ""
        for i in range(len(GBanksBID[2])):
            HTML_Good_BID_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksBID[2][i][2]) + " " + "Цена продажи: " + str(GBanksBID[2][i][3]) + "<br>" + str(GBanksBID[2][i][4]) + "<br>" + str(GBanksBID[2][i][6]) + "<br>" + "<br>"

    if BasketName == "Basket_D":
        HTML_Good_BID_Banks = ""
        for i in range(len(GBanksBID[3])):
            HTML_Good_BID_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksBID[3][i][2]) + " " + "Цена продажи: " + str(GBanksBID[3][i][3]) + "<br>" + str(GBanksBID[3][i][4]) + "<br>" + str(GBanksBID[3][i][6]) + "<br>" + "<br>"


    text_part_4_5 = HTML_Good_BID_Banks
    
    text_part_5 = """</td>
    </tr>
    <tr>
        <td colspan="2"> График лучших цен покупки и продажи</td>
        <td colspan="2" height="30"><h3><i><b>Лучшие курсы продажи:</b></i></h3></td>
    </tr>
    <tr>
        <td colspan="2"><img src="""
    #Here we will put BID_ASK plot(file name : "/home/consta/Desktop/Programing/SchoolProject/PlotPics/Basket_D_plot.jpg"
    
    text_part_5_6 = '"/home/consta/Desktop/Programing/SchoolProject/PlotPics/' + BasketName + '_BID_ASK_plot.jpg"'

    text_part_6 = """ alt="Spread Plot" width="550" ></td>
        <td height="100">"""
    #Here we will put BID banks
    if BasketName == "Basket_A":
        HTML_Good_ASK_Banks = ""
        for i in range(len(GBanksASK[0])):
            HTML_Good_ASK_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksASK[0][i][2]) + " " + "Цена продажи: " + str(GBanksASK[0][i][3]) + "<br>" + str(GBanksASK[0][i][4]) + "<br>" + str(GBanksASK[0][i][6]) + "<br>" + "<br>"
    
    if BasketName == "Basket_B":
        HTML_Good_ASK_Banks = ""
        for i in range(len(GBanksASK[1])):
            HTML_Good_ASK_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksASK[1][i][2]) + " " + "Цена продажи: " + str(GBanksASK[1][i][3]) + "<br>" + str(GBanksASK[1][i][4]) + "<br>" + str(GBanksASK[1][i][6]) + "<br>" + "<br>"

    if BasketName == "Basket_C":
        HTML_Good_ASK_Banks = ""
        for i in range(len(GBanksASK[2])):
            HTML_Good_ASK_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksASK[2][i][2]) + " " + "Цена продажи: " + str(GBanksASK[2][i][3]) + "<br>" + str(GBanksASK[2][i][4]) + "<br>" + str(GBanksASK[2][i][6]) + "<br>" + "<br>"

    if BasketName == "Basket_D":
        HTML_Good_ASK_Banks = ""
        for i in range(len(GBanksASK[3])):
            HTML_Good_ASK_Banks += str(i + 1) + ") " + "Цена покупки: " + str(GBanksASK[3][i][2]) + " " + "Цена продажи: " + str(GBanksASK[3][i][3]) + "<br>" + str(GBanksASK[3][i][4]) + "<br>" + str(GBanksASK[3][i][6]) + "<br>" + "<br>"


    text_part_6_7 = HTML_Good_ASK_Banks
    text_part_7 = """</td>
    </tr>
    </table>

    </body>
    </html>
    """
    
    maintext = text_part_1 + text_part_1_2 + text_part_2 + text_part_2_3 + text_part_3 + text_part_3_4 + text_part_4 + text_part_4_5 + text_part_5 + text_part_5_6 + text_part_6 + text_part_6_7 + text_part_7
    HTMLpage.write(maintext)
    HTMLpage.close()



Spread_Time_A = []#Median Spread, Max Spread, Min Spread, time
Spread_Time_B = []
Spread_Time_C = []
Spread_Time_D = []
Cost_Time_A = [] #BID, ASK, time 
Cost_Time_B = []
Cost_Time_C = []
Cost_Time_D = []

DtimeNow = datetime.datetime.now()
    
for i in range(288,0, -1 ):
    a = DtimeNow - datetime.timedelta(minutes = (5 * i))
    
    Spread_Time_A.append([0, 0, 0, a])
    Spread_Time_B.append([0, 0, 0, a])
    Spread_Time_C.append([0, 0, 0, a])
    Spread_Time_D.append([0, 0, 0, a])
    
    Cost_Time_A.append([0, 0, a]) 
    Cost_Time_B.append([0, 0, a])
    Cost_Time_C.append([0, 0, a])
    Cost_Time_D.append([0, 0, a])

print("Start ploting BID/ASK Basket_A_startplot... ", end = "")
Make_Start_BID_ASK_plot("Basket_A", Cost_Time_A)
print("finished.")
print("Start ploting BID/ASK Basket_B_startplot... ", end = "")
Make_Start_BID_ASK_plot("Basket_B", Cost_Time_B)
print("finished.")
print("Start ploting BID/ASK Basket_C_startplot... ", end = "")
Make_Start_BID_ASK_plot("Basket_C", Cost_Time_C)
print("finished.")
print("Start ploting BID/ASK Basket_D_startplot... ", end = "")
Make_Start_BID_ASK_plot("Basket_D", Cost_Time_D)
print("finished.")


print("Start ploting Basket_A_startplot... ", end = "")
Make_Start_Plot("Basket_A", Spread_Time_A)
print("finished.")
print("Start ploting Basket_B_startplot... ", end = "")
Make_Start_Plot("Basket_B", Spread_Time_B)
print("finished.")
print("Start ploting Basket_C_startplot... ", end = "")
Make_Start_Plot("Basket_C", Spread_Time_C)
print("finished.")
print("Start ploting Basket_D_startplot... ", end = "")
Make_Start_Plot("Basket_D", Spread_Time_D)
print("finished.")

print("Makeing HTMLpage...")
driver = webdriver.Firefox()
driver.get('file:///home/consta/Desktop/Programing/SchoolProject/Basket_A_HTMLpage.html')
print("finished.")

while True:
    try:   
        ID = []
        Volume = []
        BID = [] #SaleCost
        ASK = [] #BuyCost
        Name = [] #bank name
        Commission = []
        TM = []
        Address = []
        N = []

        url = "http://quote.rbc.ru/cash/#!/?sortf=BID&sortd=DESC&city=1&currency=3&summa=&period=60&pagerLimiter=600&pageNumber=1"

        #print("Opening RBC data...",end="")
        parser = MyHTMLParser()
        parser.feed(req.urlopen(url).readall().decode())
        N = Get_N_array(ID, Volume, BID, ASK, Name, Commission, Address, TM)
        #print("finished.")
        Archive = open("/home/consta/Desktop/Programing/SchoolProject/Archive/tm.txt", "a")
        MiddleSpread = open("/home/consta/Desktop/Programing/SchoolProject/Archive/MS.txt", "a")
        List_Of_GBanks = open("/home/consta/Desktop/Programing/SchoolProject/Archive/List_Of_GBanks.txt", "a")
        #print("saving quotes...")
        for i in N:
            Archive.write(",".join(i))
            Archive.write("\n")
        print("Start to looking for good banks...", end="")
        (GBanksBID, GBanksASK) = GoodBanks(N) 
        print("finished")
        NumberOfID = ID.__len__()
        
        (Spread_A_Value, Spread_B_Value, Spread_C_Value, Spread_D_Value) = Get_Spread_Arrays(NumberOfID, N)
        (Spread_Time_A, Spread_Time_B, Spread_Time_C, Spread_Time_D) = Get_Med_Max_Min_Spread_Time_Arr(Spread_Time_A, Spread_Time_B, Spread_Time_C, Spread_Time_D, Spread_A_Value, Spread_B_Value, Spread_C_Value, Spread_D_Value)
       
        (Cost_Time_A, Cost_Time_B, Cost_Time_C, Cost_Time_D) = Get_BID_ASK_cost(N, Cost_Time_A, Cost_Time_B, Cost_Time_C, Cost_Time_D)

        Print_Good_Banks(GBanksBID, GBanksASK)
        for i in Cost_Time_B:
            for j in i:
                List_Of_GBanks.write(str(j))
                List_Of_GBanks.write(";")
            List_Of_GBanks.write("\n")
        
        Print_Spread_Plot("Basket_A", Spread_Time_A)
        Print_Spread_Plot("Basket_B", Spread_Time_B)
        Print_Spread_Plot("Basket_C", Spread_Time_C)
        Print_Spread_Plot("Basket_D", Spread_Time_D)
        
        Print_BID_ASK_Plot("Basket_A", Cost_Time_A)
        Print_BID_ASK_Plot("Basket_B", Cost_Time_B)
        Print_BID_ASK_Plot("Basket_C", Cost_Time_C)
        Print_BID_ASK_Plot("Basket_D", Cost_Time_D)
        #print("finished plot.")
        
        Make_HTML_page("Basket_A", GBanksBID, GBanksASK)
        
        driver.refresh()


        Archive.close()
        MiddleSpread.close()
        List_Of_GBanks.close()
        CurTimeSec = time.time()
        #print("waintung until: ",CurTimeSec +5*60)

    except (socket.gaierror, urllib.error.URLError):
        Spread_Time_A = Spread_Time_A[1:]
        Spread_Time_B = Spread_Time_B[1:]
        Spread_Time_C = Spread_Time_C[1:]
        Spread_Time_D = Spread_Time_D[1:]

        a = datetime.datetime.now()

        Spread_Time_A.append([0, 0, 0, a])
        Spread_Time_B.append([0, 0, 0, a])
        Spread_Time_C.append([0, 0, 0, a])
        Spread_Time_D.append([0, 0, 0, a])

        Print_Spread_Plot("Basket_A", Spread_Time_A)
        Print_Spread_Plot("Basket_B", Spread_Time_B)
        Print_Spread_Plot("Basket_C", Spread_Time_C)
        Print_Spread_Plot("Basket_D", Spread_Time_D)



    while time.time()<CurTimeSec +5*60:
        time.sleep(1)
Archive.close()
MiddleSpread.close()
List_Of_GBanks.close()
