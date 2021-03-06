import dota2api
from operator import itemgetter  
import json
from collections import OrderedDict
import time
from pymongo import MongoClient
import sys
import re
import os
import datetime

import requests;

LOCAL = os.environ['SERVER']
MONGO_LINK = os.environ['MONGO_LINK']

# make DB and client global
CLIENT = MongoClient(MONGO_LINK)
DB = CLIENT['dota']
key = DB.key.find_one()['steam']
API = dota2api.Initialise(
  key,
  # logging=True
)

All_GAMES = []
NEW_GAMES = []

# writes file as txt to local
def writeToDiskTxt(name, export):
  with open('./resources/{0}.txt'.format(name), 'w') as f:
    f.write(json.dumps(export, separators=(',',':')))


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
    time.sleep(1.2)
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
    time.sleep(1.2)
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
    time.sleep(1.2)
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

  # league.pop('description');
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
def formatSeriesType(seriesTypeWins, wins):
  series = []
  seriesType = {0: 1, 1: 2, 2: 3}
  seriesTypes = seriesType[seriesTypeWins]

  series = [-1]*(seriesTypes)
  for x in range(wins):
    series[x] = 1;
  return series

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
  vials = [1025, 1026, 1027, 1024, 1021, 1022, 1023];
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
          if player[item] in vials:
            allItems.append('None')
          else:
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

  allDraft = allDraft + [-1]*(5 - len(allDraft))
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

def buybackStatus(gameTime, level):
  minutes = int(gameTime / 60)
  return int(round(100 + ( level * level * 1.5 ) + (minutes * 15)))


# switches barracks/tower to binary format, 1 is true, 0 is false
# https://dota2API.readthedocs.io/en/latest/responses.html#single-team-tower-status
def formatObjectives(scoreboard):
  scoreboard['dire']['barracks_state'] = "{0:06b}".format(scoreboard['dire']['barracks_state'])
  scoreboard['dire']['tower_state'] = "{0:11b}".format(scoreboard['dire']['tower_state'])
  scoreboard['radiant']['barracks_state'] = "{0:06b}".format(scoreboard['radiant']['barracks_state'])
  scoreboard['radiant']['tower_state'] = "{0:11b}".format(scoreboard['radiant']['tower_state'])
  return scoreboard

def didGameStart(scoreboard):
  for player in scoreboard['dire']['players']:
    if (player['hero_id'] == 0):
      return False
  for player in scoreboard['radiant']['players']:
    if (player['hero_id'] == 0):
      return False
  return True;

