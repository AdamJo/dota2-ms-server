const dotenv = require('dotenv').config();
const request = require('request');
const sortObj = require('sort-object');
const MongoClient = require('mongodb').MongoClient;
const firebase = require('firebase');
const fs = require('fs');
const Rx= require('rxjs')

URLS = {
  'GetLeagueListing' : `http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1/?key=${process.env.steamApiKey}`,
  'GetLiveLeagueGames' : `https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key=${process.env.steamApiKey}`
}

function easyItems(player) {
  let allItems = [];
  let items = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5'];
  for (let item of items) {
      //console.log(JSON.parse(data)[player[item]])    
      allItems.push(player[item]);
      delete player[item];
  };
  return allItems;
}

function formatLeague(selectedGame) {
  console.log(callLeagueListing, 'formatLeague')
  if (callLeagueListing) {
    console.log('call League')
    let leagueId = selectedGame['league_id'];
    request.get(URLS['GetLeagueListing'],  (error, response, body) => {
      if (error) {
        console.log('get league failed ', error);
      }
      else {
        leagueListing = JSON.parse(body)['result']['leagues'];
        //writeToDisk('LeagueListings', leagueListing)
        for (league of leagueListing) {
          if (leagueId === league['leagueid']) {
            delete league['description'];
            delete league['itemdef'];
            league['name'].replace('#DOTA_Item_', '').split('_').join(' ');
            selectedGame['league'] = league;
            delete selectedGame['league_id'];
            if (league['leagueid']) {
              league['league_id'] = league['leagueid'];
              delete league['leagueid'] // the naming on this bothered ; all others were seperated by an _ but not this
            }
            break;
          }
        }
        formatPlayers(selectedGame);
      }
    });
  } else {
    formatPlayers(selectedGame);
  }
}

function formatLeagueTier(league_tier) {
  let leagueTier = {0: 'None', 1: 'Amateur', 2: 'Professional', 3: 'Premier'};
  league_tier = leagueTier[league_tier];
  return league_tier;
}

function formatPlayers(selectedGame) {
  
  console.log('formatPlayers')
  // LEAGUE_TIER
  if (selectedGame["league_tier"]) {
    selectedGame['league_tier'] = formatLeagueTier(selectedGame['league_tier']);
  }
  // SERIES
  if (selectedGame['series_type']) {
    selectedGame['series_type'] = formatSeriesType(selectedGame['series_type']);
  }
  // TEAM 
  // since I can't get all the pictures I'll do this for now
  // pictures API seems to be broken in some way
  if (selectedGame['radiant_team']) {
    selectedGame['radiant_team'] = selectedGame['radiant_team']['team_name'];
  }
  if (selectedGame['dire_team']) {
    selectedGame['dire_team'] = selectedGame['dire_team']['team_name'];
  }
  if (selectedGame['scoreboard']) {
    // game has started
    // duration is in milliseconds
    // else in drafting phase and nothing needs to be done
    if (selectedGame['scoreboard']['duration'] > 0) {
      
      // just returns seconds / normally seconds and milliseconds
      selectedGame['scoreboard']['roshan_respawn_timer'] = (selectedGame['scoreboard']['roshan_respawn_timer'] | 0);
      selectedGame['scoreboard']['duration'] = (selectedGame['scoreboard']['duration'] | 0);

      // create a day night cycle for the client side map
      selectedGame['scoreboard']['day_cycle'] = nightDayCycle(selectedGame['scoreboard']['duration']);

      // add player name to scoreboard dictionary
      selectedGame['players'].forEach(player => {
        
        selectedGame['scoreboard']['radiant']['players'].forEach((p, i) => {
          let team = 'radiant'
          if (player['account_id'] === p['account_id']) {
            selectedGame['scoreboard'][team]['players'][i]['position_x'] = (selectedGame['scoreboard'][team]['players'][i]['position_x'] | 0)
            selectedGame['scoreboard'][team]['players'][i]['position_y'] = (selectedGame['scoreboard'][team]['players'][i]['position_y'] | 0)
            selectedGame['scoreboard'][team]['players'][i]['items'] = easyItems(selectedGame['scoreboard'][team]['players'][i])
            selectedGame['scoreboard'][team]['players'][i]['name'] = player['name']
          };       
        });
        selectedGame['scoreboard']['dire']['players'].map((p, i) => {
          team = 'dire';
          if (player['account_id'] === p['account_id']) {
            selectedGame['scoreboard'][team]['players'][i]['position_x'] = (selectedGame['scoreboard'][team]['players'][i]['position_x'] | 0);
            selectedGame['scoreboard'][team]['players'][i]['position_y'] = (selectedGame['scoreboard'][team]['players'][i]['position_y'] | 0);
            selectedGame['scoreboard'][team]['players'][i]['items'] = easyItems(selectedGame['scoreboard'][team]['players'][i]);
            selectedGame['scoreboard'][team]['players'][i]['name'] = player['name'];
          };
        });
      });
    };
  } else {
    console.log('no scoreboard');
  }

  saveGame(selectedGame)

  var end = new Date().getTime();
  console.log('time ', (end - start) / 1000);
  global_db.close();
};

