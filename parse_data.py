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

# Data is in a tabular format written in HTML
# Find the table row which contains the column names
columns = soup.find('tr', {'class': 'tableclmhdr'})

# The first player information is in the <tr> tag right after
cur_player = columns.findNext('tr')

finished = False
# Initialize player_data to empty list
player_data = []

while finished != True:
    try:
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
                player_data.append(name)
            else:
                # For all other columns in the table
                stat = info[i].get_text().strip()
                player_data.append(stat)

        # Last table row has no player data, hacky fix to not append it
        if i == len(info) - 1:
            print(player_data)
            player_data = []

        # Move onto the next player
        cur_player = cur_player.findNext('tr')

    except Exception as e:
        print(e)
        finished = True