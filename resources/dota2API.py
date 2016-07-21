import dota2api
from operator import itemgetter  
import json
import collections
import time
import os
from pymongo import MongoClient
import sys
from pprint import pprint
from deepdiff import DeepDiff
#used for testing size
def writeToDisk(name, export):
  print('writing {0}'.format(name))
  with open('./{0}.txt'.format(name), 'w') as f:
    f.write(json.dumps(export, separators=(',',':')))

def formatItem(player, items):
    print('formatedItem')
    newItems = []
    for x in range(0, 6):
      currentItem = 'item'+str(x)
      newItems.append(player[currentItem])
      player.pop(currentItem)
    player['items'] = newItems;
    return player

def formatDraft(draft):
    # change draft dictionary to array
    newDraft = []
    for index, hero in enumerate(draft):
      newDraft.append(hero['hero_id'])

    return newDraft

def formatItemReference(items):
  #items['base_url'] = 'http://cdn.dota2.com/apps/dota2/images/items/'
  
  for index, item in enumerate(items):
    # items[index]['url_image'] = items[index]['url_image'].split('/')[-1]
    # items[index]['url_image'] = items[index]['url_image'].replace("_lg.png", ' ')

      # print (items[index]['url_image'])
    if (item['recipe'] == 1):
      items[index]['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'
     # items[index].pop('side_shop')
     # items[index].pop('secret_shop')
      #items[index].pop('cost')
    # items[index].pop('name')
    # items[index].pop('recipe')
  
  writeToDisk('items', items)
  # each player has 6 item slots
  ''' 
  for x in range(0, 6):
    currentItem = 'item'+str(x)
    player_item = player[currentItem]
    player_item_info = {}
    for item in items:
      if item['id'] == player_item:
        player_item_info = item['localized_name'];
        print (item)
        if (item['recipe'] == 1):
          player_item_info = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'
    player[currentItem] = player_item_info
  '''
  '''
    player_item_info = {}
    if (player[currentItem]) > 0:
      player_item = player[currentItem]
  
      player_item_info = next(item for item in items if item['id'] == player_item)
      if (player_item_info['recipe'] == 1):
        player_item_info['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'
      
    else:
      player_item_info = 0
    allItems.append(player_item_info)
    player.pop(currentItem)
  player['items'] = allItems
  '''

def getItemMetaData(player, items):
  allItems = []
  for x in range(0, 6):
    currentItem = 'item'+str(x)
    player_item = player[currentItem]
    player_item_info = {}
    
    if (player[currentItem]) > 0:
      player_item = player[currentItem]
  
      player_item_info = next(item for item in items if item['id'] == player_item)
      if (player_item_info['recipe'] == 1):
        player_item_info['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'
      
    else:
      player_item_info = 0
    player.pop(currentItem)
    allItems.append(player_item_info)
  
  player['items'] = allItems
  return player

# grab league name, shoudl only be used once per new game
def formatLeague(api, leagueId):
  getLeagueListing = api.get_league_listing()
  leagueListing = getLeagueListing['leagues']
  writeToDisk('LeagueListings', leagueListing)
  league = next(league for league in leagueListing if leagueId == league['leagueid'])
  writeToDisk('league', league)
  league.pop('description');
  if 'leagueid' in league:
    league.pop('leagueid') # the naming on this bothered ; all others were seperated by an _ but not this
    league['league_id'] = leagueId;

  return league

def formatLeagueTier(league_tier):
  leagueTier = {0: 'None', 1: 'Amateur', 2: 'Professional', 3: 'Premier'}
  league_tier = leagueTier[league_tier]
  return league_tier

def formatSeriesType(series_type):
  seriesType = {0: 'None', 1: 'bo1', 2: 'bo3', 3: 'bo5'}
  series_type = seriesType[series_type]
  return series_type

# (NOTE) possibly shorten to abbreviations if I need more space 
def formatTowers(towers):
  objectives = [
    'ancient_bottom',
    'ancient_top',
    'bottom_tier_3',
    'bottom_tier_2',
    'bottom_tier_1',
    'middle_tier_3',
    'middle_tier_2',
    'middle_tier_1',
    'top_tier_3',
    'top_tier_2',
    'top_tier_1'
  ]
  splitTowers = list("{0:011b}".format(towers))
  allTowers = []
  for index, objective in enumerate(objectives): 
    allTowers.append({objective: splitTowers[index]})
  return allTowers

def formatBarracks(barracks):
  objectives = [
    'bottom_ranged',
    'bottom_melee',
    'middle_ranged',
    'middle melee',
    'top_ranged',
    'top_melee'
  ]
  splitBarracks = list("{0:06b}".format(barracks))
  allBarracks = []
  for index, objective in enumerate(objectives): 
    allBarracks.append({objective: splitBarracks[index] })
  return allBarracks


# seconds to MM:SS
def formatTime(duration):
  duration = int(duration)
  minutes, seconds = divmod(duration, 60)
  return ('{0:02d}:{1:02d}'.format(minutes, seconds), minutes)

def nightDayCycle(duration):
  duration = int(duration)
  minutes = int(duration / 60)
  cycle = minutes % 8;
  if cycle < 4:
    return 'day'
  else:
    return 'night'

# organize player and tournament information
def formatPlayers(api, heroes, items, selectedGame):

  #matchDetails = api.get_match_details(match_id=2484820760)
  #print (matchDetails)

  
  # possibly drop the json that is only used once with the rest of the requests
  if 'league' not in selectedGame:
    selectedGame['league'] = formatLeague(api, selectedGame['league_id'])
    selectedGame.pop('league_id')

  if 'league_tier' in selectedGame:
    selectedGame['league_tier'] = formatLeagueTier(selectedGame['league_tier'])

  if 'series_type' in selectedGame:
    selectedGame['series_type'] = formatLeagueTier(selectedGame['series_type'])  
  '''
  if 'radiant_team' in selectedGame:
    selectedGame['radiant_team_name'] = selectedGame['radiant_team']['team_name']
    selectedGame.pop('radiant_team')
  if 'dire_team' in selectedGame:
    selectedGame['dire_team_name'] = selectedGame['dire_team']['team_name']
    selectedGame.pop('dire_team')
  '''


  selectedGame['scoreboard']['duration'] = int(selectedGame['scoreboard']['duration'])
  # MAKE SMALLER
  # picks and bans are always shown in the same order
  '''
  selectedGame['scoreboard']['radiant']['picks'] = formatDraft(selectedGame['scoreboard']['radiant']['picks'])
  selectedGame['scoreboard']['radiant']['bans'] = formatDraft(selectedGame['scoreboard']['radiant']['bans'])
  selectedGame['scoreboard']['dire']['picks'] = formatDraft(selectedGame['scoreboard']['dire']['picks'])
  selectedGame['scoreboard']['dire']['bans'] = formatDraft(selectedGame['scoreboard']['dire']['bans'])
  '''
  # game officially started
  # all players have picked heroes
  # false would mean game is in drafting phase

  # selectedGame['scoreboard']['duration'] = 0
  if (selectedGame['scoreboard']['duration'] > 1):

    if selectedGame['scoreboard']['roshan_respawn_timer'] > 0:
      (selectedGame['scoreboard']['roshan_respawn_timer'], minutes) = formatTime(selectedGame['scoreboard']['roshan_respawn_timer'])
    
    (selectedGame['scoreboard']['time'], minutes) = formatTime(selectedGame['scoreboard']['duration'])

    

    # tower and barracks are stored as integers that need to be processed as binary
    # doing the conversion server side. trying to limit what the client has to do.
    
    selectedGame['scoreboard']['radiant']['tower_state'] = formatTowers(selectedGame['scoreboard']['radiant']['tower_state'])
    selectedGame['scoreboard']['dire']['tower_state'] = formatTowers(selectedGame['scoreboard']['dire']['tower_state'])
    selectedGame['scoreboard']['radiant']['barracks_state'] = formatBarracks(selectedGame['scoreboard']['radiant']['barracks_state'])
    selectedGame['scoreboard']['dire']['barracks_state'] = formatBarracks(selectedGame['scoreboard']['dire']['barracks_state'])
    
    selectedGame['scoreboard']['day_cycle'] = nightDayCycle(selectedGame['scoreboard']['duration'])
    
    for player in selectedGame['players']:
      for i, p in enumerate(selectedGame['scoreboard']['radiant']['players']):
        if player['account_id'] == p['account_id']:
          
          # selectedGame['scoreboard']['radiant']['players'][i] = formatItem(selectedGame['scoreboard']['radiant']['players'][i], items)
          
          selectedGame['scoreboard']['radiant']['players'][i]['position_y'] = int(selectedGame['scoreboard']['radiant']['players'][i]['position_y'])
          selectedGame['scoreboard']['radiant']['players'][i]['position_x'] = int(selectedGame['scoreboard']['radiant']['players'][i]['position_x'])

          # position of array I'll be overwritting'
          playerMetaInfo = selectedGame['scoreboard']['radiant']['players'][i]

          # individual hero id for logging
          heroId = player['hero_id']

          #playerMetaInfo['name'] = player['name']
          selectedGame['scoreboard']['radiant']['players'][i] = playerMetaInfo
          # add hero name
          playerMetaInfo['hero'] = next(hero for hero in heroes if hero['id'] == heroId )
          playerMetaInfo.pop('hero_id')
          selectedGame['scoreboard']['radiant']['players'][i] = playerMetaInfo
          # add items metadata array list and delete individual items
          playerMetaInfo = getItemMetaData(playerMetaInfo, items)

          selectedGame['scoreboard']['radiant']['players'][i] = playerMetaInfo

      for i, p in enumerate(selectedGame['scoreboard']['dire']['players']):
        if player['account_id'] == p['account_id']:

            # selectedGame['scoreboard']['dire']['players'][i] = formatItem(selectedGame['scoreboard']['dire']['players'][i], items)
            selectedGame['scoreboard']['dire']['players'][i]['position_y'] = int(selectedGame['scoreboard']['dire']['players'][i]['position_y'])
            selectedGame['scoreboard']['dire']['players'][i]['position_x'] = int(selectedGame['scoreboard']['dire']['players'][i]['position_x'])

            #position of array I'll be overwritting'
            playerMetaInfo = selectedGame['scoreboard']['dire']['players'][i]
            #individual hero id for logging
            heroId = player['hero_id']

            # print (player['name'])
            #playerMetaInfo['name'] = player['name']
            
            # add hero name
            print (heroId)
            playerMetaInfo['hero'] = next(hero for hero in heroes if hero['id'] == heroId )
            playerMetaInfo.pop('hero_id')
          
            # add items metadata array list and delete individual items
            playerMetaInfo = getItemMetaData(playerMetaInfo, items)

            selectedGame['scoreboard']['dire']['players'][i] = playerMetaInfo
      

  else:
    draftGame = {}
    draftGame = selectedGame.copy()
    draftGame.pop('scoreboard')
    
    draftGame['scoreboard'] = {}
    draftGame['scoreboard']['radiant'] = {}
    draftGame['scoreboard']['dire'] = {}
    draftGame['scoreboard']['radiant']['picks'] = {}
    draftGame['scoreboard']['radiant']['bans'] = {}
    draftGame['scoreboard']['dire']['picks'] = {}
    draftGame['scoreboard']['dire']['bans'] = {}

    draftGame['scoreboard']['radiant']['picks'] = draft(selectedGame['scoreboard']['radiant']['picks'], heroes)
    draftGame['scoreboard']['radiant']['bans'] = draft(selectedGame['scoreboard']['radiant']['bans'], heroes)
    draftGame['scoreboard']['dire']['picks'] = draft(selectedGame['scoreboard']['dire']['picks'], heroes)
    draftGame['scoreboard']['dire']['bans'] = draft(selectedGame['scoreboard']['dire']['bans'], heroes)
    writeToDisk('draftGame', draftGame)
    return draftGame
    # selectedGame.pop('scoreboard')

 
  print (sys.getsizeof(selectedGame))
  # selectedGame.pop('players')
  selectedGame = collections.OrderedDict(sorted(selectedGame.items()))
  stringy = json.dumps(selectedGame);
  json.loads(stringy)

  writeToDisk('selectedGame', selectedGame)

  print ('selectedGame', sys.getsizeof(selectedGame))
  # writeToDisk('onlyScoreboard', selectedGame['scoreboard'])
  # print ('scoreboard', sys.getsizeof(selectedGame['scoreboard']))

  return selectedGame

def draft(draft, heroes):
  newDraft = []
  for picks in draft:
    for hero in heroes:
      if picks['hero_id'] == hero['id']:
        newDraft.append(hero)
  return newDraft

def findDiff(d1, d2, path=""):
    for k in d1.keys():
        if k not in d2:
            print (path, ":")
            print (k + " as key not in d2", "\n")
        else:
            if type(d1[k]) is dict:
                if path == "":
                    path = k
                else:
                    path = path + "->" + k
                findDiff(d1[k],d2[k], path)
            else:
                if d1[k] != d2[k]:
                    print (path, ":")
                    print (" - ", k," : ", d1[k])
                    print (" + ", k," : ", d2[k]) 

def main():

  client = MongoClient("mongodb://localhost:27017/")

  db = client['dota']
  collection  = db.key.find()[0]

  start_time = time.time()  
  api = dota2api.Initialise(
    collection['steam'],
    # logging=True # add in production
  )

  heroes = api.get_heroes()
  heroes = heroes['heroes'];

  items = api.get_game_items();
  items = items['items'];
  formatItemReference(items)
  liveLeageGame = api.get_live_league_games()

  # sort list by spectators
  sortedGamesBySpectators = sorted(liveLeageGame['games'], key=itemgetter('spectators'), reverse=True)

  selectedGame = sortedGamesBySpectators[0]

  # try :
    # api.get_match_details(match_id=selectedGame['match_id'])
  #except Exception:
    #formatPlayers(api, heroes, items, selectedGame)

  selectedGame = formatPlayers(api, heroes, items, selectedGame)

  selectedGame['_id'] = 1
  _id = db.currentGame.save(selectedGame)
  # currentGame = db.currentGame.find({'_id': 1})
  # game1 = db.currentGame.find()[0]
  # game2 = db.currentGame.find()[1]

  # pprint(DeepDiff(game1, game2))

if __name__ == '__main__':
  start_time = time.time()
  main()
  print("--- %s seconds ---" % (time.time() - start_time))
  print (os.path.getsize('./selectedGame.txt') / 1000)

