const { createReadStream, createWriteStream } = require('fs');
const { AsyncParser, transforms: { unwind } } = require('json2csv');
 
const fields = [
{"label":"ID", "value":"_id"},
{"label":"addressType_0", "value":"applicationRequest.request.applicant.address[0].addressType"},
{"label":"AddLine1_0","value":"applicationRequest.request.applicant.address[0].addressLine1"},
{"label":"AddLine2_0","value":"applicationRequest.request.applicant.address[0].addressLine2"},
{"label":"City_0","value":"applicationRequest.request.applicant.address[0].city"},
{"label":"Pin_0","value":"applicationRequest.request.applicant.address[0].pin.$numberLong"},
{"label":"State_0","value":"applicationRequest.request.applicant.address[0].state"},
{"label":"LandMark_0","value":"applicationRequest.request.applicant.address[0].landMark"},
{"label":"addressType_1", "value":"applicationRequest.request.applicant.address[1].addressType"},
{"label":"AddLine1_1","value":"applicationRequest.request.applicant.address[1].addressLine1"},
{"label":"AddLine2_1","value":"applicationRequest.request.applicant.address[1].addressLine2"},
{"label":"City_1","value":"applicationRequest.request.applicant.address[1].city"},
{"label":"Pin_1","value":"applicationRequest.request.applicant.address[1].pin.$numberLong"},
{"label":"State_1","value":"applicationRequest.request.applicant.address[1].state"},
{"label":"LandMark_1","value":"applicationRequest.request.applicant.address[1].landMark"},
{"label":"addressType_2", "value":"applicationRequest.request.applicant.address[2].addressType"},
{"label":"AddLine1_2","value":"applicationRequest.request.applicant.address[2].addressLine1"},
{"label":"AddLine2_2","value":"applicationRequest.request.applicant.address[2].addressLine2"},
{"label":"City_2","value":"applicationRequest.request.applicant.address[2].city"},
{"label":"Pin_2","value":"applicationRequest.request.applicant.address[2].pin.$numberLong"},
{"label":"State_2","value":"applicationRequest.request.applicant.address[2].state"},
{"label":"LandMark_2","value":"applicationRequest.request.applicant.address[2].landMark"}
]

const opts = { fields };
const transformOpts = { highWaterMark: 8192 };
//const transformOpts = [unwind({ paths: ['applicationRequest.request.applicant.address'] })]; 

// Using the promise API
const input = createReadStream('goNoGoCustomerApplication28july.json', { encoding: 'utf8' });
const asyncParser = new AsyncParser(opts, transformOpts);
//const parsingProcessor = asyncParser.fromInput(input);

const output = createWriteStream('GONOGO_28JULY_Address_FINAL.csv', { encoding: 'utf8' });

const parsingProcessor = asyncParser.fromInput(input).toOutput(output);
 
parsingProcessor.promise()
  .then(csv => console.log(csv))
  .catch(err => console.error(err));
 
// Using the promise API just to know when the process finnish
// but not actually load the CSV in memory
//const input = createReadStream(gonogo_28july.json, { encoding: 'utf8' });

//const asyncParser = new JSON2CSVAsyncParser(opts, transformOpts);

 
//parsingProcessor.promise(false).catch(err => console.error(err));