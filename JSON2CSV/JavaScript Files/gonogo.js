const { Parser, transforms: { unwind } } = require('json2csv');

const FileSystem = require('fs');
 
const gonogo = [
  
{
  "_id" : "566840116961",
  "actionList" : [ ],
  "intrimStatus" : {
    "startTime" : "2019-04-25T10:06:00.439Z",
    "appStart" : "DEFAULT",
    "dedupe" : "DEFAULT1",
    "posidexDedupeStatus" : "DEFAULT",
    "emailStatus" : "DEFAULT",
    "otpStatus" : "COMPLETE",
    "appsStatus" : "COMPLETE",
    "panStatus" : "COMPLETE",
    "aadharStatus" : "UNAUTHORISED",
    "hunterStatus" : "DEFAULT",
    "mbStatus" : "COMPLETE",
    "creditVidyaStatus" : "DEFAULT",
    "saathiPullStatus" : "DEFAULT",
    "varScoreStatus" : "COMPLETE",
    "scoreStatus" : "COMPLETE",
    "cibilScore" : "DEFAULT",
    "experianStatus" : "COMPLETE",
    "highmarkStatus" : "COMPLETE",
    "croStatus" : "COMPLETE",
    "awsS3Status" : "DEFAULT",
    "ntcStatus" : "COMPLETE",
    "panModuleResult" : {
      "fieldName" : "PAN Verification",
      "order" : 4,
      "fieldValue" : "NO_RESPONSE",
      "message" : "NO_RESPONSE",
      "status" : "FAILED",
      "addStability" : 0
    },
    "cibilModuleResult" : {
      "fieldName" : "CIBIL Score",
      "order" : 3,
      "fieldValue" : "NO RESPONSE",
      "message" : "No Score",
      "addStability" : 0
    },
    "scoringModuleResult" : {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "20",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    },
    "aadharModuleResult" : {
      "fieldName" : "AADHAR Verification",
      "order" : 7,
      "fieldValue" : "NOT_AUTHORIZED",
      "message" : "NOT_AUTHORIZED",
      "addStability" : 0
    },
    "experianModuleResult" : {
      "fieldName" : "Experian Score",
      "order" : 6,
      "fieldValue" : "-",
      "message" : "BUREAU-ERROR",
      "addStability" : 0
    },
    "chmModuleResult" : {
      "fieldName" : "Highmark Score",
      "order" : 12,
      "fieldValue" : "-",
      "message" : "SUCCESS",
      "addStability" : 0
    },
    "mbModuleResult" : {
      "fieldName" : "MB",
      "order" : 0,
      "status" : "SUCCESS",
      "addStability" : 0
    },
    "additionalProperties" : {
      
    },
    "karzaPanStatus" : "DEFAULT",
    "karzaVoterIdStatus" : "DEFAULT",
    "karzaDlStatus" : "DEFAULT"
  },
  "parentID" : "56684000127",
  "rootID" : "56684000115",
  "productSequenceNumber" : 3,
  "dateTime" : "2019-04-26T11:41:00.846Z",
  "applicationStatus" : "Approved",
  "statusFlag" : true,
  "reInitiateCount" : 0,
  "reappraiseReq" : false,
  "reProcessCount" : 0,
  "applicationRequest" : {
    "_id" : "56684000136",
    "header" : {
      "applicationId" : "",
      "institutionId" : "4019",
      "sourceId" : "GONOGO_HDBFS",
      "applicationSource" : "WEB 4.02.01",
      "requestType" : "application/json",
      "dateTime" : "2019-04-26T11:41:00.846Z",
      "dsaId" : "HDBFS_DSA1@softcell.com",
      "croId" : "STP",
      "dealerId" : "56684",
      "product" : "LSL",
      "userName" : "CHDBSDSA1",
      "userRole" : "",
      "applicationDate" : "2019-04-25T10:44:10.158Z"
    },
    "request" : {
      "applicant" : {
        "applicantId" : "APPLICANT_1",
        "applicantName" : {
          "firstName" : "MUKESH",
          "middleName" : "",
          "lastName" : "AMBANI"
        },
        "fatherName" : {
          "firstName" : "KJSDFNKJDS"
        },
        "isStaff" : false,
        "isStaffRelated" : false,
        "motherName" : {
          "firstName" : "SKJDFHDSJK"
        },
        "gender" : "Male",
        "dateOfBirth" : "27032001",
        "age" : 18,
        "maritalStatus" : "Single",
        "kyc" : [
          {
            "kycName" : "APPLICANT-PHOTO",
            "kycNumber" : "",
            "documentVerified" : false
          },
          {
            "kycName" : "DRIVING-LICENSE",
            "kycNumber" : "KXJDJHJUDSHSFJ",
            "documentVerified" : false
          },
          {
            "kycName" : "PAN",
            "kycNumber" : "CHMPK6466D",
            "documentVerified" : false
          },
          {
            "kycName" : "INCOME-PROOF1",
            "kycNumber" : "MXHBDCVJHS",
            "documentVerified" : false
          },
          {
            "kycName" : "INCOME-PROOF2",
            "kycNumber" : "JSDFJJHHJ",
            "documentVerified" : false
          },
          {
            "kycName" : "BANK-PASSBOOK",
            "kycNumber" : "",
            "documentVerified" : false
          }
        ],
        "isResidenceAddSameAsAbove" : true,
        "address" : [
          {
            "timeAtAddress" : 0,
            "addressType" : "RESIDENCE",
            "residenceAddressType" : "OWNED-BUNGLOW",
            "monthAtCity" : 26,
            "monthAtAddress" : 13,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeArea" : "",
            "negativeAreaReason" : "",
            "negativeAreaNotApplicableFlag" : true,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "JHDSGJFDSHV",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "distanceFrom" : 0,
            "landMark" : "EJHGDSBDSJ",
            "outOfGeoLimit" : "YES"
          },
          {
            "timeAtAddress" : 0,
            "addressType" : "OFFICE",
            "residenceAddressType" : "",
            "monthAtCity" : 0,
            "monthAtAddress" : 0,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeAreaNotApplicableFlag" : false,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "DZHBJDGHDS",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "line3" : "",
            "distanceFrom" : 0,
            "landMark" : "SDGFHSDJFHJS"
          },
          {
            "timeAtAddress" : 0,
            "addressType" : "PERMANENT",
            "residenceAddressType" : "OWNED-BUNGLOW",
            "monthAtCity" : 26,
            "monthAtAddress" : 13,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeAreaNotApplicableFlag" : false,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "JHDSGJFDSHV",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "distanceFrom" : 0,
            "landMark" : "EJHGDSBDSJ"
          }
        ],
        "phone" : [
          {
            "phoneType" : "PERSONAL_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "3487534875",
            "extension" : ""
          },
          {
            "phoneType" : "PERSONAL_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "RESIDENCE_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "3487534875",
            "extension" : ""
          },
          {
            "phoneType" : "RESIDENCE_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "OFFICE_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "OFFICE_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "9384598345",
            "extension" : ""
          }
        ],
        "email" : [
          {
            "emailType" : "PERSONAL",
            "emailAddress" : "hsgdhg@jd.dj",
            "verified" : false
          },
          {
            "emailType" : "PERMANENT",
            "emailAddress" : "hsgdhg@jd.dj",
            "verified" : false
          },
          {
            "emailType" : "WORK",
            "emailAddress" : "skdjk@js.sj",
            "verified" : false
          }
        ],
        "employment" : [
          {
            "employmentType" : "SELF-EMPLOYED",
            "employmentName" : "Softcell Technologies Limited",
            "timeWithEmployer" : 26,
            "monthlySalary" : 20000,
            "grossSalary" : 0,
            "lastMonthIncome" : [ ],
            "constitution" : "SELF-EMPLOYED",
            "itrAmount" : 0,
            "totalExps" : 0,
            "otherGrossIncome" : 0,
            "employerCatg" : "CATC",
            "retirementAge" : 0,
            "annualIncome" : 0,
            "netMonthlyIncome" : 0
          }
        ],
        "noOfDependents" : 0,
        "noOfEarningMembers" : 0,
        "noOfFamilyMembers" : 0,
        "applicantReferences" : [ ],
        "education" : "GRADUATE",
        "mobileVerified" : false,
        "addharVerified" : false,
        "emailVerified" : false,
        "emailVerificationSkip" : true,
        "emailOtpStatus" : false,
        "isAadhaarDetailsSameAsExisting" : false,
        "bankingDetails" : [
          {
            "accountHolderName" : {
              "firstName" : "kjsdfhdsjfgjs",
              "middleName" : "",
              "lastName" : ""
            },
            "bankName" : "STATE BANK OF HYDERABAD",
            "branchName" : "PUNE NIGADI PIMPRI CHINCHWAD",
            "accountType" : "SAVINGS",
            "accountNumber" : "7485435776373",
            "ifscCode" : "SBHY0020765",
            "salaryAccount" : false,
            "avgBankBalance" : 0,
            "deductedEmiAmt" : 0,
            "mentionAmount" : 0,
            "yearHeld" : 2,
            "bankingType" : "Primary",
            "isSelected" : true,
            "dateTime" : "2019-04-25T10:48:30.380Z",
            "status" : "NOT_SUPPORTED",
            "remarks" : "Bank name not in the list",
            "isBankingRequired" : false,
            "bankingImageDetails" : {
              "breDecision" : "Approved",
              "bankingImageStatus" : "Approved",
              "bankingImageRequired" : true,
              "bankingImageId" : "5cc191148f4c18b90ab08a6a",
              "bankingImageName" : "CROSS_CHEQUE",
              "dateTime" : "2019-04-25T10:48:37.007Z"
            },
            "attemptID" : "1A56684000115"
          }
        ],
        "incomeDetails" : {
          "otherSourceIncomeAmount" : 0,
          "netMonthlyAmt" : 0,
          "grossMonthlyAmt" : 0,
          "otherSrcMnthlyIncmAmt" : 0,
          "totFmlyMnthlyIncmAmt" : 0
        },
        "surrogate" : {
          "additionalProperties" : {
            
          }
        },
        "consentToCall" : false,
        "idfyAnalyticDetails" : {
          
        },
        "bookAndWait" : false,
        "ResiCumOffice" : false,
        "bureauAnalyticDetails" : {
          "bureauApplicantNameMatch" : "100",
          "bureauApplicantDobMatch" : "Matched"
        },
        "bankingAnalyticDetails" : {
          
        },
        "isKarzaKycSkipped" : false,
        "consentToKyc" : true,
        "otherKyc" : false,
        "isDrivingLicenceKarzaEligible" : "Y",
        "isVoterIdKarzaEligible" : "Y",
        "isIdfyEligible" : "Y",
        "promoCode" : "UAT_ALL",
        "ideaOtp" : false
      },
      "application" : {
        "loanType" : "LSL",
        "productID" : "01",
        "loanAmount" : 30000,
        "loanTenor" : 2,
        "loanApr" : 0,
        "emi" : 0,
        "numberOfAdvanceEmi" : 0,
        "dedupeEmiPaid" : 0,
        "dedupeTenor" : 0,
        "marginAmount" : 0,
        "asset" : [
          {
            "assetCtg" : "FITNESS EQUIPMENT",
            "dlrName" : "RAMVEL HOME APLINCS N CMP AVINSI RD",
            "assetMake" : "EVOKE",
            "assetModelMake" : "FITNESS EQUIPMENT",
            "modelNo" : "TREAD MILL",
            "price" : ""
          }
        ],
        "termsConditionAgreement" : false,
        "dndAgrrement" : false,
        "preApprovedAmount" : 0,
        "higherLoanAmtReq" : false,
        "higherLoanAmt" : 0
      },
      "suspiciousActivity" : "No",
      "masterDataInfo" : {
        
      }
    },
    "currentStageId" : "APRV",
    "dealerRank" : 0,
    "alphaNumDealerRank" : "",
    "appMetaData" : {
      "branchV2" : {
        "_id" : "4019_1017",
        "institutionId" : 4019,
        "branchId" : 1017,
        "branchName" : "SALEM-SF",
        "active" : true
      },
      "dsaName" : {
        "firstName" : "HDBFS",
        "lastName" : "DSA"
      },
      "dsaEmailId" : {
        "emailAddress" : "HDBFS_DSA1@softcell.com",
        "verified" : false
      },
      "phone" : {
        "phoneNumber" : "9999999999"
      },
      "sourcingDetails" : {
        "s1" : {
          "_id" : "5ca884e48f4c18f0b204254f",
          "branchId" : "0",
          "makerId" : "HDB69246",
          "authId" : "HDB51988",
          "moduleId" : "LEA",
          "key1" : "SOURCE",
          "key2" : "",
          "value" : "HDB14165",
          "description" : "RAJA SEKHAR G.V.",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2017-07-16T18:30:00.000Z",
          "cgpEndDate" : "2037-07-16T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T09:59:45.989Z",
          "active" : true
        },
        "s2" : [
          {
            "_id" : "5ca884e48f4c18f0b204534e",
            "branchId" : "0",
            "makerId" : "HDB06943",
            "authId" : "HDB37485",
            "moduleId" : "LEA",
            "key1" : "SOURCEID",
            "key2" : "HDB14165",
            "value" : "HDB11311",
            "description" : "HARISH RAO S",
            "status" : "A",
            "moduleFlag" : "0",
            "appFlag" : "0",
            "disableFlag" : "Y",
            "cgpStartDate" : "2015-09-01T18:30:00.000Z",
            "cgpEndDate" : "2025-03-30T18:30:00.000Z",
            "mApplyFlag" : "",
            "institutionId" : "4019",
            "insertDate" : "2019-04-06T10:18:14.606Z",
            "active" : true
          }
        ],
        "s3" : {
          "_id" : "5ca884e48f4c18f0b204bef0",
          "branchId" : "0",
          "makerId" : "MADHAV",
          "authId" : "USER1",
          "moduleId" : "LEA",
          "key1" : "VALIDSRC",
          "key2" : "HDB14165",
          "value" : "HDB13010",
          "description" : "CHANDRA SEKHAR GANDLA",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2012-08-22T18:30:00.000Z",
          "cgpEndDate" : "2025-08-22T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T10:49:45.964Z",
          "active" : true
        },
        "s4" : {
          "_id" : "5ca884e48f4c18f0b2045657",
          "branchId" : "0",
          "makerId" : "HDB55412",
          "authId" : "HDB37485",
          "moduleId" : "LEA",
          "key1" : "SOURCEID",
          "key2" : "HDB13010",
          "value" : "HDB18458",
          "description" : "RAJASHEKAR S",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2017-01-31T18:30:00.000Z",
          "cgpEndDate" : "2026-11-10T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T10:19:26.975Z",
          "active" : true
        }
      }
    },
    "applicantType" : "EXPRESS",
    "qdeDecision" : false,
    "appSubStage" : "SCHEME_BRE_A",
    "multiBreType" : "SCHEME_DETAILS_BRE",
    "isManualBre" : false,
    "karzaFlag" : false,
    "surrogateDecision" : false
  },
  "applicantComponentResponse" : {
    "multiBureauJsonRespose" : {
      "header" : {
        "applicationID" : "56684000115",
        "consumerID" : "56684000115",
        "dateOfRequest" : "25042019 15:35:27",
        "responseType" : "RESPONSE"
      },
      "acknowledgmentId" : 3394243,
      "status" : "COMPLETED",
      "finishedList" : [
        {
          "trackingId" : 1555979,
          "bureau" : "HIGHMARK",
          "product" : "BASE V2.0",
          "status" : "SUCCESS",
          "bureauString" : "<BASE-REPORT-FILE><BASE-REPORTS><BASE-REPORT>  <HEADER>    <DATE-OF-REQUEST>25-04-2019 00:00:00</DATE-OF-REQUEST>    <PREPARED-FOR>HDB FINANCIAL SERVICES</PREPARED-FOR>    <PREPARED-FOR-ID>NBF0000153</PREPARED-FOR-ID>    <DATE-OF-ISSUE>25-04-2019</DATE-OF-ISSUE>    <REPORT-ID>HDB 190425CR44387821</REPORT-ID>    <BATCH-ID>6546229190425</BATCH-ID>    <STATUS>SUCCESS</STATUS>  </HEADER>  <REQUEST>    <NAME><![CDATA[MUKESH AMBANI]]></NAME>    <DOB>27-03-2001</DOB>    <AGE-AS-ON/>    <EMAIL-1>hsgdhg@jd.dj</EMAIL-1>    <GENDER>Male</GENDER>    <ADDRESS-1><![CDATA[JHDSGJFDSHV,      PUNE 411041 MH]]></ADDRESS-1>    <PHONE-1>3487534875</PHONE-1>    <BRANCH><![CDATA[1017]]></BRANCH>    <MBR-ID><![CDATA[56684000115]]></MBR-ID>    <CREDIT-INQ-PURPS-TYP>ACCT-ORIG</CREDIT-INQ-PURPS-TYP>    <CREDIT-INQ-PURPS-TYP-DESC>00</CREDIT-INQ-PURPS-TYP-DESC>    <CREDIT-INQUIRY-STAGE>PRE-SCREEN</CREDIT-INQUIRY-STAGE>    <CREDIT-REQ-TYP>INDV</CREDIT-REQ-TYP>    <CREDIT-RPT-TRN-DT-TM>56684000115</CREDIT-RPT-TRN-DT-TM>    <LOS-APP-ID><![CDATA[56684000115]]></LOS-APP-ID>    <LOAN-AMOUNT>30000</LOAN-AMOUNT>  </REQUEST>  <PERSONAL-INFO-VARIATION>    <NAME-VARIATIONS/>    <ADDRESS-VARIATIONS/>    <PAN-VARIATIONS/>    <DRIVING-LICENSE-VARIATIONS/>    <DATE-OF-BIRTH-VARIATIONS/>    <VOTER-ID-VARIATIONS/>    <PASSPORT-VARIATIONS/>    <PHONE-NUMBER-VARIATIONS/>    <RATION-CARD-VARIATIONS/>    <EMAIL-VARIATIONS/>  </PERSONAL-INFO-VARIATION>  <SECONDARY-MATCHES/>  <ACCOUNTS-SUMMARY>    <DERIVED-ATTRIBUTES>      <INQUIRIES-IN-LAST-SIX-MONTHS>0</INQUIRIES-IN-LAST-SIX-MONTHS>      <LENGTH-OF-CREDIT-HISTORY-YEAR>0</LENGTH-OF-CREDIT-HISTORY-YEAR>      <LENGTH-OF-CREDIT-HISTORY-MONTH>0</LENGTH-OF-CREDIT-HISTORY-MONTH>      <AVERAGE-ACCOUNT-AGE-YEAR>0</AVERAGE-ACCOUNT-AGE-YEAR>      <AVERAGE-ACCOUNT-AGE-MONTH>0</AVERAGE-ACCOUNT-AGE-MONTH>      <NEW-ACCOUNTS-IN-LAST-SIX-MONTHS>0</NEW-ACCOUNTS-IN-LAST-SIX-MONTHS>      <NEW-DELINQ-ACCOUNT-IN-LAST-SIX-MONTHS>0</NEW-DELINQ-ACCOUNT-IN-LAST-SIX-MONTHS>    </DERIVED-ATTRIBUTES>    <PRIMARY-ACCOUNTS-SUMMARY>      <PRIMARY-NUMBER-OF-ACCOUNTS>0</PRIMARY-NUMBER-OF-ACCOUNTS>      <PRIMARY-ACTIVE-NUMBER-OF-ACCOUNTS>0</PRIMARY-ACTIVE-NUMBER-OF-ACCOUNTS>      <PRIMARY-OVERDUE-NUMBER-OF-ACCOUNTS>0</PRIMARY-OVERDUE-NUMBER-OF-ACCOUNTS>      <PRIMARY-SECURED-NUMBER-OF-ACCOUNTS>0</PRIMARY-SECURED-NUMBER-OF-ACCOUNTS>      <PRIMARY-UNSECURED-NUMBER-OF-ACCOUNTS>0</PRIMARY-UNSECURED-NUMBER-OF-ACCOUNTS>      <PRIMARY-UNTAGGED-NUMBER-OF-ACCOUNTS>0</PRIMARY-UNTAGGED-NUMBER-OF-ACCOUNTS>      <PRIMARY-CURRENT-BALANCE>0</PRIMARY-CURRENT-BALANCE>      <PRIMARY-SANCTIONED-AMOUNT>0</PRIMARY-SANCTIONED-AMOUNT>      <PRIMARY-DISBURSED-AMOUNT>0</PRIMARY-DISBURSED-AMOUNT>    </PRIMARY-ACCOUNTS-SUMMARY>    <SECONDARY-ACCOUNTS-SUMMARY>      <SECONDARY-NUMBER-OF-ACCOUNTS>0</SECONDARY-NUMBER-OF-ACCOUNTS>      <SECONDARY-ACTIVE-NUMBER-OF-ACCOUNTS>0</SECONDARY-ACTIVE-NUMBER-OF-ACCOUNTS>      <SECONDARY-OVERDUE-NUMBER-OF-ACCOUNTS>0</SECONDARY-OVERDUE-NUMBER-OF-ACCOUNTS>      <SECONDARY-SECURED-NUMBER-OF-ACCOUNTS>0</SECONDARY-SECURED-NUMBER-OF-ACCOUNTS>      <SECONDARY-UNSECURED-NUMBER-OF-ACCOUNTS>0</SECONDARY-UNSECURED-NUMBER-OF-ACCOUNTS>      <SECONDARY-UNTAGGED-NUMBER-OF-ACCOUNTS>0</SECONDARY-UNTAGGED-NUMBER-OF-ACCOUNTS>      <SECONDARY-CURRENT-BALANCE>0</SECONDARY-CURRENT-BALANCE>      <SECONDARY-SANCTIONED-AMOUNT>0</SECONDARY-SANCTIONED-AMOUNT>      <SECONDARY-DISBURSED-AMOUNT>0</SECONDARY-DISBURSED-AMOUNT>    </SECONDARY-ACCOUNTS-SUMMARY>  </ACCOUNTS-SUMMARY>    <SCORES/><PRINTABLE-REPORT><TYPE>HTML/XML</TYPE><FILE-NAME>HDB 190425CR44387821.html</FILE-NAME><CONTENT><![CDATA[<!DOCTYPE html PUBLIC \\\"-//W3C//DTD XHTML 1.0 Transitional//EN\\\" \\\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\\\"><html><head><meta http-equiv=\\\"Content-Type\\\" content=\\\"text/html; charset=UTF-8\\\"><title>Consumer Base Report</title><style type=\\\"text/css\\\">@media print{  table { page-break-after:auto;   -webkit-print-color-adjust:exact;}  thead { display:table-header-group; }  tfoot { display:table-footer-group; }  body\t{\tmargin-top:10px;\tmargin-bottom:10px;\tmargin-right:25px;\tmargin-left:30px;\t}}.infoValueNote {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 500;\tcolor: grey;\tpadding-right: 15px;\tfont-style: normal;}.shading{\tbackground-color: #e6e6ff;\tbackground:#e6e6ff;}.box {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: thin;\tborder-color: #FFFFFF;\tborder-collapse: collapse;\ttext-align: left;\t-moz-box-shadow: 0px 0px 30px #DADADA;\t-webkit-box-shadow: 0px 0px 30px #DADADA;\tbox-shadow: 0px 0px 30px #DADADA;}.box1 {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: 0px;\tborder-collapse: collapse;\ttext-align: left;}.tabStyle {\tbackground: #FFFFFF;\tborder-style: inset;\tborder-width: thin;\tborder-color: black;\tborder-collapse: collapse;}.rowStyle {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: thin;\tborder-color: grey;\tborder-collapse: collapse;}.box1 tr:nt-child(even) {\tbackground-color: white;}.box1 tr:nth-child(odd) {\tbackground-color: #F1F3F5;}.style14 {\tfont-face: segoe ui semibold;\tfont-size: 2px;}.summarytable {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: 0px;\tborder-collapse: collapse;\ttext-align: left;\tborder-left: none;\tborder-right: none;}.reportHead {\tfont-family: segoe ui semibold;\tfont-size: 24px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;}.dataHead {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: right;\ttext-indent: 5px;}.mainHeader {\tfont-family: segoe ui semibold;\tfont-size: 16px;\tcolor: #FFFFFF;\tbackground: #0f3f6b;\ttext-align: left;\tfont-weight: 600;\tpadding-bottom: 3px;}.subHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\ttext-align: left;\tborder-width: thin;\tborder-collapse: collapse;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 0px;\tborder-right: 0px;\tborder-top: 0px;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.subHeader1 {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tborder-width: thin;\tborder-collapse: collapse;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 0px;\tborder-right: 0px;\tborder-top: 0px;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.dataHeaderNone {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: center;\ttext-indent: 5px;\twhite-space: nowrap;\theight : 23;\t\tvalign:middle}.subHeader2 {\tfont-family: segoe ui semibold;\tborder-collapse: collapse;\tborder-bottom: 0px;\tborder-left: 1px solid #ffffff;\tborder-right: 0px;\tborder-top: 1px solid #ffffff;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.dataHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\twhite-space: nowrap;\tpadding-top: 2px;}.dataHeaderScore {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tcolor: #464646;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\twhite-space: nowrap;\tpadding-top: 2px;}.dataValueValue {\tfont-family: segoe ui semibold;\tfont-size: 25px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataValuePerform {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataValuePerform2 {\tborder-collapse: separate;        Color: #464646;        font-family: segoe ui semibold;       font-size: 12px;\tfont-weight: 280;}.dataHeadern {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\tpadding-top: 2px;}.dataValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataAmtValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: right;\tpadding-right: 7px;\t\tpadding-top: 1px;}.dataHeader1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;}.dataValue1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\ttext-indent: 5px;}.mainAccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #FFFFFF;\tbackground: #0f3f6b;\tfont-weight: 600;}.AccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-indent: 5px;}.subAccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tbackground: #e6e6ff;\tfont-weight: 600;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\t}.AccValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;}.AccValue1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;}.AccSummaryTab {\tborder-width: thin;\tborder-collapse: collapse;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\tborder-bottom: 0px;\ttext-indent: 5px;}.disclaimerValue {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 500;\tcolor: grey;}.infoValue {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 500;\tcolor: grey;\tpadding-right: 15px;\tfont-style: normal;}.maroonFields {\tcolor: Maroon;\tfont-family: segoe ui semibold;\tfont-size: 15px;\tfont-weight: 600;}.AccValueComm2 {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;}.AccValue2 {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\t}.container {\t/* this will give container dimension, because floated child nodes don't give any */\t/* if your child nodes are inline-blocked, then you don't have to set it */\toverflow: auto;}.container .headActive {\t/* float your elements or inline-block them to display side by side */\tfloat: left;\t/* these are height and width dimensions of your header */\theight: 10em;\twidth: 1.5em;\t/* set to hidden so when there's too much vertical text it will be clipped. */\toverflow: hidden;\t/* these are not relevant and are here to better see the elements */\tbackground: #ffe1dc;\tcolor: #be0000;\tmargin-right: 1px;\tfont-family: segoe ui ;\tfont-weight:bold;}.container .headActive .vertActive {\t/* line height should be equal to header width so text will be middle aligned */\tline-height: 1.5em;\t/* setting background may yield better results in IE text clear type rendering */\tbackground: #ffe1dc;\tcolor: #be0000;\tdisplay: block;\t/* this will prevent it from wrapping too much text */\twhite-space: nowrap;\t/* so it stays off the edge */\tpadding-left: 3px;\tfont-family: segoe ui ;\tfont-weight:bold;\t/* CSS3 specific totation CODE */\t/* translate should have the same negative dimension as head height */\ttransform: rotate(-270deg) translate(1em, 0);\ttransform-origin: -5px 30px;\t-moz-transform: rotate(-270deg) translate(1em, 0);\t-moz-transform-origin: -5px 30px;\t-webkit-transform: rotate(-270deg) translate(1em, 0);\t-webkit-transform-origin: -5px 30px;\t-ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}.container .headClosed {\t/* float your elements or inline-block them to display side by side */\tfloat: left;\t/* these are height and width dimensions of your header */\theight: 10em;\twidth: 1.5em;\t/* set to hidden so when there's too much vertical text it will be clipped. */\toverflow: hidden;\t/* these are not relevant and are here to better see the elements */\tbackground: #e1f0be;\tcolor: #415a05;\tmargin-right: 1px;\tfont-family: segoe ui ;\tfont-weight:bold;}.container .headClosed .vertClosed {\t/* line height should be equal to header width so text will be middle aligned */\tline-height: 1.5em;\t/* setting background may yield better results in IE text clear type rendering */\tbackground: #ffe1dc;\tcolor: #415a05;\tdisplay: block;\t/* this will prevent it from wrapping too much text */\twhite-space: nowrap;\t/* so it stays off the edge */\tpadding-left: 3px;\tfont-family: segoe ui ;\tfont-weight:bold;\t/* CSS3 specific totation CODE */\t/* translate should have the same negative dimension as head height */\ttransform: rotate(-270deg) translate(1em, 0);\ttransform-origin: -5px 30px;\t-moz-transform: rotate(-270deg) translate(1em, 0);\t-moz-transform-origin: -5px 30px;\t-webkit-transform: rotate(-270deg) translate(1em, 0);\t-webkit-transform-origin: -5px 30px;\t-ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}</style></head><body style=\\\"font-family: segoe ui semibold, arial, verdana;\\\"><table class=\\\"box\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t<thead>\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"2\\\" valign=\\\"top\\\"><img src=\\\"data:image/gif;base64,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\\\" alt=\\\"CRIF HighMark Credit Information Services Pvt. Ltd.\\\" align=\\\"left\\\" width=\\\"120\\\" height=\\\"80\\\"/></td>\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"120\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"380\\\" valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t<table border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"reportHead\\\">CONSUMER BASE&trade; REPORT <br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHead\\\" align=\\\"right\\\" valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tFor MUKESH AMBANI </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td rowspan=\\\"2\\\" align=\\\"right\\\" valign=\\\"top\\\" width=\\\"350\\\">\t\t\t\t\t\t\t\t\t\t\t\t<table>\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">CHM Ref #:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">HDB 190425CR44387821 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Prepared For:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">HDB FINANCIAL SERVICES </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Application ID:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">56684000115  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Date of Request:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">25-04-2019 00:00:00 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Date of Issue:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">25-04-2019 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t<td height=\\\"10\\\">\t\t\t\t\t\t\t\t\t<hr size=\\\"1\\\" style=\\\"color: #C8C8C8;\\\" />\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t\t</thead>\t <tfoot>\t\t<tr>\t\t\t<td>\t\t\t\t<table summary=\\\"\\\" align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t<tbody>\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t<table summary=\\\"\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<hr color=\\\"silver\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC\\\" valign=\\\"top\\\" width=\\\"70\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Disclaimer:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"4\\\" class=\\\"disclaimerValue\\\">This document contains proprietary information to CRIF High Mark and may not be used or disclosed to others, except with the written permission of CRIF High Mark. Any paper copy of this document will be considered uncontrolled. If you are not the intended recipient, you are not authorized to read, print, retain, copy, disseminate, distribute, or use this information or any part thereof. PERFORM score provided in this document is joint work of CRIF SPA (Italy) and CRIF High Mark (India).</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td><br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"left\\\" width=\\\"300\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Copyrights reserved\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(c) 2019</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"center\\\" width=\\\"400\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">CRIF High Mark Credit\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation Services Pvt. Ltd</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"right\\\" width=\\\"300\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Company Confidential\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tData</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70\\\"><br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t</td>\t\t\t\t\t\t</tr>\t\t\t\t\t</tbody>\t\t\t\t</table>\t\t\t</td>\t\t</tr>\t\t\t\t\t\t</tfoot>\t\t\t<tbody>\t\t<tr>\t\t\t<td>\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Inquiry Input Information</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table border=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"10px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"110 px\\\" class=\\\"dataHeader\\\">Name:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"270 px\\\" class=\\\"dataValue\\\"> MUKESH AMBANI </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">DOB/Age:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"190 px\\\" class=\\\"dataValue\\\">27-03-2001   </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Gender:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"200 px\\\" class=\\\"dataValue\\\">MALE </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Father:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Spouse:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"100 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Mother:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"120 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\" width=\\\"100 px\\\">Phone\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tNumbers:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"> 3487534875 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\">ID(s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\">Email ID(s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"> hsgdhg@jd.dj </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Entity\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tId:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Current\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAddress:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\"> JHDSGJFDSHV,      PUNE 411041 MH </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Other\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAddress:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr> \t\t\t\t\t\t \t\t\t\t\t\t <tr>\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">CRIF HM Score (s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t \t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td class=\\\"dataHeaderNone\\\" align=\\\"center\\\">None</td>\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t                        \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"30px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Personal Information -\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tVariations</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: These\t\t\t\t\t\t\t\t\tare applicant's personal information variations as contributed\t\t\t\t\t\t\t\t\tby various financial institutions.</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\">\t\t\t\t\t\t\t\t\t<table cellpadding=\\\"2\\\" cellspacing=\\\"4\\\" border=\\\"0px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" align=\\\"left\\\">None</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: All\t\t\t\t\t\t\t\t\t\t\t\tamounts are in INR.</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr></tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Account Summary</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: Current Balance & Disbursed Amount is considered ONLY for ACTIVE accounts.</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\" height=\\\"20\\\"></td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" style=\\\"text-align:center\\\">None</td>\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t<td height=\\\"30px\\\"></td>\t\t\t</tr>\t\t\t<tr>\t\t\t<td>\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t</td></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Inquiries (reported for past 24\t\t\t\t\t\t\t\t\t\t\t\tmonths)</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Member Name</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Date of Inquiry</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Purpose</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Ownership Type</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"subHeader\\\">Amount</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Remark</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"30\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Comments</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\">Description</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"subHeader\\\" width=\\\"115\\\">Date</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"dataValue\\\" width=\\\"115\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"AccHeader\\\">-END OF CONSUMER BASE REPORT-</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t</tr><tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<hr color=\\\"silver\\\">\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Appendix</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"250\\\">Section</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"220\\\">Code</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"480\\\">Description</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSummary</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">Number\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tof Delinquent Accounts</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tIndicates number of accounts that the applicant has\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdefaulted on within the last 6 months</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation - Credit Grantor</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXXX</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tName of grantor undisclosed as credit grantor is\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdifferent from inquiring institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation - Account #</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">xxxx</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAccount Number undisclosed as credit grantor is\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdifferent from inquiring institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXX</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Data\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tnot reported by institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">&nbsp;&nbsp;&nbsp;&nbsp;-</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Not applicable</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">STD</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as STANDARD Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SUB</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as SUB-STANDARD Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">DBT</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as DOUBTFUL Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">LOS</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as LOSS Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SMA</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as SPECIAL MENTION</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tScore has reckoned from credit history, pursuit of new credit, payment history, type of credit in &nbsp;&nbsp;use and outstanding debt.</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<!--<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Score of \\\"0\\\" is no hit.</td> -->\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"20\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t</table></body></html>]]></CONTENT></PRINTABLE-REPORT></BASE-REPORT></BASE-REPORTS></BASE-REPORT-FILE>",
          "pdfReport" : "BinData(0,\"JVBERi0xLjQKJcfl9OXwCjEgMCBvYmoKmore8612bytes+application/pd\")",
          "responseJsonObject" : {
            "baseReports" : {
              "baseReport" : {
                "request" : {
                  "loanAmount" : "30000",
                  "creditRequestType" : "INDV",
                  "creditInquiryStage" : "PRE-SCREEN",
                  "address1" : "JHDSGJFDSHV,      PUNE 411041 MH",
                  "creditInquiryPurposeType" : "ACCT-ORIG",
                  "phone1" : "3487534875",
                  "email1" : "hsgdhg@jd.dj",
                  "creditInquiryPurposeTypeDescription" : "00",
                  "name" : "MUKESH AMBANI",
                  "dob" : "27-03-2001",
                  "creditReportTransectionDatetime" : "56684000115",
                  "branch" : "1017",
                  "gender" : "Male",
                  "memberId" : "56684000115",
                  "losApplicationId" : "56684000115"
                },
                "printableReport" : {
                  "content" : "<!DOCTYPE html PUBLIC \\\"-//W3C//DTD XHTML 1.0 Transitional//EN\\\" \\\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\\\"><html><head><meta http-equiv=\\\"Content-Type\\\" content=\\\"text/html; charset=UTF-8\\\"><title>Consumer Base Report</title><style type=\\\"text/css\\\">@media print{  table { page-break-after:auto;   -webkit-print-color-adjust:exact;}  thead { display:table-header-group; }  tfoot { display:table-footer-group; }  body { margin-top:10px; margin-bottom:10px; margin-right:25px; margin-left:30px; }}.infoValueNote { font-family: segoe ui semibold; font-size: 11px; font-weight: 500; color: grey; padding-right: 15px; font-style: normal;}.shading{ background-color: #e6e6ff; background:#e6e6ff;}.box { background: #FFFFFF; border-style: solid; border-width: thin; border-color: #FFFFFF; border-collapse: collapse; text-align: left; -moz-box-shadow: 0px 0px 30px #DADADA; -webkit-box-shadow: 0px 0px 30px #DADADA; box-shadow: 0px 0px 30px #DADADA;}.box1 { background: #FFFFFF; border-style: solid; border-width: 0px; border-collapse: collapse; text-align: left;}.tabStyle { background: #FFFFFF; border-style: inset; border-width: thin; border-color: black; border-collapse: collapse;}.rowStyle { background: #FFFFFF; border-style: solid; border-width: thin; border-color: grey; border-collapse: collapse;}.box1 tr:nt-child(even) { background-color: white;}.box1 tr:nth-child(odd) { background-color: #F1F3F5;}.style14 { font-face: segoe ui semibold; font-size: 2px;}.summarytable { background: #FFFFFF; border-style: solid; border-width: 0px; border-collapse: collapse; text-align: left; border-left: none; border-right: none;}.reportHead { font-family: segoe ui semibold; font-size: 24px; color: #0f3f6b; font-weight: 600; text-align: left;}.dataHead { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: right; text-indent: 5px;}.mainHeader { font-family: segoe ui semibold; font-size: 16px; color: #FFFFFF; background: #0f3f6b; text-align: left; font-weight: 600; padding-bottom: 3px;}.subHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; text-align: left; border-width: thin; border-collapse: collapse; border-bottom: 1px solid #A7CBE3; border-left: 0px; border-right: 0px; border-top: 0px; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.subHeader1 { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; border-width: thin; border-collapse: collapse; border-bottom: 1px solid #A7CBE3; border-left: 0px; border-right: 0px; border-top: 0px; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.dataHeaderNone { font-family: segoe ui semibold; font-size: 14px; color: #0f3f6b; font-weight: 600; text-align: center; text-indent: 5px; white-space: nowrap; height : 23;  valign:middle}.subHeader2 { font-family: segoe ui semibold; border-collapse: collapse; border-bottom: 0px; border-left: 1px solid #ffffff; border-right: 0px; border-top: 1px solid #ffffff; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.dataHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px; white-space: nowrap; padding-top: 2px;}.dataHeaderScore { font-family: segoe ui semibold; font-size: 12px; color: #464646; font-weight: 600; text-align: left; text-indent: 5px; white-space: nowrap; padding-top: 2px;}.dataValueValue { font-family: segoe ui semibold; font-size: 25px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataValuePerform { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataValuePerform2 { border-collapse: separate;        Color: #464646;        font-family: segoe ui semibold;       font-size: 12px; font-weight: 280;}.dataHeadern { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px; padding-top: 2px;}.dataValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataAmtValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-align: right; padding-right: 7px;  padding-top: 1px;}.dataHeader1 { font-family: segoe ui semibold; font-size: 12px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px;}.dataValue1 { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: left; text-indent: 5px;}.mainAccHeader { font-family: segoe ui semibold; font-size: 13px; color: #FFFFFF; background: #0f3f6b; font-weight: 600;}.AccHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-indent: 5px;}.subAccHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; background: #e6e6ff; font-weight: 600; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; }.AccValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-indent: 5px;}.AccValue1 { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3;}.AccSummaryTab { border-width: thin; border-collapse: collapse; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; border-bottom: 0px; text-indent: 5px;}.disclaimerValue { font-family: segoe ui semibold; font-size: 12px; font-weight: 500; color: grey;}.infoValue { font-family: segoe ui semibold; font-size: 12px; font-weight: 500; color: grey; padding-right: 15px; font-style: normal;}.maroonFields { color: Maroon; font-family: segoe ui semibold; font-size: 15px; font-weight: 600;}.AccValueComm2 { font-family: segoe ui semibold; font-size: 11px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3;}.AccValue2 { font-family: segoe ui semibold; font-size: 11px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; }.container { /* this will give container dimension, because floated child nodes don't give any */ /* if your child nodes are inline-blocked, then you don't have to set it */ overflow: auto;}.container .headActive { /* float your elements or inline-block them to display side by side */ float: left; /* these are height and width dimensions of your header */ height: 10em; width: 1.5em; /* set to hidden so when there's too much vertical text it will be clipped. */ overflow: hidden; /* these are not relevant and are here to better see the elements */ background: #ffe1dc; color: #be0000; margin-right: 1px; font-family: segoe ui ; font-weight:bold;}.container .headActive .vertActive { /* line height should be equal to header width so text will be middle aligned */ line-height: 1.5em; /* setting background may yield better results in IE text clear type rendering */ background: #ffe1dc; color: #be0000; display: block; /* this will prevent it from wrapping too much text */ white-space: nowrap; /* so it stays off the edge */ padding-left: 3px; font-family: segoe ui ; font-weight:bold; /* CSS3 specific totation CODE */ /* translate should have the same negative dimension as head height */ transform: rotate(-270deg) translate(1em, 0); transform-origin: -5px 30px; -moz-transform: rotate(-270deg) translate(1em, 0); -moz-transform-origin: -5px 30px; -webkit-transform: rotate(-270deg) translate(1em, 0); -webkit-transform-origin: -5px 30px; -ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}.container .headClosed { /* float your elements or inline-block them to display side by side */ float: left; /* these are height and width dimensions of your header */ height: 10em; width: 1.5em; /* set to hidden so when there's too much vertical text it will be clipped. */ overflow: hidden; /* these are not relevant and are here to better see the elements */ background: #e1f0be; color: #415a05; margin-right: 1px; font-family: segoe ui ; font-weight:bold;}.container .headClosed .vertClosed { /* line height should be equal to header width so text will be middle aligned */ line-height: 1.5em; /* setting background may yield better results in IE text clear type rendering */ background: #ffe1dc; color: #415a05; display: block; /* this will prevent it from wrapping too much text */ white-space: nowrap; /* so it stays off the edge */ padding-left: 3px; font-family: segoe ui ; font-weight:bold; /* CSS3 specific totation CODE */ /* translate should have the same negative dimension as head height */ transform: rotate(-270deg) translate(1em, 0); transform-origin: -5px 30px; -moz-transform: rotate(-270deg) translate(1em, 0); -moz-transform-origin: -5px 30px; -webkit-transform: rotate(-270deg) translate(1em, 0); -webkit-transform-origin: -5px 30px; -ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}</style></head><body style=\\\"font-family: segoe ui semibold, arial, verdana;\\\"><table class=\\\"box\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1020px\\\"> <thead> <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr height=\\\"10\\\">            <td></td>           </tr>           <tr>            <td colspan=\\\"2\\\" valign=\\\"top\\\"><img src=\\\"data:image/gif;base64,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\\\" alt=\\\"CRIF HighMark Credit Information Services Pvt. Ltd.\\\" align=\\\"left\\\" width=\\\"120\\\" height=\\\"80\\\"/></td>            <td width=\\\"120\\\"></td>            <td align=\\\"left\\\" width=\\\"380\\\" valign=\\\"top\\\">            <table border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">             <tbody>              <tr>               <td align=\\\"center\\\" class=\\\"reportHead\\\">CONSUMER BASE&trade; REPORT <br>               </td>              </tr>              <tr valign=\\\"top\\\">               <td class=\\\"dataHead\\\" align=\\\"right\\\" valign=\\\"top\\\">               For MUKESH AMBANI </td>              </tr>             </tbody>            </table>            </td>            <td width=\\\"70\\\"></td>            <td rowspan=\\\"2\\\" align=\\\"right\\\" valign=\\\"top\\\" width=\\\"350\\\">            <table>             <tbody>              <tr>               <td class=\\\"dataHeader1\\\">CHM Ref #:</td>               <td class=\\\"dataValue1\\\">HDB 190425CR44387821 </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Prepared For:</td>               <td class=\\\"dataValue1\\\">HDB FINANCIAL SERVICES </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Application ID:</td>               <td class=\\\"dataValue1\\\">56684000115  </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Date of Request:</td>               <td class=\\\"dataValue1\\\">25-04-2019 00:00:00 </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Date of Issue:</td>               <td class=\\\"dataValue1\\\">25-04-2019 </td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr><tr>         <td height=\\\"10\\\">         <hr size=\\\"1\\\" style=\\\"color: #C8C8C8;\\\" />         </td>        </tr>       </tbody>      </table>      </td>     </tr>      </thead>  <tfoot>  <tr>   <td>    <table summary=\\\"\\\" align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">     <tbody>      <tr>       <td>        <table summary=\\\"\\\" border=\\\"0\\\" width=\\\"1020px\\\">                   <tbody>                    <tr height=\\\"10\\\">                     <td colspan=\\\"5\\\">                     <hr color=\\\"silver\\\">                     </td>                    </tr>                    <tr>                     <td color=\\\"#CCCCCC\\\" valign=\\\"top\\\" width=\\\"70\\\"                      class=\\\"disclaimerValue\\\">Disclaimer:</td>                     <td colspan=\\\"4\\\" class=\\\"disclaimerValue\\\">This document contains proprietary information to CRIF High Mark and may not be used or disclosed to others, except with the written permission of CRIF High Mark. Any paper copy of this document will be considered uncontrolled. If you are not the intended recipient, you are not authorized to read, print, retain, copy, disseminate, distribute, or use this information or any part thereof. PERFORM score provided in this document is joint work of CRIF SPA (Italy) and CRIF High Mark (India).</td>                    </tr>                    <tr>                     <td><br>                     <br>                     </td>                     <td color=\\\"#CCCCCC \\\" align=\\\"left\\\" width=\\\"300\\\"                      class=\\\"disclaimerValue\\\">Copyrights reserved                     (c) 2019</td>                     <td color=\\\"#CCCCCC \\\" align=\\\"center\\\" width=\\\"400\\\"                      class=\\\"disclaimerValue\\\">CRIF High Mark Credit                     Information Services Pvt. Ltd</td>                     <td color=\\\"#CCCCCC \\\" align=\\\"right\\\" width=\\\"300\\\"                      class=\\\"disclaimerValue\\\">Company Confidential                     Data</td>                     <td width=\\\"70\\\"><br>                     <br>                     </td>                    </tr>                   </tbody>                  </table>       </td>      </tr>     </tbody>    </table>   </td>  </tr>      </tfoot>   <tbody>  <tr>   <td>   <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">    <tbody>          <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"       width=\\\"1020px\\\">       <tbody>                <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Inquiry Input Information</td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1030px\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1030px\\\">          <tbody>           <tr>            <td>            <table border=\\\"0\\\" width=\\\"1030px\\\">             <tbody>              <tr>               <td height=\\\"10px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"110 px\\\" class=\\\"dataHeader\\\">Name:</td>               <td align=\\\"left\\\" width=\\\"270 px\\\" class=\\\"dataValue\\\"> MUKESH AMBANI </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">DOB/Age:</td>               <td width=\\\"190 px\\\" class=\\\"dataValue\\\">27-03-2001   </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Gender:</td>               <td width=\\\"200 px\\\" class=\\\"dataValue\\\">MALE </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Father:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"> </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Spouse:</td>               <td width=\\\"100 px\\\" class=\\\"dataValue\\\"> </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Mother:</td>               <td width=\\\"120 px\\\" class=\\\"dataValue\\\"> </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\" width=\\\"100 px\\\">Phone               Numbers:</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"> 3487534875 </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>               </table>               </td>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\">ID(s):</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>               </table>               </td>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\">Email ID(s):</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"> hsgdhg@jd.dj </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>               </table>               </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Entity               Id:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\">  </td>                             </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Current               Address:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\"> JHDSGJFDSHV,      PUNE 411041 MH </td>                             </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Other               Address:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\">  </td>               </td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>               <tr>        <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr>            <td>             <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"              width=\\\"1020px\\\">              <tbody>               <tr height=\\\"20\\\">                <td width=\\\"10\\\"></td>                <td class=\\\"mainHeader\\\">CRIF HM Score (s):</td>               </tr>              </tbody>             </table>            </td>           </tr>          </tbody>         </table>        </td>       </tr>               <tr>       <td class=\\\"dataHeaderNone\\\" align=\\\"center\\\">None</td>         </tr>                                                    <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"       width=\\\"1020px\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr>            <td height=\\\"30px\\\"></td>           </tr>           <tr>            <td>            <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"             width=\\\"1020px\\\">             <tbody>              <tr height=\\\"20\\\">               <td width=\\\"10\\\"></td>               <td class=\\\"mainHeader\\\">Personal Information -               Variations</td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"20\\\">         <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: These         are applicant's personal information variations as contributed         by various financial institutions.</td>        </tr>        <tr>         <td align=\\\"center\\\">         <table cellpadding=\\\"2\\\" cellspacing=\\\"4\\\" border=\\\"0px\\\">          <tbody>                      <td class=\\\"dataHeader\\\" align=\\\"left\\\">None</td>                     </tbody>         </table>         </td>        </tr>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\">          <tbody>           <tr height=\\\"10\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\"></td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: All            amounts are in INR.</td>           </tr>           <tr></tr>           <tr>            <td>            <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"             width=\\\"1020px\\\">             <tbody>              <tr height=\\\"20\\\">               <td width=\\\"10\\\"></td>               <td class=\\\"mainHeader\\\">Account Summary</td>              </tr>             </tbody>            </table>            </td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: Current Balance & Disbursed Amount is considered ONLY for ACTIVE accounts.</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr>         <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\" height=\\\"20\\\"></td>        </tr>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>                 <tr>       <td class=\\\"dataHeader\\\" style=\\\"text-align:center\\\">None</td>       </tr>                 </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>          <tr>    <td height=\\\"30px\\\"></td>   </tr>   <tr>   <td>         <tr>      <td>          <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>                                          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"10\\\"></td>     </tr>     </td></tr>               <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr height=\\\"10\\\"></tr>        <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"          width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Inquiries (reported for past 24            months)</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"10\\\"></tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>           <tr height=\\\"20\\\">            <td align=\\\"center\\\" class=\\\"subHeader\\\">Member Name</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Date of Inquiry</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Purpose</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Ownership Type</td>            <td align=\\\"right\\\" class=\\\"subHeader\\\">Amount</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Remark</td>           </tr>                     </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"30\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr height=\\\"10\\\"></tr>        <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"          width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Comments</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"10\\\"></tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>           <tr height=\\\"20\\\">            <td align=\\\"left\\\" class=\\\"subHeader\\\">Description</td>            <td align=\\\"right\\\" class=\\\"subHeader\\\" width=\\\"115\\\">Date</td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"left\\\" class=\\\"dataValue\\\"></td>            <td align=\\\"right\\\" class=\\\"dataValue\\\" width=\\\"115\\\"></td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"10\\\"></td>     </tr><tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\">          <tbody>           <tr>            <td>            <table width=\\\"1000px\\\">             <tbody>              <tr>               <td align=\\\"center\\\" class=\\\"AccHeader\\\">-END OF CONSUMER BASE REPORT-</td>              </tr>             </tbody>            </table>            </td>           </tr><tr>           <td height=\\\"10\\\"></td>          </tr><tr height=\\\"10\\\">           <td>            <hr color=\\\"silver\\\">           </td>          </tr>                      <tr>            <td>            <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"             cellspacing=\\\"0\\\">             <tbody>              <tr height=\\\"10\\\"></tr>              <tr>               <td>               <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"                width=\\\"1020px\\\">                <tbody>                 <tr height=\\\"20\\\">                  <td width=\\\"10\\\"></td>                  <td class=\\\"mainHeader\\\">Appendix</td>                 </tr>                </tbody>               </table>               </td>              </tr>              <tr height=\\\"10\\\"></tr>             </tbody>            </table>            </td>           </tr>           <tr>            <td height=\\\"5\\\"></td>           </tr>           <tr>            <td>            <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"             cellspacing=\\\"0\\\">             <tbody>              <tr>               <td>               <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\"                cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1000px\\\">                <tbody>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"250\\\">Section</td>                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"220\\\">Code</td>                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"480\\\">Description</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Summary</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">Number                  of Delinquent Accounts</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Indicates number of accounts that the applicant has                  defaulted on within the last 6 months</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Information - Credit Grantor</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXXX</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Name of grantor undisclosed as credit grantor is                  different from inquiring institution</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Information - Account #</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">xxxx</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Account Number undisclosed as credit grantor is                  different from inquiring institution</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXX</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Data                  not reported by institution</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">&nbsp;&nbsp;&nbsp;&nbsp;-</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Not applicable</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">STD</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as STANDARD Asset</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SUB</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as SUB-STANDARD Asset</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">DBT</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as DOUBTFUL Asset</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">LOS</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as LOSS Asset</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SMA</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as SPECIAL MENTION</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Score has reckoned from credit history, pursuit of new credit, payment history, type of credit in &nbsp;&nbsp;use and outstanding debt.</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <!--<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>                   <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Score of \\\"0\\\" is no hit.</td> -->                 </tr>                </tbody>               </table>               </td>              </tr>             </tbody>            </table>            </td>           </tr>           <tr>            <td height=\\\"20\\\"></td>           </tr>                        </tbody>            </table>            </td>           </tr>       </tbody>             </table></body></html>",
                  "fileName" : "HDB 190425CR44387821.html"
                },
                "personalInfoVariation" : {
                  
                },
                "header" : {
                  "status" : "SUCCESS",
                  "dateOfRequest" : "25-04-2019 00:00:00",
                  "batchId" : "6546229190425",
                  "reportId" : "HDB 190425CR44387821",
                  "dateOfIssue" : "25-04-2019",
                  "preparedForId" : "NBF0000153",
                  "preparedFor" : "HDB FINANCIAL SERVICES"
                },
                "accountSummary" : {
                  "drivedAttributes" : {
                    "lengthOfCreditHistoryYear" : "0",
                    "inquiriesInLastSixMonth" : "0",
                    "newAccountInLastSixMonths" : "0",
                    "averageAccountAgeYear" : "0",
                    "averageAccountAgeMonth" : "0",
                    "newDlinqAccountInLastSixMonths" : "0",
                    "lengthOfCreditHistoryMonth" : "0"
                  },
                  "secondaryAccountSummary" : {
                    "secondaryUntaggedNumberOfAccounts" : "0",
                    "secondaryNumberOfAccounts" : "0",
                    "secondarySanctionedAmount" : "0",
                    "secondarySecuredNumberOfAccounts" : "0",
                    "secondaryActiveNumberOfAccounts" : "0",
                    "secondaryUnsecuredNumberOfAccounts" : "0",
                    "secondaryCurrentBalance" : "0",
                    "secondaryOverdueNumberOfAccounts" : "0",
                    "secondaryDisbursedAmount" : "0"
                  },
                  "primaryAccountsSummary" : {
                    "primaryUnsecuredNumberOfAccounts" : "0",
                    "primaryOverdueNumberOfAccounts" : "0",
                    "primaryCurrentBalance" : "0",
                    "primaryDisbursedAmount" : "0",
                    "primarySanctionedAmount" : "0",
                    "primaryActiveNumberOfAccounts" : "0",
                    "primaryUntaggedNumberOfAccounts" : "0",
                    "primaryNumberOfAccounts" : "0",
                    "primarySecuredNumberOfAccounts" : "0"
                  }
                }
              }
            }
          }
        },
        {
          "trackingId" : 1555978,
          "bureau" : "EXPERIAN",
          "product" : "CIR",
          "status" : "BUREAU-ERROR",
          "bureauString" : "<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\" standalone=\\\"yes\\\"?> <INProfileResponse>     <Header>         <SystemCode>0</SystemCode>         <MessageText></MessageText>         <ReportDate>20190425</ReportDate>         <ReportTime>153443</ReportTime>     </Header>     <UserMessage>         <UserMessageText>SYS100007(Invalid Enquiry reason/ Search Type)</UserMessageText>     </UserMessage>     <CreditProfileHeader>         <Enquiry_Username></Enquiry_Username>         <ReportDate></ReportDate>         <ReportTime></ReportTime>         <Version>V2.4</Version>         <ReportNumber></ReportNumber>         <Subscriber></Subscriber>         <Subscriber_Name>HDB Financial Services Limited</Subscriber_Name>     </CreditProfileHeader>     <Current_Application>         <Current_Application_Details>             <Enquiry_Reason>00</Enquiry_Reason>             <Finance_Purpose></Finance_Purpose>             <Amount_Financed>30000</Amount_Financed>             <Duration_Of_Agreement>0</Duration_Of_Agreement>             <Current_Applicant_Details>                 <Last_Name>AMBANI</Last_Name>                 <First_Name>MUKESH</First_Name>                 <Middle_Name1></Middle_Name1>                 <Middle_Name2></Middle_Name2>                 <Middle_Name3></Middle_Name3>                 <Gender_Code>2</Gender_Code>                 <IncomeTaxPan></IncomeTaxPan>                 <PAN_Issue_Date></PAN_Issue_Date>                 <PAN_Expiration_Date></PAN_Expiration_Date>                 <Passport_Number></Passport_Number>                 <Passport_Issue_Date></Passport_Issue_Date>                 <Passport_Expiration_Date></Passport_Expiration_Date>                 <Voter_s_Identity_Card></Voter_s_Identity_Card>                 <Voter_ID_Issue_Date></Voter_ID_Issue_Date>                 <Voter_ID_Expiration_Date></Voter_ID_Expiration_Date>                 <Driver_License_Number></Driver_License_Number>                 <Driver_License_Issue_Date></Driver_License_Issue_Date>                 <Driver_License_Expiration_Date></Driver_License_Expiration_Date>                 <Ration_Card_Number></Ration_Card_Number>                 <Ration_Card_Issue_Date></Ration_Card_Issue_Date>                 <Ration_Card_Expiration_Date></Ration_Card_Expiration_Date>                 <Universal_ID_Number></Universal_ID_Number>                 <Universal_ID_Issue_Date></Universal_ID_Issue_Date>                 <Universal_ID_Expiration_Date></Universal_ID_Expiration_Date>                 <Date_Of_Birth_Applicant>20010327</Date_Of_Birth_Applicant>                 <Telephone_Number_Applicant_1st>3487534875</Telephone_Number_Applicant_1st>                 <Telephone_Extension></Telephone_Extension>                 <Telephone_Type>01</Telephone_Type>                 <MobilePhoneNumber></MobilePhoneNumber>                 <EMailId>hsgdhg@jd.dj</EMailId>             </Current_Applicant_Details>             <Current_Other_Details>                 <Income></Income>                 <Marital_Status>1</Marital_Status>                 <Employment_Status></Employment_Status>                 <Time_with_Employer></Time_with_Employer>                 <Number_of_Major_Credit_Card_Held></Number_of_Major_Credit_Card_Held>             </Current_Other_Details>             <Current_Applicant_Address_Details>                 <FlatNoPlotNoHouseNo>JHDSGJFDSHV,</FlatNoPlotNoHouseNo>                 <BldgNoSocietyName></BldgNoSocietyName>                 <RoadNoNameAreaLocality></RoadNoNameAreaLocality>                 <City>PUNE</City>                 <Landmark></Landmark>                 <State>27</State>                 <PINCode>411041</PINCode>                 <Country_Code>IB</Country_Code>             </Current_Applicant_Address_Details>             <Current_Applicant_Additional_Address_Details/>         </Current_Application_Details>     </Current_Application> </INProfileResponse>",
          "pdfReport" : "BinData(0,\"JVBERi0xLjQKJcfl9OXwCjEgMCBvYmoKmore2084bytes+application/pd\")",
          "responseJsonObject" : {
            "currentApplication" : {
              "currentApplicationDetails" : {
                "financePurpose" : "",
                "currentApplicantAddressDetails" : {
                  "pinCode" : "411041",
                  "landmark" : "",
                  "state" : "27",
                  "countryCode" : "IB",
                  "roadNumbernameAreaLocality" : "",
                  "bldgNumberSocietyName" : "",
                  "flatNoPlotNoHouseNo" : "JHDSGJFDSHV,",
                  "city" : "PUNE"
                },
                "enquiryReason" : "00",
                "currentOtherDetails" : {
                  "timeWithEmployer" : "",
                  "numberofMajorcreditCardHeld" : "",
                  "income" : "",
                  "maritialStatus" : "1",
                  "employmentStatus" : ""
                },
                "currentApplicantdetails" : {
                  "votersIdentityCard" : "",
                  "universalIdIssueDate" : "",
                  "universalIdNumber" : "",
                  "passportNumber" : "",
                  "rationCardNumber" : "",
                  "mobilePhoneNumber" : "",
                  "dateofBirthApplicant" : "20010327",
                  "universalIdExpirationDate" : "",
                  "emailid" : "hsgdhg@jd.dj",
                  "middleName1" : "",
                  "telephoneExtension" : "",
                  "passportExpirationDate" : "",
                  "middleName3" : "",
                  "middleName2" : "",
                  "voterIdExpirationdate" : "",
                  "voterIdIssueDate" : "",
                  "firstName" : "MUKESH",
                  "driverLicenceExpirationdate" : "",
                  "driverLicenceIssueDate" : "",
                  "lastName" : "AMBANI",
                  "driverLicenceNumber" : "",
                  "rationCardExpirationDate" : "",
                  "telephoneType" : "01",
                  "incometaxPan" : "",
                  "panIssueDate" : "",
                  "telephoneNumberApplicant1st" : "3487534875",
                  "panExpirationDate" : "",
                  "rationCardIssueDate" : "",
                  "passportIssueDate" : "",
                  "genderCode" : "2"
                },
                "amountFinanced" : "30000",
                "durationOfAgreement" : "0"
              }
            },
            "creditProfileHeader" : {
              "reportNumber" : "",
              "reporttime" : "",
              "subscriberName" : "HDB Financial Services Limited",
              "reportDate" : "",
              "subscriber" : "",
              "enquiryUserName" : "",
              "version" : "V2.4"
            },
            "userMessage" : {
              "userMessageText" : "SYS100007(Invalid Enquiry reason/ Search Type)"
            },
            "header" : {
              "reportTime" : "153443",
              "messageText" : "",
              "systemCode" : "0",
              "reportDate" : "20190425"
            }
          }
        }
      ],
      "creditInsightDomain" : {
        "pastEnquiry" : [ ],
        "bureauReported" : "EXPERIAN (XP), CRIF HIGH MARK (CR)",
        "refNumber" : "3394243",
        "revcSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        },
        "issuedDate" : "Thu Apr 25 15:35:27 IST 2019",
        "activeTradelines" : [ ],
        "totalNumEnquiries" : "0",
        "secSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        },
        "bureauFeeds" : {
          "chmScore" : [ ],
          "experianScore" : [ ],
          "equifaxScore" : [ ],
          "cibilScore" : [ ]
        },
        "totalNumCreditLines" : "0",
        "enquiryData" : {
          "name" : "MUKESH AMBANI",
          "dob" : "Tue Mar 27 00:00:00 IST 2001",
          "gender" : "Male"
        },
        "disparateCredentials" : {
          "kycIDList" : [ ],
          "addressList" : [ ],
          "phoneList" : [ ],
          "dobList" : [ ],
          "nameList" : [ ],
          "emailList" : [ ]
        },
        "unSecSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        }
      },
      "reject" : [
        {
          "trackingId" : 1555977,
          "bureau" : "CIBIL",
          "product" : "CIR",
          "status" : "ERROR",
          "errorList" : [
            {
              "code" : "E207",
              "description" : "At least one valid id/phone must be present"
            }
          ],
          "warningList" : [
            {
              "code" : "E203",
              "description" : "Phone1 is not valid"
            }
          ]
        }
      ]
    },
    "scoringServiceResponse" : {
      "header" : {
        "institutionId" : "4019",
        "custId" : "56684000115",
        "responseDate" : "25042019 16:12:32",
        "applicationId" : "56684000115"
      },
      "ackId" : "931769",
      "status" : "COMPLETED",
      "scoreData" : {
        "finalScore" : "20",
        "status" : "SUCCESS",
        "scoreCardName" : "TEST BRE 2",
        "scoreValue" : "20",
        "scoreDetails" : {
          "Test C" : {
            "Test A" : {
              "IRP$sApplicantType" : {
                "dField" : "IRP$sApplicantType",
                "FieldName" : "APPLICANT_TYPE",
                "dScore" : 20,
                "weight" : 1,
                "cScore" : 20,
                "expression" : " ( ( IRP$sApplicantType = EXPRESS ) )",
                "value" : {
                  "APPLICANT_TYPE" : "EXPRESS"
                }
              }
            }
          }
        },
        "finalBand" : "",
        "additionalProperties" : {
          
        }
      },
      "scoreTree" : {
        "masterMap" : {
          "Test C" : {
            "Test A" : {
              "IRP$sApplicantType" : {
                "dField" : "IRP$sApplicantType",
                "FieldName" : "APPLICANT_TYPE",
                "dScore" : 20,
                "weight" : 1,
                "cScore" : 20,
                "expression" : " ( ( IRP$sApplicantType = EXPRESS ) )",
                "value" : {
                  "APPLICANT_TYPE" : "EXPRESS"
                }
              }
            }
          }
        },
        "baseOperator" : "",
        "Scores" : [
          {
            "name" : "Test C",
            "score" : 20,
            "Plans" : [
              [
                {
                  "name" : "Test A",
                  "score" : 20,
                  "Fields" : [
                    [
                      {
                        "name" : "IRP$sApplicantType",
                        "score" : 20
                      }
                    ]
                  ]
                }
              ]
            ]
          }
        ],
        "AppScore" : 20,
        "TableID" : 121,
        "SCORECARD_NAME" : "TEST BRE 2",
        "FINAL_SCORE" : 20
      },
      "eligibilityResponse" : {
        "eligibleId" : "78",
        "approvedAmount" : 30000,
        "decision" : "Queue",
        "maxAmount" : 0,
        "minAmount" : 0,
        "dp" : 0,
        "maxTenor" : 0,
        "reMark" : "No eligibility criteria matched",
        "computedAmount" : 0,
        "eligibilityAmount" : 0,
        "cnt" : 0,
        "productsAllowed" : 0,
        "additionalProperties" : {
          
        },
        "additionalFields" : {
          
        }
      },
      "decisionResponse" : {
        "ruleId" : 25,
        "decision" : "Declined",
        "details" : [
          {
            "criteriaID" : 1,
            "ruleName" : "CHECK PAN STATUS",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( PAN_VERIFY_STATUS is FAKE_PAN ) ) ",
            "fieldValues" : {
              "PAN_VERIFY_STATUS" : "NO_RESPONSE"
            }
          },
          {
            "criteriaID" : 3,
            "ruleName" : "BRE 1 ELG AMT > 20K",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( QDE_BRE_ELIGIBILITY_AMOUNT > 20000 ) ) ",
            "fieldValues" : {
              "QDE_BRE_ELIGIBILITY_AMOUNT" : "0"
            }
          },
          {
            "criteriaID" : 6,
            "ruleName" : "CURRENT MOBILE MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_MOBILE_CHANGE is Yes ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_MOBILE_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 9,
            "ruleName" : "CURRENT NAME MISMATCH QUEUE RUL",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( ( 50 <= EXISTING_CURRENT_NAME_PERCENTAGE ) && ( EXISTING_CURRENT_NAME_PERCENTAGE < 100 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 10,
            "ruleName" : "CURENT NAME MISMATCH DECLN RUL",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_NAME_PERCENTAGE < 50 ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 15,
            "ruleName" : "DEBIT CARD TYPE IS SILVER",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CC_TYPE is SILVER ) ) ",
            "fieldValues" : {
              "CC_TYPE" : "null"
            }
          },
          {
            "criteriaID" : 20,
            "ruleName" : "EXISTING NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE < 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE < 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 21,
            "ruleName" : "EXISTING NAME MODIFIED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 22,
            "ruleName" : "EXISTNG NAME MODIFY CREDIT CHK1",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE < 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 23,
            "ruleName" : "EXISTNG NAME MODIFY CREDIT CHK2",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE < 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 25,
            "ruleName" : "EXISTING CURRENT PINCODE CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_PINCODE_CHANGE is Yes ) &&  ( ( APPLICANT_TYPE is EXISTING ) ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_PINCODE_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 26,
            "ruleName" : "EXISTNG FIRST NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 27,
            "ruleName" : "EXISTNG LAST NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( APPLICANT_TYPE is EXISTING ) ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS"
            }
          },
          {
            "criteriaID" : 28,
            "ruleName" : "OTHER KYC CHECK RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( OTP_STATUS is N ) ||  ( ( OTP_STATUS is Y ) ) ) && ( ( LOGIN_USING_KYC is Y ) ) && ( ( OTHER_KYC_CHECK_CIBIL_TEST is Queue ) ) ",
            "fieldValues" : {
              "OTHER_KYC_CHECK_CIBIL_TEST" : "Queue",
              "LOGIN_USING_KYC" : "N",
              "OTP_STATUS" : "N"
            }
          },
          {
            "criteriaID" : 29,
            "ruleName" : "EXISTING-CURRENT ADDR MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CURRENT_ADDRESS_SAME_AS is Others ) ||  ( ( EXISTING_CURRENT_ADDRESS_PERCENTAGE < 100 ) ) ) && ( ( APPLICANT_RESI_SCORE < 70 ) ) ",
            "fieldValues" : {
              "CURRENT_ADDRESS_SAME_AS" : "null",
              "EXISTING_CURRENT_ADDRESS_PERCENTAGE" : "null",
              "APPLICANT_RESI_SCORE" : "null"
            }
          },
          {
            "criteriaID" : 31,
            "ruleName" : "IDFY PAN MATCH APPROVE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_PAN_FACE_MATCH_BAND is green ) ) ",
            "fieldValues" : {
              "IDFY_PAN_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 32,
            "ruleName" : "IDFY PAN MATCH QUEUE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_PAN_FACE_MATCH_BAND is amber ) ) ",
            "fieldValues" : {
              "IDFY_PAN_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 34,
            "ruleName" : "IDFY DL MATCH APPROVE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_DRIVING_LICENSE_FACE_MATCH_BAND is green ) ) ",
            "fieldValues" : {
              "IDFY_DRIVING_LICENSE_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 35,
            "ruleName" : "IDFY DL MATCH QUEUE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_DRIVING_LICENSE_FACE_MATCH_BAND is amber ) ) ",
            "fieldValues" : {
              "IDFY_DRIVING_LICENSE_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 36,
            "ruleName" : "KARZA ID MISMATCH WITH EXISTING",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_ID_TYPE_MATCH_WITH_KARZA is Y ) &&  ( ( EXISTING_ID_NUMBER_MATCH_WITH_KARZA is N ) ) ) && ( ( EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE > 0 ) &&  ( ( EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE < 80 ) ) ) ",
            "fieldValues" : {
              "EXISTING_ID_NUMBER_MATCH_WITH_KARZA" : "null",
              "EXISTING_ID_TYPE_MATCH_WITH_KARZA" : "null",
              "EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 37,
            "ruleName" : "EXISTING & CURENT NAME MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_NAME_PERCENTAGE < 70 ) ) && ( ( EXISTING_ID_NUMBER_MATCH_WITH_KARZA is N ) &&  ( ( EXISTING_DOB_MATCH_WITH_KARZA is N ) ) ) ",
            "fieldValues" : {
              "EXISTING_ID_NUMBER_MATCH_WITH_KARZA" : "null",
              "EXISTING_DOB_MATCH_WITH_KARZA" : "null",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 38,
            "ruleName" : "E-MAIL ID VALIDATED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is SUCCESS ) &&  ( ( EMAIL_ID_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_STATUS" : "N"
            }
          },
          {
            "criteriaID" : 39,
            "ruleName" : "E-MAIL ID VALIDATION SKIP",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is SUCCESS ) &&  ( ( EMAIL_ID_SKIP_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_SKIP_STATUS" : "Y"
            }
          },
          {
            "criteriaID" : 40,
            "ruleName" : "JUNK E-MAIL ID",
            "outcome" : "Declined",
            "remark" : "E-Mail ID does not exist",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is FAILED ) &&  ( ( EMAIL_ID_SKIP_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_SKIP_STATUS" : "Y"
            }
          },
          {
            "criteriaID" : 41,
            "ruleName" : "NEGATIVE AREA CHECK",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IS_NEGATIVE_AREA is Yes ) &&  ( ( APPLICANT_ADDR_CITY_TIER is not 10 ) ) ) ",
            "fieldValues" : {
              "APPLICANT_ADDR_CITY_TIER" : "null",
              "IS_NEGATIVE_AREA" : "No"
            }
          },
          {
            "criteriaID" : 43,
            "ruleName" : "INTERNAL DEDUPE CHECK-LOAN TYPE",
            "outcome" : "Queue",
            "remark" : "SYS: login other product same month - check status",
            "expression" : " ( ( DEDUPE_CUSTOMER_STATUS is Y ) &&  ( ( DEDUPE_LOAN_TYPE is not TW ) ) ) && ( ( ( 0 <= DEDUPE_DECLINE_DAYS_DIFF ) && ( DEDUPE_DECLINE_DAYS_DIFF < 30 ) ) ) ",
            "fieldValues" : {
              "DEDUPE_LOAN_TYPE" : "[LSL, LSL]",
              "DEDUPE_CUSTOMER_STATUS" : "Y",
              "DEDUPE_DECLINE_DAYS_DIFF" : "0"
            }
          },
          {
            "criteriaID" : 44,
            "ruleName" : "EXISTING-CURRENT CITY CHANGED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_CITY_CHANGED is YES ) ||  ( ( EXISTING_CURRENT_CITY_PERCENTAGE < 100 ) ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_CITY_PERCENTAGE" : "null",
              "EXISTING_CURRENT_CITY_CHANGED" : "null"
            }
          },
          {
            "criteriaID" : 48,
            "ruleName" : "DC NAME MATCH WITH APPLICANT",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( NAME_ON_DEBIT_CARD_MATCH_WITH_APPLICANT_NAME_PERCENTAGE < 100 ) ) ",
            "fieldValues" : {
              "NAME_ON_DEBIT_CARD_MATCH_WITH_APPLICANT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 49,
            "ruleName" : "DECLINED CASE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CRO_LATEST_MANUAL_DECISION is Declined ) ) ",
            "fieldValues" : {
              "CRO_LATEST_MANUAL_DECISION" : "null"
            }
          },
          {
            "criteriaID" : 52,
            "ruleName" : "ZERO PRE-APPROVED LOAN AMOUNT",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( APPLICATION_PRE_APPROVED_AMOUNT == 0 ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "APPLICATION_PRE_APPROVED_AMOUNT" : "0"
            }
          },
          {
            "criteriaID" : 54,
            "ruleName" : "IDFY CHECK RESULT",
            "outcome" : "Queue",
            "remark" : "SYS: KYC ID image mismatch. Please check manually before decision",
            "expression" : " ( ( IDFY_CHECK_RESULT_TEST is Queue ) ) ",
            "fieldValues" : {
              "IDFY_CHECK_RESULT_TEST" : "Queue"
            }
          },
          {
            "criteriaID" : 56,
            "ruleName" : "TS SCORE TEST RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( ( 600 <= SOCIAL_SCORE ) && ( SOCIAL_SCORE < 801 ) ) ) ",
            "fieldValues" : {
              "SOCIAL_SCORE" : "null"
            }
          }
        ]
      },
      "derivedFields" : {
        "CUSTOM_FIELDS$TW_TVR" : "true",
        "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
        "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$CC" : "NA",
        "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
        "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
        "POLICY_ID" : 610,
        "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
        "POLICY_NAME" : "LSL POLICY BRE 2",
        "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
        "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
        "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
      },
      "additionalProperties" : {
        
      }
    }
  },
  "applicantComponentResponseList" : [ ],
  "croDecisions" : [
    {
      "amtApproved" : 30000,
      "interestRate" : 0,
      "downPayment" : 0,
      "emi" : 0,
      "tenor" : 2,
      "eligibleAmt" : 0,
      "unUtilizedAmt" : 29400,
      "utilizedAmt" : 16928,
      "decisionUpdateDate" : "2019-04-25T10:44:21.406Z",
      "ltv" : 0,
      "subjectTo" : "kjsdfjk",
      "remark" : "jsdj",
      "ltvMax" : 0,
      "ltvMin" : 0,
      "sobreLtv" : 0,
      "finalAssetPrice" : 0,
      "masterAssetPrice" : 0,
      "totalAssetCost" : 0
    }
  ],
  "negativePincode" : false,
  "applScoreVector" : [
    {
      "fieldName" : "PAN Verification",
      "order" : 4,
      "fieldValue" : "NO_RESPONSE",
      "message" : "NO_RESPONSE",
      "status" : "FAILED",
      "addStability" : 0
    },
    {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "0",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    },
    {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "20",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    }
  ],
  "dedupedApplications" : [
    {
      "refId" : "56684000010",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    },
    {
      "refId" : "1234567820",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    },
    {
      "refId" : "56684000030",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    }
  ],
  "croJustification" : [
    {
      "subjectTo" : "kjsdfjk",
      "remark" : "jsdj",
      "croID" : "HDBFS_CRO1@softcell.com",
      "decisionCase" : "Approved",
      "croJustificationUpdateDate" : "2019-04-25T10:45:03.150Z",
      "croEmpId" : "HDB41732"
    }
  ],
  "subProcesses" : [ ],
  "interimStatusList" : [ ],
  "finalApplicationStatus" : "PENDING",
  "isEditable" : true,
  "multiBREDetails" : {
    "qdeBreInfo" : {
      "dateTime" : "2019-04-25T10:06:54.787Z",
      "multiBREType" : "QDE_DETAILS_BRE",
      "eligibityGridId" : "78",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 15:34:38",
          "applicationId" : "56684000115"
        },
        "ackId" : "931729",
        "eligibilityResponse" : {
          "eligibleId" : "78",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 25,
          "decision" : "Declined"
        },
        "derivedFields" : {
          "CUSTOM_FIELDS$TW_TVR" : "true",
          "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$CC" : "NA",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
          "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
          "POLICY_ID" : 609,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
          "POLICY_NAME" : "LSL POLICY BRE 1",
          "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
          "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "ddeBreInfo" : {
      "dateTime" : "2019-04-25T10:44:21.372Z",
      "multiBREType" : "DDE_DETAILS_BRE",
      "eligibityGridId" : "78",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 16:12:32",
          "applicationId" : "56684000115"
        },
        "ackId" : "931769",
        "eligibilityResponse" : {
          "eligibleId" : "78",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 25,
          "decision" : "Declined"
        },
        "derivedFields" : {
          "CUSTOM_FIELDS$TW_TVR" : "true",
          "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$CC" : "NA",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
          "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
          "POLICY_ID" : 610,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
          "POLICY_NAME" : "LSL POLICY BRE 2",
          "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
          "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "bankingBreInfo" : {
      "dateTime" : "2019-04-25T10:48:36.993Z",
      "multiBREType" : "BANKING_DETAILS_BRE",
      "eligibityGridId" : "58.1",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 16:16:47",
          "applicationId" : "56684000115"
        },
        "ackId" : "931776",
        "eligibilityResponse" : {
          "values" : {
            "APPLICATION_LOAN_AMOUNT" : 30000,
            "DDE_BRE_ELIGIBILITY_AMOUNT" : 0
          },
          "eligibleId" : "58",
          "gridId" : 1,
          "approvedAmount" : 30000,
          "decision" : "Approved",
          "computeDisp" : "( 40000 )",
          "computeLogic" : "( 40000 )",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "bre 2 elg amt > 20k",
          "computedAmount" : 40000,
          "eligibilityAmount" : 40000,
          "cnt" : 0,
          "ruleExucSeq" : 1,
          "gridExpression" : " ( ( DDE_BRE_ELIGIBILITY_AMOUNT >= 20000 ) || ( APPLICATION_LOAN_AMOUNT >= 10000 )  ) ",
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 21,
          "decision" : "Approved"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 3",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 611,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "assetBreInfo" : {
      "dateTime" : "2019-04-25T13:26:33.080Z",
      "multiBREType" : "ASSET_DETAILS_BRE",
      "eligibityGridId" : "57",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000126",
          "responseDate" : "25042019 18:54:43",
          "applicationId" : "56684000126"
        },
        "ackId" : "931954",
        "eligibilityResponse" : {
          "eligibleId" : "57",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 22,
          "decision" : "Queue"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 4_1",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 612,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "schemeBreInfo" : {
      "dateTime" : "2019-04-26T11:45:30.378Z",
      "multiBREType" : "SCHEME_DETAILS_BRE",
      "eligibityGridId" : "66.1",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000136",
          "responseDate" : "26042019 17:13:40",
          "applicationId" : "56684000136"
        },
        "ackId" : "932336",
        "eligibilityResponse" : {
          "values" : {
            "APPLICATION_LOAN_AMOUNT" : 30000,
            "DDE_BRE_ELIGIBILITY_AMOUNT" : 0
          },
          "eligibleId" : "66",
          "gridId" : 1,
          "approvedAmount" : 60,
          "decision" : "Approved",
          "computeDisp" : "( POST_IPA_ASSET_NET_FUNDING_AMOUNT / POST_IPA_ASSET_TOTAL_ASSET_COST * 100 )",
          "computeLogic" : "( GNG_POST_IPA_DETAILS$oPostIpaDetails$dNetFundingAmt / GNG_POST_IPA_DETAILS$oPostIpaDetails$dTotAssCost * 100 )",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "Approved",
          "computedAmount" : 60,
          "eligibilityAmount" : 60,
          "cnt" : 0,
          "ruleExucSeq" : 1,
          "gridExpression" : " ( ( DDE_BRE_ELIGIBILITY_AMOUNT > 0 ) || ( APPLICATION_LOAN_AMOUNT >= 7000 )  ) ",
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 34,
          "decision" : "Approved"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 4_2",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 613,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    }
  },
  "tvrDataList" : [ ],
  "applicantsSubProcess" : [ ],
  "componentModule" : [ ],
  "componentList" : {
    
  },
  "interfaceName" : "GONOGO",
  "createdDate" : "2019-04-26T11:41:00.880Z",
  "createdBy" : "prateek",
  "updatedDate" : "2019-04-26T11:41:00.880Z",
  "updateBy" : "prateek",
  "version" : 2
}, 