function formatSeriesType(series_type) {
  let seriesType = {0: 'None', 1: 'bo1', 2: 'bo3', 3: 'bo5'};
  series_type = seriesType[series_type];
  return series_type;
};

function nightDayCycle(time) {
  let duration = time | 0; // returns integer
  let minutes = Math.floor(duration / 60);
  let cycle = minutes % 8;
  if (cycle < 4) {
    return 'day';
  }
  else {
    return 'night';
  };
};

function saveGame(selectedGame) {
  console.log('saving game');
  //delete selectedGame['players'];
  //delete selectedGame['lobby_id'];

  selectedGame = sortObj(selectedGame, {sortOrder: 'ASC'});
  selectedGame['_id'] = 1;
  let collection = global_db.collection('currentGame');
  collection.save(selectedGame);

  //saving to firebase
  console.log("\n - updating data to firebase - \n");
  //database.ref('currentGame').set(selectedGame);
  console.log("\n + updated data to firebase + \n");
}

function sortBySpectators(allLiveGames) {
  return allLiveGames.sort((a, b) => {
    if (a.spectators > b.spectators)
      return -1;
    if (a.spectators < b.spectators)
      return 1;
    return 0;
  });
}

function main(currentGame) {
  console.log('running');
  request.get(URLS['GetLiveLeagueGames'], (error, response, body) => {
    if (error) {
      console.log('get live league game failed ', error);
    }
    else {
      let liveLeagueGames = JSON.parse(body)['result']['games'];
      let sortedGamesBySpectators = sortBySpectators(liveLeagueGames);
      if (
        sortedGamesBySpectators[0] !== undefined ||
        sortedGamesBySpectators.length > 0
      ) {
          selectedGame = sortedGamesBySpectators[0];
          //checks for previous league ID
          if (currentGame.hasOwnProperty('league') && selectedGame.hasOwnProperty('league_id')) {
            if (currentGame['league']['league_id'] === selectedGame['league_id']) {
              
              //if same replace with current and don't call leagueGames
              console.log('+ callLeagueListing : False +'); 
              selectedGame['league'] = currentGame['league'];
              delete selectedGame['league_id'];
              selectedgame = formatPlayers(selectedGame)
            }
            else {
              //else call both
              console.log ('+ callLeagueListing 1: True +') 
              callLeagueListing = true
              selectedGame = formatLeague(selectedGame);
              //console.log(selectedGame)
            }
          }
          else {
            //else call both
            console.log ('+ callLeagueListing 2: True +')  
            callLeagueListing = true
            selectedGame = formatLeague(selectedGame);
            //selectedgame = formatPlayers(selectedGame)
          }
      }
      else {
        console.log('something is wrong #most likely empty#');
        console.log(sortedGamesBySpectators);
      };
    };
  });
}


var ITEMS;


let config = {
  //(TODO) change 'serviceAccount' on linux box
  serviceAccount: "E:/Projects/firebase-server/dota2-project-d42951d006e1.json",
  databaseURL: "https://dota2-project-c0fd5.firebaseio.com"
};
firebase.initializeApp(config);

//var database = firebase.database();


callLeagueListing = false;
var global_db;
var start = new Date().getTime();
MongoClient.connect("mongodb://localhost:27017/dota", (err, db) => {
  if(!err) {
    global_db = db
    let dbCurrentGame = global_db.collection('currentGame');
    dbCurrentGame.findOne({"_id": 1}, (err, result) => {
      if (err) {
        console.log('currentGame findOne err ', err);
      } else {
        main(result)
      }
    
    });
  }

});
