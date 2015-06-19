from html.parser import HTMLParser
import urllib.request as req
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

def GoodBanks(N):
    GBanksBID = [[], [], [], []]#cost of dollar that you sale to bank   - index = 2/needed - max from B
    GBanksASK = [[], [], [], []]#cost of dollar that bank sales to  you - index = 3/needed - min from A
    NewN = []
    
    for i in range(len(N)):
        if N[i][2] != "None/'," and N[i][3] != "None/',":
            NewN.append(N[i])
    
    A = NewN
    B = NewN[:]
    A.sort(key=lambda x: x[3])
    B.sort(key=lambda x: x[2])
    B.reverse()
    if A == B :
        print("A == B")    
    for i in range(len(B)):
        if 1 <= int(B[i][1]) <= 1000 and GBanksBID[0].__len__() < 10:
            GBanksBID[0].append(B[i])
        elif 1001 <= int(B[i][1]) <= 5000 and GBanksBID[1].__len__() < 10:
            GBanksBID[1].append(B[i])
        elif 5001 <= int(B[i][1]) <= 10000 and GBanksBID[2].__len__() < 10:
            GBanksBID[2].append(B[i])
        elif 10001 <= int(B[i][1]) and GBanksBID[3].__len__() < 10:
            GBanksBID[3].append(B[i])
        elif GBanksBID[0].__len__() == 10 and GBanksBID[1].__len__() == 10 and GBanksBID[2].__len__() == 10 and GBanksBID[3].__len__() == 10 :
            break
    
    for i in range(len(A)):
        if 1 <=int(A[i][1]) <= 1000 and GBanksASK[0].__len__() < 10:
            GBanksASK[0].append(A[i])
        elif 1001 <= int(A[i][1]) <= 5000 and GBanksASK[1].__len__() < 10:
            GBanksASK[1].append(A[i])
        elif 5001 <= int(A[i][1])<= 10000 and GBanksASK[2].__len__() < 10:
            GBanksASK[2].append(A[i])
        elif 10001 <= int(A[i][1]) and GBanksASK[3].__len__() < 10:
            GBanksASK[3].append(A[i])
        elif GBanksASK[0].__len__() == 10 and GBanksASK[1].__len__() == 10 and GBanksASK[2].__len__() == 10 and GBanksASK[3].__len__() == 10 :
            break

    return (GBanksBID, GBanksASK)


"""def Print_Good_Banks(GBanksBID, GBanksASK, List_Of_GBanks):
    File = open(List_Of_GBanks, "a")
    File.write("Basket A, Good BID banks - good to sale your money to them, ")
    File.write(time.ctime(time.time()))
    File.write(":")
    File.write("\n")
    for i in GBanksBID[0]:
        File.write(",".join(i))
        File.write("\n")
    File.write("Basket A, Good ASK banks - good to buy your money from them, ")
    File.write(time.ctime(time.time()))
    File.write(":")
    File.write("\n")
    for i in GBanksASK[0]:
        File.write(",".join(i))
        File.write("\n")
"""
url = "http://quote.rbc.ru/cash/#!/?sortf=BID&sortd=DESC&city=1&currency=3&summa=&period=60&pagerLimiter=600&pageNumber=1"



class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
                self.CurrSt_tag = tag
                self.CurrSt_tagAttrs = attrs
                if self.CurrSt_tag == "tr" and len(self.CurrSt_tagAttrs) >= 1 and len(self.CurrSt_tagAttrs[0]) >= 2 and self.CurrSt_tagAttrs[0][0] == "title" and self.CurrSt_tagAttrs[0][1] != None:
                        name.append(self.CurrSt_tagAttrs[0][1])
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



Spread_Time_A = []
Spread_Time_B = []
Spread_Time_C = []
Spread_Time_D = []
DtimeNow = datetime.datetime.now()
for i in range(1, 289):
    a = DtimeNow - datetime.timedelta(minutes = (5 * i))
    Spread_Time_A.append([0, 0, 0, a])
    Spread_Time_B.append([0, 0, 0, a])
    Spread_Time_C.append([0, 0, 0, a])
    Spread_Time_D.append([0, 0, 0, a])

yA1 =  [Spread_Time_A[i][0] for i in range(Spread_Time_A.__len__())]
yA2 =  [Spread_Time_A[i][1] for i in range(Spread_Time_A.__len__())]
yA3 =  [Spread_Time_A[i][2] for i in range(Spread_Time_A.__len__())]
xA =  [Spread_Time_A[i][3] for i in range(Spread_Time_A.__len__())]
        
plt.plot(xA, yA1, "w-", xA, yA1, "wo")#MedianA
plt.plot(xA, yA2, "w-", xA, yA2, "wo")#MaxA
plt.plot(xA, yA3, "w-", xA, yA3, "wo")#MinA

CurTimeSec = time.time()-5*60

