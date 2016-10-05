const firebase = require('firebase');
const MongoClient = require('mongodb').MongoClient;
const child_process = require('child_process');
const CronJob = require('cron').CronJob;
const request = require('request');

function runPython() {
  console.log('- running python... -');
  child_process.execSync('python3 '+ process.env.SERVER +'/dotaApi.py', {timeout: 10000, stdio:[0,1,2]});
  console.log('+ Python completed! +');
  return 'update Run Python Done'
}

function getUpcomingGames() {
  console.log('- running getUpcomingGames... -');
  request('http://dailydota2.com/match-api', (error, response, body) => {

    if (!error && response.statusCode == 200) {
      games = JSON.parse(body)
      upcomingGames = games['matches'].map(game => {
        if ('team1'in game) {
          if ('team_name' in game['team1']) {
            game['team1_name'] = game['team1']['team_name']
          } else {
            game['team1_name'] = ''
          }
          if ('team_tag' in game['team1']) {
            game['team1_tag'] = game['team1']['team_tag']
          }
          else {
            game['team1_tag'] = ''
          }
          delete game['team1'];
        }

        if ('team2'in game) {
          if ('team_name' in game['team2']) {
            game['team2_name'] = game['team2']['team_name']
          } else {
            game['team2_name'] = ''
          }
          if ('team_tag' in game['team2']) {const request = require('request');
            game['team2_tag'] = game['team2']['team_tag']
          }
          else {
            game['team2_tag'] = ''
          }
          delete game['team2'];
        }

        if ('league'in game) {
          game['league'] = game['league']['name']
        } else {
          game['league'] = ''
        }

        delete game['status']
        delete game['starttime_unix']
        delete game['comment']
        delete game['viewers']

        return game
      })
      DATABASE.ref('upcomingGames').set(upcomingGames);
      console.log('+ running getUpcomingGames... +');
    }
  });
}

function updateMatchHistory(db) {
  console.log("- get Match History +")
  oldGames = []

  let matchHistory = db.collection('matchHistory').find().sort({_id:-1});
  matchHistory.each((err, doc) => {
    if (doc != null) {
      if (doc['league_tier'] > 1) {
        delete doc._id;
        delete doc.league_tier;
        delete doc.dire_score;
        delete doc.duration;
        delete doc.negative_votes;
        delete doc.positive_votes;
        delete doc.radiant_score;
        delete doc.start_time;
        oldGames.push(doc);
      }
    }
    else {
      if (oldGames.length > 0) {
        DATABASE.ref('matchHistory').set(oldGames);
      }
    } 
  })
  console.log("+ get Match History +");
}

function updateTopGames(db) {
  console.log("- get top games -");
  allGames = []

  runPython()
  let topGamesCursor = db.collection('topGames').find();
  topGamesCursor.each((err, doc) => {

  if (doc != null) {
      delete doc._id;
      delete doc.dire_series_wins;
      delete doc.game_number;
      delete doc.league_game_id;
      delete doc.league_id;
      delete doc.league_tier;
      delete doc.radiant_series_wins;
      delete doc.stage_name;
      delete doc.series_type;

      allGames.push(doc)
    } else {
      allGames.sort((a, b) => {
        if (a.spectators > b.spectators)
          return -1;
        if (a.spectators < b.spectators)
          return 1;
        return 0;
      })
      DATABASE.ref('sortedGames').set(allGames);
    }
  })
  console.log("+ get Top Games +");
}

function mmrTop(db) {
  let topGame = []

  console.log("- top mmr game -");
  let mmrTop = db.collection('mmrTop').find();

  mmrTop.each((err, doc) => {
    console.log(doc)
    if (doc != null) {
      for (let i = 0; i < doc['games'].length; i++) {
        delete doc['games'][i]._id;
        delete doc['games'][i].league_id;
        delete doc['games'][i].game_mode;
        delete doc['games'][i].lobby_type;
        delete doc['games'][i].building_state;
        delete doc['games'][i].activate_time;
        delete doc['games'][i].deactivate_time;
        delete doc['games'][i].last_update_time;
        delete doc['games'][i].radiant_lead;
        delete doc['games'][i].sort_score;
        topGame.push(doc['games'][i])
      }
    } else {
      console.log(topGame)
      DATABASE.ref('mmrTop').set(topGame);
    }
  })
  console.log("+ top mmr game +")
}

var config = {
  serviceAccount: process.env.FIREBASE_LOCAL,
  databaseURL: process.env.FIREBASE_DATABASE_URL
};
firebase.initializeApp(config);

var DATABASE = firebase.database();

getUpcomingGamesJob = new CronJob({
  cronTime: '0 */10 * * * *',
  onTick: () => {
	  getUpcomingGames()
  },
  start: true,
  runOnInit: true
});

updateDatabaseJob = new CronJob({
  cronTime: '*/15 * * * * *',
  onTick: () => {
    MongoClient.connect("mongodb://127.0.0.1:27017/dota", (err, db) => {
      if (!err) {
        updateTopGames(db)
        updateMatchHistory(db)
        mmrTop(db)
        db.close();
      } else {
          console.log('error with mongo');
          console.log(err);
        }
      });
  },
  start: true,
  runOnInit: true
});
