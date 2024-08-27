import math
from selenium import webdriver #Library to open html source code
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
plt.style.use('seaborn')


# Solve Model (By Filip Antonopoulos)
# Defining the equations of the model
def SIR(s,i,r,beta,gamma):
    s_dot = -s*i*beta/(s+i+r)
    i_dot = s*i*beta/(s+i+r)-gamma*i
    r_dot = gamma*i
    return s_dot, i_dot, r_dot

def Solve_Model(Recovered, Infected, Susceptible, Date):
    # Defining initial conditions (If you want the beta and gamma to change add it as a perametre in the function domain)
    beta = 0.18
    gamma = 0.037
    # Stating the x variable and the steps of the simple Euler
    steps = np.arange(0, 3650, 1)
    time = 0.1*steps
    dt = 0.1
    
    # Setting up the variable lists
    tlen = len(time)
    s = np.empty((tlen))
    i = np.empty((tlen))
    r = np.empty((tlen))

  
    T = [0]
    # for z in DateList:
    #     T.append(z)
       
    
  
    plt.plot(T, Susceptible[0],'o',label = 'Susceptible Data')#You have to make another time array for dots
    # plt.plot(time, RecoveredList,'o', label = 'Recovered Data')
    # plt.plot(time, CaseList,'o', label = 'Infected Data')

    r[0]= 3295
    i[0]= 3170
    s[0]= 10359859 - r[0] - i[0]

    # Simple Euler Iterations 
    for t in steps:
        if t < len(steps)-1:
            s_dot, i_dot, r_dot = SIR(s[t], i[t], r[t],beta, gamma)
            s[t+1] = s[t]+dt*s_dot
            i[t+1] = i[t]+dt*i_dot
            r[t+1] = r[t]+dt*r_dot
    # Plotting the results
    plt.plot(time, s,label = 'Susceptible')
    plt.plot(time, i, label = 'Infected')
    plt.plot(time, r, label = 'Recovered')
    


    plt.legend()
    plt.title("SIR" + ' ' + "Model Simulation")
    plt.xlabel("time(days)")
    plt.ylabel("Number of People")
    plt.show()


#Get Date

def Date():
    today = date.today()
    Day = today.strftime("%d")
    return Day


#Function read from Data.csv
def Read(x):
    with open('C:/Users/chris/OneDrive/CovidAlgo/SIRV-Model/Data.csv','r') as csv_file:
        reader = csv.reader(csv_file)
        if x == "Cases":
            for line in reader:
                CaseList.append(line[0])
        elif x == "Susceptible":
             for line in reader:
                    PopulationList.append(line[1])
        elif x == "Recovered":
            for line in reader :
                RecoveredList.append(line[2])
        elif x == "Date":
            for line in reader :
                DateList.append(line[3])
        

#Function write in Data.csv the previous and todays today Data 
def Write(x,y,z,d): 
    with open('C:/Users/chris/OneDrive/CovidAlgo/SIRV-Model/Data.csv','w', encoding='UTF-8',newline='') as csv_file:
        writer = csv.writer(csv_file)
        # if(x2 != 0):#If they are not Data from yesterday it doesn't read them
        #     writer.writerow([x2]+[y2]+[z2]+[d2])
        for i in range(0,len(x)):
            writer.writerow([x[i]]+[y[i]]+[z[i]]+[d[i]])


#Opens website html source
driver = webdriver.Chrome(executable_path='C:/Users/chris/Desktop/python/chromedriver_win32/chromedriver.exe')
driver.get('https://covid19.innews.gr/iframe')
results = []
content = driver.page_source

#casesPerDay
Data = re.findall(r'<div class="today number">(.*?)</div>',content)#pattern with regular expressions

if '.' in Data[0]:
    ans = re.findall('[0-9]{1,}',Data[2])
    casesPerDay = int(ans[0] + ans[1])
else:
    casesPerDay = int(Data[0]) 

#testsPerDay
Data2  = re.findall(r'<td class="today number">(.*?)</td>',content)#pattern with regular expressions
 
if '.' in Data2[0]:
    ans = re.findall('[0-9]{1,}',Data2[0])
    testsPerDay1 = int(ans[0] + ans[1])
else:
    testsPerDay1 = int(Data2[0]) 

if '.' in Data2[1]:
    ans = re.findall('[0-9]{1,}',Data2[1])
    testsPerDay2 = int(ans[0] + ans[1])
else:
    testsPerDay2 = int(Data2[1]) 

testsPerDay = testsPerDay1 + testsPerDay2

#ΜΕΘ
Data3 =  re.findall(r'<div class="today number">(.*?)</div>',content)#pattern with regular expressions

if '.' in Data3[2]:
    ans = re.findall('[0-9]{1,}',Data3[2])
    METHperDay = int(ans[0]+ans[1])
else:
    METHperDay = int(Data3[2])

#Exits from Hospital
Data4 = re.findall(r'<div class="today number">(.*?)<span class="asterisk">',content)

if '.' in Data4[1]:
    ans = re.findall('[0-9]{1,}',Data4[1])
    Exits = int(ans[0] + ans[1])
else:
    Exits = int(Data4[1])


#Opens website html source
driver.get('https://emvolio.gov.gr/vaccinationtracker')
results2 = []
content2  = driver.page_source

pattern = "+"
Data2 = re.findall(r'<strong>(.*?)</strong>',content2)#pattern with regular expressions

#vaccinatedPerDay
for d in Data2:
    if pattern in d:
        ans = re.findall('[0-9]{1,}',d)
        results2.append(ans)

vaccinatedPerDay = int(results2[2][0] + results2[2][1])

#vaccinated
Data2_1 = re.findall(r'<h2>(.*?)<br>',content2)

if '.' in Data2_1[2]:
    ans = re.findall('[0-9]{1,}',Data2_1[2])
    vaccinated = int(ans[0] + ans[1] + ans[2])
else:
    vaccinated = int(Data2_1[2]) 


#Opens website html source
driver.get('https://www.worldometers.info/world-population/greece-population/')
content3 = driver.page_source
results3 =[]
Data3 =  re.findall(r'<strong>(.*?)</strong>',content3)#pattern with regular expressions

#populationPerDay
for e in Data3:
    if ',' in e:
        ans = re.findall('[0-9]{1,}',e)
        results3.append(ans)
        
populationPerDay = int(results3[0][0] + results3[0][1] + results3[0][2])

#List where I gather all the data from csv files

CaseList = []
PopulationList = []
RecoveredList = []
DateList = []

Recovered = int(Exits + METHperDay)
Susceptible = int(populationPerDay - casesPerDay - Recovered)

Date = Date()
# Day = Date()[0]
# Month = Date()[1]



#Write(casesPerDay,Susceptible,Recovered,Date)

Read("Cases")
Read("Susceptible")
Read("Recovered")
Read("Date")



CaseList.append(casesPerDay)
PopulationList.append(Susceptible)
RecoveredList.append(Recovered)
DateList.append(Date)




Write(CaseList, PopulationList, RecoveredList, DateList)


Days = int(DateList[-2]) - int(DateList[-1])


Solve_Model(RecoveredList, CaseList , PopulationList , Days)

