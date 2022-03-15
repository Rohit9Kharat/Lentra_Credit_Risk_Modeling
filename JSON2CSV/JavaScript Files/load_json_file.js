const { Parser, transforms: { unwind }} = require('json2csv');

const fs = require('fs');

function loadJSON(filename = ''){
	return JSON.parse(
		fs.existsSync(filename)
			? fs.readFileSync(filename).toString()
			: '""'
	)
}

function saveJSON(filename = '', json = '""'){
	return fs.writeFileSync(filename, JSON.stringify(json))
}


var content = loadJSON('fieldsConfig.json')