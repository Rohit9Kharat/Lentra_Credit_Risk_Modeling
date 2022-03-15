const { createReadStream, createWriteStream } = require('fs');

const { AsyncParser, 
	transforms: { unwind, flatten }, stringExcelFormatter} = require('json2csv');

//const { formatters: { string: stringExcelFormatter() } } = require('json2csv');

const fields = [
{"label":"ID", "value":"_id"},
{"label":"age", "value":"applicationRequest.request.applicant.age"},
{"label":"gender", "value":"applicationRequest.request.applicant.gender"},
{"label":"empType", "value":"applicationRequest.request.applicant.employment[0].employmentType"},
{"label":"education", "value":"applicationRequest.request.applicant.education"},
{"label":"addrsCategory", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].addressCategory"},
{"label":"pinCode", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].pinCode"},
{"label":"addrsStateCode", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.addressList[0].stateCode"},
{"label":"phoneType", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.phoneList[0].telephoneType"},
{"label":"accountType", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.accountType"},
{"label":"maritalStatus", "value":"applicationRequest.request.applicant.maritalStatus"},
{"label":"bureauName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.bureau"},
{"label":"bureauScore", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList.score"},
{"label":"bureauScoreCardName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList.scoreCardName"},
{"label":"bureauScoreName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList.scoreName"},
{"label":"writtenOffAndSettledStatus", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.writtenOffAndSettledStatus"},
{"label":"writtenOffAmountPrincipal", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.writtenOffAmountPrincipal"},
{"label":"netMonthlyIncome", "value":"applicationRequest.request.applicant.incomeDetails.netMonthlyAmt"},
{"label":"sanctionAmount", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.highCreditOrSanctionedAmount"},
{"label":"currentBalance", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.currentBalance"},
{"label":"creditLimit", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.creditLimit"},
{"label":"loanAmt", "value":"applicationRequest.request.application.loanAmount"},
{"label":"overdueAmount", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.overdueAmount"},
{"label":"loanTenure", "value":"applicationRequest.request.application.loanTenor"},
{"label":"loginDate", "value":"intrimStatus.startTime.$date"},
{"label":"dateReportedAndCertified", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.dateReportedAndCertified"},
{"label":"dateOpenedOrDisbursed", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.dateOpenedOrDisbursed"},
{"label":"dateClosed", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.dateClosed"},
{"label":"PHSD", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistoryStartDate"},
{"label":"PHED", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistoryEndDate"},
{"label":"suitFiledOrWilfulDefault", "value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.suitFiledOrWilfulDefault"},
{"label":"paymentHist1","value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistory1"},
{"label":"paymentHist2","value": "applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.paymentHistory2"}
]

// {"label":"Target", "value":"applicationStatus"},
// {"label": "sanctionAmount", "value": "applicantComponentResponse.scoringServiceResponse.eligibilityResponse.values.HIGH_SANC_AMT"}

//const opts = { fields };
//const transformOpts = { highWaterMark: 8192 };paymentHistoryStartDate
// const transforms = [flatten({ objects: false, arrays: true })];

const transforms = [unwind({ paths: ['applicantComponentResponse.multiBureauJsonRespose.finishedList',
	'applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList',
	'applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.scoreList'] })];

// Using the promise API
const input = createReadStream('goNoGoCustomerApplication28july.json', { encoding: 'utf8' });

const asyncParser = new AsyncParser({fields, transforms});

const output = createWriteStream('cibil_test.csv', { stringExcel: stringExcelFormatter }, { encoding: 'utf8' });

const parsingProcessor = asyncParser.fromInput(input).toOutput(output);
 
parsingProcessor.promise()
  .then(csv => console.log(csv))
  .catch(err => console.error(err));
 
// Using the promise API just to know when the process finnish
// but not actually load the CSV in memory
//const input = createReadStream(gonogo_28july.json, { encoding: 'utf8' });
//const asyncParser = new JSON2CSVAsyncParser(opts, transformOpts);
//parsingProcessor.promise(false).catch(err => console.error(err));

