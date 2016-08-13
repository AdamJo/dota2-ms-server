const MongoClient = require('mongodb').MongoClient;

function near() {
  console.log('here')
}

MongoClient.connect("mongodb://127.0.0.1:27017/dota", (err, db) => {
    if(!err) {

      let collection = db.collection('currentGame');
      let allGames = db.collection('topGames');

      var cursor = db.collection('topGames').find();
      allGames = [];

      
      cursor.each((err, doc) => {
          if (doc != null) {
            key = doc['match_id']
            obj = {}
            obj[key] = doc
            console.log(obj)
            // allGames.push( { match_id : doc})
            // console.log(match_id)
          } else {
            console.log(allGames);
          }
        })
      

    } else {
      console.log('error with mongo');
      console.log(err);
    }
});