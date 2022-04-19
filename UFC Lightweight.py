#Libraries used:
import requests
import pandas as pd
import bar_chart_race as bcr
import warnings

warnings.filterwarnings("ignore")

#Storing of site's address with data as variable:
link = "https://www.mma-stats.com"

#Getting of list with dates of rankings' actualization:
start_page_data = requests.get(link)
start_page_data = start_page_data.text
start_page_data = start_page_data.replace('https://www.mma-stats.com/rankings/',
                                          '@@@https://www.mma-stats.com/rankings/')
start_page_data = start_page_data.split('@@@')[1:]
links = [i.split('"')[0] for i in start_page_data]
dates = [i.split('/')[-1] for i in links]

#Getting of indexes of dates when title was vacant:
for i in range(0, len(dates)):
    if dates[i] == "2021-03-23":
        vaccant_date_index_2 = i
    elif dates[i] == "2021-05-10":
        vaccant_date_index_1 = i

#Getting of lists of top fighters for every date (result is 2D list):

fighters = []
for i in links:
    data = requests.get(i)
    data = data.text
    data = data.replace('Lightweight', '@@@Lightweight')
    data = data.replace('Welterweight', '@@@Welterweight')
    data = data.split("@@@")[1]
    fighters.append(data)
    
fighters = [i.split("fighters/")[1:] for i in fighters]

for i in range(0, len(fighters)):
    for j in range(0, len(fighters[i])):
        fighters[i][j] = fighters[i][j].split('">')[0]

for i in range(0, len(fighters)):
    if i >= vaccant_date_index_1 and i <= vaccant_date_index_2:
        fighters[i] = ['Vacant'] + fighters[i]


#Replacing of just fighters' names by lists with fighters' names, dates, and positions (result is 3D list):
        
for i in range(0, len(fighters)):
    for j in range(0, len(fighters[i])):
        fighters[i][j] = [dates[i], fighters[i][j], -j]

#Reshaping of 3D list to 2D list:        
fighters_formatted = []
for i in fighters:
    fighters_formatted = fighters_formatted + i

#Conversion of 2D list of information about fighters to pandas dataframe:
fighters_formatted = pd.DataFrame(fighters_formatted, columns = ['Date', 'Fighter', 'Position'])
fighters_formatted = fighters_formatted.drop_duplicates(subset=['Date', 'Fighter'])

#Conversion of date to correct format:
fighters_formatted["Date"] = pd.to_datetime(fighters_formatted["Date"])

#Subsetting of data for cases when only top 10 positions are available:
fighters_formatted_10 = fighters_formatted[ fighters_formatted["Date"] < "30-12-2013"]

#Subsetting of data for cases when top 15 positions are available:
fighters_formatted_15 = fighters_formatted[ fighters_formatted["Date"] >= "30-12-2013"]

#Preparations of datasets for construction of plots:
data_wide_10 = fighters_formatted_10.pivot(index='Date', columns='Fighter', values='Position')
data_wide_15 = fighters_formatted_15.pivot(index='Date', columns='Fighter', values='Position')
data_wide_10 = data_wide_10.fillna(-11)
data_wide_15 = data_wide_15.fillna(-16)

#Construction of plots:
bcr.bar_chart_race(df = data_wide_10, n_bars=11, filename = 'video1.mp4',
                   title = "UFC Lightweight ranking, 2013-2022 (0 = champion, -15 = 15th position)",
                   title_size = 9,
                   sort='desc')

bcr.bar_chart_race(df = data_wide_15, n_bars=16, filename = 'video2.mp4',
                   title = "UFC Lightweight ranking, 2013-2022 (0 = champion, -15 = 15th position)",
                   title_size = 9,
                   sort='desc')

