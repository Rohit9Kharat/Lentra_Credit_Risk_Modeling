const { createReadStream, createWriteStream } = require('fs');

const { AsyncParser, 
	transforms: { unwind, flatten }, stringExcelFormatter} = require('json2csv');

//const { formatters: { string: stringExcelFormatter() } } = require('json2csv');

const fields = [
{"label":"ID", "value":"_id"},
{"label":"paymentHist1","value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistory1"},
{"label":"paymentHist2","value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistory2"},
{"label":"empType", "value":"applicationRequest.request.applicant.employment[0].employmentType"},
{"label":"education", "value":"applicationRequest.request.applicant.education"},
{"label":"age", "value":"applicationRequest.request.applicant.age"},
{"label":"gender", "value":"applicationRequest.request.applicant.gender"},
{"label":"addrsCategory", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].addressCategory"},
{"label":"pinCode", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].pinCode"},
{"label":"addrsStateCode", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].stateCode"},
{"label":"phoneType", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.phoneList[0].telephoneType"},
{"label":"maritalStatus", "value":"applicationRequest.request.applicant.maritalStatus"},
{"label":"netMonthlyIncome", "value":"applicationRequest.request.applicant.incomeDetails.netMonthlyAmt"},
{"label": "sanctionAmount", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.highCreditOrSanctionedAmount"},
{"label":"loanType", "value":"applicationRequest.request.application.loanType"},
{"label":"loanAmt", "value":"applicationRequest.request.application.loanAmount"},
{"label":"loanTenure", "value":"applicationRequest.request.application.loanTenor"},
{"label":"bureauName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.bureau"},
{"label":"bureauScore", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList[0].score"},
{"label":"bureauScoreCardName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList[0].scoreCardName"},
{"label":"bureauScoreName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList[0].scoreName"}
]

// {"label":"Target", "value":"applicationStatus"},
// {"label": "sanctionAmount", "value": "applicantComponentResponse.scoringServiceResponse.eligibilityResponse.values.HIGH_SANC_AMT"}

//const opts = { fields };
//const transformOpts = { highWaterMark: 8192 };
// const transforms = [flatten({ objects: false, arrays: true })];

const transforms = [unwind({ paths: ['applicantComponentResponse.multiBureauJsonRespose.finishedList',
	'applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList'] })];

// Using the promise API
const input = createReadStream('goNoGoCustomerApplication28july.json', { encoding: 'utf8' });

const asyncParser = new AsyncParser({fields, transforms});

const output = createWriteStream('cibil_test2.csv', { stringExcel: stringExcelFormatter }, { encoding: 'utf8' });

const parsingProcessor = asyncParser.fromInput(input).toOutput(output);
 
parsingProcessor.promise()
  .then(csv => console.log(csv))
  .catch(err => console.error(err));
 
// Using the promise API just to know when the process finnish
// but not actually load the CSV in memory
//const input = createReadStream(gonogo_28july.json, { encoding: 'utf8' });
//const asyncParser = new JSON2CSVAsyncParser(opts, transformOpts);
//parsingProcessor.promise(false).catch(err => console.error(err));

