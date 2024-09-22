import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


matplotlib.rcParams['font.family'] = 'Arial Unicode MS'  


url = "https://www.weather.gov.hk/tc/cis/normal/1991_2020/15day_normal.htm"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}
response = requests.get(url=url, headers=headers)
html = response.text
soup = BeautifulSoup(html, "html.parser")


all_rowodd = soup.findAll("td", attrs={"class": "rowodd"})


data = []
for rowodd in all_rowodd:
    if rowodd.string:  
        data.append(rowodd.string.strip())  


dates = []
rainfalls = []
for i in range(0, len(data), 5):
    if i + 4 < len(data):  
        date = data[i]
        max_temp = data[i + 1]
        average_temp = data[i + 2]
        min_temp = data[i + 3]
        rainfall = data[i + 4]

        dates.append(date)
        rainfalls.append(float(rainfall))  


cmap = LinearSegmentedColormap.from_list("green_to_blue", ["green", "blue"])


plt.figure(figsize=(10, 5))

norm = plt.Normalize(0, max(rainfalls))  
colors = cmap(norm(rainfalls)) 

plt.plot(dates, rainfalls, marker='o', linestyle='-', color='b', alpha=0.7)  
for i in range(len(dates) - 1):
    plt.plot(dates[i:i + 2], rainfalls[i:i + 2], marker='o', linestyle='-', color=colors[i])  

plt.title('Rainfall Over Dates')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.xticks(rotation=45)  
plt.grid()
plt.tight_layout() 
plt.show()
