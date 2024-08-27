#https://covid19.gov.gr/covid19-live-analytics
import math
from selenium import webdriver
import re

driver = webdriver.Chrome(executable_path='C:/Users/chris/Desktop/python/chromedriver_win32/chromedriver.exe')
driver.get('https://covid19.innews.gr/iframe')
results = []
content = driver.page_source


Data = re.findall(r'<div class="today number">(.*?)</div>',content)

for c in Data:
    if '.' in c:
        ans = re.findall('[0-9]{1,}',c)
        results.append(ans)

casesPerDay = int(results[0][0] + results[0][1])
print(casesPerDay)


driver.get('https://emvolio.gov.gr/vaccinationtracker')
results2 = []
content2  = driver.page_source

pattern = "+"
Data2 = re.findall(r'<strong>(.*?)</strong>',content2)

for d in Data2:
    if pattern in d:
        ans = re.findall('[0-9]{1,}',d)
        results2.append(ans)

vaccinatedPerDay = int(results2[2][0] + results2[2][1])
print(vaccinatedPerDay)

driver.get('https://www.worldometers.info/world-population/greece-population/')
content3 = driver.page_source
results3 =[]
Data3 =  re.findall(r'<strong>(.*?)</strong>',content3)

for e in Data3:
    if ',' in e:
        ans = re.findall('[0-9]{1,}',e)
        results3.append(ans)
        
populationPerDay = int(results3[0][0] + results3[0][1] + results3[0][2])
print(populationPerDay)

yearlyRatio = -0.48/100
time1 = 1/365

populationInAMonth = populationPerDay* math.pow(math.e, yearlyRatio*time1)
print(populationInAMonth)

#todayPop = 10375456
#tomorrowPop =  10375319

#cases:808
#deaths:24


infected = 411534 + casesPerDay
vaccinated = 2369187 + vaccinatedPerDay
populationWI = populationPerDay - infected - vaccinated + (6/100*infected) + (1/100*vaccinated)
print(populationWI)
imun = (vaccinatedPerDay*(99/100) + casesPerDay*(92/100))
print("Imunnity in one day", imun)