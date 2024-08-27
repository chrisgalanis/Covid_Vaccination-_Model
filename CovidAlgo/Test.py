import math
from selenium import webdriver #Library to open html source code
import re
import csv


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






