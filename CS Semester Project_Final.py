# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



#Import statements required for some code functionality 
#Implementing web scraping in python with beautifulsoup. (2020, August 20). Retrieved March 11, 2021, from https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
#J. (2016, March 12). Check if certain value is contained in a dataframe column in pandas. Retrieved February 28, 2021, from https://stackoverflow.com/questions/35956712/check-if-certain-value-is-contained-in-a-dataframe-column-in-pandas
#Seif, G. (2018, March 01). 5 quick and easy data visualizations in Python with code. Retrieved March 13, 2021, from https://towardsdatascience.com/5-quick-and-easy-data-visualizations-in-python-with-code-a2284bae952f
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

#Empty lists to grab player names and cities in upcoming loop
names = []
cities = []


#Creates multiple empty lists for each stat that will be added to the CSV file for each player

gp = []
minutes = []
points = []
fgm = []
fga = []
fgperc = []
threepm = []
threepa = []
threepperc = []
ftm = []
fta = []
ftperc =[]
reb = []
ast = []
stl = []
blk = []
to = []
dd2 = []
td3 = []
perc = []
position = []

basketball = {}

theYears = []

for year in years:
	
	url = "https://www.espn.com/nba/stats/player/_/season/" + str(year) + "/seasontype/2/table/offensive/sort/avgPoints/dir/desc"
	
	#Grabs Top 50 NBA players based on Points per Game (PPG) from ESPN.com
	#Implementing web scraping in python with beautifulsoup. (2020, August 20). Retrieved March 11, 2021, from https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
	#2020-21 NBA player stats. (n.d.). Retrieved March 07, 2021, from https://www.espn.com/nba/stats/player/_/table/offensive/sort/avgPoints/dir/desc
	#Code to send HTTP request to website and grab URL using Beautiful Soup
	page = requests.get(url) ##Implementing web scraping in python with beautifulsoup. (2020, August 20). Retrieved March 11, 2021, from https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
	soup = BeautifulSoup(page.content, 'html.parser') #Implementing web scraping in python with beautifulsoup. (2020, August 20). Retrieved March 11, 2021, from https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/


	#Grab the table of data on the webpage that is encompased by the below id
	results = soup.find(id="fittPageContainer") #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup

	#Grab the following tag information from the HTML on the webpage assoicated with player names and their assoicated stats
	players = results.find_all('tr', class_= "Table__TR Table__TR--sm Table__even") #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup
	stats = results.find_all('td', class_ = "Table__TD") #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup

	#Counter to help bypass unnecessary data for upcoming loop
	num = 1

	#Loops through each player in the web page for the associated HTML tags and grabs the name and city of the player's team
	for player in players:

		#name = player.find('tbody',class_='Table__TBODY')
		#Finds the name of each player and the city of their team within the specifed HTML tags on the website 
		name = player.find('a',class_= "AnchorLink") #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup
		city = player.find('span', class_ = "pl2 n10 athleteCell__teamAbbrev") #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup

		#Passes any element that has nothing in it and continues the loop
		if None in (name, city): #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup
			continue

		#Adds the player's name and their team city to the appropriate list while grabing the text, instead of the HTML, and removing whitespace
		names.append(name.text.strip()) #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup
		cities.append(city.text.strip()) #Breuss, M. (2021, March 06). Beautiful soup: Build a web scraper with python. Retrieved March 07, 2021, from https://realpython.com/beautiful-soup-web-scraper-python/#part-3-parse-html-code-with-beautiful-soup


	#Create a list that contains the possible positions in the ESPN data
	#The list is used as a indicator of when the next player's stats can be collected 
	listPos = ["G", "PG", "SG", "F", "SF", "PF", "C", "NA"]

	indStats = [] #Create a list that grabs each player's stats until a position name comes up
	playerStats = [] #Create a master list for all players (a list of lists)


	#Create a for loop that goes through each players stats
	#For loop will bypass any unnecessary data - about 100 rows need to be bypassed for this script
	#Once the needed data is reached, an if statement looks to see if the data is the position of the player. If it is the position of the player, this means that all the players stats have been collected in indStats and can be added to the master list playerStats (which will be a list of list)
	#Once a player's stats are added to the master list, the indStats list gets cleared
	#The else statement will add the player's stats into the indStats list (means that the current item is a stat we need)

	for stat in stats:

		if num > 101:
			#print(stat.text)
			if stat.text in listPos:
				playerStats.append(indStats)
				indStats = []
				continue
			else:
				indStats.append(stat.text)
		else:
			num += 1 #Increases counter by one


	#Adds the last player to the master list because the data does not end on a player position so it does not know to add the last player to the loop
	playerStats.append(indStats)

	#print(indStats)
	#print(playerStats)

	#print(names)

	#Creates a counter
	i = 0 
	#Creates a dictionary 
	#basketball = {}

	#basketball = {{names[i]: playerStats[i]} for name in names (i = i + 1) }

	#While loop will perform the encompassed function as long as the counter is below 50; want to grab the 50 elements from the names list and playerStats list

	while i < 50: 

		basketball[names[i]] = playerStats[i] #Adds to the dictionary using the player's name as a key and their list of stats as the value
		i += 1 #Increases counter by 1


	values = [] #Creates an empty list to grab the stats of each player in a list of lists

	#Loops through the basketball dictionary (of only the values) and adds them to the values list

	for ball in basketball.values():
		values.append(ball)
		#print(len(values))

	#print(values)

	#Creates multiple empty lists for each stat that will be added to the CSV file for each player

	#Loops through each list in the list values (list of list) and takes each stat and appends them to the appropriate list for each player
	#Values grabbed are float casted to convert into continous data and allow for the mean function to work later on
	#Data is organized in a way that allows us to know where each value will be and match it to the players (since the data is ordered)

	for value in values:

		gp.append(float(value[0]))
		minutes.append(float(value[1]))
		points.append(float(value[2]))
		fgm.append(float(value[3]))
		fga.append(float(value[4]))
		fgperc.append(float(value[5]))
		threepm.append(float(value[6]))
		threepa.append(float(value[7]))
		threepperc.append(float(value[8]))
		ftm.append(float(value[9]))
		fta.append(float(value[10]))
		ftperc.append(float(value[11]))
		reb.append(float(value[12]))
		ast.append(float(value[13]))
		stl.append(float(value[14]))
		blk.append(float(value[15]))
		to.append(float(value[16]))
		dd2.append(float(value[17]))
		td3.append(float(value[18]))
		perc.append(float(value[19]))



	count  = 1 #Counter to bypass any unncessary data for upcoming loop
	#position = [] #Empty list for to grab each player's position in upcoming loop

	#Loops through to the Web Page to find the position of each player
	#Skips any data that is unnecessary with counter
	#In the second if statement, if the player's position starts with P or S, that indicates a two letter position (PG, PF, SG, SF) and the first two indexes need to be grabbed
	#Otherwise just grab the first index 
	#Else statement increases counter

	for player in players:
		
		#print(player.text.strip() + '\n')
		if count > 50:
			#print(player.text.strip())
			#Grab the position of the player
			if player.text[0] == "N": #Data cleaning to get rid of NA value in position of a particular player
				position.append("C")
			elif player.text[0] == "P" or player.text[0] == "S":
				position.append(player.text[0] + player.text[1])
			else: 
				position.append(player.text[0])	

		else:
			count += 1

	#print(names)
	#print(cities)
	#print(position)

	i = 0

	while i < 50:

		theYears.append(year)
		i += 1


