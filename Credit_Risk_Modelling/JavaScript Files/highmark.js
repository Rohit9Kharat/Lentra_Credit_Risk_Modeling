const { createReadStream, createWriteStream } = require('fs');
const { AsyncParser, transforms: { unwind, flatten } } = require('json2csv');


const fields = [
{"label":"ID", "value":"_id"},
{"label":"Target", "value":"applicationStatus"},
{"label":"empType", "value":"applicationRequest.request.applicant.employment[0].employmentType"},
{"label":"education", "value":"applicationRequest.request.applicant.education"},
{"label":"age", "value":"applicationRequest.request.applicant.age"},
{"label":"gender", "value":"applicationRequest.request.applicant.gender"},
{"label":"addrsCategory", "value":"applicationRequest.request.applicant.address[0].addressType"},
{"label":"pinCode", "value":"applicationRequest.request.applicant.address[0].pin.$numberLong"},
{"label":"addrsStateCode", "value":"applicationRequest.request.applicant.address[0].state"},
{"label":"phoneType", "value":"applicationRequest.request.applicant.phone[0].phoneType"},
{"label":"maritalStatus", "value":"applicationRequest.request.applicant.maritalStatus"},
{"label":"netMonthlyIncome", "value":"applicationRequest.request.applicant.incomeDetails.netMonthlyAmt"},
{"label":"loanType", "value":"applicationRequest.request.application.loanType"},
{"label":"loanAmt", "value":"applicationRequest.request.application.loanAmount"},
{"label":"loanTenure", "value":"applicationRequest.request.application.loanTenor"},
{"label":"bureauName", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.bureau"},
{"label":"bureauScore", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.scores.scoreList[0].scoreValue"},
{"label":"disbursedDate", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.disbursedDate"},
{"label":"creditLimit", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.creditLimit"},
{"label":"currentBalance", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.currentBalance"},
{"label":"accountType", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.accountType"},
{"label":"repaymentTenure", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.repaymentTenure"},
{"label":"disbursedAmount", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.disbursedAmount"},
{"label":"writeOffAmount", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.writeOffAmount"},
{"label":"overdueAmount", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList.overdueAmount"},
{"label":"lengthOfCreditHistoryYear", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountSummary.lengthOfCreditHistoryYear"},
{"label":"lengthOfCreditHistoryMonth", "value":"applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountSummary.lengthOfCreditHistoryMonth"}
]

//const opts = { fields };

//const transformOpts = { highWaterMark: 8192 };

// const transforms = [flatten({ objects: false, arrays: true })];
const transforms = [unwind({ paths: ['applicantComponentResponse.multiBureauJsonRespose.finishedList','applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.baseReports.baseReport.accountList'] })];

// Using the promise API
const input = createReadStream('goNoGoCustomerApplication28july.json', { encoding: 'utf8' });

const asyncParser = new AsyncParser({fields, transforms});

const output = createWriteStream('highmark_test.csv', { encoding: 'utf8' });

const parsingProcessor = asyncParser.fromInput(input).toOutput(output);
 
parsingProcessor.promise()
  .then(csv => console.log(csv))
  .catch(err => console.error(err));
 
// Using the promise API just to know when the process finnish
// but not actually load the CSV in memory
//const input = createReadStream(gonogo_28july.json, { encoding: 'utf8' });

//const asyncParser = new JSON2CSVAsyncParser(opts, transformOpts);

 
//parsingProcessor.promise(false).catch(err => console.error(err));

