#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import pprint
import csv

pp = pprint.PrettyPrinter(indent=2)
api_key = "db0fd4dde5fa0817e39fbc41457d4060" # Temporary public key available in November 2013


# STEP 1: Get standing of a specific league
# Documentation: https://github.com/menmo/everysport-api-documentation/blob/master/endpoints/GET_leagues_id_standings.md
# - id (required) - The League ID
# - apikey (required) - your APIKEY
# - type - one of 'total' (default), 'home' and 'away'
# - round - specifies standings after a specific round, eg. '10'. Default is the last played round.
# - size - specifies the amount of statistics data for the teams. Default is 'large' which retrieves all available data. Use 'medium' and 'small' to get less data.
# - sort - the key by which the standings is sorted. Can be any of the attribute names from the Team Stats objects (eg. 'stats.pts') or 'team.name' to sort by the name of the team. By default, sorting is by 'stats.pts'.

# Function: get standing from league
def getStandingFromLeague(id, round):
	query_standing = "http://api.everysport.com/v1/leagues/{0}/standings?apikey={1}&round={2}&size=small".format(id,api_key,round) # Define the url
	print query_standing
	response = urllib2.urlopen(query_standing) # Open the url
	response_json = json.load(response) # Read json
	standing = response_json['groups'][0]['standings'] # Get standing
	pos = 1
	for row in standing:
		team = row['team']["name"].encode('utf-8')
		print pos,"-",team
		if team not in data:
			data[team] = {}
		data[team][round] = pos
		pos += 1

# STEP 2: Iterate rounds, get standing at every round and store data
# To get id's of current and  historical leagues, go to http://www.everysport.com/sport/ishockey/2012-2013/elitserien-herr/elitserien/54258
data = {}
league = 54258
rounds = 15
for round in range(1,rounds):
	print "Get standing in round ",round
	getStandingFromLeague(league, round)

# STEP 3: Write data to file
writerClear = csv.writer(open('data.csv', 'w')) # Open data.csv and clear it
headers = ["team"] # Create a list of headers
for round in range(1,rounds): # Append rounds to the list
	headers.append(round)	
writerClear.writerow(headers) # Write row to file

writerAdd = csv.writer(open('data.csv', 'a'))


for team in data: # Iterate data dictionary
	row = [team] # Create row list
	for round in range(1,rounds): # Iterate rounds
		pos = data[team][round] # Get position at given round
		row.append(pos) # Add position to row list
	writerAdd.writerow(row) # Write row to file

#standing_url = "http://api.everysport.com/v1/leagues/{0}/standings/?apikey={1}&round={2}&size=small".format(leagueId,round)