# #Place the data into a CSV file

# #Hiremath, O. S. (2020, November 25). Web scraping with python - a beginner's guide. Retrieved March 07, 2021, from https://www.edureka.co/blog/web-scraping-with-python/
# #Places data into a dataframe and exports it to a CSV file
df = pd.DataFrame({'Player Name':names, 'Cities': cities, 'Position': position, 'Season':theYears,'Games Played': gp, 'Minutes Played Per Game': minutes, 'Points Per Game': points, 'Average Field Goals made': fgm, 'Average Field Goals Attempted': fga, 'Field Goal Percentage': fgperc, 'Average 3-Point Field Goals Made': threepm, 'Average 3-Point Field Goals Attempted': threepa, '3-Point Field Goal Percentage': threepperc, 'Average Free Throws Made': ftm, 'Average Free Throws Attempted': fta, 'Free Throw Percentage': ftperc, 'Rebounds Per Game': reb, 'Assists Per Game': ast, 'Steals Per Game': stl,'Blocks Per Game': blk, 'Turnovers Per Game': to, 'Double Double': dd2, 'Triple Double': td3, 'Player Efficiency Rating': perc} )
df.to_csv('nba.csv', index=False, encoding = 'utf-8') #Creates a CSV file with each key as the header and value as the columns from previous line of code

#Read CSV file back into python script - NOTE: COMMENT OUT THE FOLLOWING LINE TO ALLOW THE SCRIPT TO WORK ON YOUR OWN COMPUTER
#df = pd.read_csv("/Users/rsemunegus/Desktop/cs5010/hw/nba.csv")

### Manpreet's ###

#finding average 3-point field goals by Season and Position
allseasons =df.groupby(['Position','Season']).mean()['Average 3-Point Field Goals Made']

