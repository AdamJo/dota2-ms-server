const firebase = require('firebase');
const MongoClient = require('mongodb').MongoClient;
const child_process = require('child_process');
const CronJob = require('cron').CronJob;


var config = {
  serviceAccount: "/home/boomsy/projects/firebase-server-update/dota2-project.json",
  databaseURL: "https://dota2-project-c0fd5.firebaseio.com"
};
firebase.initializeApp(config);

var database = firebase.database();

function runPython() {
  console.log('- running python... -')
  child_process.execSync('python3 /home/boomsy/projects/firebase-server-update/dotaApi.py', {timeout: 10000, stdio:[0,1,2]})
  console.log('+ Python completed! +')
}

function updateDatabase() {

  MongoClient.connect("mongodb://127.0.0.1:27017/dota", (err, db) => {
    if(!err) {

        //runs python to update mongodb database with new data
        runPython()

        let collection = db.collection('currentGame')

        collection.findOne({'_id': 1}, (err, doc) => {
          console.log("+ updating data to firebase +")

	  //not needed for web client
          delete doc._id;
          delete doc.league.league_id;

          //database.ref('currentGame').set(doc);
          console.log("- updated data to firebase -")

   	  db.close();
        });
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
new CronJob('*/16 * * * * *', () => {
	updateDatabase()
}, null, true, null, null, true);
