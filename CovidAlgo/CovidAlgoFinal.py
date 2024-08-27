# In Task Schedule I have programmed the file CovidAlgoFinal to be executed every day at 21:30

import math
from selenium import webdriver #Library to open html source code
import re
import csv

#Function read from Data.csv
def Read(x):
    with open('C:/Users/chris/Desktop/CovidAlgo/Data.csv','r') as csv_file:
        reader = csv.reader(csv_file)
        if x == "Cases":
            for line in reader:
                CaseList.append(line[0])
        elif x == "Population":
             for line in reader:
                    PopulationList.append(line[1])
        elif x == "Vaccination":
            for line in reader :
                VaccinationList.append(line[2])
        elif x == "Tests":
            for line in reader:
                TestsList.append(line[3])

#Function write in Data.csv the previous and todays today Data 
def Write(x1,y1,z1,t1,x2,y2,z2,t2): 
    with open('C:/Users/chris/Desktop/CovidAlgo/Data.csv','w', encoding='UTF-8',newline='') as csv_file:
        writer = csv.writer(csv_file)
        if(x2 != 0):#If they are not Data from yesterday it doesn't read them
            writer.writerow([x2]+[y2]+[z2]+[t2])
        writer.writerow([x1]+[y1]+[z1]+[t1])

#Function read from Prediction.csv the predections
def ReadPrediction():
     with open('C:/Users/chris/Desktop/CovidAlgo/Prediction.csv','r') as csv_file2:
        reader2 = csv.reader(csv_file2)
        for line2 in reader2:
            PredictionList.append(line2[0])

#Function write in Prediction.csv todays and yesterdays predictions
def WritePrediction(x1,x2): 
    with open('C:/Users/chris/Desktop/CovidAlgo/Prediction.csv','w', encoding='UTF-8',newline='') as csv_file:
        writer2 = csv.writer(csv_file)
        writer2.writerow([x1])
        writer2.writerow([x2])
        
               

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
Data2  = re.findall(r'td class="today number">(.*?)</td>',content)#pattern with regular expressions
 
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
VaccinationList = []
TestsList = []
PredictionList = []

#I am reading firstly the yesterday's data and I write them I again with todays' data
Read("Cases")
Read("Vaccination")
Read("Population")
Read("Tests")
Write(casesPerDay, populationPerDay, vaccinatedPerDay,testsPerDay, CaseList[0], PopulationList[0], VaccinationList[0], TestsList[0])

#Gathering data from lists to variables
Read("Cases")
Read("Tests")
TestsToday  = int(TestsList[-1])
TestsYesterday = int(TestsList[-2])
print("Tests Today-Tests Yesterday:",TestsToday, TestsYesterday)
CasesToday = int(CaseList[-1])
CasesYesterday = int(CaseList[-2])
print("Cases Today-Cases Yesterday:",CasesToday, CasesYesterday)
#I calculate Ratio in cases per day and tests per day
CasesRatio = ((CasesToday/TestsToday) - (CasesYesterday/TestsYesterday))/(CasesYesterday/TestsYesterday)#Ratio calculated from formula ( Today - Yesterday / Yesterday )
print("Cases Ratio:",CasesRatio)

Read("Population")
PopulationToday = int(PopulationList[-1])
PopulationYesterday = int(PopulationList[-2])
print("Population Today-Population Yesterday:",PopulationToday, PopulationYesterday)

PopulationRatio = (PopulationToday - PopulationYesterday)/PopulationYesterday#Ratio calculated from formula ( Today - Yesterday / Yesterday )
print(PopulationRatio)

Read("Vaccination")
VaccinationToday = int(VaccinationList[-1])
VaccinationYesterday = int(VaccinationList[-2])
print("Vaccination Today-Vaccination Yesterday:",VaccinationToday, VaccinationYesterday)

VaccinationRatio = (VaccinationToday - VaccinationYesterday)/VaccinationYesterday#Ratio calculated from formula ( Today - Yesterday / Yesterday )
print("Vaccination Ratio:",VaccinationRatio)



infected = 413954 + casesPerDay
vaccinated = 2660260 + vaccinatedPerDay
populationWI = populationPerDay - infected - vaccinated + (6/100*infected) + (1/100*vaccinated)
print("Population without immunity:",populationWI)
imun = (vaccinatedPerDay*(99/100) + casesPerDay*(92/100))
print("Imunity:",imun)

#I read yesterday's prediction and use it to calculate population, vaccinated and cases 
ReadPrediction()
print(PredictionList[0])
populationTomorrow = populationPerDay * math.pow(math.e, PopulationRatio*(int(PredictionList[0])/365))
vaccinatedTomorrow = vaccinatedPerDay * math.pow(math.e, VaccinationRatio*(int(PredictionList[0])/365))
casesTomorrow = casesPerDay * math.pow(math.e, CasesRatio*(int(PredictionList[0])/365))

infected2 = infected + casesTomorrow
vaccinated2 = vaccinated + vaccinatedTomorrow
populationWI2 = populationTomorrow - infected2 - vaccinated + (6/100*infected2) + (1/100*vaccinated2)

imun2 = (vaccinatedTomorrow*(99/100) + casesTomorrow*(92/100))

#I make a new prediction, which append in the list
Days = (populationWI2 * (70/100))/imun2
PredictionList.append(Days)
print(Days)

#Calculating Average Value from yesterday's prediction and today's
Sum = 0  
j = 0 
for i in range(0,len(PredictionList)):
    Sum = int(PredictionList[i]) + Sum
    j +=1

DaysMO = Sum / j
print(DaysMO)

print((vaccinated/populationPerDay)*100)
#Writing the prediction for today and yesterday
WritePrediction(int(DaysMO), PredictionList[0])
#I am writing today's data on the top, so the next time programm will be executed, it will read them, instead of yesterday's data
Write(CaseList[0], PopulationList[0], VaccinationList[0], TestsList[0],casesPerDay, populationPerDay, vaccinatedPerDay,testsPerDay)