C3n = allseasons.xs("C",axis=0)
G3n = allseasons.xs("G",axis=0)
PG3n = allseasons.xs("PG",axis=0)
SG3n = allseasons.xs("SG",axis=0)
F3n = allseasons.xs("F",axis=0)
SF3n = allseasons.xs("SF",axis=0)
PF3n = allseasons.xs("PF",axis=0)

#Finding the number of players of each position for each season

#Counts = df.groupby('Season')['Position'].value_counts()

Final = df.groupby('Season')['Position'].value_counts().unstack().fillna(0)
#https://towardsdatascience.com/pandas-tips-and-tricks-33bcc8a40bb9
#https://towardsdatascience.com/pandas-tips-and-tricks-33bcc8a40bb9
#http://pytolearn.csd.auth.gr/b4-pandas/40/plotserdf.html
#https://realpython.com/pandas-groupby/

C = Final.xs('C', axis=1)
G = Final.xs('G', axis=1)
PG= Final.xs('PG', axis=1)
SG = Final.xs('SG', axis=1)
F = Final.xs('F', axis=1)
SF = Final.xs('SF', axis=1)
PF = Final.xs('PF', axis=1)

#bar plot for number of each position each season 
p1 = C.plot(kind='bar', title='Number of Centers Each Season', yticks=[1, 10, 20])
p2 = G.plot(kind='bar', title='Number of Guards Each Season', yticks=[1, 10, 20])
p3 = PG.plot(kind='bar', title='Number of Point Guards Each Season', yticks=[1, 10, 20])
p4 = SG.plot(kind='bar', title='Number of Shooting Guards Each Season', yticks=[1, 10, 20])
p5 = F.plot(kind='bar', title='Number of Forwards Each Season', yticks=[1, 10, 20])
p6 = SF.plot(kind='bar', title='Number of Small Forwards Each Season', yticks=[1, 10, 20])
p7 = PF.plot(kind='bar', title='Number of Power Forwards Each Season', yticks=[1, 10, 20])

#bar plot for average 3-point field goals for each position
p8 = C3n.plot(kind='bar', title='Average 3-Point Field Goalds for Centers Each Season', yticks=[1, 2, 3])
p9 = G3n.plot(kind='bar', title='Average 3-Point Field Goalds for Guards Each Season', yticks=[1, 2, 3])
p10 = PG3n.plot(kind='bar', title='Average 3-Point Field Goalds for Point Guards Each Season', yticks=[1, 2, 3])
p11 = SG3n.plot(kind='bar', title='Average 3-Point Field Goalds for Shooting Guards Each Season', yticks=[1, 2, 3])
p12 = F3n.plot(kind='bar', title='Average 3-Point Field Goalds for Forwards Each Season', yticks=[1, 2, 3])
p13 = SF3n.plot(kind='bar', title='Average 3-Point Field Goalds for Small Forwards Each Season', yticks=[1, 2, 3])
p14 = PF3n.plot(kind='bar', title='Average 3-Point Field Goalds for Power Forwards Each Season', yticks=[1, 2, 3])

# =============================================================================
# Robel's Code
# =============================================================================



#Sadawi, N. (Director). (2016, December 28). 34- Pandas DataFraames: Aggregation [Video file]. Retrieved March 26, 2021, from https://www.youtube.com/watch?v=2I2E1ZbF8pg&amp;ab_channel=NoureddinSadawi
#Markham, K. (Director). (2016, May 19). When should i use a "groupby" in pandas? [Video file]. Retrieved March 26, 2021, from https://www.youtube.com/watch?v=qy0fDqoMJx8&amp;t=228s&amp;ab_channel=DataSchool
#Patel, D. (Director). (2017, March 26). Python Pandas Tutorial 7. Group By (Split Apply Combine) [Video file]. Retrieved March 26, 2021, from https://www.youtube.com/watch?v=Wb2Tp35dZ-I&amp;t=371s&amp;ab_channel=codebasics

# original = sys.stdout
# sys.stdout = open('NBA Queries', 'a')

## -- DATA CLEANING -- ##

print(len(df)) # Checks current size of the dataset
df = df.drop_duplicates() # Drops any duplicate rows in teh data
print(len(df)) # Checks dataset size after dropping duplicates (there are no duploicates)
df = df.dropna() # Drops any rows with missing data (there is no missing data)


## - START DATA QUERIES -- ##

pd.set_option('display.max_rows', None) # How to print an entire pandas DataFrame in Python. (n.d.). Retrieved April 06, 2021, from https://www.kite.com/python/answers/how-to-print-an-entire-pandas-dataframe-in-python


# Has the number of FGs attempted in a season increased over time?

seasonGroup = df.groupby("Season")
print(seasonGroup['Average Field Goals Attempted'].mean())

fieldGoals = {}
i = 0
for fg in seasonGroup['Average Field Goals Attempted'].mean():

	fieldGoals[years[i]] = fg
	i +=  1