while time.time() <= CurTimeSec + 5* 60 + 2:                       #+2sec to give some time to program
    if time.time() >= CurTimeSec + 5 * 60:                          #but list still reloads every 15 min
        
        ID = []
        Volume = []
        BID = [] #SaleCost
        ASK = [] #BuyCost
        name = [] #bank name
        Commission = []
        TM = []
        Address = []
        N = []
        Spread_A_Value = []
        Spread_B_Value = []
        Spread_C_Value = []
        Spread_D_Value = []

        url = "http://quote.rbc.ru/cash/#!/?sortf=BID&sortd=DESC&city=1&currency=3&summa=&period=60&pagerLimiter=600&pageNumber=1"



        parser = MyHTMLParser()
        parser.feed(req.urlopen(url).readall().decode())

        Archive = open("/home/consta/Desktop/Programing/SchoolProject/Archive/tm.txt", "a")
        MiddleSpread = open("/home/consta/Desktop/Programing/SchoolProject/Archive/MS.txt", "a")
        List_Of_GBanks = open("/home/consta/Desktop/Programing/SchoolProject/Archive/List_Of_GBanks.txt", "a")
        
        TM = TM[2:]
        NumberOfID = ID.__len__()                               #NumberOfId = how much deals I get
        N = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(NumberOfID)]  #N will be an array that is made of 
        for i in range(NumberOfID):                             #small arrs that conists of Name of Bank,Id,salecost,buycost,last time upload(TM),Commission(Y/N)
            N[i][0] = ID[i]         #uniq number for the exect deal 
        for i in range(NumberOfID):
            N[i][1] = Volume[i]     #max cost of sale(volume of sale)
        for i in range(NumberOfID):
            N[i][2] = BID[i]        #cost of sale to banks
        for i in range(NumberOfID):
            N[i][3] = ASK[i]        #cost of buying from banks
        for i in range(NumberOfID):
            N[i][4] = name[i]       #name of the bank
        for i in range(NumberOfID):
            N[i][5] = Commission[i] #commission of that bank
        for i in range(NumberOfID):
            N[i][6] = Address[i]
        for i in range(NumberOfID):
            N[i][7] = TM[i]

        for i in N:
            Archive.write(",".join(i))
            Archive.write("\n")
        
        (GBanksBID, GBanksASK) = GoodBanks(N) 
        #Print_Good_Banks(GBanksBID, GBanksASK, "/home/consta/Desktop/Programing/SchoolProject/Archive/List_Of_GBanks.txt")

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
        
        os.remove('/home/consta/Desktop/Programing/SchoolProject/PlotPics/testplot.jpg')
        yA1 =  [Spread_Time_A[i][0] for i in range(Spread_Time_A.__len__())]#median Spread
        yA2 =  [Spread_Time_A[i][1] for i in range(Spread_Time_A.__len__())]#Max Spread
        yA3 =  [Spread_Time_A[i][2] for i in range(Spread_Time_A.__len__())]#Min Spread
        xA =  [Spread_Time_A[i][3] for i in range(Spread_Time_A.__len__())]#Current time
        

        for i in range(1, yA1.__len__()):
            [Cord_x_A_1, Cord_x_A_2, Cord_y_A_1, Cord_y_A_2, Cord_y_A_3, Cord_y_A_4, Cord_y_A_5, Cord_y_A_6] = [xA[i-1], xA[i], yA1[i-1], yA1[i], yA2[i-1], yA2[i], yA3[i-1], yA3[i]]
            if Cord_y_A_1 != 0 and Cord_y_A_2 != 0 and Cord_y_A_3 != 0 and Cord_y_A_4 != 0 and Cord_y_A_5 != 0 and Cord_y_A_6 != 0:
                plt.plot([Cord_x_A_1, Cord_y_A_1], [Cord_x_A_2, Cord_y_A_2], "g:", [Cord_x_A_1, Cord_y_A_1], [Cord_x_A_2, Cord_y_A_2], "ko")#MedianA
                plt.plot([Cord_x_A_1, Cord_y_A_3], [Cord_x_A_2, Cord_y_A_4], "r-", [Cord_x_A_1, Cord_y_A_3], [Cord_x_A_2, Cord_y_A_4], "ko")#MaxA
                plt.plot([Cord_x_A_1, Cord_y_A_5], [Cord_x_A_2, Cord_y_A_6], "b-", [Cord_x_A_1, Cord_y_A_5], [Cord_x_A_2, Cord_y_A_6], "ko")#MinA
            elif Cord_y_A_1 != 0 and Cord_y_A_2 == 0 and Cord_y_A_3 != 0 and Cord_y_A_4 == 0 and Cord_y_A_5 != 0 and Cord_y_A_6 == 0:
                plt.plot([Cord_x_A_1, Cord_y_A_1], [Cord_x_A_2, Cord_y_A_2], "w:", [Cord_x_A_2, Cord_y_A_2], "wo")#MedianA
                plt.plot([Cord_x_A_1, Cord_y_A_3], [Cord_x_A_2, Cord_y_A_4], "w-", [Cord_x_A_2, Cord_y_A_4], "wo")#MaxA
                plt.plot([Cord_x_A_1, Cord_y_A_5], [Cord_x_A_2, Cord_y_A_6], "w-", [Cord_x_A_2, Cord_y_A_6], "wo")#MinA
            elif Cord_y_A_1 == 0 and Cord_y_A_2 != 0 and Cord_y_A_3 == 0 and Cord_y_A_4 != 0 and Cord_y_A_5 == 0 and Cord_y_A_6 != 0:
                plt.plot([Cord_x_A_1, Cord_y_A_1], [Cord_x_A_2, Cord_y_A_2], "w:", [Cord_x_A_1, Cord_y_A_1], "wo")#MedianA
                plt.plot([Cord_x_A_1, Cord_y_A_3], [Cord_x_A_2, Cord_y_A_4], "w-", [Cord_x_A_1, Cord_y_A_3], "wo")#MaxA
                plt.plot([Cord_x_A_1, Cord_y_A_5], [Cord_x_A_2, Cord_y_A_6], "w-", [Cord_x_A_1, Cord_y_A_5], "wo")#MinA  
        #plt.axis(xmin, xmax, ymin, ymax)
        plt.gcf().autofmt_xdate()
        plt.savefig('/home/consta/Desktop/Programing/SchoolProject/PlotPics/testplot.jpg')

        Archive.close()
        MiddleSpread.close()
        List_Of_GBanks.close()
        CurTimeSec = time.time()
    time.sleep(2)
Archive.close()
MiddleSpread.close()
List_Of_GBanks.close()
