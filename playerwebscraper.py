import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import xlwt
from xlwt import Workbook

class Team():
	def __init__(self, team_name, stats_link, roster):
		self.team_name = team_name
		self.stats_link = stats_link
		self.roster = roster

class Player():
	def __init__(self, name, ppg):
		self.name = name
		self.ppg = ppg

def ScrapeNCAATeamData():
	url = 'https://www.espn.com/mens-college-basketball/teams/_/group/50'
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	results = soup.find(id="fittPageContainer")
	teams = results.find_all("div", class_="pl3")

	team_data = []
	for team in teams:
		team_name = team.find("h2", class_="di").text
		stats_link = 'https://www.espn.com' + team.find_all("a")[1]["href"]
		team_data.append( Team(team_name, stats_link, []) )

	return team_data

def ScrapeTeamRosterData(link):
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')

	results = soup.find(id="fittPageContainer")
	table = results.find("table", class_="Table")
	players = table.find_all("tr", class_="Table__TR")
	
	player_data = []
	counter = 0
	for player in players:
		name = player.find("a")

		if(name == None):
			continue
		else:
			if(counter > 4):
				continue
			else:
				player_data.append( Player(name.text, None) )
				counter = counter + 1

	stats_html = results.find("div", class_="Table__Scroller")
	stats_table = stats_html.find_all("tr", class_="Table__TR")

	counter = 0
	for stat in stats_table:
		ppg = stat.find_all("span")[2].text

		if(ppg.isalpha() or counter > 4):
			continue
		else:
			player_data[counter].ppg = ppg
			counter = counter + 1

	return player_data

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

teams = ScrapeNCAATeamData()
for team in teams:
	team.roster = ScrapeTeamRosterData(team.stats_link)

index = 0
for team in teams:
	sheet1.write(index, 0, team.team_name)
	index = index + 1
	for player in team.roster:
		sheet1.write(index, 0, player.name + " (" + player.ppg + ")")
		index = index + 1

wb.save('xlwt ncaatourneydata.xls')