# From Module 6 - Visualiation class resources 
figure = plt.figure()
plot =figure.add_subplot(1,1,1)

plot.plot(fieldGoals.keys(), fieldGoals.values())

plot.set_xticks([2002, 2008, 2014, 2020])
plot.set_xlabel("Season")
plot.set_ylabel("Average Field Goals Attempted")
plot.set_title("Average FGs Attempted")

plt.show()

# What position has the highest PER?
posGroup = df.groupby('Position')

perPos = posGroup['Player Efficiency Rating'].mean()
print(perPos)

figure = plt.figure()
plot = figure.add_subplot(1,1,1)
plot.set_title("PER by Position")
#Specifically from Visualizaiton.ipynb script - https://colab.research.google.com/drive/15vpBKRBuHnbYSRbGgf1BG0xrW_hijAp-?usp=sharing#scrollTo=YoMb5RshMYbA
sns.barplot(x="Position", y = "Player Efficiency Rating", data = df)
plt.show()


# Create a starting 5 based on points, rebounds, assists, blocks, and player efficiency

# -- Find the player with the highest average PPG in the data set -- #

myTopFive = []
myTopPoints = 0
myTopRebs = 0
myTopAssists = 0
myTopBlocks = 0
myTopPER = 0

maxPoints = 0 # Set the max PPG to 0
i = 0 # Counter to grab row in dataset for loops
maxI = 0 # Counter to hold the index of the data needed
for points in df['Points Per Game']: # Loops through the PPG column to find what the highest PPG in the dataset is

	if points > maxPoints: # If the current PPG has a higher PPG than the current max value, then set the current PPG as the max
		maxPoints = points
		maxI = i
	i += 1

myTopPoints = float(maxPoints)

i = 0
playerName = ""
for name in df['Player Name']: # Loops through to find the name of the player with the highest average PPG in the dataset
	
	if i == maxI:
		playerName = name
		myTopFive.append(playerName) # Add the player to the top 5 list
		i = 0		
		break
		
	i += 1

playerPos = ""
for position in df['Position']: # Loops through to find the position of the player with the highest average PPG
	
	if i == maxI:
		playerPos = position
		i = 0
		break 
	i += 1

theSeason1 = 0
theSeason2 = 0
for season in df['Season']: # Loops through to find the season in which the player scored the highest PPG

	if i == maxI:
		int(season) # Convert to an integer
		theSeason1 = season - 1 # Finding the year the season started
		theSeason2 = season # Finding the year the season ended
		i = 0
		break
	i += 1

print("The top player selected for points was " + playerName + " who averaged " + str(maxPoints) + " points per game in the " + str(theSeason1) + "-" + str(theSeason2) + " season as a " + playerPos)

# -- Find the player with the highest average RPG in the data set -- #

# Source: Used class resources/notes/slides (Module 6 Visualization and Visualization.ipynb)
# Source: Gavande, J. (2020, April 30). Box plot in Python using matplotlib. Retrieved March 20, 2021, from https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
plt.boxplot(df['Points Per Game'])
plt.title("Points Per Game")
plt.ylabel("Points")
plt.show()

plt.boxplot(df['Rebounds Per Game'])
plt.title("Rebounds Per Game")
plt.ylabel("Rebounds")
plt.show()

plt.boxplot(df['Assists Per Game'])
plt.title("Assists Per Game")
plt.ylabel("Assists")
plt.show()

plt.boxplot(df['Blocks Per Game'])
plt.title("Blocks Per Game")
plt.ylabel("Blocks")
plt.show()

plt.boxplot(df['Player Efficiency Rating'])
plt.title("Player Efficiency Rating (PER)")
plt.ylabel("PER")
plt.show()

maxReb = 0 # Set the max RPG to 0
i = 0 # Resets counter to grab row in dataset for loops
maxI = 0 # Counter to hold the index of the data needed
for reb in df['Rebounds Per Game']: # Loops through the RPG column to find what the highest PPG in the dataset is

	if reb > maxReb: # If the current RPG has a higher RPG than the current max value, then set the current PPG as the max
		maxReb = reb
		maxI = i
	i += 1

myTopRebs = float(maxReb)

i = 0
playerName = ""
for name in df['Player Name']: # Loops through to find the name of the player with the highest average RPG in the dataset
	
	if i == maxI:
		playerName = name
		myTopFive.append(playerName) # Add the player to the top 5 list
		i = 0		
		break
		
	i += 1

playerPos = ""
for position in df['Position']: # Loops through to find the position of the player with the highest average RPG
	
	if i == maxI:
		playerPos = position
		i = 0
		break 
	i += 1