# organize player and tournament information
def formatPlayers(selectedGame, callLeagueListing):

  scoreboard = selectedGame['scoreboard']
  dire = selectedGame['scoreboard']['dire']
  radiant = selectedGame['scoreboard']['radiant']

  # replace league_id with league info, only calls if does not exist in current one.
  # if callLeagueListing:
  print('+ formatLeague +')
  selectedGame['league'] = formatLeague(selectedGame['league_id'])
  # selectedGame.pop('league_id')
  print('- formatLeague -')

  # LEAGUE_TIER
  # print('+ league tier +')
  # if 'league_tier' in selectedGame:
  #   selectedGame['league_tier'] = formatLeagueTier(selectedGame['league_tier'])
  # print('- league tier -')

  # SERIES
  print('+ series type +')
  if 'series_type' in selectedGame and 'dire_series_wins' in selectedGame and 'radiant_series_wins' in selectedGame:
    selectedGame['series'] = { 
      'dire_series_wins': formatSeriesType(selectedGame['series_type'], selectedGame['dire_series_wins']),
      'radiant_series_wins': formatSeriesType(selectedGame['series_type'], selectedGame['radiant_series_wins'])
    }

  print('- series type -')
  # TEAM 
  # since I can't get all the pictures I'll do this for now
  # pictures API seems to be broken in some way
  print('+ team +')
  if 'radiant_team' in selectedGame:
    if len(selectedGame['radiant_team']['team_name']) > 0:
      selectedGame['radiant_team_name'] = selectedGame['radiant_team']['team_name']
      selectedGame.pop('radiant_team')
    else:
      selectedGame['radiant_team_name'] = 'Radiant'
      selectedGame.pop('radiant_team')
  else:
    selectedGame['radiant_team_name'] = 'Radiant'
  if 'dire_team' in selectedGame:
    if len(selectedGame['dire_team']['team_name']) > 0:
      selectedGame['dire_team_name'] = selectedGame['dire_team']['team_name']
      selectedGame.pop('dire_team')
    else:
      selectedGame['dire_team_name'] = 'Dire'
      selectedGame.pop('dire_team')
  else:
    selectedGame['dire_team_name'] = 'Dire'
  print('- team -')

  # format draft
  print ('+ draft +')
  if 'bans' in dire: 
    dire['bans'] = formatDraft(dire['bans'])
  else:
    dire['bans'] = [-1, -1, -1, -1, -1]

  if 'picks' in dire: 
    dire['picks'] = formatDraft(dire['picks'])
  else:
    dire['picks'] = [-1, -1, -1, -1, -1]

  if 'bans' in radiant: 
    radiant['bans'] = formatDraft(radiant['bans'])
  else:
    radiant['bans'] = [-1, -1, -1, -1, -1]

  if 'picks' in radiant:
    radiant['picks'] = formatDraft(radiant['picks'])
  else:
    radiant['picks'] = [-1, -1, -1, -1, -1]

  print ('- draft -')

  # format barracks and towers to correct
  scoreboard = formatObjectives(scoreboard)
  scoreboard['did_game_start'] = didGameStart(scoreboard)
  # game has started
  # duration is in milliseconds
  # else in drafting phase and nothing needs to be done
  if scoreboard['did_game_start']:

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
          if (player['name']):
            dire['players'][i]['name'] = player['name']
          else:
            print("! hero name did not exist !")
            scoreboard['did_game_start'] = False
          dire['players'][i].pop('hero_id')
          dire['players'][i]['buyback_status'] = buybackStatus(scoreboard['duration'], dire['players'][i]['level'])
      for i, p in enumerate(radiant['players']):
        if player['account_id'] == p['account_id']:
          radiant['players'][i]['position_x'] = int(radiant['players'][i]['position_x'])
          radiant['players'][i]['position_y'] = int(radiant['players'][i]['position_y'])
          radiant['players'][i]['items'] = easyItems(radiant['players'][i])
          radiant['players'][i]['hero'] = easyHeroes(radiant['players'][i]['hero_id'])
          if (player['name']):
            radiant['players'][i]['name'] = player['name']
          else:
            print("! hero name did not exist !")
            scoreboard['did_game_start'] = False
          radiant['players'][i].pop('hero_id')
          radiant['players'][i]['buyback_status'] = buybackStatus(scoreboard['duration'], radiant['players'][i]['level'])
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

def pullPlayers():

  callLeagueListing = False
  count = 0;

  try:
    time.sleep(1)
    liveLeageGame = API.get_live_league_games()
    time.sleep(.2)
    DB.statusCode.save({'_id': 100, 'get_live_league_games': 'Up'})
  except Exception:
    DB.statusCode.save({'_id': 100, 'get_live_league_games': 'Down'})
    return
  
  try:
    # sort list by spectators
    sortedGamesBySpectators = sorted(liveLeageGame['games'], key=itemgetter('spectators'), reverse=True)
    # writeToDisk('gamesSorted', sortedGamesBySpectators)
  except Exception as e:
    print('sort by spectators failed')
    print ('error {0}'.format(e))
    return

  # if this fails then something went wrong with the api call and don't run the program
  if len(sortedGamesBySpectators) > 0:
    for index, game in enumerate(sortedGamesBySpectators):
      if 'scoreboard' in sortedGamesBySpectators[index]:
        # only grab game where both sides have at least 1 player and at most 5
        if (
          len(sortedGamesBySpectators[index]['scoreboard']['dire']['players']) >= 1 and
          len(sortedGamesBySpectators[index]['scoreboard']['dire']['players']) <= 5 and
          len(sortedGamesBySpectators[index]['scoreboard']['radiant']['players']) >= 1 and
          len(sortedGamesBySpectators[index]['scoreboard']['radiant']['players']) <= 5):
          # determines if game is a bot game with league pass
          if len(sortedGamesBySpectators[index]['players']) > len(sortedGamesBySpectators[index]['scoreboard']['dire']['players']):
            selectedGame = sortedGamesBySpectators[index]

            selectedGame = formatPlayers(selectedGame, callLeagueListing)

            try:
              NEW_GAMES.append(selectedGame['match_id'])
              selectedGame['_id'] = selectedGame['match_id']
              DB.topGames.save(selectedGame)
              count += 1
              if count == 5:
                return
            except Exception as e:
              print('mongodb save failed')
              print('error {0}'.format(e))
              return
  else:
    print('game length < 0')