{
  "_id" : "566840116960",
  "actionList" : [ ],
  "intrimStatus" : {
    "startTime" : "2019-04-25T10:06:00.439Z",
    "appStart" : "DEFAULT",
    "dedupe" : "DEFAULT1",
    "posidexDedupeStatus" : "DEFAULT",
    "emailStatus" : "DEFAULT",
    "otpStatus" : "COMPLETE",
    "appsStatus" : "COMPLETE",
    "panStatus" : "COMPLETE",
    "aadharStatus" : "UNAUTHORISED",
    "hunterStatus" : "DEFAULT",
    "mbStatus" : "COMPLETE",
    "creditVidyaStatus" : "DEFAULT",
    "saathiPullStatus" : "DEFAULT",
    "varScoreStatus" : "COMPLETE",
    "scoreStatus" : "COMPLETE",
    "cibilScore" : "DEFAULT",
    "experianStatus" : "COMPLETE",
    "highmarkStatus" : "COMPLETE",
    "croStatus" : "COMPLETE",
    "awsS3Status" : "DEFAULT",
    "ntcStatus" : "COMPLETE",
    "panModuleResult" : {
      "fieldName" : "PAN Verification",
      "order" : 4,
      "fieldValue" : "NO_RESPONSE",
      "message" : "NO_RESPONSE",
      "status" : "FAILED",
      "addStability" : 0
    },
    "cibilModuleResult" : {
      "fieldName" : "CIBIL Score",
      "order" : 3,
      "fieldValue" : "NO RESPONSE",
      "message" : "No Score",
      "addStability" : 0
    },
    "scoringModuleResult" : {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "20",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    },
    "aadharModuleResult" : {
      "fieldName" : "AADHAR Verification",
      "order" : 7,
      "fieldValue" : "NOT_AUTHORIZED",
      "message" : "NOT_AUTHORIZED",
      "addStability" : 0
    },
    "experianModuleResult" : {
      "fieldName" : "Experian Score",
      "order" : 6,
      "fieldValue" : "-",
      "message" : "BUREAU-ERROR",
      "addStability" : 0
    },
    "chmModuleResult" : {
      "fieldName" : "Highmark Score",
      "order" : 12,
      "fieldValue" : "-",
      "message" : "SUCCESS",
      "addStability" : 0
    },
    "mbModuleResult" : {
      "fieldName" : "MB",
      "order" : 0,
      "status" : "SUCCESS",
      "addStability" : 0
    },
    "additionalProperties" : {
      
    },
    "karzaPanStatus" : "DEFAULT",
    "karzaVoterIdStatus" : "DEFAULT",
    "karzaDlStatus" : "DEFAULT"
  },
  "parentID" : "56684000127",
  "rootID" : "56684000115",
  "productSequenceNumber" : 3,
  "dateTime" : "2019-04-26T11:41:00.846Z",
  "applicationStatus" : "Approved",
  "statusFlag" : true,
  "reInitiateCount" : 0,
  "reappraiseReq" : false,
  "reProcessCount" : 0,
  "applicationRequest" : {
    "_id" : "56684000136",
    "header" : {
      "applicationId" : "",
      "institutionId" : "4019",
      "sourceId" : "GONOGO_HDBFS",
      "applicationSource" : "WEB 4.02.01",
      "requestType" : "application/json",
      "dateTime" : "2019-04-26T11:41:00.846Z",
      "dsaId" : "HDBFS_DSA1@softcell.com",
      "croId" : "STP",
      "dealerId" : "56684",
      "product" : "LSL",
      "userName" : "CHDBSDSA1",
      "userRole" : "",
      "applicationDate" : "2019-04-25T10:44:10.158Z"
    },
    "request" : {
      "applicant" : {
        "applicantId" : "APPLICANT_1",
        "applicantName" : {
          "firstName" : "MUKESH",
          "middleName" : "",
          "lastName" : "AMBANI"
        },
        "fatherName" : {
          "firstName" : "KJSDFNKJDS"
        },
        "isStaff" : false,
        "isStaffRelated" : false,
        "motherName" : {
          "firstName" : "SKJDFHDSJK"
        },
        "gender" : "Male",
        "dateOfBirth" : "27032001",
        "age" : 18,
        "maritalStatus" : "Single",
        "kyc" : [
          {
            "kycName" : "APPLICANT-PHOTO",
            "kycNumber" : "",
            "documentVerified" : false
          },
          {
            "kycName" : "DRIVING-LICENSE",
            "kycNumber" : "KXJDJHJUDSHSFJ",
            "documentVerified" : false
          },
          {
            "kycName" : "PAN",
            "kycNumber" : "CHMPK6466D",
            "documentVerified" : false
          },
          {
            "kycName" : "INCOME-PROOF1",
            "kycNumber" : "MXHBDCVJHS",
            "documentVerified" : false
          },
          {
            "kycName" : "INCOME-PROOF2",
            "kycNumber" : "JSDFJJHHJ",
            "documentVerified" : false
          },
          {
            "kycName" : "BANK-PASSBOOK",
            "kycNumber" : "",
            "documentVerified" : false
          }
        ],
        "isResidenceAddSameAsAbove" : true,
        "address" : [
          {
            "timeAtAddress" : 0,
            "addressType" : "RESIDENCE",
            "residenceAddressType" : "OWNED-BUNGLOW",
            "monthAtCity" : 26,
            "monthAtAddress" : 13,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeArea" : "",
            "negativeAreaReason" : "",
            "negativeAreaNotApplicableFlag" : true,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "JHDSGJFDSHV",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "distanceFrom" : 0,
            "landMark" : "EJHGDSBDSJ",
            "outOfGeoLimit" : "YES"
          },
          {
            "timeAtAddress" : 0,
            "addressType" : "OFFICE",
            "residenceAddressType" : "",
            "monthAtCity" : 0,
            "monthAtAddress" : 0,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeAreaNotApplicableFlag" : false,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "DZHBJDGHDS",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "line3" : "",
            "distanceFrom" : 0,
            "landMark" : "SDGFHSDJFHJS"
          },
          {
            "timeAtAddress" : 0,
            "addressType" : "PERMANENT",
            "residenceAddressType" : "OWNED-BUNGLOW",
            "monthAtCity" : 26,
            "monthAtAddress" : 13,
            "rentAmount" : 0,
            "yearAtCity" : 0,
            "negativeAreaNotApplicableFlag" : false,
            "latitude" : 0,
            "longitude" : 0,
            "noOfYearsAtResidence" : 0,
            "addressLine1" : "JHDSGJFDSHV",
            "addressLine2" : "",
            "city" : "PUNE",
            "pin" : 411041,
            "state" : "MAHARASHTRA",
            "country" : "India",
            "distanceFrom" : 0,
            "landMark" : "EJHGDSBDSJ"
          }
        ],
        "phone" : [
          {
            "phoneType" : "PERSONAL_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "3487534875",
            "extension" : ""
          },
          {
            "phoneType" : "PERSONAL_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "RESIDENCE_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "3487534875",
            "extension" : ""
          },
          {
            "phoneType" : "RESIDENCE_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "OFFICE_PHONE",
            "areaCode" : "020",
            "countryCode" : "+91",
            "phoneNumber" : "",
            "extension" : ""
          },
          {
            "phoneType" : "OFFICE_MOBILE",
            "areaCode" : "",
            "countryCode" : "+91",
            "phoneNumber" : "9384598345",
            "extension" : ""
          }
        ],
        "email" : [
          {
            "emailType" : "PERSONAL",
            "emailAddress" : "hsgdhg@jd.dj",
            "verified" : false
          },
          {
            "emailType" : "PERMANENT",
            "emailAddress" : "hsgdhg@jd.dj",
            "verified" : false
          },
          {
            "emailType" : "WORK",
            "emailAddress" : "skdjk@js.sj",
            "verified" : false
          }
        ],
        "employment" : [
          {
            "employmentType" : "SELF-EMPLOYED",
            "employmentName" : "Softcell Technologies Limited",
            "timeWithEmployer" : 26,
            "monthlySalary" : 20000,
            "grossSalary" : 0,
            "lastMonthIncome" : [ ],
            "constitution" : "SELF-EMPLOYED",
            "itrAmount" : 0,
            "totalExps" : 0,
            "otherGrossIncome" : 0,
            "employerCatg" : "CATC",
            "retirementAge" : 0,
            "annualIncome" : 0,
            "netMonthlyIncome" : 0
          }
        ],
        "noOfDependents" : 0,
        "noOfEarningMembers" : 0,
        "noOfFamilyMembers" : 0,
        "applicantReferences" : [ ],
        "education" : "GRADUATE",
        "mobileVerified" : false,
        "addharVerified" : false,
        "emailVerified" : false,
        "emailVerificationSkip" : true,
        "emailOtpStatus" : false,
        "isAadhaarDetailsSameAsExisting" : false,
        "bankingDetails" : [
          {
            "accountHolderName" : {
              "firstName" : "kjsdfhdsjfgjs",
              "middleName" : "",
              "lastName" : ""
            },
            "bankName" : "STATE BANK OF HYDERABAD",
            "branchName" : "PUNE NIGADI PIMPRI CHINCHWAD",
            "accountType" : "SAVINGS",
            "accountNumber" : "7485435776373",
            "ifscCode" : "SBHY0020765",
            "salaryAccount" : false,
            "avgBankBalance" : 0,
            "deductedEmiAmt" : 0,
            "mentionAmount" : 0,
            "yearHeld" : 2,
            "bankingType" : "Primary",
            "isSelected" : true,
            "dateTime" : "2019-04-25T10:48:30.380Z",
            "status" : "NOT_SUPPORTED",
            "remarks" : "Bank name not in the list",
            "isBankingRequired" : false,
            "bankingImageDetails" : {
              "breDecision" : "Approved",
              "bankingImageStatus" : "Approved",
              "bankingImageRequired" : true,
              "bankingImageId" : "5cc191148f4c18b90ab08a6a",
              "bankingImageName" : "CROSS_CHEQUE",
              "dateTime" : "2019-04-25T10:48:37.007Z"
            },
            "attemptID" : "1A56684000115"
          }
        ],
        "incomeDetails" : {
          "otherSourceIncomeAmount" : 0,
          "netMonthlyAmt" : 0,
          "grossMonthlyAmt" : 0,
          "otherSrcMnthlyIncmAmt" : 0,
          "totFmlyMnthlyIncmAmt" : 0
        },
        "surrogate" : {
          "additionalProperties" : {
            
          }
        },
        "consentToCall" : false,
        "idfyAnalyticDetails" : {
          
        },
        "bookAndWait" : false,
        "ResiCumOffice" : false,
        "bureauAnalyticDetails" : {
          "bureauApplicantNameMatch" : "100",
          "bureauApplicantDobMatch" : "Matched"
        },
        "bankingAnalyticDetails" : {
          
        },
        "isKarzaKycSkipped" : false,
        "consentToKyc" : true,
        "otherKyc" : false,
        "isDrivingLicenceKarzaEligible" : "Y",
        "isVoterIdKarzaEligible" : "Y",
        "isIdfyEligible" : "Y",
        "promoCode" : "UAT_ALL",
        "ideaOtp" : false
      },
      "application" : {
        "loanType" : "LSL",
        "productID" : "01",
        "loanAmount" : 30000,
        "loanTenor" : 2,
        "loanApr" : 0,
        "emi" : 0,
        "numberOfAdvanceEmi" : 0,
        "dedupeEmiPaid" : 0,
        "dedupeTenor" : 0,
        "marginAmount" : 0,
        "asset" : [
          {
            "assetCtg" : "FITNESS EQUIPMENT",
            "dlrName" : "RAMVEL HOME APLINCS N CMP AVINSI RD",
            "assetMake" : "EVOKE",
            "assetModelMake" : "FITNESS EQUIPMENT",
            "modelNo" : "TREAD MILL",
            "price" : ""
          }
        ],
        "termsConditionAgreement" : false,
        "dndAgrrement" : false,
        "preApprovedAmount" : 0,
        "higherLoanAmtReq" : false,
        "higherLoanAmt" : 0
      },
      "suspiciousActivity" : "No",
      "masterDataInfo" : {
        
      }
    },
    "currentStageId" : "APRV",
    "dealerRank" : 0,
    "alphaNumDealerRank" : "",
    "appMetaData" : {
      "branchV2" : {
        "_id" : "4019_1017",
        "institutionId" : 4019,
        "branchId" : 1017,
        "branchName" : "SALEM-SF",
        "active" : true
      },
      "dsaName" : {
        "firstName" : "HDBFS",
        "lastName" : "DSA"
      },
      "dsaEmailId" : {
        "emailAddress" : "HDBFS_DSA1@softcell.com",
        "verified" : false
      },
      "phone" : {
        "phoneNumber" : "9999999999"
      },
      "sourcingDetails" : {
        "s1" : {
          "_id" : "5ca884e48f4c18f0b204254f",
          "branchId" : "0",
          "makerId" : "HDB69246",
          "authId" : "HDB51988",
          "moduleId" : "LEA",
          "key1" : "SOURCE",
          "key2" : "",
          "value" : "HDB14165",
          "description" : "RAJA SEKHAR G.V.",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2017-07-16T18:30:00.000Z",
          "cgpEndDate" : "2037-07-16T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T09:59:45.989Z",
          "active" : true
        },
        "s2" : [
          {
            "_id" : "5ca884e48f4c18f0b204534e",
            "branchId" : "0",
            "makerId" : "HDB06943",
            "authId" : "HDB37485",
            "moduleId" : "LEA",
            "key1" : "SOURCEID",
            "key2" : "HDB14165",
            "value" : "HDB11311",
            "description" : "HARISH RAO S",
            "status" : "A",
            "moduleFlag" : "0",
            "appFlag" : "0",
            "disableFlag" : "Y",
            "cgpStartDate" : "2015-09-01T18:30:00.000Z",
            "cgpEndDate" : "2025-03-30T18:30:00.000Z",
            "mApplyFlag" : "",
            "institutionId" : "4019",
            "insertDate" : "2019-04-06T10:18:14.606Z",
            "active" : true
          }
        ],
        "s3" : {
          "_id" : "5ca884e48f4c18f0b204bef0",
          "branchId" : "0",
          "makerId" : "MADHAV",
          "authId" : "USER1",
          "moduleId" : "LEA",
          "key1" : "VALIDSRC",
          "key2" : "HDB14165",
          "value" : "HDB13010",
          "description" : "CHANDRA SEKHAR GANDLA",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2012-08-22T18:30:00.000Z",
          "cgpEndDate" : "2025-08-22T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T10:49:45.964Z",
          "active" : true
        },
        "s4" : {
          "_id" : "5ca884e48f4c18f0b2045657",
          "branchId" : "0",
          "makerId" : "HDB55412",
          "authId" : "HDB37485",
          "moduleId" : "LEA",
          "key1" : "SOURCEID",
          "key2" : "HDB13010",
          "value" : "HDB18458",
          "description" : "RAJASHEKAR S",
          "status" : "A",
          "moduleFlag" : "0",
          "appFlag" : "0",
          "disableFlag" : "Y",
          "cgpStartDate" : "2017-01-31T18:30:00.000Z",
          "cgpEndDate" : "2026-11-10T18:30:00.000Z",
          "mApplyFlag" : "",
          "institutionId" : "4019",
          "insertDate" : "2019-04-06T10:19:26.975Z",
          "active" : true
        }
      }
    },
    "applicantType" : "EXPRESS",
    "qdeDecision" : false,
    "appSubStage" : "SCHEME_BRE_A",
    "multiBreType" : "SCHEME_DETAILS_BRE",
    "isManualBre" : false,
    "karzaFlag" : false,
    "surrogateDecision" : false
  },
  "applicantComponentResponse" : {
    "multiBureauJsonRespose" : {
      "header" : {
        "applicationID" : "56684000115",
        "consumerID" : "56684000115",
        "dateOfRequest" : "25042019 15:35:27",
        "responseType" : "RESPONSE"
      },
      "acknowledgmentId" : 3394243,
      "status" : "COMPLETED",
      "finishedList" : [
        {
          "trackingId" : 1555979,
          "bureau" : "HIGHMARK",
          "product" : "BASE V2.0",
          "status" : "SUCCESS",
          "bureauString" : "<BASE-REPORT-FILE><BASE-REPORTS><BASE-REPORT>  <HEADER>    <DATE-OF-REQUEST>25-04-2019 00:00:00</DATE-OF-REQUEST>    <PREPARED-FOR>HDB FINANCIAL SERVICES</PREPARED-FOR>    <PREPARED-FOR-ID>NBF0000153</PREPARED-FOR-ID>    <DATE-OF-ISSUE>25-04-2019</DATE-OF-ISSUE>    <REPORT-ID>HDB 190425CR44387821</REPORT-ID>    <BATCH-ID>6546229190425</BATCH-ID>    <STATUS>SUCCESS</STATUS>  </HEADER>  <REQUEST>    <NAME><![CDATA[MUKESH AMBANI]]></NAME>    <DOB>27-03-2001</DOB>    <AGE-AS-ON/>    <EMAIL-1>hsgdhg@jd.dj</EMAIL-1>    <GENDER>Male</GENDER>    <ADDRESS-1><![CDATA[JHDSGJFDSHV,      PUNE 411041 MH]]></ADDRESS-1>    <PHONE-1>3487534875</PHONE-1>    <BRANCH><![CDATA[1017]]></BRANCH>    <MBR-ID><![CDATA[56684000115]]></MBR-ID>    <CREDIT-INQ-PURPS-TYP>ACCT-ORIG</CREDIT-INQ-PURPS-TYP>    <CREDIT-INQ-PURPS-TYP-DESC>00</CREDIT-INQ-PURPS-TYP-DESC>    <CREDIT-INQUIRY-STAGE>PRE-SCREEN</CREDIT-INQUIRY-STAGE>    <CREDIT-REQ-TYP>INDV</CREDIT-REQ-TYP>    <CREDIT-RPT-TRN-DT-TM>56684000115</CREDIT-RPT-TRN-DT-TM>    <LOS-APP-ID><![CDATA[56684000115]]></LOS-APP-ID>    <LOAN-AMOUNT>30000</LOAN-AMOUNT>  </REQUEST>  <PERSONAL-INFO-VARIATION>    <NAME-VARIATIONS/>    <ADDRESS-VARIATIONS/>    <PAN-VARIATIONS/>    <DRIVING-LICENSE-VARIATIONS/>    <DATE-OF-BIRTH-VARIATIONS/>    <VOTER-ID-VARIATIONS/>    <PASSPORT-VARIATIONS/>    <PHONE-NUMBER-VARIATIONS/>    <RATION-CARD-VARIATIONS/>    <EMAIL-VARIATIONS/>  </PERSONAL-INFO-VARIATION>  <SECONDARY-MATCHES/>  <ACCOUNTS-SUMMARY>    <DERIVED-ATTRIBUTES>      <INQUIRIES-IN-LAST-SIX-MONTHS>0</INQUIRIES-IN-LAST-SIX-MONTHS>      <LENGTH-OF-CREDIT-HISTORY-YEAR>0</LENGTH-OF-CREDIT-HISTORY-YEAR>      <LENGTH-OF-CREDIT-HISTORY-MONTH>0</LENGTH-OF-CREDIT-HISTORY-MONTH>      <AVERAGE-ACCOUNT-AGE-YEAR>0</AVERAGE-ACCOUNT-AGE-YEAR>      <AVERAGE-ACCOUNT-AGE-MONTH>0</AVERAGE-ACCOUNT-AGE-MONTH>      <NEW-ACCOUNTS-IN-LAST-SIX-MONTHS>0</NEW-ACCOUNTS-IN-LAST-SIX-MONTHS>      <NEW-DELINQ-ACCOUNT-IN-LAST-SIX-MONTHS>0</NEW-DELINQ-ACCOUNT-IN-LAST-SIX-MONTHS>    </DERIVED-ATTRIBUTES>    <PRIMARY-ACCOUNTS-SUMMARY>      <PRIMARY-NUMBER-OF-ACCOUNTS>0</PRIMARY-NUMBER-OF-ACCOUNTS>      <PRIMARY-ACTIVE-NUMBER-OF-ACCOUNTS>0</PRIMARY-ACTIVE-NUMBER-OF-ACCOUNTS>      <PRIMARY-OVERDUE-NUMBER-OF-ACCOUNTS>0</PRIMARY-OVERDUE-NUMBER-OF-ACCOUNTS>      <PRIMARY-SECURED-NUMBER-OF-ACCOUNTS>0</PRIMARY-SECURED-NUMBER-OF-ACCOUNTS>      <PRIMARY-UNSECURED-NUMBER-OF-ACCOUNTS>0</PRIMARY-UNSECURED-NUMBER-OF-ACCOUNTS>      <PRIMARY-UNTAGGED-NUMBER-OF-ACCOUNTS>0</PRIMARY-UNTAGGED-NUMBER-OF-ACCOUNTS>      <PRIMARY-CURRENT-BALANCE>0</PRIMARY-CURRENT-BALANCE>      <PRIMARY-SANCTIONED-AMOUNT>0</PRIMARY-SANCTIONED-AMOUNT>      <PRIMARY-DISBURSED-AMOUNT>0</PRIMARY-DISBURSED-AMOUNT>    </PRIMARY-ACCOUNTS-SUMMARY>    <SECONDARY-ACCOUNTS-SUMMARY>      <SECONDARY-NUMBER-OF-ACCOUNTS>0</SECONDARY-NUMBER-OF-ACCOUNTS>      <SECONDARY-ACTIVE-NUMBER-OF-ACCOUNTS>0</SECONDARY-ACTIVE-NUMBER-OF-ACCOUNTS>      <SECONDARY-OVERDUE-NUMBER-OF-ACCOUNTS>0</SECONDARY-OVERDUE-NUMBER-OF-ACCOUNTS>      <SECONDARY-SECURED-NUMBER-OF-ACCOUNTS>0</SECONDARY-SECURED-NUMBER-OF-ACCOUNTS>      <SECONDARY-UNSECURED-NUMBER-OF-ACCOUNTS>0</SECONDARY-UNSECURED-NUMBER-OF-ACCOUNTS>      <SECONDARY-UNTAGGED-NUMBER-OF-ACCOUNTS>0</SECONDARY-UNTAGGED-NUMBER-OF-ACCOUNTS>      <SECONDARY-CURRENT-BALANCE>0</SECONDARY-CURRENT-BALANCE>      <SECONDARY-SANCTIONED-AMOUNT>0</SECONDARY-SANCTIONED-AMOUNT>      <SECONDARY-DISBURSED-AMOUNT>0</SECONDARY-DISBURSED-AMOUNT>    </SECONDARY-ACCOUNTS-SUMMARY>  </ACCOUNTS-SUMMARY>    <SCORES/><PRINTABLE-REPORT><TYPE>HTML/XML</TYPE><FILE-NAME>HDB 190425CR44387821.html</FILE-NAME><CONTENT><![CDATA[<!DOCTYPE html PUBLIC \\\"-//W3C//DTD XHTML 1.0 Transitional//EN\\\" \\\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\\\"><html><head><meta http-equiv=\\\"Content-Type\\\" content=\\\"text/html; charset=UTF-8\\\"><title>Consumer Base Report</title><style type=\\\"text/css\\\">@media print{  table { page-break-after:auto;   -webkit-print-color-adjust:exact;}  thead { display:table-header-group; }  tfoot { display:table-footer-group; }  body\t{\tmargin-top:10px;\tmargin-bottom:10px;\tmargin-right:25px;\tmargin-left:30px;\t}}.infoValueNote {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 500;\tcolor: grey;\tpadding-right: 15px;\tfont-style: normal;}.shading{\tbackground-color: #e6e6ff;\tbackground:#e6e6ff;}.box {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: thin;\tborder-color: #FFFFFF;\tborder-collapse: collapse;\ttext-align: left;\t-moz-box-shadow: 0px 0px 30px #DADADA;\t-webkit-box-shadow: 0px 0px 30px #DADADA;\tbox-shadow: 0px 0px 30px #DADADA;}.box1 {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: 0px;\tborder-collapse: collapse;\ttext-align: left;}.tabStyle {\tbackground: #FFFFFF;\tborder-style: inset;\tborder-width: thin;\tborder-color: black;\tborder-collapse: collapse;}.rowStyle {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: thin;\tborder-color: grey;\tborder-collapse: collapse;}.box1 tr:nt-child(even) {\tbackground-color: white;}.box1 tr:nth-child(odd) {\tbackground-color: #F1F3F5;}.style14 {\tfont-face: segoe ui semibold;\tfont-size: 2px;}.summarytable {\tbackground: #FFFFFF;\tborder-style: solid;\tborder-width: 0px;\tborder-collapse: collapse;\ttext-align: left;\tborder-left: none;\tborder-right: none;}.reportHead {\tfont-family: segoe ui semibold;\tfont-size: 24px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;}.dataHead {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: right;\ttext-indent: 5px;}.mainHeader {\tfont-family: segoe ui semibold;\tfont-size: 16px;\tcolor: #FFFFFF;\tbackground: #0f3f6b;\ttext-align: left;\tfont-weight: 600;\tpadding-bottom: 3px;}.subHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\ttext-align: left;\tborder-width: thin;\tborder-collapse: collapse;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 0px;\tborder-right: 0px;\tborder-top: 0px;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.subHeader1 {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tborder-width: thin;\tborder-collapse: collapse;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 0px;\tborder-right: 0px;\tborder-top: 0px;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.dataHeaderNone {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: center;\ttext-indent: 5px;\twhite-space: nowrap;\theight : 23;\t\tvalign:middle}.subHeader2 {\tfont-family: segoe ui semibold;\tborder-collapse: collapse;\tborder-bottom: 0px;\tborder-left: 1px solid #ffffff;\tborder-right: 0px;\tborder-top: 1px solid #ffffff;\tbackground: #FFFFFF;\ttext-indent: 5px;\tfont-weight: 600;}.dataHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\twhite-space: nowrap;\tpadding-top: 2px;}.dataHeaderScore {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tcolor: #464646;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\twhite-space: nowrap;\tpadding-top: 2px;}.dataValueValue {\tfont-family: segoe ui semibold;\tfont-size: 25px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataValuePerform {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataValuePerform2 {\tborder-collapse: separate;        Color: #464646;        font-family: segoe ui semibold;       font-size: 12px;\tfont-weight: 280;}.dataHeadern {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;\tpadding-top: 2px;}.dataValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\tpadding-left: 7px;\t\tpadding-top: 1px;}.dataAmtValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: right;\tpadding-right: 7px;\t\tpadding-top: 1px;}.dataHeader1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-align: left;\ttext-indent: 5px;}.dataValue1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-align: left;\ttext-indent: 5px;}.mainAccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #FFFFFF;\tbackground: #0f3f6b;\tfont-weight: 600;}.AccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tfont-weight: 600;\ttext-indent: 5px;}.subAccHeader {\tfont-family: segoe ui semibold;\tfont-size: 13px;\tcolor: #0f3f6b;\tbackground: #e6e6ff;\tfont-weight: 600;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\t}.AccValue {\tfont-family: segoe ui semibold;\tfont-size: 14px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;}.AccValue1 {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;}.AccSummaryTab {\tborder-width: thin;\tborder-collapse: collapse;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\tborder-bottom: 0px;\ttext-indent: 5px;}.disclaimerValue {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 500;\tcolor: grey;}.infoValue {\tfont-family: segoe ui semibold;\tfont-size: 12px;\tfont-weight: 500;\tcolor: grey;\tpadding-right: 15px;\tfont-style: normal;}.maroonFields {\tcolor: Maroon;\tfont-family: segoe ui semibold;\tfont-size: 15px;\tfont-weight: 600;}.AccValueComm2 {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;}.AccValue2 {\tfont-family: segoe ui semibold;\tfont-size: 11px;\tfont-weight: 600;\tcolor: #464646;\ttext-indent: 5px;\tborder-width: thin;\tborder-bottom: 1px solid #A7CBE3;\tborder-left: 1px solid #A7CBE3;\tborder-right: 1px solid #A7CBE3;\tborder-top: 1px solid #A7CBE3;\t}.container {\t/* this will give container dimension, because floated child nodes don't give any */\t/* if your child nodes are inline-blocked, then you don't have to set it */\toverflow: auto;}.container .headActive {\t/* float your elements or inline-block them to display side by side */\tfloat: left;\t/* these are height and width dimensions of your header */\theight: 10em;\twidth: 1.5em;\t/* set to hidden so when there's too much vertical text it will be clipped. */\toverflow: hidden;\t/* these are not relevant and are here to better see the elements */\tbackground: #ffe1dc;\tcolor: #be0000;\tmargin-right: 1px;\tfont-family: segoe ui ;\tfont-weight:bold;}.container .headActive .vertActive {\t/* line height should be equal to header width so text will be middle aligned */\tline-height: 1.5em;\t/* setting background may yield better results in IE text clear type rendering */\tbackground: #ffe1dc;\tcolor: #be0000;\tdisplay: block;\t/* this will prevent it from wrapping too much text */\twhite-space: nowrap;\t/* so it stays off the edge */\tpadding-left: 3px;\tfont-family: segoe ui ;\tfont-weight:bold;\t/* CSS3 specific totation CODE */\t/* translate should have the same negative dimension as head height */\ttransform: rotate(-270deg) translate(1em, 0);\ttransform-origin: -5px 30px;\t-moz-transform: rotate(-270deg) translate(1em, 0);\t-moz-transform-origin: -5px 30px;\t-webkit-transform: rotate(-270deg) translate(1em, 0);\t-webkit-transform-origin: -5px 30px;\t-ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}.container .headClosed {\t/* float your elements or inline-block them to display side by side */\tfloat: left;\t/* these are height and width dimensions of your header */\theight: 10em;\twidth: 1.5em;\t/* set to hidden so when there's too much vertical text it will be clipped. */\toverflow: hidden;\t/* these are not relevant and are here to better see the elements */\tbackground: #e1f0be;\tcolor: #415a05;\tmargin-right: 1px;\tfont-family: segoe ui ;\tfont-weight:bold;}.container .headClosed .vertClosed {\t/* line height should be equal to header width so text will be middle aligned */\tline-height: 1.5em;\t/* setting background may yield better results in IE text clear type rendering */\tbackground: #ffe1dc;\tcolor: #415a05;\tdisplay: block;\t/* this will prevent it from wrapping too much text */\twhite-space: nowrap;\t/* so it stays off the edge */\tpadding-left: 3px;\tfont-family: segoe ui ;\tfont-weight:bold;\t/* CSS3 specific totation CODE */\t/* translate should have the same negative dimension as head height */\ttransform: rotate(-270deg) translate(1em, 0);\ttransform-origin: -5px 30px;\t-moz-transform: rotate(-270deg) translate(1em, 0);\t-moz-transform-origin: -5px 30px;\t-webkit-transform: rotate(-270deg) translate(1em, 0);\t-webkit-transform-origin: -5px 30px;\t-ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}</style></head><body style=\\\"font-family: segoe ui semibold, arial, verdana;\\\"><table class=\\\"box\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t<thead>\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"2\\\" valign=\\\"top\\\"><img src=\\\"data:image/gif;base64,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\\\" alt=\\\"CRIF HighMark Credit Information Services Pvt. Ltd.\\\" align=\\\"left\\\" width=\\\"120\\\" height=\\\"80\\\"/></td>\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"120\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"380\\\" valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t<table border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"reportHead\\\">CONSUMER BASE&trade; REPORT <br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHead\\\" align=\\\"right\\\" valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tFor MUKESH AMBANI </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td rowspan=\\\"2\\\" align=\\\"right\\\" valign=\\\"top\\\" width=\\\"350\\\">\t\t\t\t\t\t\t\t\t\t\t\t<table>\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">CHM Ref #:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">HDB 190425CR44387821 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Prepared For:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">HDB FINANCIAL SERVICES </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Application ID:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">56684000115  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Date of Request:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">25-04-2019 00:00:00 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader1\\\">Date of Issue:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue1\\\">25-04-2019 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t<td height=\\\"10\\\">\t\t\t\t\t\t\t\t\t<hr size=\\\"1\\\" style=\\\"color: #C8C8C8;\\\" />\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t\t</thead>\t <tfoot>\t\t<tr>\t\t\t<td>\t\t\t\t<table summary=\\\"\\\" align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t<tbody>\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t<table summary=\\\"\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<hr color=\\\"silver\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC\\\" valign=\\\"top\\\" width=\\\"70\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Disclaimer:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td colspan=\\\"4\\\" class=\\\"disclaimerValue\\\">This document contains proprietary information to CRIF High Mark and may not be used or disclosed to others, except with the written permission of CRIF High Mark. Any paper copy of this document will be considered uncontrolled. If you are not the intended recipient, you are not authorized to read, print, retain, copy, disseminate, distribute, or use this information or any part thereof. PERFORM score provided in this document is joint work of CRIF SPA (Italy) and CRIF High Mark (India).</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td><br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"left\\\" width=\\\"300\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Copyrights reserved\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(c) 2019</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"center\\\" width=\\\"400\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">CRIF High Mark Credit\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation Services Pvt. Ltd</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td color=\\\"#CCCCCC \\\" align=\\\"right\\\" width=\\\"300\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tclass=\\\"disclaimerValue\\\">Company Confidential\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tData</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70\\\"><br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t</td>\t\t\t\t\t\t</tr>\t\t\t\t\t</tbody>\t\t\t\t</table>\t\t\t</td>\t\t</tr>\t\t\t\t\t\t</tfoot>\t\t\t<tbody>\t\t<tr>\t\t\t<td>\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Inquiry Input Information</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table border=\\\"0\\\" width=\\\"1030px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"10px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"110 px\\\" class=\\\"dataHeader\\\">Name:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"270 px\\\" class=\\\"dataValue\\\"> MUKESH AMBANI </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">DOB/Age:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"190 px\\\" class=\\\"dataValue\\\">27-03-2001   </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Gender:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"200 px\\\" class=\\\"dataValue\\\">MALE </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Father:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Spouse:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"100 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Mother:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"120 px\\\" class=\\\"dataValue\\\"> </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\" width=\\\"100 px\\\">Phone\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tNumbers:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"> 3487534875 </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\">ID(s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" valign=\\\"top\\\">Email ID(s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td valign=\\\"top\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\"> hsgdhg@jd.dj </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataValue\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Entity\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tId:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Current\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAddress:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\"> JHDSGJFDSHV,      PUNE 411041 MH </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Other\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAddress:</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcolspan=\\\"5\\\">  </td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr> \t\t\t\t\t\t \t\t\t\t\t\t <tr>\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">CRIF HM Score (s):</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t \t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td class=\\\"dataHeaderNone\\\" align=\\\"center\\\">None</td>\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t                        \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"30px\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Personal Information -\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tVariations</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: These\t\t\t\t\t\t\t\t\tare applicant's personal information variations as contributed\t\t\t\t\t\t\t\t\tby various financial institutions.</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\">\t\t\t\t\t\t\t\t\t<table cellpadding=\\\"2\\\" cellspacing=\\\"4\\\" border=\\\"0px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" align=\\\"left\\\">None</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: All\t\t\t\t\t\t\t\t\t\t\t\tamounts are in INR.</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr></tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Account Summary</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: Current Balance & Disbursed Amount is considered ONLY for ACTIVE accounts.</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\" height=\\\"20\\\"></td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t<td class=\\\"dataHeader\\\" style=\\\"text-align:center\\\">None</td>\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t<td height=\\\"30px\\\"></td>\t\t\t</tr>\t\t\t<tr>\t\t\t<td>\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t</td></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Inquiries (reported for past 24\t\t\t\t\t\t\t\t\t\t\t\tmonths)</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Member Name</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Date of Inquiry</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Purpose</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Ownership Type</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"subHeader\\\">Amount</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"subHeader\\\">Remark</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"30\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Comments</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td>\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\">Description</td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"subHeader\\\" width=\\\"115\\\">Date</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"right\\\" class=\\\"dataValue\\\" width=\\\"115\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t</table>\t\t\t\t\t\t</td>\t\t\t\t\t</tr>\t\t\t\t\t<tr>\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"center\\\" class=\\\"AccHeader\\\">-END OF CONSUMER BASE REPORT-</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr><tr>\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t</tr><tr height=\\\"10\\\">\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<hr color=\\\"silver\\\">\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\twidth=\\\"1020px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td width=\\\"10\\\"></td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class=\\\"mainHeader\\\">Appendix</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"10\\\"></tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"5\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t<table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"\t\t\t\t\t\t\t\t\t\t\t\t\tcellspacing=\\\"0\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tcellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1000px\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"250\\\">Section</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"220\\\">Code</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"480\\\">Description</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSummary</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">Number\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tof Delinquent Accounts</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tIndicates number of accounts that the applicant has\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdefaulted on within the last 6 months</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation - Credit Grantor</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXXX</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tName of grantor undisclosed as credit grantor is\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdifferent from inquiring institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tInformation - Account #</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">xxxx</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tAccount Number undisclosed as credit grantor is\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdifferent from inquiring institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXX</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Data\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tnot reported by institution</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">&nbsp;&nbsp;&nbsp;&nbsp;-</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Not applicable</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">STD</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as STANDARD Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SUB</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as SUB-STANDARD Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">DBT</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as DOUBTFUL Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">LOS</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as LOSS Asset</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tHistory / Asset Classification</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SMA</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tReported as SPECIAL MENTION</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tScore has reckoned from credit history, pursuit of new credit, payment history, type of credit in &nbsp;&nbsp;use and outstanding debt.</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<!--<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Score of \\\"0\\\" is no hit.</td> -->\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t<tr>\t\t\t\t\t\t\t\t\t\t\t\t<td height=\\\"20\\\"></td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t</table>\t\t\t\t\t\t\t\t\t\t\t\t</td>\t\t\t\t\t\t\t\t\t\t\t</tr>\t\t\t\t\t\t\t</tbody>\t\t\t\t\t\t\t\t\t\t\t\t\t</table></body></html>]]></CONTENT></PRINTABLE-REPORT></BASE-REPORT></BASE-REPORTS></BASE-REPORT-FILE>",
          "pdfReport" : "BinData(0,\"JVBERi0xLjQKJcfl9OXwCjEgMCBvYmoKmore8612bytes+application/pd\")",
          "responseJsonObject" : {
            "baseReports" : {
              "baseReport" : {
                "request" : {
                  "loanAmount" : "30000",
                  "creditRequestType" : "INDV",
                  "creditInquiryStage" : "PRE-SCREEN",
                  "address1" : "JHDSGJFDSHV,      PUNE 411041 MH",
                  "creditInquiryPurposeType" : "ACCT-ORIG",
                  "phone1" : "3487534875",
                  "email1" : "hsgdhg@jd.dj",
                  "creditInquiryPurposeTypeDescription" : "00",
                  "name" : "MUKESH AMBANI",
                  "dob" : "27-03-2001",
                  "creditReportTransectionDatetime" : "56684000115",
                  "branch" : "1017",
                  "gender" : "Male",
                  "memberId" : "56684000115",
                  "losApplicationId" : "56684000115"
                },
                "printableReport" : {
                  "content" : "<!DOCTYPE html PUBLIC \\\"-//W3C//DTD XHTML 1.0 Transitional//EN\\\" \\\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\\\"><html><head><meta http-equiv=\\\"Content-Type\\\" content=\\\"text/html; charset=UTF-8\\\"><title>Consumer Base Report</title><style type=\\\"text/css\\\">@media print{  table { page-break-after:auto;   -webkit-print-color-adjust:exact;}  thead { display:table-header-group; }  tfoot { display:table-footer-group; }  body { margin-top:10px; margin-bottom:10px; margin-right:25px; margin-left:30px; }}.infoValueNote { font-family: segoe ui semibold; font-size: 11px; font-weight: 500; color: grey; padding-right: 15px; font-style: normal;}.shading{ background-color: #e6e6ff; background:#e6e6ff;}.box { background: #FFFFFF; border-style: solid; border-width: thin; border-color: #FFFFFF; border-collapse: collapse; text-align: left; -moz-box-shadow: 0px 0px 30px #DADADA; -webkit-box-shadow: 0px 0px 30px #DADADA; box-shadow: 0px 0px 30px #DADADA;}.box1 { background: #FFFFFF; border-style: solid; border-width: 0px; border-collapse: collapse; text-align: left;}.tabStyle { background: #FFFFFF; border-style: inset; border-width: thin; border-color: black; border-collapse: collapse;}.rowStyle { background: #FFFFFF; border-style: solid; border-width: thin; border-color: grey; border-collapse: collapse;}.box1 tr:nt-child(even) { background-color: white;}.box1 tr:nth-child(odd) { background-color: #F1F3F5;}.style14 { font-face: segoe ui semibold; font-size: 2px;}.summarytable { background: #FFFFFF; border-style: solid; border-width: 0px; border-collapse: collapse; text-align: left; border-left: none; border-right: none;}.reportHead { font-family: segoe ui semibold; font-size: 24px; color: #0f3f6b; font-weight: 600; text-align: left;}.dataHead { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: right; text-indent: 5px;}.mainHeader { font-family: segoe ui semibold; font-size: 16px; color: #FFFFFF; background: #0f3f6b; text-align: left; font-weight: 600; padding-bottom: 3px;}.subHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; text-align: left; border-width: thin; border-collapse: collapse; border-bottom: 1px solid #A7CBE3; border-left: 0px; border-right: 0px; border-top: 0px; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.subHeader1 { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; border-width: thin; border-collapse: collapse; border-bottom: 1px solid #A7CBE3; border-left: 0px; border-right: 0px; border-top: 0px; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.dataHeaderNone { font-family: segoe ui semibold; font-size: 14px; color: #0f3f6b; font-weight: 600; text-align: center; text-indent: 5px; white-space: nowrap; height : 23;  valign:middle}.subHeader2 { font-family: segoe ui semibold; border-collapse: collapse; border-bottom: 0px; border-left: 1px solid #ffffff; border-right: 0px; border-top: 1px solid #ffffff; background: #FFFFFF; text-indent: 5px; font-weight: 600;}.dataHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px; white-space: nowrap; padding-top: 2px;}.dataHeaderScore { font-family: segoe ui semibold; font-size: 12px; color: #464646; font-weight: 600; text-align: left; text-indent: 5px; white-space: nowrap; padding-top: 2px;}.dataValueValue { font-family: segoe ui semibold; font-size: 25px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataValuePerform { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataValuePerform2 { border-collapse: separate;        Color: #464646;        font-family: segoe ui semibold;       font-size: 12px; font-weight: 280;}.dataHeadern { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px; padding-top: 2px;}.dataValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-align: left; padding-left: 7px;  padding-top: 1px;}.dataAmtValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-align: right; padding-right: 7px;  padding-top: 1px;}.dataHeader1 { font-family: segoe ui semibold; font-size: 12px; color: #0f3f6b; font-weight: 600; text-align: left; text-indent: 5px;}.dataValue1 { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-align: left; text-indent: 5px;}.mainAccHeader { font-family: segoe ui semibold; font-size: 13px; color: #FFFFFF; background: #0f3f6b; font-weight: 600;}.AccHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; font-weight: 600; text-indent: 5px;}.subAccHeader { font-family: segoe ui semibold; font-size: 13px; color: #0f3f6b; background: #e6e6ff; font-weight: 600; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; }.AccValue { font-family: segoe ui semibold; font-size: 14px; font-weight: 600; color: #464646; text-indent: 5px;}.AccValue1 { font-family: segoe ui semibold; font-size: 12px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3;}.AccSummaryTab { border-width: thin; border-collapse: collapse; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; border-bottom: 0px; text-indent: 5px;}.disclaimerValue { font-family: segoe ui semibold; font-size: 12px; font-weight: 500; color: grey;}.infoValue { font-family: segoe ui semibold; font-size: 12px; font-weight: 500; color: grey; padding-right: 15px; font-style: normal;}.maroonFields { color: Maroon; font-family: segoe ui semibold; font-size: 15px; font-weight: 600;}.AccValueComm2 { font-family: segoe ui semibold; font-size: 11px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3;}.AccValue2 { font-family: segoe ui semibold; font-size: 11px; font-weight: 600; color: #464646; text-indent: 5px; border-width: thin; border-bottom: 1px solid #A7CBE3; border-left: 1px solid #A7CBE3; border-right: 1px solid #A7CBE3; border-top: 1px solid #A7CBE3; }.container { /* this will give container dimension, because floated child nodes don't give any */ /* if your child nodes are inline-blocked, then you don't have to set it */ overflow: auto;}.container .headActive { /* float your elements or inline-block them to display side by side */ float: left; /* these are height and width dimensions of your header */ height: 10em; width: 1.5em; /* set to hidden so when there's too much vertical text it will be clipped. */ overflow: hidden; /* these are not relevant and are here to better see the elements */ background: #ffe1dc; color: #be0000; margin-right: 1px; font-family: segoe ui ; font-weight:bold;}.container .headActive .vertActive { /* line height should be equal to header width so text will be middle aligned */ line-height: 1.5em; /* setting background may yield better results in IE text clear type rendering */ background: #ffe1dc; color: #be0000; display: block; /* this will prevent it from wrapping too much text */ white-space: nowrap; /* so it stays off the edge */ padding-left: 3px; font-family: segoe ui ; font-weight:bold; /* CSS3 specific totation CODE */ /* translate should have the same negative dimension as head height */ transform: rotate(-270deg) translate(1em, 0); transform-origin: -5px 30px; -moz-transform: rotate(-270deg) translate(1em, 0); -moz-transform-origin: -5px 30px; -webkit-transform: rotate(-270deg) translate(1em, 0); -webkit-transform-origin: -5px 30px; -ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}.container .headClosed { /* float your elements or inline-block them to display side by side */ float: left; /* these are height and width dimensions of your header */ height: 10em; width: 1.5em; /* set to hidden so when there's too much vertical text it will be clipped. */ overflow: hidden; /* these are not relevant and are here to better see the elements */ background: #e1f0be; color: #415a05; margin-right: 1px; font-family: segoe ui ; font-weight:bold;}.container .headClosed .vertClosed { /* line height should be equal to header width so text will be middle aligned */ line-height: 1.5em; /* setting background may yield better results in IE text clear type rendering */ background: #ffe1dc; color: #415a05; display: block; /* this will prevent it from wrapping too much text */ white-space: nowrap; /* so it stays off the edge */ padding-left: 3px; font-family: segoe ui ; font-weight:bold; /* CSS3 specific totation CODE */ /* translate should have the same negative dimension as head height */ transform: rotate(-270deg) translate(1em, 0); transform-origin: -5px 30px; -moz-transform: rotate(-270deg) translate(1em, 0); -moz-transform-origin: -5px 30px; -webkit-transform: rotate(-270deg) translate(1em, 0); -webkit-transform-origin: -5px 30px; -ms-transform-origin:none;-ms-transform:none;-ms-writing-mode:tb-rl;*writing-mode:tb-rl;}</style></head><body style=\\\"font-family: segoe ui semibold, arial, verdana;\\\"><table class=\\\"box\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1020px\\\"> <thead> <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr height=\\\"10\\\">            <td></td>           </tr>           <tr>            <td colspan=\\\"2\\\" valign=\\\"top\\\"><img src=\\\"data:image/gif;base64,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\\\" alt=\\\"CRIF HighMark Credit Information Services Pvt. Ltd.\\\" align=\\\"left\\\" width=\\\"120\\\" height=\\\"80\\\"/></td>            <td width=\\\"120\\\"></td>            <td align=\\\"left\\\" width=\\\"380\\\" valign=\\\"top\\\">            <table border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">             <tbody>              <tr>               <td align=\\\"center\\\" class=\\\"reportHead\\\">CONSUMER BASE&trade; REPORT <br>               </td>              </tr>              <tr valign=\\\"top\\\">               <td class=\\\"dataHead\\\" align=\\\"right\\\" valign=\\\"top\\\">               For MUKESH AMBANI </td>              </tr>             </tbody>            </table>            </td>            <td width=\\\"70\\\"></td>            <td rowspan=\\\"2\\\" align=\\\"right\\\" valign=\\\"top\\\" width=\\\"350\\\">            <table>             <tbody>              <tr>               <td class=\\\"dataHeader1\\\">CHM Ref #:</td>               <td class=\\\"dataValue1\\\">HDB 190425CR44387821 </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Prepared For:</td>               <td class=\\\"dataValue1\\\">HDB FINANCIAL SERVICES </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Application ID:</td>               <td class=\\\"dataValue1\\\">56684000115  </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Date of Request:</td>               <td class=\\\"dataValue1\\\">25-04-2019 00:00:00 </td>              </tr>              <tr>               <td class=\\\"dataHeader1\\\">Date of Issue:</td>               <td class=\\\"dataValue1\\\">25-04-2019 </td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr><tr>         <td height=\\\"10\\\">         <hr size=\\\"1\\\" style=\\\"color: #C8C8C8;\\\" />         </td>        </tr>       </tbody>      </table>      </td>     </tr>      </thead>  <tfoot>  <tr>   <td>    <table summary=\\\"\\\" align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">     <tbody>      <tr>       <td>        <table summary=\\\"\\\" border=\\\"0\\\" width=\\\"1020px\\\">                   <tbody>                    <tr height=\\\"10\\\">                     <td colspan=\\\"5\\\">                     <hr color=\\\"silver\\\">                     </td>                    </tr>                    <tr>                     <td color=\\\"#CCCCCC\\\" valign=\\\"top\\\" width=\\\"70\\\"                      class=\\\"disclaimerValue\\\">Disclaimer:</td>                     <td colspan=\\\"4\\\" class=\\\"disclaimerValue\\\">This document contains proprietary information to CRIF High Mark and may not be used or disclosed to others, except with the written permission of CRIF High Mark. Any paper copy of this document will be considered uncontrolled. If you are not the intended recipient, you are not authorized to read, print, retain, copy, disseminate, distribute, or use this information or any part thereof. PERFORM score provided in this document is joint work of CRIF SPA (Italy) and CRIF High Mark (India).</td>                    </tr>                    <tr>                     <td><br>                     <br>                     </td>                     <td color=\\\"#CCCCCC \\\" align=\\\"left\\\" width=\\\"300\\\"                      class=\\\"disclaimerValue\\\">Copyrights reserved                     (c) 2019</td>                     <td color=\\\"#CCCCCC \\\" align=\\\"center\\\" width=\\\"400\\\"                      class=\\\"disclaimerValue\\\">CRIF High Mark Credit                     Information Services Pvt. Ltd</td>                     <td color=\\\"#CCCCCC \\\" align=\\\"right\\\" width=\\\"300\\\"                      class=\\\"disclaimerValue\\\">Company Confidential                     Data</td>                     <td width=\\\"70\\\"><br>                     <br>                     </td>                    </tr>                   </tbody>                  </table>       </td>      </tr>     </tbody>    </table>   </td>  </tr>      </tfoot>   <tbody>  <tr>   <td>   <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">    <tbody>          <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"       width=\\\"1020px\\\">       <tbody>                <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Inquiry Input Information</td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1030px\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" width=\\\"1030px\\\">          <tbody>           <tr>            <td>            <table border=\\\"0\\\" width=\\\"1030px\\\">             <tbody>              <tr>               <td height=\\\"10px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"110 px\\\" class=\\\"dataHeader\\\">Name:</td>               <td align=\\\"left\\\" width=\\\"270 px\\\" class=\\\"dataValue\\\"> MUKESH AMBANI </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">DOB/Age:</td>               <td width=\\\"190 px\\\" class=\\\"dataValue\\\">27-03-2001   </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Gender:</td>               <td width=\\\"200 px\\\" class=\\\"dataValue\\\">MALE </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Father:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"> </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Spouse:</td>               <td width=\\\"100 px\\\" class=\\\"dataValue\\\"> </td>               <td width=\\\"70 px\\\" class=\\\"dataHeader\\\">Mother:</td>               <td width=\\\"120 px\\\" class=\\\"dataValue\\\"> </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\" width=\\\"100 px\\\">Phone               Numbers:</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"> 3487534875 </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>               </table>               </td>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\">ID(s):</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>                <tr>                 <td class=\\\"dataValue\\\"></td>                </tr>               </table>               </td>               <td class=\\\"dataHeader\\\" valign=\\\"top\\\">Email ID(s):</td>               <td valign=\\\"top\\\">               <table width=\\\"200px\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">                <tr>                 <td class=\\\"dataValue\\\"> hsgdhg@jd.dj </td>                </tr>                <tr>                 <td class=\\\"dataValue\\\">  </td>                </tr>               </table>               </td>              </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Entity               Id:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\">  </td>                             </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Current               Address:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\"> JHDSGJFDSHV,      PUNE 411041 MH </td>                             </tr>              <tr>               <td height=\\\"5px\\\"></td>              </tr>              <tr>               <td align=\\\"left\\\" width=\\\"100 px\\\" class=\\\"dataHeader\\\">Other               Address:</td>               <td align=\\\"left\\\" width=\\\"200 px\\\" class=\\\"dataValue\\\"                colspan=\\\"5\\\">  </td>               </td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>               <tr>        <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr>            <td>             <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"              width=\\\"1020px\\\">              <tbody>               <tr height=\\\"20\\\">                <td width=\\\"10\\\"></td>                <td class=\\\"mainHeader\\\">CRIF HM Score (s):</td>               </tr>              </tbody>             </table>            </td>           </tr>          </tbody>         </table>        </td>       </tr>               <tr>       <td class=\\\"dataHeaderNone\\\" align=\\\"center\\\">None</td>         </tr>                                                    <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\"       width=\\\"1020px\\\">       <tbody>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>           <tr>            <td height=\\\"30px\\\"></td>           </tr>           <tr>            <td>            <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"             width=\\\"1020px\\\">             <tbody>              <tr height=\\\"20\\\">               <td width=\\\"10\\\"></td>               <td class=\\\"mainHeader\\\">Personal Information -               Variations</td>              </tr>             </tbody>            </table>            </td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"20\\\">         <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: These         are applicant's personal information variations as contributed         by various financial institutions.</td>        </tr>        <tr>         <td align=\\\"center\\\">         <table cellpadding=\\\"2\\\" cellspacing=\\\"4\\\" border=\\\"0px\\\">          <tbody>                      <td class=\\\"dataHeader\\\" align=\\\"left\\\">None</td>                     </tbody>         </table>         </td>        </tr>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\">          <tbody>           <tr height=\\\"10\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\"></td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: All            amounts are in INR.</td>           </tr>           <tr></tr>           <tr>            <td>            <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"             width=\\\"1020px\\\">             <tbody>              <tr height=\\\"20\\\">               <td width=\\\"10\\\"></td>               <td class=\\\"mainHeader\\\">Account Summary</td>              </tr>             </tbody>            </table>            </td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\">Tip: Current Balance & Disbursed Amount is considered ONLY for ACTIVE accounts.</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr>         <td align=\\\"right\\\" bgcolor=\\\"#FFFFFF\\\" class=\\\"infoValue\\\" height=\\\"20\\\"></td>        </tr>        <tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1020px\\\">          <tbody>                 <tr>       <td class=\\\"dataHeader\\\" style=\\\"text-align:center\\\">None</td>       </tr>                 </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>          <tr>    <td height=\\\"30px\\\"></td>   </tr>   <tr>   <td>         <tr>      <td>          <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>                                          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"10\\\"></td>     </tr>     </td></tr>               <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr height=\\\"10\\\"></tr>        <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"          width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Inquiries (reported for past 24            months)</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"10\\\"></tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>           <tr height=\\\"20\\\">            <td align=\\\"center\\\" class=\\\"subHeader\\\">Member Name</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Date of Inquiry</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Purpose</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Ownership Type</td>            <td align=\\\"right\\\" class=\\\"subHeader\\\">Amount</td>            <td align=\\\"center\\\" class=\\\"subHeader\\\">Remark</td>           </tr>                     </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"30\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr height=\\\"10\\\"></tr>        <tr>         <td>         <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"          width=\\\"1020px\\\">          <tbody>           <tr height=\\\"20\\\">            <td width=\\\"10\\\"></td>            <td class=\\\"mainHeader\\\">Comments</td>           </tr>          </tbody>         </table>         </td>        </tr>        <tr height=\\\"10\\\"></tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"5\\\"></td>     </tr>     <tr>      <td>      <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\" cellspacing=\\\"0\\\">       <tbody>        <tr>         <td>         <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\" width=\\\"1000px\\\">          <tbody>           <tr height=\\\"20\\\">            <td align=\\\"left\\\" class=\\\"subHeader\\\">Description</td>            <td align=\\\"right\\\" class=\\\"subHeader\\\" width=\\\"115\\\">Date</td>           </tr>           <tr height=\\\"20\\\">            <td align=\\\"left\\\" class=\\\"dataValue\\\"></td>            <td align=\\\"right\\\" class=\\\"dataValue\\\" width=\\\"115\\\"></td>           </tr>          </tbody>         </table>         </td>        </tr>       </tbody>      </table>      </td>     </tr>     <tr>      <td height=\\\"10\\\"></td>     </tr><tr>         <td>         <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"          cellspacing=\\\"0\\\">          <tbody>           <tr>            <td>            <table width=\\\"1000px\\\">             <tbody>              <tr>               <td align=\\\"center\\\" class=\\\"AccHeader\\\">-END OF CONSUMER BASE REPORT-</td>              </tr>             </tbody>            </table>            </td>           </tr><tr>           <td height=\\\"10\\\"></td>          </tr><tr height=\\\"10\\\">           <td>            <hr color=\\\"silver\\\">           </td>          </tr>                      <tr>            <td>            <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"             cellspacing=\\\"0\\\">             <tbody>              <tr height=\\\"10\\\"></tr>              <tr>               <td>               <table align=\\\"center\\\" bgcolor=\\\"#0f3f6b\\\" border=\\\"0\\\"                width=\\\"1020px\\\">                <tbody>                 <tr height=\\\"20\\\">                  <td width=\\\"10\\\"></td>                  <td class=\\\"mainHeader\\\">Appendix</td>                 </tr>                </tbody>               </table>               </td>              </tr>              <tr height=\\\"10\\\"></tr>             </tbody>            </table>            </td>           </tr>           <tr>            <td height=\\\"5\\\"></td>           </tr>           <tr>            <td>            <table align=\\\"center\\\" border=\\\"0\\\" cellpadding=\\\"0\\\"             cellspacing=\\\"0\\\">             <tbody>              <tr>               <td>               <table class=\\\"box1\\\" align=\\\"center\\\" border=\\\"0px\\\"                cellpadding=\\\"0\\\" cellspacing=\\\"0\\\" width=\\\"1000px\\\">                <tbody>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"250\\\">Section</td>                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"220\\\">Code</td>                  <td align=\\\"left\\\" class=\\\"subHeader\\\" width=\\\"480\\\">Description</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Summary</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">Number                  of Delinquent Accounts</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Indicates number of accounts that the applicant has                  defaulted on within the last 6 months</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Information - Credit Grantor</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXXX</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Name of grantor undisclosed as credit grantor is                  different from inquiring institution</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Account                  Information - Account #</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">xxxx</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Account Number undisclosed as credit grantor is                  different from inquiring institution</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">XXX</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Data                  not reported by institution</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">&nbsp;&nbsp;&nbsp;&nbsp;-</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Not applicable</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">STD</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as STANDARD Asset</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SUB</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as SUB-STANDARD Asset</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">DBT</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as DOUBTFUL Asset</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">LOS</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as LOSS Asset</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">Payment                  History / Asset Classification</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">SMA</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Account                   Reported as SPECIAL MENTION</td>                 </tr>                 <tr height=\\\"20\\\">                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">                  Score has reckoned from credit history, pursuit of new credit, payment history, type of credit in &nbsp;&nbsp;use and outstanding debt.</td>                 </tr>                 <tr height=\\\"20\\\"  bgcolor=\\\"#F1F3F5\\\">                  <!--<td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"250\\\">CRIF HIGHMARK SCORE (S)</td>                  <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"220\\\">PERFORM-Consumer</td>                   <td align=\\\"left\\\" class=\\\"dataValue1\\\" width=\\\"480\\\">Score of \\\"0\\\" is no hit.</td> -->                 </tr>                </tbody>               </table>               </td>              </tr>             </tbody>            </table>            </td>           </tr>           <tr>            <td height=\\\"20\\\"></td>           </tr>                        </tbody>            </table>            </td>           </tr>       </tbody>             </table></body></html>",
                  "fileName" : "HDB 190425CR44387821.html"
                },
                "personalInfoVariation" : {
                  
                },
                "header" : {
                  "status" : "SUCCESS",
                  "dateOfRequest" : "25-04-2019 00:00:00",
                  "batchId" : "6546229190425",
                  "reportId" : "HDB 190425CR44387821",
                  "dateOfIssue" : "25-04-2019",
                  "preparedForId" : "NBF0000153",
                  "preparedFor" : "HDB FINANCIAL SERVICES"
                },
                "accountSummary" : {
                  "drivedAttributes" : {
                    "lengthOfCreditHistoryYear" : "0",
                    "inquiriesInLastSixMonth" : "0",
                    "newAccountInLastSixMonths" : "0",
                    "averageAccountAgeYear" : "0",
                    "averageAccountAgeMonth" : "0",
                    "newDlinqAccountInLastSixMonths" : "0",
                    "lengthOfCreditHistoryMonth" : "0"
                  },
                  "secondaryAccountSummary" : {
                    "secondaryUntaggedNumberOfAccounts" : "0",
                    "secondaryNumberOfAccounts" : "0",
                    "secondarySanctionedAmount" : "0",
                    "secondarySecuredNumberOfAccounts" : "0",
                    "secondaryActiveNumberOfAccounts" : "0",
                    "secondaryUnsecuredNumberOfAccounts" : "0",
                    "secondaryCurrentBalance" : "0",
                    "secondaryOverdueNumberOfAccounts" : "0",
                    "secondaryDisbursedAmount" : "0"
                  },
                  "primaryAccountsSummary" : {
                    "primaryUnsecuredNumberOfAccounts" : "0",
                    "primaryOverdueNumberOfAccounts" : "0",
                    "primaryCurrentBalance" : "0",
                    "primaryDisbursedAmount" : "0",
                    "primarySanctionedAmount" : "0",
                    "primaryActiveNumberOfAccounts" : "0",
                    "primaryUntaggedNumberOfAccounts" : "0",
                    "primaryNumberOfAccounts" : "0",
                    "primarySecuredNumberOfAccounts" : "0"
                  }
                }
              }
            }
          }
        },
        {
          "trackingId" : 1555978,
          "bureau" : "EXPERIAN",
          "product" : "CIR",
          "status" : "BUREAU-ERROR",
          "bureauString" : "<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\" standalone=\\\"yes\\\"?> <INProfileResponse>     <Header>         <SystemCode>0</SystemCode>         <MessageText></MessageText>         <ReportDate>20190425</ReportDate>         <ReportTime>153443</ReportTime>     </Header>     <UserMessage>         <UserMessageText>SYS100007(Invalid Enquiry reason/ Search Type)</UserMessageText>     </UserMessage>     <CreditProfileHeader>         <Enquiry_Username></Enquiry_Username>         <ReportDate></ReportDate>         <ReportTime></ReportTime>         <Version>V2.4</Version>         <ReportNumber></ReportNumber>         <Subscriber></Subscriber>         <Subscriber_Name>HDB Financial Services Limited</Subscriber_Name>     </CreditProfileHeader>     <Current_Application>         <Current_Application_Details>             <Enquiry_Reason>00</Enquiry_Reason>             <Finance_Purpose></Finance_Purpose>             <Amount_Financed>30000</Amount_Financed>             <Duration_Of_Agreement>0</Duration_Of_Agreement>             <Current_Applicant_Details>                 <Last_Name>AMBANI</Last_Name>                 <First_Name>MUKESH</First_Name>                 <Middle_Name1></Middle_Name1>                 <Middle_Name2></Middle_Name2>                 <Middle_Name3></Middle_Name3>                 <Gender_Code>2</Gender_Code>                 <IncomeTaxPan></IncomeTaxPan>                 <PAN_Issue_Date></PAN_Issue_Date>                 <PAN_Expiration_Date></PAN_Expiration_Date>                 <Passport_Number></Passport_Number>                 <Passport_Issue_Date></Passport_Issue_Date>                 <Passport_Expiration_Date></Passport_Expiration_Date>                 <Voter_s_Identity_Card></Voter_s_Identity_Card>                 <Voter_ID_Issue_Date></Voter_ID_Issue_Date>                 <Voter_ID_Expiration_Date></Voter_ID_Expiration_Date>                 <Driver_License_Number></Driver_License_Number>                 <Driver_License_Issue_Date></Driver_License_Issue_Date>                 <Driver_License_Expiration_Date></Driver_License_Expiration_Date>                 <Ration_Card_Number></Ration_Card_Number>                 <Ration_Card_Issue_Date></Ration_Card_Issue_Date>                 <Ration_Card_Expiration_Date></Ration_Card_Expiration_Date>                 <Universal_ID_Number></Universal_ID_Number>                 <Universal_ID_Issue_Date></Universal_ID_Issue_Date>                 <Universal_ID_Expiration_Date></Universal_ID_Expiration_Date>                 <Date_Of_Birth_Applicant>20010327</Date_Of_Birth_Applicant>                 <Telephone_Number_Applicant_1st>3487534875</Telephone_Number_Applicant_1st>                 <Telephone_Extension></Telephone_Extension>                 <Telephone_Type>01</Telephone_Type>                 <MobilePhoneNumber></MobilePhoneNumber>                 <EMailId>hsgdhg@jd.dj</EMailId>             </Current_Applicant_Details>             <Current_Other_Details>                 <Income></Income>                 <Marital_Status>1</Marital_Status>                 <Employment_Status></Employment_Status>                 <Time_with_Employer></Time_with_Employer>                 <Number_of_Major_Credit_Card_Held></Number_of_Major_Credit_Card_Held>             </Current_Other_Details>             <Current_Applicant_Address_Details>                 <FlatNoPlotNoHouseNo>JHDSGJFDSHV,</FlatNoPlotNoHouseNo>                 <BldgNoSocietyName></BldgNoSocietyName>                 <RoadNoNameAreaLocality></RoadNoNameAreaLocality>                 <City>PUNE</City>                 <Landmark></Landmark>                 <State>27</State>                 <PINCode>411041</PINCode>                 <Country_Code>IB</Country_Code>             </Current_Applicant_Address_Details>             <Current_Applicant_Additional_Address_Details/>         </Current_Application_Details>     </Current_Application> </INProfileResponse>",
          "pdfReport" : "BinData(0,\"JVBERi0xLjQKJcfl9OXwCjEgMCBvYmoKmore2084bytes+application/pd\")",
          "responseJsonObject" : {
            "currentApplication" : {
              "currentApplicationDetails" : {
                "financePurpose" : "",
                "currentApplicantAddressDetails" : {
                  "pinCode" : "411041",
                  "landmark" : "",
                  "state" : "27",
                  "countryCode" : "IB",
                  "roadNumbernameAreaLocality" : "",
                  "bldgNumberSocietyName" : "",
                  "flatNoPlotNoHouseNo" : "JHDSGJFDSHV,",
                  "city" : "PUNE"
                },
                "enquiryReason" : "00",
                "currentOtherDetails" : {
                  "timeWithEmployer" : "",
                  "numberofMajorcreditCardHeld" : "",
                  "income" : "",
                  "maritialStatus" : "1",
                  "employmentStatus" : ""
                },
                "currentApplicantdetails" : {
                  "votersIdentityCard" : "",
                  "universalIdIssueDate" : "",
                  "universalIdNumber" : "",
                  "passportNumber" : "",
                  "rationCardNumber" : "",
                  "mobilePhoneNumber" : "",
                  "dateofBirthApplicant" : "20010327",
                  "universalIdExpirationDate" : "",
                  "emailid" : "hsgdhg@jd.dj",
                  "middleName1" : "",
                  "telephoneExtension" : "",
                  "passportExpirationDate" : "",
                  "middleName3" : "",
                  "middleName2" : "",
                  "voterIdExpirationdate" : "",
                  "voterIdIssueDate" : "",
                  "firstName" : "MUKESH",
                  "driverLicenceExpirationdate" : "",
                  "driverLicenceIssueDate" : "",
                  "lastName" : "AMBANI",
                  "driverLicenceNumber" : "",
                  "rationCardExpirationDate" : "",
                  "telephoneType" : "01",
                  "incometaxPan" : "",
                  "panIssueDate" : "",
                  "telephoneNumberApplicant1st" : "3487534875",
                  "panExpirationDate" : "",
                  "rationCardIssueDate" : "",
                  "passportIssueDate" : "",
                  "genderCode" : "2"
                },
                "amountFinanced" : "30000",
                "durationOfAgreement" : "0"
              }
            },
            "creditProfileHeader" : {
              "reportNumber" : "",
              "reporttime" : "",
              "subscriberName" : "HDB Financial Services Limited",
              "reportDate" : "",
              "subscriber" : "",
              "enquiryUserName" : "",
              "version" : "V2.4"
            },
            "userMessage" : {
              "userMessageText" : "SYS100007(Invalid Enquiry reason/ Search Type)"
            },
            "header" : {
              "reportTime" : "153443",
              "messageText" : "",
              "systemCode" : "0",
              "reportDate" : "20190425"
            }
          }
        }
      ],
      "creditInsightDomain" : {
        "pastEnquiry" : [ ],
        "bureauReported" : "EXPERIAN (XP), CRIF HIGH MARK (CR)",
        "refNumber" : "3394243",
        "revcSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        },
        "issuedDate" : "Thu Apr 25 15:35:27 IST 2019",
        "activeTradelines" : [ ],
        "totalNumEnquiries" : "0",
        "secSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        },
        "bureauFeeds" : {
          "chmScore" : [ ],
          "experianScore" : [ ],
          "equifaxScore" : [ ],
          "cibilScore" : [ ]
        },
        "totalNumCreditLines" : "0",
        "enquiryData" : {
          "name" : "MUKESH AMBANI",
          "dob" : "Tue Mar 27 00:00:00 IST 2001",
          "gender" : "Male"
        },
        "disparateCredentials" : {
          "kycIDList" : [ ],
          "addressList" : [ ],
          "phoneList" : [ ],
          "dobList" : [ ],
          "nameList" : [ ],
          "emailList" : [ ]
        },
        "unSecSummary" : {
          "days30Overdue" : 0,
          "openAccount" : 0,
          "balance" : 0,
          "days60Overdue" : 0,
          "payments" : 0,
          "days90Overdue" : 0,
          "overdueAmount" : 0,
          "percentageUsed" : 0
        }
      },
      "reject" : [
        {
          "trackingId" : 1555977,
          "bureau" : "CIBIL",
          "product" : "CIR",
          "status" : "ERROR",
          "errorList" : [
            {
              "code" : "E207",
              "description" : "At least one valid id/phone must be present"
            }
          ],
          "warningList" : [
            {
              "code" : "E203",
              "description" : "Phone1 is not valid"
            }
          ]
        }
      ]
    },
    "scoringServiceResponse" : {
      "header" : {
        "institutionId" : "4019",
        "custId" : "56684000115",
        "responseDate" : "25042019 16:12:32",
        "applicationId" : "56684000115"
      },
      "ackId" : "931769",
      "status" : "COMPLETED",
      "scoreData" : {
        "finalScore" : "20",
        "status" : "SUCCESS",
        "scoreCardName" : "TEST BRE 2",
        "scoreValue" : "20",
        "scoreDetails" : {
          "Test C" : {
            "Test A" : {
              "IRP$sApplicantType" : {
                "dField" : "IRP$sApplicantType",
                "FieldName" : "APPLICANT_TYPE",
                "dScore" : 20,
                "weight" : 1,
                "cScore" : 20,
                "expression" : " ( ( IRP$sApplicantType = EXPRESS ) )",
                "value" : {
                  "APPLICANT_TYPE" : "EXPRESS"
                }
              }
            }
          }
        },
        "finalBand" : "",
        "additionalProperties" : {
          
        }
      },
      "scoreTree" : {
        "masterMap" : {
          "Test C" : {
            "Test A" : {
              "IRP$sApplicantType" : {
                "dField" : "IRP$sApplicantType",
                "FieldName" : "APPLICANT_TYPE",
                "dScore" : 20,
                "weight" : 1,
                "cScore" : 20,
                "expression" : " ( ( IRP$sApplicantType = EXPRESS ) )",
                "value" : {
                  "APPLICANT_TYPE" : "EXPRESS"
                }
              }
            }
          }
        },
        "baseOperator" : "",
        "Scores" : [
          {
            "name" : "Test C",
            "score" : 20,
            "Plans" : [
              [
                {
                  "name" : "Test A",
                  "score" : 20,
                  "Fields" : [
                    [
                      {
                        "name" : "IRP$sApplicantType",
                        "score" : 20
                      }
                    ]
                  ]
                }
              ]
            ]
          }
        ],
        "AppScore" : 20,
        "TableID" : 121,
        "SCORECARD_NAME" : "TEST BRE 2",
        "FINAL_SCORE" : 20
      },
      "eligibilityResponse" : {
        "eligibleId" : "78",
        "approvedAmount" : 30000,
        "decision" : "Queue",
        "maxAmount" : 0,
        "minAmount" : 0,
        "dp" : 0,
        "maxTenor" : 0,
        "reMark" : "No eligibility criteria matched",
        "computedAmount" : 0,
        "eligibilityAmount" : 0,
        "cnt" : 0,
        "productsAllowed" : 0,
        "additionalProperties" : {
          
        },
        "additionalFields" : {
          
        }
      },
      "decisionResponse" : {
        "ruleId" : 25,
        "decision" : "Declined",
        "details" : [
          {
            "criteriaID" : 1,
            "ruleName" : "CHECK PAN STATUS",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( PAN_VERIFY_STATUS is FAKE_PAN ) ) ",
            "fieldValues" : {
              "PAN_VERIFY_STATUS" : "NO_RESPONSE"
            }
          },
          {
            "criteriaID" : 3,
            "ruleName" : "BRE 1 ELG AMT > 20K",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( QDE_BRE_ELIGIBILITY_AMOUNT > 20000 ) ) ",
            "fieldValues" : {
              "QDE_BRE_ELIGIBILITY_AMOUNT" : "0"
            }
          },
          {
            "criteriaID" : 6,
            "ruleName" : "CURRENT MOBILE MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_MOBILE_CHANGE is Yes ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_MOBILE_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 9,
            "ruleName" : "CURRENT NAME MISMATCH QUEUE RUL",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( ( 50 <= EXISTING_CURRENT_NAME_PERCENTAGE ) && ( EXISTING_CURRENT_NAME_PERCENTAGE < 100 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 10,
            "ruleName" : "CURENT NAME MISMATCH DECLN RUL",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_NAME_PERCENTAGE < 50 ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 15,
            "ruleName" : "DEBIT CARD TYPE IS SILVER",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CC_TYPE is SILVER ) ) ",
            "fieldValues" : {
              "CC_TYPE" : "null"
            }
          },
          {
            "criteriaID" : 20,
            "ruleName" : "EXISTING NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE < 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE < 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 21,
            "ruleName" : "EXISTING NAME MODIFIED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 22,
            "ruleName" : "EXISTNG NAME MODIFY CREDIT CHK1",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE < 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 23,
            "ruleName" : "EXISTNG NAME MODIFY CREDIT CHK2",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_FIRST_NAME_PERCENTAGE >= 50 ) ) ) && ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( EXISTING_CURRENT_LAST_NAME_PERCENTAGE < 50 ) ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_FIRST_NAME_PERCENTAGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "EXISTING_CURRENT_LAST_NAME_PERCENTAGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 25,
            "ruleName" : "EXISTING CURRENT PINCODE CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_PINCODE_CHANGE is Yes ) &&  ( ( APPLICANT_TYPE is EXISTING ) ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_PINCODE_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 26,
            "ruleName" : "EXISTNG FIRST NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_FIRST_NAME_CHANGE is Yes ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "EXISTING_CURRENT_FIRST_NAME_CHANGE" : "null"
            }
          },
          {
            "criteriaID" : 27,
            "ruleName" : "EXISTNG LAST NAME CHANGE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_LAST_NAME_CHANGE is Yes ) &&  ( ( APPLICANT_TYPE is EXISTING ) ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_LAST_NAME_CHANGE" : "null",
              "APPLICANT_TYPE" : "EXPRESS"
            }
          },
          {
            "criteriaID" : 28,
            "ruleName" : "OTHER KYC CHECK RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( OTP_STATUS is N ) ||  ( ( OTP_STATUS is Y ) ) ) && ( ( LOGIN_USING_KYC is Y ) ) && ( ( OTHER_KYC_CHECK_CIBIL_TEST is Queue ) ) ",
            "fieldValues" : {
              "OTHER_KYC_CHECK_CIBIL_TEST" : "Queue",
              "LOGIN_USING_KYC" : "N",
              "OTP_STATUS" : "N"
            }
          },
          {
            "criteriaID" : 29,
            "ruleName" : "EXISTING-CURRENT ADDR MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CURRENT_ADDRESS_SAME_AS is Others ) ||  ( ( EXISTING_CURRENT_ADDRESS_PERCENTAGE < 100 ) ) ) && ( ( APPLICANT_RESI_SCORE < 70 ) ) ",
            "fieldValues" : {
              "CURRENT_ADDRESS_SAME_AS" : "null",
              "EXISTING_CURRENT_ADDRESS_PERCENTAGE" : "null",
              "APPLICANT_RESI_SCORE" : "null"
            }
          },
          {
            "criteriaID" : 31,
            "ruleName" : "IDFY PAN MATCH APPROVE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_PAN_FACE_MATCH_BAND is green ) ) ",
            "fieldValues" : {
              "IDFY_PAN_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 32,
            "ruleName" : "IDFY PAN MATCH QUEUE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_PAN_FACE_MATCH_BAND is amber ) ) ",
            "fieldValues" : {
              "IDFY_PAN_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 34,
            "ruleName" : "IDFY DL MATCH APPROVE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_DRIVING_LICENSE_FACE_MATCH_BAND is green ) ) ",
            "fieldValues" : {
              "IDFY_DRIVING_LICENSE_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 35,
            "ruleName" : "IDFY DL MATCH QUEUE RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IDFY_DRIVING_LICENSE_FACE_MATCH_BAND is amber ) ) ",
            "fieldValues" : {
              "IDFY_DRIVING_LICENSE_FACE_MATCH_BAND" : "null"
            }
          },
          {
            "criteriaID" : 36,
            "ruleName" : "KARZA ID MISMATCH WITH EXISTING",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_ID_TYPE_MATCH_WITH_KARZA is Y ) &&  ( ( EXISTING_ID_NUMBER_MATCH_WITH_KARZA is N ) ) ) && ( ( EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE > 0 ) &&  ( ( EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE < 80 ) ) ) ",
            "fieldValues" : {
              "EXISTING_ID_NUMBER_MATCH_WITH_KARZA" : "null",
              "EXISTING_ID_TYPE_MATCH_WITH_KARZA" : "null",
              "EXISTING_NAME_MATCH_WITH_KARZA_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 37,
            "ruleName" : "EXISTING & CURENT NAME MISMATCH",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_NAME_PERCENTAGE < 70 ) ) && ( ( EXISTING_ID_NUMBER_MATCH_WITH_KARZA is N ) &&  ( ( EXISTING_DOB_MATCH_WITH_KARZA is N ) ) ) ",
            "fieldValues" : {
              "EXISTING_ID_NUMBER_MATCH_WITH_KARZA" : "null",
              "EXISTING_DOB_MATCH_WITH_KARZA" : "null",
              "EXISTING_CURRENT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 38,
            "ruleName" : "E-MAIL ID VALIDATED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is SUCCESS ) &&  ( ( EMAIL_ID_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_STATUS" : "N"
            }
          },
          {
            "criteriaID" : 39,
            "ruleName" : "E-MAIL ID VALIDATION SKIP",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is SUCCESS ) &&  ( ( EMAIL_ID_SKIP_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_SKIP_STATUS" : "Y"
            }
          },
          {
            "criteriaID" : 40,
            "ruleName" : "JUNK E-MAIL ID",
            "outcome" : "Declined",
            "remark" : "E-Mail ID does not exist",
            "expression" : " ( ( EMAIL_ID_RESPONSE_STATUS is FAILED ) &&  ( ( EMAIL_ID_SKIP_STATUS is Y ) ) ) ",
            "fieldValues" : {
              "EMAIL_ID_RESPONSE_STATUS" : "FAILED",
              "EMAIL_ID_SKIP_STATUS" : "Y"
            }
          },
          {
            "criteriaID" : 41,
            "ruleName" : "NEGATIVE AREA CHECK",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( IS_NEGATIVE_AREA is Yes ) &&  ( ( APPLICANT_ADDR_CITY_TIER is not 10 ) ) ) ",
            "fieldValues" : {
              "APPLICANT_ADDR_CITY_TIER" : "null",
              "IS_NEGATIVE_AREA" : "No"
            }
          },
          {
            "criteriaID" : 43,
            "ruleName" : "INTERNAL DEDUPE CHECK-LOAN TYPE",
            "outcome" : "Queue",
            "remark" : "SYS: login other product same month - check status",
            "expression" : " ( ( DEDUPE_CUSTOMER_STATUS is Y ) &&  ( ( DEDUPE_LOAN_TYPE is not TW ) ) ) && ( ( ( 0 <= DEDUPE_DECLINE_DAYS_DIFF ) && ( DEDUPE_DECLINE_DAYS_DIFF < 30 ) ) ) ",
            "fieldValues" : {
              "DEDUPE_LOAN_TYPE" : "[LSL, LSL]",
              "DEDUPE_CUSTOMER_STATUS" : "Y",
              "DEDUPE_DECLINE_DAYS_DIFF" : "0"
            }
          },
          {
            "criteriaID" : 44,
            "ruleName" : "EXISTING-CURRENT CITY CHANGED",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( EXISTING_CURRENT_CITY_CHANGED is YES ) ||  ( ( EXISTING_CURRENT_CITY_PERCENTAGE < 100 ) ) ) ",
            "fieldValues" : {
              "EXISTING_CURRENT_CITY_PERCENTAGE" : "null",
              "EXISTING_CURRENT_CITY_CHANGED" : "null"
            }
          },
          {
            "criteriaID" : 48,
            "ruleName" : "DC NAME MATCH WITH APPLICANT",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( NAME_ON_DEBIT_CARD_MATCH_WITH_APPLICANT_NAME_PERCENTAGE < 100 ) ) ",
            "fieldValues" : {
              "NAME_ON_DEBIT_CARD_MATCH_WITH_APPLICANT_NAME_PERCENTAGE" : "null"
            }
          },
          {
            "criteriaID" : 49,
            "ruleName" : "DECLINED CASE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( CRO_LATEST_MANUAL_DECISION is Declined ) ) ",
            "fieldValues" : {
              "CRO_LATEST_MANUAL_DECISION" : "null"
            }
          },
          {
            "criteriaID" : 52,
            "ruleName" : "ZERO PRE-APPROVED LOAN AMOUNT",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( APPLICATION_PRE_APPROVED_AMOUNT == 0 ) ) && ( ( APPLICANT_TYPE is EXISTING ) ) ",
            "fieldValues" : {
              "APPLICANT_TYPE" : "EXPRESS",
              "APPLICATION_PRE_APPROVED_AMOUNT" : "0"
            }
          },
          {
            "criteriaID" : 54,
            "ruleName" : "IDFY CHECK RESULT",
            "outcome" : "Queue",
            "remark" : "SYS: KYC ID image mismatch. Please check manually before decision",
            "expression" : " ( ( IDFY_CHECK_RESULT_TEST is Queue ) ) ",
            "fieldValues" : {
              "IDFY_CHECK_RESULT_TEST" : "Queue"
            }
          },
          {
            "criteriaID" : 56,
            "ruleName" : "TS SCORE TEST RULE",
            "outcome" : " ",
            "remark" : "No Rule Match",
            "expression" : " ( ( ( 600 <= SOCIAL_SCORE ) && ( SOCIAL_SCORE < 801 ) ) ) ",
            "fieldValues" : {
              "SOCIAL_SCORE" : "null"
            }
          }
        ]
      },
      "derivedFields" : {
        "CUSTOM_FIELDS$TW_TVR" : "true",
        "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
        "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$CC" : "NA",
        "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
        "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
        "POLICY_ID" : 610,
        "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
        "POLICY_NAME" : "LSL POLICY BRE 2",
        "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
        "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
        "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
        "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
        "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
      },
      "additionalProperties" : {
        
      }
    }
  },
  "applicantComponentResponseList" : [ ],
  "croDecisions" : [
    {
      "amtApproved" : 30000,
      "interestRate" : 0,
      "downPayment" : 0,
      "emi" : 0,
      "tenor" : 2,
      "eligibleAmt" : 0,
      "unUtilizedAmt" : 29400,
      "utilizedAmt" : 16928,
      "decisionUpdateDate" : "2019-04-25T10:44:21.406Z",
      "ltv" : 0,
      "subjectTo" : "kjsdfjk",
      "remark" : "jsdj",
      "ltvMax" : 0,
      "ltvMin" : 0,
      "sobreLtv" : 0,
      "finalAssetPrice" : 0,
      "masterAssetPrice" : 0,
      "totalAssetCost" : 0
    }
  ],
  "negativePincode" : false,
  "applScoreVector" : [
    {
      "fieldName" : "PAN Verification",
      "order" : 4,
      "fieldValue" : "NO_RESPONSE",
      "message" : "NO_RESPONSE",
      "status" : "FAILED",
      "addStability" : 0
    },
    {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "0",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    },
    {
      "fieldName" : "Application Score",
      "order" : 5,
      "fieldValue" : "20",
      "message" : "COMPLETED",
      "status" : "SUCCESS",
      "addStability" : 0
    }
  ],
  "dedupedApplications" : [
    {
      "refId" : "56684000010",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    },
    {
      "refId" : "1234567820",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    },
    {
      "refId" : "56684000030",
      "status" : "DCLN",
      "processDate" : "2019-04-16T06:19:05.404Z",
      "dedupeParam" : {
        "PAN Number" : "CHMPK6466D"
      }
    }
  ],
  "croJustification" : [
    {
      "subjectTo" : "kjsdfjk",
      "remark" : "jsdj",
      "croID" : "HDBFS_CRO1@softcell.com",
      "decisionCase" : "Approved",
      "croJustificationUpdateDate" : "2019-04-25T10:45:03.150Z",
      "croEmpId" : "HDB41732"
    }
  ],
  "subProcesses" : [ ],
  "interimStatusList" : [ ],
  "finalApplicationStatus" : "PENDING",
  "isEditable" : true,
  "multiBREDetails" : {
    "qdeBreInfo" : {
      "dateTime" : "2019-04-25T10:06:54.787Z",
      "multiBREType" : "QDE_DETAILS_BRE",
      "eligibityGridId" : "78",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 15:34:38",
          "applicationId" : "56684000115"
        },
        "ackId" : "931729",
        "eligibilityResponse" : {
          "eligibleId" : "78",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 25,
          "decision" : "Declined"
        },
        "derivedFields" : {
          "CUSTOM_FIELDS$TW_TVR" : "true",
          "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$CC" : "NA",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
          "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
          "POLICY_ID" : 609,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
          "POLICY_NAME" : "LSL POLICY BRE 1",
          "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
          "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "ddeBreInfo" : {
      "dateTime" : "2019-04-25T10:44:21.372Z",
      "multiBREType" : "DDE_DETAILS_BRE",
      "eligibityGridId" : "78",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 16:12:32",
          "applicationId" : "56684000115"
        },
        "ackId" : "931769",
        "eligibilityResponse" : {
          "eligibleId" : "78",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 25,
          "decision" : "Declined"
        },
        "derivedFields" : {
          "CUSTOM_FIELDS$TW_TVR" : "true",
          "CUSTOM_FIELDS$UNSEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_OFFC" : "false",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$CC" : "NA",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$HIGH_CREDIT_SANC_AMT" : "0",
          "CUSTOM_FIELDS$SEC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI_CUM_OFFC" : "false",
          "POLICY_ID" : 610,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N",
          "POLICY_NAME" : "LSL POLICY BRE 2",
          "CUSTOM_FIELDS$CC_HIGH_CREDIT_SANC_AMT" : 0,
          "CUSTOM_FIELDS$TW_CPV_RESI" : "false",
          "CUSTOM_FIELDS$BRE_MULTI_PRODUCT" : 3,
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "bankingBreInfo" : {
      "dateTime" : "2019-04-25T10:48:36.993Z",
      "multiBREType" : "BANKING_DETAILS_BRE",
      "eligibityGridId" : "58.1",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000115",
          "responseDate" : "25042019 16:16:47",
          "applicationId" : "56684000115"
        },
        "ackId" : "931776",
        "eligibilityResponse" : {
          "values" : {
            "APPLICATION_LOAN_AMOUNT" : 30000,
            "DDE_BRE_ELIGIBILITY_AMOUNT" : 0
          },
          "eligibleId" : "58",
          "gridId" : 1,
          "approvedAmount" : 30000,
          "decision" : "Approved",
          "computeDisp" : "( 40000 )",
          "computeLogic" : "( 40000 )",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "bre 2 elg amt > 20k",
          "computedAmount" : 40000,
          "eligibilityAmount" : 40000,
          "cnt" : 0,
          "ruleExucSeq" : 1,
          "gridExpression" : " ( ( DDE_BRE_ELIGIBILITY_AMOUNT >= 20000 ) || ( APPLICATION_LOAN_AMOUNT >= 10000 )  ) ",
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 21,
          "decision" : "Approved"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 3",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 611,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "assetBreInfo" : {
      "dateTime" : "2019-04-25T13:26:33.080Z",
      "multiBREType" : "ASSET_DETAILS_BRE",
      "eligibityGridId" : "57",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000126",
          "responseDate" : "25042019 18:54:43",
          "applicationId" : "56684000126"
        },
        "ackId" : "931954",
        "eligibilityResponse" : {
          "eligibleId" : "57",
          "approvedAmount" : 30000,
          "decision" : "Queue",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "No eligibility criteria matched",
          "computedAmount" : 0,
          "eligibilityAmount" : 0,
          "cnt" : 0,
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 22,
          "decision" : "Queue"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 4_1",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 612,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    },
    "schemeBreInfo" : {
      "dateTime" : "2019-04-26T11:45:30.378Z",
      "multiBREType" : "SCHEME_DETAILS_BRE",
      "eligibityGridId" : "66.1",
      "scoringResponse" : {
        "header" : {
          "institutionId" : "4019",
          "custId" : "56684000136",
          "responseDate" : "26042019 17:13:40",
          "applicationId" : "56684000136"
        },
        "ackId" : "932336",
        "eligibilityResponse" : {
          "values" : {
            "APPLICATION_LOAN_AMOUNT" : 30000,
            "DDE_BRE_ELIGIBILITY_AMOUNT" : 0
          },
          "eligibleId" : "66",
          "gridId" : 1,
          "approvedAmount" : 60,
          "decision" : "Approved",
          "computeDisp" : "( POST_IPA_ASSET_NET_FUNDING_AMOUNT / POST_IPA_ASSET_TOTAL_ASSET_COST * 100 )",
          "computeLogic" : "( GNG_POST_IPA_DETAILS$oPostIpaDetails$dNetFundingAmt / GNG_POST_IPA_DETAILS$oPostIpaDetails$dTotAssCost * 100 )",
          "maxAmount" : 0,
          "minAmount" : 0,
          "dp" : 0,
          "maxTenor" : 0,
          "reMark" : "Approved",
          "computedAmount" : 60,
          "eligibilityAmount" : 60,
          "cnt" : 0,
          "ruleExucSeq" : 1,
          "gridExpression" : " ( ( DDE_BRE_ELIGIBILITY_AMOUNT > 0 ) || ( APPLICATION_LOAN_AMOUNT >= 7000 )  ) ",
          "productsAllowed" : 0,
          "additionalProperties" : {
            
          },
          "additionalFields" : {
            
          }
        },
        "decisionResponse" : {
          "ruleId" : 34,
          "decision" : "Approved"
        },
        "derivedFields" : {
          "POLICY_NAME" : "LSL POLICY BRE 4_2",
          "CUSTOM_FIELDS$SF_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$DPL_DEALER_RANK_4_5" : "No",
          "CUSTOM_FIELDS$REAPPRAISAL_REASON" : "N",
          "POLICY_ID" : 613,
          "CUSTOM_FIELDS$SOFTCELL_DDE_QDE_BRE_CHECK" : "N"
        },
        "additionalProperties" : {
          
        }
      }
    }
  },
  "tvrDataList" : [ ],
  "applicantsSubProcess" : [ ],
  "componentModule" : [ ],
  "componentList" : {
    
  },
  "interfaceName" : "GONOGO",
  "createdDate" : "2019-04-26T11:41:00.880Z",
  "createdBy" : "prateek",
  "updatedDate" : "2019-04-26T11:41:00.880Z",
  "updateBy" : "prateek",
  "version" : 2
}
];
 