theSeason1 = 0
theSeason2 = 0
for season in df['Season']: # Loops through to find the season in which the player scored the highest RPG

	if i == maxI:
		int(season) # Convert to an integer
		theSeason1 = season - 1 # Finding the year the season started
		theSeason2 = season # Finding the year the season ended
		i = 0
		break
	i += 1

print("The top player selected for rebounds was " + playerName + " who averaged " + str(maxReb) + " rebounds per game in the " + str(theSeason1) + "-" + str(theSeason2) + " season as a " + playerPos)


#-- Find the player with the highest average APG in the data set --#

maxAssist = 0 # Holds the maximum number of average assits int he dataset
i = 0 # Resets counter to 0
maxI = 0
for assist in df['Assists Per Game']: # Loops through the data set to determine what the highest average assists per game is

	if assist > maxAssist: # Compares the current assist value to the max value; if the current value is higher then set it as the maximum
		maxAssist = assist
		maxI = i
	i += 1

myTopAssists = float(maxAssist)

i = 0 # Reset counter back to 0
playerName = "" # Will hold the name of the player we are looking for
for name in df['Player Name']: # Find the name of the player with the highest assists per game in the dataset
	if i == maxI:
		playerName = name
		myTopFive.append(playerName)
		i = 0		
		break
		
	i += 1

playerPos = "" # Will hold the position of the player we are looking for
for position in df['Position']: # Finds the position of the palyer with the highest assists per gaem
	
	if i == maxI:
		playerPos = position
		i = 0
		break 
	i += 1

theSeason1 = 0 # Start year of the season
theSeason2 = 0 # Finish year of the season
for season in df['Season']:

	if i == maxI:
		int(season) # Caste as an integer
		theSeason1 = season - 1 # Find the start year of the season
		theSeason2 = season # Find the finish year of the season
		i = 0 # Reset counter
		break
	i += 1

print("The top player selected for assists was " + playerName + " who averaged " + str(maxAssist) + " assists per game in the " + str(theSeason1) + "-" + str(theSeason2) + " season as a " + playerPos)

#-- Find the player with the highest average BPG in the data set --#

maxBlocks = 0 # Set the max BPG to 0
i = 0 # Resets counter to grab row in dataset for loops
maxI = 0 # Counter to hold the index of the data needed
for blocks in df['Blocks Per Game']: # Loops through the BPG column to find what the highest BPG in the dataset is

	if blocks > maxBlocks: # If the current BPG has a higher BPG than the current max value, then set the current BPG as the max
		maxBlocks = blocks
		maxI = i
	i += 1

myTopBlocks = float(maxBlocks)

i = 0
playerName = ""
for name in df['Player Name']: # Loops through to find the name of the player with the highest average BPG in the dataset
	
	if i == maxI:
		playerName = name
		myTopFive.append(playerName) # Add the player to the top 5 list
		i = 0		
		break
		
	i += 1

playerPos = ""
for position in df['Position']: # Loops through to find the position of the player with the highest average BPG
	
	if i == maxI:
		playerPos = position
		i = 0
		break 
	i += 1

theSeason1 = 0
theSeason2 = 0
for season in df['Season']: # Loops through to find the season in which the player scored the highest BPG

	if i == maxI:
		int(season) # Convert to an integer
		theSeason1 = season - 1 # Finding the year the season started
		theSeason2 = season # Finding the year the season ended
		i = 0
		break
	i += 1

print("The top player selected for blocks was " + playerName + " who averaged " + str(maxBlocks) + " blocks per game in the " + str(theSeason1) + "-" + str(theSeason2) + " season as a " + playerPos)

#-- Find the player with the highest Player Efficiency Rating (PER) in the data set --#

maxPER = 0 # Set the max PER to 0
i = 0 # Resets counter to grab row in dataset for loops
maxI = 0 # Counter to hold the index of the data needed
for per in df['Player Efficiency Rating']: # Loops through the PER column to find what the highest PER in the dataset is

	if per > maxPER: # If the current PER has a higher PER than the current max value, then set the current PER as the max
		maxPER = per
		maxI = i
	i += 1

myTopPER = float(maxPER)


i = 0
playerName = ""
for name in df['Player Name']: # Loops through to find the name of the player with the highest average PER in the dataset
	
	if i == maxI:
		playerName = name
		myTopFive.append(playerName) # Add the player to the top 5 list
		i = 0		
		break
		
	i += 1

playerPos = ""
for position in df['Position']: # Loops through to find the position of the player with the highest average PER
	
	if i == maxI:
		playerPos = position
		i = 0
		break 
	i += 1

theSeason1 = 0
theSeason2 = 0
for season in df['Season']: # Loops through to find the season in which the player scored the highest PER

	if i == maxI:
		int(season) # Convert to an integer
		theSeason1 = season - 1 # Finding the year the season started
		theSeason2 = season # Finding the year the season ended
		i = 0
		break
	i += 1

