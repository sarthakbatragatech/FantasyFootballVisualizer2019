import os
from bs4 import BeautifulSoup
import re
import pandas as pd

cwd = os.getcwd()

position = 'RB'
week = '1'
html_path = cwd + '/data/week' + week + '/' + position + '/' + position + '_urlrawhtml.txt' 

# Reading raw html stored in text file at path
def open_html(path):
    with open(path, 'rb') as f:
        print(f'Opening File: {html_path} \n')
        return f.read()

html = open_html(html_path)
    
soup = BeautifulSoup(html, 'html.parser')

# Data is in a tabular format written in HTML
# Find the table row which contains the column names
columns = soup.find('tr', {'class': 'tableclmhdr'})

# The first player information is in the <tr> tag right after
cur_player = columns.findNext('tr')

finished = False
# Initialize player_data to empty list
player_data = []
# Initialize master list which will store all player data
all_data = []

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
            all_data.append(player_data)
            player_data = []

        # Move onto the next player
        cur_player = cur_player.findNext('tr')

    except Exception as e:
        print("Done parsing all data\n")
        finished = True

# Initialize dataframe which will store master list of all player data
columns = ['Player', 'Team', 'Games', 'Attempts', 
'RushingYards', 'RushingTD', 'Targets', 'Receptions', 
'ReceivingYards', 'ReceivingTD', 'FantasyPoints', 'FantasyPointsPerGame']

df = pd.DataFrame(all_data, columns = columns)
csv_path = cwd + '/data/week' + week + '/' + position + '/' + position + '.csv'
df.to_csv(csv_path, index = False)
print(f'{position} Dataframe written to csv\n')

df.head()