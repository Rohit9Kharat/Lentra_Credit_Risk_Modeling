const { Parser, transforms: { unwind }} = require('json2csv');

const fs = require('fs');

// var content = fs.readFileSync('goNoGoCustomerApplication28july.json');
fs.readFile('./goNoGo.json', 'utf-8', (err, jsonString) => {
	if (err) {
		console.log(err);
	} else {
		try{
			const data = JSON.parse(jsonString);
			console.log(data.actionList);
		} catch (err) {
			console.log('Erorr parsing JSON', err);
		}
	}
});