print("The top player selected for PER was " + playerName + " who had a " + str(maxPER) + " PER in the " + str(theSeason1) + "-" + str(theSeason2) + " season as a " + playerPos)

print("Based on the dataset and using the criteria of PPG, RPG, APG, BPG, and PER, the 5 players on my team would be " + myTopFive[0] + ", " + myTopFive[1] + ", " + myTopFive[2] + ", " + myTopFive[3] + ", "+ myTopFive[4])


## -- What position is least likely to turnover the ball? -- ##

print(posGroup['Turnovers Per Game'].mean())


## -- Since the 2001-2002 season, have all the MVPs been in the top 10 list for scoreres? -- ##

mvps = ["Tim Duncan", "Tim Duncan", "Kevin Garnett", "Steve Nash", "Steve Nash", "Dirk Nowitzki", "Kobe Bryant", "LeBron James", "LeBron James", "Derrick Rose", "LeBron James", "LeBron James", "Kevin Durant", "Stephen Curry", "Stephen Curry", "Russell Westbrook", "James Harden", "Giannis Antetokounmpo", "Giannis Antetokounmpo"]
mvpYear = {}
i = 0
for year in years:

	mvpYear[mvps[i]] = years[i]
	i += 1

## -- Should Lebron have more MVPs based on his stats during the MVP seasons (b/w 2011 and 2020 where he didn't win? -- #

count = 0 # Counter for years
theMVPStats = [] # Will hold the relevant stats for the MVP of the observed season
theLebronStats = [] # Will hold the relevant stats for Lebron of the observed season
theMVPList = []

# Loop goes through the list of MVPs of each year of our data set
# Grabs the points, assists, rebounds, steals, blocks, and PER of the MVP
# Skips any year where Lebron was the MVP
# Reports the same info gathered for the MVP (when not Lebron) for Lebron in non-MVP seasons
# Displays bar plots for each stat to compare Lebron and the MVP that season to see how they compare
for mvp in mvps:


	if mvp != "LeBron James" and years[count] > 2003:

		theMVPList.append(mvp)
		theMVP = df[df['Player Name'] == mvp]
		theMVP = theMVP[theMVP['Season'] == years[count]]
		print(mvp + " - " + str(years[count]) + " MVP Stats")
		print("Points: " + str(theMVP['Points Per Game'].sum()))
		print("Assists: " + str(theMVP['Assists Per Game'].sum()))
		print("Rebounds: " + str(theMVP['Rebounds Per Game'].sum()))
		print("Steals: " + str(theMVP['Steals Per Game'].sum()))
		print("Blocks: " + str(theMVP['Blocks Per Game'].sum()))
		print("PER: " + str(theMVP['Player Efficiency Rating'].sum()))
		print('\n')

		theMVPStats.append(theMVP['Points Per Game'].sum())
		theMVPStats.append(theMVP['Assists Per Game'].sum())
		theMVPStats.append(theMVP['Rebounds Per Game'].sum())
		theMVPStats.append(theMVP['Steals Per Game'].sum())
		theMVPStats.append(theMVP['Blocks Per Game'].sum())		
		theMVPStats.append(theMVP['Player Efficiency Rating'].sum())

		lebron = df[df['Player Name'] == "LeBron James"]
		lebron = lebron[lebron['Season'] == years[count]]
		print("LeBron James" + " - " + str(years[count])+ " Stats")
		print("Points: " + str(lebron['Points Per Game'].sum()))
		print("Assists: " + str(lebron['Assists Per Game'].sum()))
		print("Rebounds: " + str(lebron['Rebounds Per Game'].sum()))
		print("Steals: " + str(lebron['Steals Per Game'].sum()))
		print("Blocks: " + str(lebron['Blocks Per Game'].sum()))
		print("PER: " + str(lebron['Player Efficiency Rating'].sum()))
		print('\n')

		theLebronStats.append(lebron['Points Per Game'].sum())
		theLebronStats.append(lebron['Assists Per Game'].sum())
		theLebronStats.append(lebron['Rebounds Per Game'].sum())
		theLebronStats.append(lebron['Steals Per Game'].sum())
		theLebronStats.append(lebron['Blocks Per Game'].sum())
		theLebronStats.append(lebron['Player Efficiency Rating'].sum())

		# Source: Python bar plot - visualize categorical data in python. (2020, September 28). Retrieved April 14, 2021, from https://www.askpython.com/python/python-bar-plot
		# Source: Used class resources/notes/slides (Module 6 Visualization and Visualization.ipynb)
		# Source: Sadawi, N. (2016, December 28). 47- pandas Dataframes: Generating bar and line plots. Retrieved April 14, 2021, from https://www.youtube.com/watch?v=LHeNrY1jGO8&amp;t=260s&amp;ab_channel=NoureddinSadawi
		theStatNames = ["Points", "Assists", "Rebounds", "Steals", "Blocks", "PER"]
		xAxis = np.arange(len(theStatNames))
		# Source: Nalla, G. (2021, February 25). Plotting multiple bar charts using matplotlib in Python. Retrieved April 14, 2021, from https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
		plt.bar(xAxis - 0.2, theMVPStats, 0.4, label = mvp)
		plt.bar(xAxis + 0.2, theLebronStats, 0.4, label = "LeBron James")
		plt.xticks(xAxis, theStatNames)
		plt.xlabel("Stats")
		plt.ylabel("Value")
		plt.title("LeBron James vs " + mvp + " Stats (Year: " + str(years[count]) + ")")
		plt.legend()
		plt.show()

	count += 1
	theMVPStats = []
	theLebronStats = []


