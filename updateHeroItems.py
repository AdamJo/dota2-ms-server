import dota2api
from pymongo import MongoClient
import json

# writes file as txt to local
def writeToDisk(name, export):
  with open('./resources/{0}.txt'.format(name), 'w') as f:
    f.write(json.dumps(export, separators=(',',':')))

# writes file as json to local
def jsonWriteToDisk(name, export):
  with open('./resources/{0}.json'.format(name), 'w') as f:
    f.write(json.dumps(export, separators=(',',':')))
  print('+ wrote {0} to ./resources/{0}.json +'.format(name))

# convert from array of object to key and object
# adds blank item slot and replaces recipe url to work
def formatItemReference(items):
  # add blank item
  blankId = {
    'id': 0,
    'localized_name': '', 
    'name': 'blank',
    'url_image': '',
    "cost": 0,
    "side_shop": 0,
    "secret_shop": 0,
    "recipe": 0
  }
  itemJson = {};
  for index, item in enumerate(items):
    if (item['recipe'] == 1):
      items[index]['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png'
      item['url_image'] = 'http://cdn.dota2.com/apps/dota2/images/items/recipe_lg.png';
    itemJson[items[index]['id']] = item
  itemJson["0"] = blankId
  jsonWriteToDisk('items', itemJson)

  items = [blankId] + items
  writeToDisk('items', items)

# convert from array of object to key and object
# adds "0" hero incase 
def updateHeroes(api):
  heroes = api.get_heroes()
  heroes = heroes['heroes'];
  heroJson = {}
  heroJson['0'] = {"url_full_portrait": "",
    "localized_name": "",
    "url_vertical_portrait": "",
    "name": "",
    "id": 0,
    "url_large_portrait": "",
    "url_small_portrait": ""
  }
  for index, hero in enumerate(heroes):
    heroJson[heroes[index]['id']] = hero
  
  jsonWriteToDisk('heroes', heroJson)
  writeToDisk('heroes', heroes)

# grabs items from steam api
def updateItems(api):
  items = api.get_game_items();
  items = items['items'];
  formatItemReference(items)

# starts mongo, grabs key, runs update
def main():
  client = MongoClient("mongodb://127.0.0.1:27017/")

  db = client['dota']
  collection  = db.key.find_one()

  api = dota2api.Initialise(
    collection['steam'],
    logging=False # add in production
  )

  updateItems(api)
  updateHeroes(api)

if __name__ == '__main__':
  main()
