import dota2api
from operator import itemgetter  
import json
from collections import OrderedDict
import time
from pymongo import MongoClient
import sys
import re
import os

LOCAL = os.environ['SERVER']

# make DB and client global
CLIENT = MongoClient("mongodb://127.0.0.1:27017/")
DB = CLIENT['dota']
API = dota2api.Initialise(
  DB.key.find_one()['steam'],
  logging=True
)

# writes the disk to json for later use
def writeToDisk(name, export):
  with open('{0}/resources/{1}.json'.format(LOCAL, name), 'w') as f:
    json.dump(export, f)
  print('+ wrote {0} to ./resources/{0}.json +'.format(name))

'''
  update items/heroes/leagues Reference()
    calls the api and creates new entries if any are needed
'''
# # updates json where items is stored
def updateItemsReference():
  try:
    items = API.get_game_items();
    items = items['items'];
    print ('! finding new Item !')
    DB.statusCode.save({'_id': 103, 'get_game_items': 'Up'})
  except Exception:
    DB.statusCode.save({'_id': 103, 'get_game_items': 'Down'})
    print('! items api down !')
    return {"0": { 'id': 0, 'url_image': '' } }

  # add blank item
  
  itemJson = {};
  itemJson[0] = {
    'id': 0,
    'url_image': '',
    "recipe": 0
  }

  for index, item in enumerate(items):
    if (item['recipe'] == 1):
      item['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png';
    itemJson[items[index]['id']] = item

  writeToDisk('items', itemJson)
  return itemJson

# updates json where  league is stored 
def formatLeagueReference():
  try:
    getLeagueListing = API.get_league_listing()
    print ('! finding new League !')
    DB.statusCode.save({'_id': 101, 'get_league_listing': 'Up'})
  except Exception:
    DB.statusCode.save({'_id': 101, 'get_league_listing': 'Down'})
    print('! league api down !')
    return {'league_id': 'None'}

  leaguesJson = {}
  leagues = getLeagueListing['leagues']
  for index, league in enumerate(leagues):
    leaguesJson[leagues[index]['leagueid']] = league

  writeToDisk('leagues', leaguesJson)
  return leaguesJson

# update json where heroes is stored
def updateHeroesReference():
  try:
    heroes = API.get_heroes()
    heroes = heroes['heroes'];
    print ('! finding new Hero !')
    DB.statusCode.save({'_id': 102, 'get_heroes': 'Up'})
  except Exception:
    DB.statusCode.save({'_id': 102, 'get_heroes': 'Down'})
    print('! heroes api down !')
    return {}

  heroJson = {}
  heroJson[0] = {
    "id": 0,
    "url_large_portrait": ""
  }

  for index, hero in enumerate(heroes):
    heroJson[heroes[index]['id']] = hero

  writeToDisk('heroes', heroJson)
  return heroJson


# human readable league name, should only be used once per new game
def formatLeague(leagueId):
  # if file doesn't exist go to league'
  try:
    with open('{0}/resources/leagues.json'.format(LOCAL), 'r') as data_file:
      league_data = json.load(data_file)
      if str(leagueId) in league_data:
        league = league_data[str(leagueId)]
      else:
        # raise to run a grab a new file
        raise FileNotFoundError
  except FileNotFoundError:
    # leagueListing = getLeagueListing['leagues']
    # writeLeagueListing('leagues', leagueListing)
    league_data = formatLeagueReference()
    if league_data:
      if str(leagueId) in league_data:
        league = league_data[str(leagueId)]
      else:
        print('! league not found !')
        return {'league_id': 'None'}
    else:
      print('! league api down !')
      return {'league_id': 'None'}

  league.pop('description');
  league.pop('itemdef');

  if 'leagueid' in league:
    league['league_id'] = league['leagueid'];
    league.pop('leagueid') # the naming on this bothered ; all others were seperated by an _ but not this
  
  return league

# human readable league tier
def formatLeagueTier(league_tier):
  leagueTier = {0: 'None', 1: 'Amateur', 2: 'Professional', 3: 'Premier'}
  league_tier = leagueTier[league_tier]
  return league_tier

# human readable series type
def formatSeriesType(series_type):
  seriesType = {0: 'None', 1: 'bo3', 2: 'bo5'}
  series_type = seriesType[series_type]
  return series_type

# used to change map on client side
def nightDayCycle(duration):
  duration = int(duration)
  minutes = int(duration / 60)
  cycle = minutes % 8;
  if cycle < 4:
    return 'day'
  else:
    return 'night'

# change items to an array to easily pull from client
def easyItems(player):
  items = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5']
  regex = re.compile('http://cdn.dota2.com/apps/dota2/images/items/([\w\d_]+)_lg.png')
  try:
    with open('{0}/resources/items.json'.format(LOCAL), 'r') as data_file:
      item_data = json.load(data_file)
      allItems = []
      for item in items:
        # using str() to read from json data
        if str(player[item]) not in item_data:
          raise FileNotFoundError
        regexSearch = regex.search(item_data[str(player[item])]['url_image']);
        if regexSearch:
          allItems.append(regexSearch.group(1))
        else:
          allItems.append('None')
  except FileNotFoundError:
    allItems = []
    item_data = updateItemsReference()
    for item in items:
      # using str() to read from json data
      if str(player[item]) not in item_data:
        player[item] = 0
      regexSearch = regex.search(item_data[player[item]]['url_image']);
      if regexSearch:
        allItems.append(regexSearch.group(1))
      else:
        allItems.append('None')
  for item in items:
    if item in player:
      player.pop(item)
  return allItems

# convert hero_id to hero name that works with link below so client can easily fetch
def easyHeroes(hero_id):
  with open('{0}/resources/heroes.json'.format(LOCAL), 'r') as data_file:
    heroes_data = json.load(data_file)
    regex = re.compile('http://cdn.dota2.com/apps/dota2/images/heroes/([\w\d_]+)_lg.png')
    # using str() to read from json data
    regexSearch = regex.search(heroes_data[str(hero_id)]['url_large_portrait']);
    if regexSearch:
      return regexSearch.group(1)
    else:
      return 'None'

# convert hero_id to hero name that works with link below so client can easily fetch
def formatDraft(draft):
  # try to open file if it exists
  try:
    with open('{0}/resources/heroes.json'.format(LOCAL), 'r') as data_file:
      allDraft = []
      heroes_data = json.load(data_file)
      for hero in draft:
        if str(hero['hero_id']) not in heroes_data:
          raise FileNotFoundError
        regex = re.compile('http://cdn.dota2.com/apps/dota2/images/heroes/([\w\d_]+)_lg.png')
        regexSearch = regex.search(heroes_data[str(hero['hero_id'])]['url_large_portrait']);
        allDraft.append(regexSearch.group(1))
  except FileNotFoundError:
    print('! new Hero !')
    allDraft = []
    heroes_data = updateHeroesReference()
    for hero in draft:
      if hero['hero_id'] not in heroes_data:
        hero['hero_id'] = 0
      regex = re.compile('http://cdn.dota2.com/apps/dota2/images/heroes/([\w\d_]+)_lg.png')
      regexSearch = regex.search(heroes_data[hero['hero_id']]['url_large_portrait']);
      allDraft.append(regexSearch.group(1))
  return allDraft

# remove unneeded values in json
def popUnused(selectedGame):
  selectedGame.pop('players')
  selectedGame.pop('lobby_id')
  selectedGame.pop('league_series_id')
  selectedGame.pop('series_id')
  if 'scoreboard' in selectedGame:
    if 'dire' in selectedGame['scoreboard']:
      if 'abilities' in selectedGame['scoreboard']['dire']:
        selectedGame['scoreboard']['dire'].pop('abilities')
    if 'radiant' in selectedGame['scoreboard']:
      if 'abilities' in selectedGame['scoreboard']['radiant']:
        selectedGame['scoreboard']['radiant'].pop('abilities')

  return selectedGame

# switches barracks/tower to binary format, 1 is true, 0 is false
# https://dota2API.readthedocs.io/en/latest/responses.html#single-team-tower-status
def formatObjectives(scoreboard):
  scoreboard['dire']['barracks_state'] = "{0:06b}".format(scoreboard['dire']['barracks_state'])
  scoreboard['dire']['tower_state'] = "{0:11b}".format(scoreboard['dire']['tower_state'])
  scoreboard['radiant']['barracks_state'] = "{0:06b}".format(scoreboard['radiant']['barracks_state'])
  scoreboard['radiant']['tower_state'] = "{0:11b}".format(scoreboard['radiant']['tower_state'])
  return scoreboard

# organize player and tournament information
def formatPlayers(selectedGame, callLeagueListing):
  
  scoreboard = selectedGame['scoreboard']
  dire = selectedGame['scoreboard']['dire']
  radiant = selectedGame['scoreboard']['radiant']

  # replace league_id with league info, only calls if does not exist in current one.
  if callLeagueListing:
    print('+ formatLeague +')
    selectedGame['league'] = formatLeague(selectedGame['league_id'])
    selectedGame.pop('league_id')
    print('- formatLeague -')

  # LEAGUE_TIER
  print('+ league tier +')
  if 'league_tier' in selectedGame:
    selectedGame['league_tier'] = formatLeagueTier(selectedGame['league_tier'])
  print('- league tier -')

  # SERIES
  print('+ series type +')
  if 'series_type' in selectedGame:
    selectedGame['series_type'] = formatSeriesType(selectedGame['series_type'])
  print('- series type -')
  # TEAM 
  # since I can't get all the pictures I'll do this for now
  # pictures API seems to be broken in some way
  print('+ team +')
  if 'radiant_team' in selectedGame:
    selectedGame['radiant_team_name'] = selectedGame['radiant_team']['team_name']
    selectedGame.pop('radiant_team')
  if 'dire_team' in selectedGame:
    selectedGame['dire_team_name'] = selectedGame['dire_team']['team_name']
    selectedGame.pop('dire_team')
  print('- team -')

  # format draft
  print ('+ draft +')
  if 'bans' in dire: 
    dire['bans'] = formatDraft(dire['bans'])
  '''
  if 'picks' in dire: 
    dire['picks'] = formatDraft(dire['picks'])
  if 'bans' in radiant: 
    radiant['bans'] = formatDraft(radiant['bans'])
  if 'picks' in radiant:
    radiant['picks'] = formatDraft(radiant['picks'])
  '''
  print ('- draft -')

  # format barracks and towers to correct
  scoreboard = formatObjectives(scoreboard)

  # game has started
  # duration is in milliseconds
  # else in drafting phase and nothing needs to be done
  if scoreboard['duration'] > 0:
    
    print('+ time +')
    # just returns seconds / normally seconds and milliseconds
    scoreboard['roshan_respawn_timer'] = int(scoreboard['roshan_respawn_timer'])
    scoreboard['duration'] = int(scoreboard['duration'])
    scoreboard['day_cycle'] = nightDayCycle(scoreboard['duration'])
    print('- time -')

    # create a day night cycle for the client side map

    # add player name to scoreboard dictionary
    print('+ player format +')
    for player in selectedGame['players']:
      for i, p in enumerate(dire['players']):
        if player['account_id'] == p['account_id']:
          dire['players'][i]['position_x'] = int(dire['players'][i]['position_x'])
          dire['players'][i]['position_y'] = int(dire['players'][i]['position_y'])
          dire['players'][i]['items'] = easyItems(dire['players'][i])
          dire['players'][i]['hero'] = easyHeroes(dire['players'][i]['hero_id'])
          dire['players'][i]['name'] = player['name']
      for i, p in enumerate(radiant['players']):
        if player['account_id'] == p['account_id']:
          radiant['players'][i]['position_x'] = int(radiant['players'][i]['position_x'])
          radiant['players'][i]['position_y'] = int(radiant['players'][i]['position_y'])
          radiant['players'][i]['items'] = easyItems(radiant['players'][i])
          radiant['players'][i]['hero'] = easyHeroes(radiant['players'][i]['hero_id'])
          radiant['players'][i]['name'] = player['name']
    print('- player format -')
    # only used player name from players and that is now in the scoreboard

  else:
    # add player name to scoreboard dictionary
    print('@ game not started @')
    print('+ player format +')
    for player in selectedGame['players']:
      for i, p in enumerate(dire['players']):
        if player['account_id'] == p['account_id']:
          dire['players'][i]['name'] = player['name']
      for i, p in enumerate(radiant['players']):
        if player['account_id'] == p['account_id']:
          radiant['players'][i]['name'] = player['name']
    print('- player format -')

  # makes it easier and more consistent to read output

  print('+ pop unused +')
  selectedGame = popUnused(selectedGame)
  print('- pop unused -')
  
  print('+ sort object +')
  selectedGame = sortOD(selectedGame)
  print('- sort object -')

  print ('currentGame', sys.getsizeof(selectedGame))

  return selectedGame

# deep sort on dictionary to makes it easier to read output
def sortOD(od):
    res = OrderedDict()
    for k, v in sorted(od.items()):
        if isinstance(v, dict):
            res[k] = sortOD(v)
        else:
            res[k] = v
    return res

def main():

  callLeagueListing = False

  try:
    liveLeageGame = API.get_live_league_games()
    DB.statusCode.save({'_id': 100, 'get_live_league_games': 'Up'})
  except Exception:
    DB.statusCode.save({'_id': 100, 'get_live_league_games': 'Down'})
    return
  
  try:
    # sort list by spectators
    sortedGamesBySpectators = sorted(liveLeageGame['games'], key=itemgetter('spectators'), reverse=True)
  except Exception as e:
    print('sort by spectators failed')
    print ('error {0}'.format(e))
    return

  # if this fails then something went wrong with the api call and don't run the program
  if len(sortedGamesBySpectators) > 0:
    try:
      for (index, game) in enumerate(sortedGamesBySpectators):
        if 'scoreboard' in game:
          #if game['scoreboard']['duration'] > 60:
          selectedGame = sortedGamesBySpectators[index]
          DB.previousGame.save({'_id': 100, 'newLiveLeagueGame': selectedGame})
          break
        else:
          print ('probably in lobby')

      leagueInfo = DB.currentGame.find_one({"_id": 1})
      if leagueInfo:
        if 'league' in leagueInfo and 'league_id' in selectedGame:
          if selectedGame['league_id'] == leagueInfo['league']['league_id']:
            print ('+ callLeagueListing : False +') 
            selectedGame['league'] = leagueInfo['league'];
            selectedGame.pop('league_id')
          else:
            print ('+ callLeagueListing : True +') 
            callLeagueListing = True
        else:
          print ('+ callLeagueListing : True +')  
          callLeagueListing = True
    except Exception as e:
      print('broke after sorting live games')
      print (e)
      return

    try:
      selectedGame = formatPlayers(selectedGame, callLeagueListing)
    except Exception as e:
      print ('format player failed')
      print('error {0}'.format(e))
      return

    try:
      writeToDisk('currentGame', selectedGame)
      selectedGame['_id'] = 1
      _id = DB.currentGame.save(selectedGame)
    except Exception as e:
      print('mongodb save failed')
      print('error {0}'.format(e))
      return
  else:
    print('game length < 0')

if __name__ == '__main__':
  start_time = time.time()
  main()
  print("--- %s seconds ---" % (time.time() - start_time))
  CLIENT.close()