### Amber's Code ###

# Ask user for input (lower case and strip response)
askPlayer = input("What player statistics do you want? ").lower().strip() 
# Create column in df with player's name also lower cased
df['name'] = df['Player Name'].str.lower()
# Create new data frame for when the player asked for is in the original dataframe
playerdf = df[df.name == askPlayer] 

# Length of this new dataframe
length = len(playerdf)

# If the length of the new dataframe is greater than 1 then the player is in the list of top 50
if length >= 1:
    # First year the player was in the top 50
    firstyear = playerdf.iloc[0]['Season']

    # Last year the player was in the top 50
    lastyear = playerdf.iloc[length -1]['Season']

    # First position of the player (rename the acronym into words)
    firstpos = playerdf.iloc[0]['Position']
    if firstpos == 'G':
      firstpos = 'guard'
    if firstpos == 'PG':
      firstpos = 'point guard'
    if firstpos == 'SG':
      firstpos = 'shooting guard'
    if firstpos == 'F':
      firstpos = 'forward'
    if firstpos == 'SF':
      firstpos = 'small forward' 
    if firstpos == 'PF':
      firstpos = 'power forward'
    if firstpos == 'C':
      firstpos = 'center'

    # Last position of the player (rename the acronym into words)
    lastpos = playerdf.iloc[length -1]['Position']
    if lastpos == 'G':
      lastpos = 'guard'
    if lastpos == 'PG':
      lastpos = 'point guard'
    if lastpos == 'SG':
      lastpos = 'shooting guard'
    if lastpos == 'F':
      lastpos = 'forward'
    if lastpos == 'SF':
      lastpos = 'small forward' 
    if lastpos == 'PF':
      lastpos = 'power forward'
    if lastpos == 'C':
      lastpos = 'center'

    # Average number of games played
    meangames = round(playerdf['Games Played'].mean(), 2)
    
    # Average number of points scored
    meanpoints = round(playerdf['Points Per Game'].mean(), 2)

    # Print statements of statistics on players
    print('From 2002 to 2020,', askPlayer, 'has been ranked in the top 50 list of NBA players', length, 'times')
    print('He first made the top 50 list in',  firstyear, 'as a', firstpos, 'and last made the list in', lastyear, 'as a', lastpos)
    print('For the years he made the list, he played on average', meangames, 'games and averaged', meanpoints, 'points per game')

# If the length of the new dataframe is less than 1 then the player does not exist
else:
    print("There is no player with that name.")
    
# Create new dataframe with specified columns
dfnew = df.copy()
dfnew = dfnew.drop(columns =['Cities', 'Position', 'Season', 'Games Played', 'Minutes Played Per Game', 'Average Field Goals made', 'Average Field Goals Attempted', 'Average 3-Point Field Goals Made', 'Average 3-Point Field Goals Attempted', 'Average Free Throws Made', 'Average Free Throws Attempted', 'Turnovers Per Game', 'Double Double', 'Triple Double', 'Player Efficiency Rating', 'name'])
# Groupby player names by overall averages of each category to two decimals (each player is only displayed once)
dfnew = round(dfnew.groupby(['Player Name']).mean(), 2)

# Create new columns with the rank value within each category (eg player with most average points per game ranked 1, second average ranked 2)
dfnew['PointsRank'] = dfnew['Points Per Game'].rank(method='min',ascending = False)
dfnew['FGPercentRank'] = dfnew['Field Goal Percentage'].rank(method='min',ascending = False)
dfnew['ThreePointPercentRank'] = dfnew['3-Point Field Goal Percentage'].rank(method='min',ascending = False)
dfnew['FTPercentRank'] = dfnew['Free Throw Percentage'].rank(method='min',ascending = False)
dfnew['ReboundsRank'] = dfnew['Rebounds Per Game'].rank(method='min',ascending = False)
dfnew['AssistsRank'] = dfnew['Assists Per Game'].rank(method='min',ascending = False)
dfnew['StealsRank'] = dfnew['Steals Per Game'].rank(method='min',ascending = False)
dfnew['BlocksRank'] = dfnew['Blocks Per Game'].rank(method='min',ascending = False)


