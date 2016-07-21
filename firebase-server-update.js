const firebase = require('firebase');
const MongoClient = require('mongodb').MongoClient;
const child_process = require('child_process');
const schedule = require('node-schedule');

function runPython() {
  console.log('\n - runing python... - \n')
  child_process.execSync('python3 dotaApi.py', {timeout: 10000})
  console.log('\n + Python completed! + \n')
}


var config = {
  serviceAccount: "./dota2-project-d42951d006e1.json",
  databaseURL: "https://dota2-project-c0fd5.firebaseio.com"
};
firebase.initializeApp(config);

var database = firebase.database();

//schedule.scheduleJob('* /16 * * * * *', () => {
  MongoClient.connect("mongodb://127.0.0.1:27017/dota", (err, db) => {
    if(!err) {

        //runs python to update mongodb database with new data
        runPython()

        let collection = db.collection('currentGame')

        collection.findOne({'_id': 1}, (err, doc) => {
          console.log("\n - updating data to firebase - \n")

          delete doc._id;
          delete doc.lobby_id;
          delete doc.league.itemdef;
          delete doc.league.league_id;

          database.ref('currentGame').set(doc);
          console.log("\n + updated data to firebase + \n")

   	  db.close();
        });
    } else {
	console.log('error with mongo');
	console.log(err);
    }

  });
//});
