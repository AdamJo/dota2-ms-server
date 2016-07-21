const mongo = require('mongodb');
const request = require('request');
var Rx = require('rx');

var async = {
    waterfall: series => {
        return Rx.Observable.defer(() => {
            var acc = series[0]();
            for (var i = 1, len = series.length; i < len; i++) {

                // Pass in func to deal with closure capture
                (function (func) {

                    // Call flatMapLatest on each function
                    acc = acc.flatMapLatest(x => func(x));
                }(series[i]));
            }

            return acc; 
        });
    }
}

var fs = require('fs'),
    path = require('path');

var file = path.join(__dirname, 'resources/currentGame.txt'),
    dest = path.join(__dirname, 'resources/extra.txt'),
    exists = Rx.Observable.fromCallback(fs.exists),
    rename = Rx.Observable.fromNodeCallback(fs.rename),
    stat = Rx.Observable.fromNodeCallback(fs.stat);

var obs = async.waterfall([
    () => exists(file),
    (flag) => {
        // Rename or throw computation
        return flag ?
            rename(file, dest) :
            Rx.Observable.throw(new Error('File does not exist.'));
    },
    () => stat(dest)
]);

obs.subscribe(
    fsStat => console.log(JSON.stringify(fsStat)),
    console.log.bind(console)
);

URLS = {
  'GetLeagueListing' : `http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1/?key=D83C21F5B8088C1AE92AC05A72F36558`,
  'GetLiveLeagueGames' : `https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key=D83C21F5B8088C1AE92AC05A72F36558`
}
