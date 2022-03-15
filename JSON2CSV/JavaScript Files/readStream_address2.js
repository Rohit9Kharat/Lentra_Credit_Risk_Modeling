const { createReadStream, createWriteStream } = require('fs');
const { AsyncParser, transforms: { unwind } } = require('json2csv');


const fields = [
{"label":"ID", "value":"_id"},
{"label":"addressType", "value":"applicationRequest.request.applicant.address.addressType"},
{"label":"AddLine1","value":"applicationRequest.request.applicant.address.addressLine1"},
{"label":"AddLine2","value":"applicationRequest.request.applicant.address.addressLine2"},
{"label":"City","value":"applicationRequest.request.applicant.address.city"},
{"label":"Pin","value":"applicationRequest.request.applicant.address.pin.$numberLong"},
{"label":"State","value":"applicationRequest.request.applicant.address.state"},
{"label":"LandMark","value":"applicationRequest.request.applicant.address.landMark"}
];

//const opts = { fields };

//const transformOpts = { highWaterMark: 8192 };

const transforms = [unwind({ paths: ['applicationRequest.request.applicant.address'] })];

// Using the promise API
const input = createReadStream('goNoGoCustomerApplication28july.json', { encoding: 'utf8' });

const asyncParser = new AsyncParser({fields, transforms});

const output = createWriteStream('GONOGO_28JULY_Address_FINAL_2.csv', { encoding: 'utf8' });

const parsingProcessor = asyncParser.fromInput(input).toOutput(output);
 
parsingProcessor.promise()
  .then(csv => console.log(csv))
  .catch(err => console.error(err));
 
// Using the promise API just to know when the process finnish
// but not actually load the CSV in memory
//const input = createReadStream(gonogo_28july.json, { encoding: 'utf8' });

//const asyncParser = new JSON2CSVAsyncParser(opts, transformOpts);

 
//parsingProcessor.promise(false).catch(err => console.error(err));