const fs = require('fs')

var importStream = fs.createReadStream('goNoGo.json', {flags: 'r', encoding: 'utf-8'});
importStream.on('data', function(chunk) {

    var pleaseBeAJSObject = JSON.parse(chunk);           
    // insert pleaseBeAJSObject in a database
});
importStream.on('end', function(item) {
   console.log("Woot, imported objects into the database!");
});