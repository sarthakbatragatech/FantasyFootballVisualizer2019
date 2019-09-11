import os
from bs4 import BeautifulSoup
import re

cwd = os.getcwd()

position = 'RB'

def open_html(path):
    with open(path, 'rb') as f:
        print(f'Opening File: {path}')
        return f.read()

html = open_html(cwd + '/' + position + '_urlrawhtml.txt')    
    
soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

data = []

# Data is in a tabular format written in HTML
# Find the table row which contains the column names
columns = soup.find('tr', {'class': 'tableclmhdr'})

# The first player information is in the <tr> tag right after
cur_player = columns.findNext('tr')

info = cur_player.find_all('td', {'class': 'sort1'})

for i in range(len(info)):
    # Special case to extract player name
    if i == 0:
        # Strip new line characters
        text = info[i].get_text().replace('\n', '')
        # String form is now '1. firstname lastname'
        # Regex pattern to get everything after period
        pattern = re.compile('\.(.*)')
        match = pattern.search(text)
        name = match.group(1).strip()
        data.append(name)
    else:
        # For all other columns in the table
        stat = info[i].get_text().strip()
        data.append(stat)
        
print(data)