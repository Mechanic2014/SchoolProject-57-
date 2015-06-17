from html.parser import HTMLParser
import urllib.request as req
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

def GoodBanks(N, MidSprA, MidSprB, MidSprC, MidSprD):
    GBanks = [[], [], [], []]
    for i in range(N.__len__()):
        if N[i][2] != "None/'," and N[i][3] != "None/',":
            Cur_MidSpr = float(N[i][3]) - float(N[i][2])
            Cur_Volume = int(N[i][1])
            if  1 <= Cur_Volume <= 1000:
                if Cur_MidSpr <= MidSprA:
                    GBanks[0].append(N[i][4])
            elif  1001 <= Cur_Volume <= 5000:
                if Cur_MidSpr <= MidSprB:
                    GBanks[1].append(N[i][4])
            elif  5001 <= Cur_Volume <= 10000:
                if Cur_MidSpr <= MidSprC:
                    GBanks[2].append(N[i][4])
            elif  10001 <= Cur_Volume <= 999999:
                if Cur_MidSpr <= MidSprD:
                    GBanks[3].append(N[i][4])
    return GBanks

def Print_Good_Banks(Good_Banks_in_Basket, File_Name, BasketName):
    File = open(File_Name, "a")
    File.write(BasketName)
    File.write(",")
    File.write(time.ctime(time.time()))
    File.write(":")
    File.write("\n")
    for i in Good_Banks_in_Basket:
        File.write(",".join(i))
        File.write("\n")

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


Spread_Time_A = []
Spread_Time_B = []
Spread_Time_C = []
Spread_Time_D = []


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
        N = []
        Spread_A_Value = 0
        Spread_A_Quantuty = 0
        Spread_B_Value = 0
        Spread_B_Quantuty = 0
        Spread_C_Value = 0
        Spread_C_Quantuty = 0
        Spread_D_Value = 0
        Spread_D_Quantuty = 0
        MidSprA = 0
        MidSprB = 0
        MidSprC = 0
        MidSprD = 0

        url = "http://quote.rbc.ru/cash/#!/?sortf=BID&sortd=DESC&city=1&currency=3&summa=&period=60&pagerLimiter=600&pageNumber=1"



        parser = MyHTMLParser()
        parser.feed(req.urlopen(url).readall().decode())

        Archive = open("/home/consta/Desktop/Programing/SchoolProject/Archive/tm.txt", "a")
        MiddleSpread = open("/home/consta/Desktop/Programing/SchoolProject/Archive/MS.txt", "a")
        List_Of_GBanks = open("/home/consta/Desktop/Programing/SchoolProject/Archive/List_Of_GBanks.txt", "a")
        
        TM = TM[2:]
        NumberOfID = ID.__len__()                               #NumberOfId = how much deals I get
        N = [[0, 0, 0, 0, 0, 0, 0] for i in range(NumberOfID)]  #N will be an array that is made of 
        for i in range(NumberOfID):                             #small arrs that conists of Name of Bank,Id,salecost,buycost,last time upload(TM),Commission(Y/N)
            N[i][0] = ID[i]         #uniq number for the exect deal 
        for i in range(NumberOfID):
            N[i][1] = Volume[i]     #max cost of sale(volume of sale)
        for i in range(NumberOfID):
            N[i][2] = BID[i]        #cost of sale
        for i in range(NumberOfID):
            N[i][3] = ASK[i]        #cost of buying
        for i in range(NumberOfID):
            N[i][4] = name[i]       #name of the bank
        for i in range(NumberOfID):
            N[i][5] = Commission[i] #commission of that bank
        for i in range(NumberOfID):
            N[i][6] = TM[i]     
        for i in N:
            Archive.write(",".join(i))
            Archive.write("\n")
        
        for i in range(NumberOfID):
            p = int(N[i][1])
            if N[i][2] != "None/'," and N[i][3] != "None/',":
                t = float(N[i][3]) - float(N[i][2])
            else:
                t = "None"
            if 1 <= p <= 1000 and t != "None":
                Spread_A_Value += t
                Spread_A_Quantuty += 1
            elif 1001 <= p <= 5000 and t != "None":
                Spread_B_Value += t
                Spread_B_Quantuty += 1
            elif 5001 <= p <= 10000 and t != "None":
                Spread_C_Value += t
                Spread_C_Quantuty += 1
            elif 10001 <= p and t != "None":
                Spread_D_Value += t
                Spread_D_Quantuty += 1


        if Spread_A_Quantuty != 0:
            MidSprA = Spread_A_Value / Spread_A_Quantuty
            MiddleSpread.write(str(MidSprA))
            MiddleSpread.write(",")
            if Spread_Time_A.__len__() < 288: 
                Spread_Time_A.append((MidSprA, datetime.datetime.now()))
            else:
                Spread_Time_A = Spread_Time_A[1:]
                Spread_Time_A.append((MidSprA, datetime.datetime.now()))
        else:
            MiddleSpread.write("none")
            MiddleSpread.write(",")

        if Spread_B_Quantuty != 0:
            MidSprB = Spread_B_Value / Spread_B_Quantuty
            MiddleSpread.write(str(MidSprB))
            MiddleSpread.write(",")
            if Spread_Time_B.__len__() < 288:
                Spread_Time_B.append((MidSprB, datetime.datetime.now()))
            else:
                Spread_Time_B = Spread_Time_B[1:]
                Spread_Time_B.append((MidSprB, datetime.datetime.now()))
        else:
            MiddleSpread.write("none")
            MiddleSpread.write(",")

        if Spread_C_Quantuty != 0:
            MidSprC = Spread_C_Value / Spread_C_Quantuty
            MiddleSpread.write(str(MidSprC))
            MiddleSpread.write(",")
            if Spread_Time_C.__len__() < 288:
                Spread_Time_C.append((MidSprC, datetime.datetime.now()))
            else:
                Spread_Time_C = Spread_Time_C[1:]
                Spread_Time_C.append((MidSprC, datetime.datetime.now()))
        else:
            MiddleSpread.write("none")
            MiddleSpread.write(",")

        if Spread_D_Quantuty != 0:
            MidSprD = Spread_D_Value / Spread_D_Quantuty
            MiddleSpread.write(str(MidSprD))
            MiddleSpread.write(",")
            if Spread_Time_D.__len__() < 288:
                Spread_Time_D.append((MidSprD, datetime.datetime.now()))
            else:
                Spread_Time_D = Spread_Time_D[1:]
                Spread_Time_D.append((MidSprD, datetime.datetime.now()))
        else:
            MiddleSpread.write("none")
            MiddleSpread.write(",")
        
        MiddleSpread.write(time.ctime(time.time())[11:19])
        MiddleSpread.write("\n")
        
        GoodNBanks = GoodBanks(N, MidSprA,MidSprB,MidSprC,MidSprD)

        #print(str(Spread_B_Quantuty))

        #Print_Good_Banks(GoodNBanks[1], "/home/consta/Desktop/Programing/SchoolProject/Archive/List_Of_GBanks.txt", "Basket A")
        os.remove('/home/consta/Desktop/Programing/SchoolProject/PlotPics/testplot.jpg')
        y =  [Spread_Time_A[i][0] for i in range(Spread_Time_A.__len__())]
        x =  [Spread_Time_A[i][1] for i in range(Spread_Time_A.__len__())]
        plt.plot(x,y)
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
