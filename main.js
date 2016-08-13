const firebase = require('firebase');
const MongoClient = require('mongodb').MongoClient;
const child_process = require('child_process');
const CronJob = require('cron').CronJob;

var config = {
  serviceAccount: process.env.FIREBASE_LOCAL,
  databaseURL: process.env.FIREBASE_DATABASE_URL
};
firebase.initializeApp(config);

var database = firebase.database();

function runPython() {
  console.log('- running python... -');
  child_process.execSync('python3 '+ process.env.SERVER +'/dotaApi.py', {timeout: 10000, stdio:[0,1,2]});
  console.log('+ Python completed! +');
}

function updateDatabase() {
  allGames = []
  MongoClient.connect("mongodb://127.0.0.1:27017/dota", (err, db) => {
    if(!err) {

      //runs python to update mongodb database with new data
      runPython();

      games = {}
      var cursor = db.collection('topGames').find();
      cursor.each((err, doc) => {
          if (doc != null) {
            delete doc._id;
            // matchId = doc['match_id']
            // games[matchId] = doc
            allGames.push(doc)
          } else {
            database.ref('topGames').set(allGames);
            let collection = db.collection('currentGame');
            collection.findOne({'_id': 1}, (err, doc) => {
              console.log("+ updating data to firebase +");

              //not needed for web client
              delete doc._id;
              // delete doc.league.league_id;

              database.ref('currentGame').set(doc);
              console.log("- updated data to firebase -");

              db.close();
            });
          }
        })
    } else {
      console.log('error with mongo');
      console.log(err);
    }
  });
}

// run evey 16 seconds, api updates every 15 seconds
// null : run on complete
// true : start the cronjob object
// null : time zone
// null : context e.g. this.stop()
// true : immediately fire the job on startup
new CronJob('*/5 * * * * *', () => {
	updateDatabase()
}, null, true, null, null, true);