const fields = ['_id', 'intrimStatus.startTime','intrimStatus.appStart','intrimStatus.dedupe','intrimStatus.posidexDedupeStatus','intrimStatus.emailStatus','intrimStatus.otpStatus','intrimStatus.appsStatus',
'intrimStatus.panStatus','intrimStatus.aadharStatus','intrimStatus.hunterStatus','intrimStatus.mbStatus','intrimStatus.creditVidyaStatus','intrimStatus.saathiPullStatus','intrimStatus.varScoreStatus',
'intrimStatus.scoreStatus','intrimStatus.cibilScore','intrimStatus.experianStatus','intrimStatus.highmarkStatus','intrimStatus.croStatus','intrimStatus.awsS3Status','intrimStatus.ntcStatus',
'parentID','rootID', 'productSequenceNumber', 'dateTime', 'applicationStatus', 'statusFlag', 'reInitiateCount', 'reappraiseReq', 'reProcessCount', 'applicationRequest', 'applicantComponentResponse', 
'croDecisions', 'negativePincode', 'applScoreVector', 'dedupedApplications', 'croJustification', 'finalApplicationStatus', 'isEditable', 'multiBREDetails', 'interfaceName', 'createdDate', 'createdBy',
'updatedDate', 'updateBy', 'version'];


const transforms = [unwind({ paths: ['intrimStatus', 'applicationRequest', 'applicantComponentResponse', 'croDecisions', 'applScoreVector', 'dedupedApplications', 'croJustification', 'multiBREDetails'] })];
 
const json2csvParser = new Parser({ fields, transforms });
const csv = json2csvParser.parse(gonogo);

FileSystem.writeFileSync("./gonogo.csv", csv);
 

//console.log(csv);