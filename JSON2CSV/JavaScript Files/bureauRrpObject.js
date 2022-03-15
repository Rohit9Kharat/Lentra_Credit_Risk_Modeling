const { Parser, transforms: { unwind }} = require('json2csv');

var fs = require('fs');


function loadJSON(filename = ''){
	if (fs.existsSync(filename)){
		return fs.readFileSync(filename).toString()
	} else {
		return ''
	}
}

var data = loadJSON('goNoGo.json')
console.log(data);

// var data = JSON.parse(fs.readFileSync('goNoGoCustomerApplication28july.json').toString());
// console.log(data);

// const data = require('goNoGoCustomerApplication28july.json');
// console.log(data);


const fields =['_id'];

const json2csvParser = new Parser({ fields });

const csv = json2csvParser.parse(data);


fs.writeFileSync("./bureau_rrp.csv", csv);
