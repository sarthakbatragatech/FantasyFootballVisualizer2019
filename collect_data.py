import requests
import os
from bs4 import BeautifulSoup

# Dictionary assisting mapping every position to its correct 'URL' value 
position_dict = {'QB': 10, 'RB': 20, 'WR': 30, 'TE': 40, 'K': 80, 'DEF': 99}
position = 'RB'
week = '1'
	
# Url for fantasy points each NFL team allows to each position
url = "https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=1&PosID=" + str(position_dict[position]) + "&LeagueID=193033"
html_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

r = requests.get(url, html_headers)
print("Request Sent...\n")
print("Request Status is %d \n" %r.status_code)

soup = BeautifulSoup(r.content, 'html.parser')

cwd = os.getcwd()
path = cwd + '/data/week' + week
os.makedirs(path, exist_ok = True)
print("Creating directory...\n")

html_path = path + '/' + position + "_urlrawhtml.txt"
outfile = open(html_path, "w")
outfile.write(str(soup.prettify()))
print("Writing raw html to output text file...\n")