def getRealTimeStats(serverSteamId):
  getRealTimeStats = 'https://api.steampowered.com/IDOTA2MatchStats_570/GetRealtimeStats/v1/?key={0}&server_steam_id={1}'.format(key, serverSteamId)
  realTimeStatsRequest = requests.get(getRealTimeStats)
  try:
    if 'teams' in realTimeStatsRequest.json():
      realTimeStatsTeamRequest = realTimeStatsRequest.json()['teams']
      if len(realTimeStatsTeamRequest[0]['players']) > 0 and len(realTimeStatsTeamRequest[1]['players']) > 0:
        return realTimeStatsTeamRequest[0]['players'] + realTimeStatsTeamRequest[1]['players']
      else:
       return []
    else:
      return []
  except Exception as e:
    print('stats not found')
    print('error {0}'.format(e))
    return []



def getTopLiveGames():
  print ('- mmr -')
  players = []
  mmr = []
  allMmrGames = []

  try:
    time.sleep(1)
    topLiveGames = API.get_top_live_games() 
  except Exception as e:
    print('game not found in top live games')
    print('error {0}'.format(e))
    return
  
  if 'game_list' in topLiveGames:
    sortedTopLiveGames = sorted(topLiveGames['game_list'], key=itemgetter('average_mmr'), reverse=True)
  else:
    sortedTopLiveGames = []
  
  if len(sortedTopLiveGames) > 0:
    # sort games by ranked matchmaking and players
    for game in sortedTopLiveGames:
      print(game['lobby_type'], game['game_time'])
      if (game['lobby_type'] == 7 and 'players' in game and game['game_time'] > 0):
        # find game games with correct number of players
        if (len(game['players']) == 10):
          mmr.append(game)

    print(len(mmr), 'length mmr found');
    if (len(mmr) > 0):
      for (position, mmrGame) in enumerate(mmr[0:5]):
        # get all player account id
        for index, player in enumerate(mmrGame['players']):
          mmrGame['players'][index]['hero'] = easyHeroes(player['hero_id'])
          mmrGame['players'][index].pop('hero_id')

        time.sleep(1)
        realTimeStatsTeam = getRealTimeStats(mmrGame['server_steam_id'])
  
        if realTimeStatsTeam:
          for (index, game) in enumerate(mmrGame['players']):
            mmrGame['players'][index]['name'] = realTimeStatsTeam[index]['name']
            mmrGame['players'][index]['kills'] = realTimeStatsTeam[index]['kill_count']
            mmrGame['players'][index]['deaths'] = realTimeStatsTeam[index]['death_count']
            mmrGame['players'][index]['assists'] = realTimeStatsTeam[index]['assists_count']
            mmrGame['players'][index].pop('account_id')

        allMmrGames.append(mmrGame)
        
      # save to same slot in db
      DB.mmrTop.save({'_id': 1, 'games': allMmrGames})
  else:
    DB.mmrTop.save({'_id': 1, 'games': []})
  print ('+ mmr +')

def getMatchDetails(matchId, leagueTier, leagueName):
  time.sleep(1.2)
  try:
    game = API.get_match_details(matchId) 
  except Exception as e:
    print('game not found in match history')
    print('error {0}'.format(e))
    return

  try:
    print('+ match details +')
    if (game.get('dire_name') != None or
        game.get('dire_name') != 'Dire' or
        game.get('radiant_name') != None or
        game.get('radiant_name') != 'Radiant'):
    
      DB.matchHistory.save(
        {
          'match_id': matchId,
          'league_tier': leagueTier,
          'league_name': leagueName,
          'start_time': game.get('start_time', None),
          'duration': game.get('duration', None),
          'dire_name': game.get('dire_name', 'Dire'),
          'dire_score': game.get('dire_score', None),
          'cluster_name': game.get('cluster_name', None),
          'positive_votes': game.get('positive_votes', 0),
          'negative_votes': game.get('negative_votes', 0),
          'radiant_name': game.get('radiant_name', 'Radiant'),
          'radiant_win': game.get('radiant_win', None),
          'radiant_score': game.get('radiant_score', 0),
          'createdAt': datetime.datetime.now()
        });
      print('+ match details saved +')

  except Exception as e:
    print('mongodb save failed')
    print('error {0}'.format(e))
    return

if __name__ == '__main__':
  start_time = time.time()
  All_GAMES = DB.topGames.find()

  pullPlayers()
  if NEW_GAMES:
    DB.statusCode.save({'_id': 99, 'steamStatus': 'Up'})
    for games in All_GAMES:
      if games['match_id'] not in NEW_GAMES:
        if (games['match_id'] > 0 and games['league_tier'] > 1):
          getMatchDetails(games['match_id'], games['league_tier'], games['league']['name'])
        DB.topGames.delete_one({'_id': games['match_id']})
      else:
        print(games['league_tier'])
  else:
    DB.statusCode.save({'_id': 99, 'steamStatus': 'Down'})
  getTopLiveGames()
  print("--- %s seconds ---" % (time.time() - start_time))
  CLIENT.close()