# Create new dataframe only displaying the ranked values
dfrank = dfnew.copy()
dfrank = dfrank.drop(columns =['Points Per Game', 'Field Goal Percentage', '3-Point Field Goal Percentage', 'Free Throw Percentage', 'Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game'])

# Create new column averaging their ranked values across all categories
dfrank['Average Rank'] = round(dfrank.mean(axis=1),2)


# Create new dataframe displaying only the Average Ranked values in ascending order
averagerank = dfrank.copy()
averagerank = averagerank.drop(columns =['PointsRank', 'FGPercentRank', 'ThreePointPercentRank', 'FTPercentRank', 'ReboundsRank', 'AssistsRank', 'StealsRank','BlocksRank'])
averagerank.sort_values(['Average Rank']).head(10)

# Create list of years for duration of dataset
years = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
# Create empty dataframe
fullrankdf = pd.DataFrame()

# For loop through list of years to create one Full Rank List
for year in years:
  # Create new dataframe with specified columns
  yeardf = df.copy()
  yeardf = yeardf.drop(columns =['Games Played', 'Minutes Played Per Game', 'Average Field Goals made', 'Average Field Goals Attempted', 'Average 3-Point Field Goals Made', 'Average 3-Point Field Goals Attempted', 'Average Free Throws Made', 'Average Free Throws Attempted', 'Turnovers Per Game', 'Double Double', 'Triple Double', 'Player Efficiency Rating', 'name'])
  # Only filter for specified year
  yeardf = yeardf[(yeardf['Season'] == year)]
  # Create new columns with the rank value within each category (eg player with most average points per game ranked 1, second average ranked 2)
  yeardf['PointsRank'] = yeardf['Points Per Game'].rank(method='min',ascending = False)
  yeardf['FGPercentRank'] = yeardf['Field Goal Percentage'].rank(method='min',ascending = False)
  yeardf['ThreePointPercentRank'] = yeardf['3-Point Field Goal Percentage'].rank(method='min',ascending = False)
  yeardf['FTPercentRank'] = yeardf['Free Throw Percentage'].rank(method='min',ascending = False)
  yeardf['ReboundsRank'] = yeardf['Rebounds Per Game'].rank(method='min',ascending = False)
  yeardf['AssistsRank'] = yeardf['Assists Per Game'].rank(method='min',ascending = False)
  yeardf['StealsRank'] = yeardf['Steals Per Game'].rank(method='min',ascending = False)
  yeardf['BlocksRank'] = yeardf['Blocks Per Game'].rank(method='min',ascending = False)
  # Create new dataframe only displaying the ranked values
  newdfrank = yeardf.copy()
  newdfrank = yeardf.drop(columns =['Points Per Game', 'Field Goal Percentage', '3-Point Field Goal Percentage', 'Free Throw Percentage', 'Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game'])
  # Create new column averaging their ranked values across all categories
  newdfrank['Average Rank'] = round(newdfrank[['PointsRank', 'FGPercentRank', 'ThreePointPercentRank', 'FTPercentRank', 'ReboundsRank', 'AssistsRank', 'StealsRank', 'BlocksRank']].mean(axis=1),2)
  # Sort the Average Ranked values in ascending order (lower average means higher ranks)
  newdfrank = newdfrank.sort_values(['Average Rank'], ascending = True)
  # Only display first 5 values
  newdfrank = newdfrank.head()
  # Append these first five values to the empty dataframe
  fullrankdf = fullrankdf.append(newdfrank)

# To view full list of all the top five players each year and their rank values
pd.set_option('display.max_rows', None)
fullrankdf

# Ask user for input (lower case and strip response)
askyear = input("What year do you want to see the top 5 players? ").strip() #Ask for user input 
# Create a new dataframe with only the Average Rank and the year specified by user
inputyeardf = fullrankdf.copy()
inputyeardf = inputyeardf.drop(columns =['PointsRank', 'FGPercentRank', 'ThreePointPercentRank', 'FTPercentRank', 'ReboundsRank', 'AssistsRank', 'StealsRank','BlocksRank'])
inputyeardf = inputyeardf[(inputyeardf['Season'] == int(askyear))]
# Display the dataframe indicating the 2top 5 players for that year
if len(inputyeardf) == 5:
  print(inputyeardf)
else:
  print('Invalid year')
