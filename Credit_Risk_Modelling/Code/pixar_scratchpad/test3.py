import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetimerange import DateTimeRange
from dateutil import rrule, parser

def run():
    data=pd.read_csv('/home/ssg0283/Documents/RISK_MODELS/Code/pixar-scratchpad/data/testtime.csv')

    data.rename(columns={'_id': '_ID', 'intrimStatus.startTime': 'startTime','applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.dateOpenedOrDisbursed':'dateOpenedOrDisbursed','applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.dateClosed':'dateClosed','applicantComponentResponse.multiBureauJsonRespose.finishedList.responseJsonObject.accountList.accountType':'accountType'}, inplace=True)

    data.dropna(subset = ["dateOpenedOrDisbursed"], inplace=True)
    data['dateOpenedOrDisbursed'].astype(int)

    data['startTime'] = data['startTime'].str.replace('Z', '')
    data['startTime'] = data['startTime'].str.replace('{', '')
    data['startTime'] = data['startTime'].str.replace('}', '')
    data['startTime'] = data['startTime'].str.replace('"', '')
    data['startTime'] = data['startTime'].str.replace('$', '')
    data['startTime'] = data['startTime'].str.replace('date:', '')
    data['startTime'] = data['startTime'].str.replace('T', '')

    data['startTime'] =  pd.to_datetime(data['startTime'], format='%Y-%m-%d%H:%M:%S.%f')

    data['dateOpenedOrDisbursed'] = data['dateOpenedOrDisbursed'].astype(int)
    data['dateClosed'] = data['dateClosed'].fillna(0)
    data['dateClosed'] = data['dateClosed'].astype(int)
    data['accountType'] = data['accountType'].astype(int)


    data['dateOpenedOrDisbursed'] = data['dateOpenedOrDisbursed'].astype(str).apply(lambda x: x.zfill(8))
    data['dateClosed'] = data['dateClosed'].astype(str).apply(lambda x: x.zfill(8))


    bureau_accType_dict = {0: "OTH", 1: "AL", 2: "HL", 3: "HL", 4: "LAS", 5: "PL", 6: "CD",
                          7: "GL", 8: "PL", 9: "SEL", 10: "CC", 11: "HL", 12: "RL",
                          13: "AL", 14: "RL", 15: "LAS", 16: "CV", 17: "CV",
                          31: "CC", 32: "AL", 33: "CV", 34: "CV", 35: "SCC", 36: "SCC",
                          37: "PL", 38: "RL", 39: "BL", 40: "MFBL", 41: "MFPL", 42: "MFHL",
                          43: "MFOT", 44: "HL", 50: "BL", 51: "BL", 52: "PLBL", 53: "PLBL",
                          54: "PLBL", 55: "RL", 56: "PLRLBL", 57: "PLRLBL", 58: "PLRLBL",
                          59: "BL", 61: "BL", 98: "SEC", 99: "UNSEC"}


    data = data.replace({"accountType": bureau_accType_dict})
    data['dateOpenedOrDisbursed'] = data['dateOpenedOrDisbursed'].apply(lambda x: dt.datetime.strptime(x, '%d%m%Y'))
    data['dateClosed'] = pd.to_datetime(data['dateClosed'], errors='coerce', format='%d%m%Y')

    data['dateOpenedOrDisbursed'] = pd.to_datetime(data['dateOpenedOrDisbursed'],errors='coerce')

    data['startTime_Date'] = pd.to_datetime(data['startTime'],errors='coerce')

    data['diff_startTime_dateOpened'] = ((data.startTime_Date - data.dateOpenedOrDisbursed)/np.timedelta64(1, 'M'))

    data['diff_startTime_dateOpened'] = data['diff_startTime_dateOpened'].round().astype(int)


    data['dateClosed'] = pd.to_datetime(data['dateClosed'],errors='coerce')

    data['dateOpenedOrDisbursed'].value_counts()

    data['diff_startTime_dateOpened'].value_counts()

    data['_ID'].value_counts()

    data = data.groupby('_ID').agg(lambda x: x.tolist()).reset_index()

    count_3M = 0
    count_6M = 0
    count_9M = 0
    count_1Y = 0
    count_2Y = 0
    count_3Y = 0
    data['opened_last3M_CNT'] = 0
    data['opened_last6M_CNT'] = 0
    data['opened_last9M_CNT'] = 0
    data['opened_last1Y_CNT'] = 0
    data['opened_last2Y_CNT'] = 0
    data['opened_last3Y_CNT'] = 0

    for i in range(data.shape[0]):
        count_3M = 0
        count_6M = 0
        count_9M = 0
        count_1Y = 0
        count_2Y = 0
        count_3Y = 0
        for j in data['diff_startTime_dateOpened'][i]:
            if j <= 3:
                count_3M = count_3M + 1
            data['opened_last3M_CNT'][i] = count_3M

            if j <= 6:
                count_6M = count_6M + 1
            data['opened_last6M_CNT'][i] = count_6M

            if j <= 9:
                count_9M = count_9M + 1
            data['opened_last9M_CNT'][i] = count_9M

            if j <= 12:
                count_1Y = count_1Y + 1
            data['opened_last1Y_CNT'][i] = count_1Y

            if j <= 24:
                count_2Y = count_2Y + 1
            data['opened_last2Y_CNT'][i] = count_2Y

            if j <= 36:
                count_3Y = count_3Y + 1
            data['opened_last3Y_CNT'][i] = count_3Y

    data.head()


    date_before_3M = dt.date
    date_before_6M = dt.date
    date_before_9M = dt.date
    date_before_1Y = dt.date
    date_before_2Y = dt.date
    date_before_3Y = dt.date


    three_mon_rel = relativedelta(months=-3)
    six_mon_rel = relativedelta(months=-6)
    nine_mon_rel = relativedelta(months=-9)
    one_year_rel = relativedelta(months=-12)
    two_year_rel = relativedelta(months=-24)
    three_year_rel = relativedelta(months=-36)


    opened_last3M_CNT_P_list= []
    opened_last6M_CNT_P_list= []
    opened_last9M_CNT_P_list= []
    opened_last1Y_CNT_P_list= []
    opened_last2Y_CNT_P_list= []
    opened_last3Y_CNT_P_list= []



    data['opened_last3M_CNT_P'] = 0
    data['opened_last6M_CNT_P'] = 0
    data['opened_last9M_CNT_P'] = 0
    data['opened_last1Y_CNT_P'] = 0
    data['opened_last2Y_CNT_P'] = 0
    data['opened_last3Y_CNT_P'] = 0


    data['opened_last3M_CNT_P'] = data['opened_last3M_CNT_P'].astype(object)
    data['opened_last6M_CNT_P'] = data['opened_last6M_CNT_P'].astype(object)
    data['opened_last9M_CNT_P'] = data['opened_last9M_CNT_P'].astype(object)
    data['opened_last1Y_CNT_P'] = data['opened_last1Y_CNT_P'].astype(object)
    data['opened_last2Y_CNT_P'] = data['opened_last2Y_CNT_P'].astype(object)
    data['opened_last3Y_CNT_P'] = data['opened_last3Y_CNT_P'].astype(object)


    #date_before_3M = (data['dateOpenedOrDisbursed'][1][1]) + three_mon_rel
    #date_before_3M = dt.date

    #print(date_before_3M)



    def search_dt_list(dateOpenedDisbursed_start,date_before_period, dateOpenedDisbursedlist):
        count=0
        for p in dateOpenedDisbursedlist:
            if dateOpenedDisbursed_start!=p and dateOpenedDisbursed_start > p >= date_before_period:
                count = count + 1
        return count


    data['opened_last3M_CNT_PL'] = 0
    data['opened_last6M_CNT_PL'] = 0
    data['opened_last9M_CNT_PL'] = 0
    data['opened_last1Y_CNT_PL'] = 0
    data['opened_last2Y_CNT_PL'] = 0
    data['opened_last3Y_CNT_PL'] = 0



    data['opened_last3M_CNT_HL'] = 0
    data['opened_last6M_CNT_HL'] = 0
    data['opened_last9M_CNT_HL'] = 0
    data['opened_last1Y_CNT_HL'] = 0
    data['opened_last2Y_CNT_HL'] = 0
    data['opened_last3Y_CNT_HL'] = 0


    data['opened_last3M_CNT_GL'] = 0
    data['opened_last6M_CNT_GL'] = 0
    data['opened_last9M_CNT_GL'] = 0
    data['opened_last1Y_CNT_GL'] = 0
    data['opened_last2Y_CNT_GL'] = 0
    data['opened_last3Y_CNT_GL'] = 0



    data['opened_last3M_CNT_AL'] = 0
    data['opened_last6M_CNT_AL'] = 0
    data['opened_last9M_CNT_AL'] = 0
    data['opened_last1Y_CNT_AL'] = 0
    data['opened_last2Y_CNT_AL'] = 0
    data['opened_last3Y_CNT_AL'] = 0



    data['opened_last3M_CNT_SEL'] = 0
    data['opened_last6M_CNT_SEL'] = 0
    data['opened_last9M_CNT_SEL'] = 0
    data['opened_last1Y_CNT_SEL'] = 0
    data['opened_last2Y_CNT_SEL'] = 0
    data['opened_last3Y_CNT_SEL'] = 0



    data['opened_last3M_CNT_LAS'] = 0
    data['opened_last6M_CNT_LAS'] = 0
    data['opened_last9M_CNT_LAS'] = 0
    data['opened_last1Y_CNT_LAS'] = 0
    data['opened_last2Y_CNT_LAS'] = 0
    data['opened_last3Y_CNT_LAS'] = 0



    data['opened_last3M_CNT_CD'] = 0
    data['opened_last6M_CNT_CD'] = 0
    data['opened_last9M_CNT_CD'] = 0
    data['opened_last1Y_CNT_CD'] = 0
    data['opened_last2Y_CNT_CD'] = 0
    data['opened_last3Y_CNT_CD'] = 0



    data['opened_last3M_CNT_CC'] = 0
    data['opened_last6M_CNT_CC'] = 0
    data['opened_last9M_CNT_CC'] = 0
    data['opened_last1Y_CNT_CC'] = 0
    data['opened_last2Y_CNT_CC'] = 0
    data['opened_last3Y_CNT_CC'] = 0


    data['opened_last3M_CNT_RL'] = 0
    data['opened_last6M_CNT_RL'] = 0
    data['opened_last9M_CNT_RL'] = 0
    data['opened_last1Y_CNT_RL'] = 0
    data['opened_last2Y_CNT_RL'] = 0
    data['opened_last3Y_CNT_RL'] = 0



    data['opened_last3M_CNT_CV'] = 0
    data['opened_last6M_CNT_CV'] = 0
    data['opened_last9M_CNT_CV'] = 0
    data['opened_last1Y_CNT_CV'] = 0
    data['opened_last2Y_CNT_CV'] = 0
    data['opened_last3Y_CNT_CV'] = 0


    data['opened_last3M_CNT_SCC'] = 0
    data['opened_last6M_CNT_SCC'] = 0
    data['opened_last9M_CNT_SCC'] = 0
    data['opened_last1Y_CNT_SCC'] = 0
    data['opened_last2Y_CNT_SCC'] = 0
    data['opened_last3Y_CNT_SCC'] = 0



    data['opened_last3M_CNT_BL'] = 0
    data['opened_last6M_CNT_BL'] = 0
    data['opened_last9M_CNT_BL'] = 0
    data['opened_last1Y_CNT_BL'] = 0
    data['opened_last2Y_CNT_BL'] = 0
    data['opened_last3Y_CNT_BL'] = 0


    data['opened_last3M_CNT_MFBL'] = 0
    data['opened_last6M_CNT_MFBL'] = 0
    data['opened_last9M_CNT_MFBL'] = 0
    data['opened_last1Y_CNT_MFBL'] = 0
    data['opened_last2Y_CNT_MFBL'] = 0
    data['opened_last3Y_CNT_MFBL'] = 0

    data['opened_last3M_CNT_MFPL'] = 0
    data['opened_last6M_CNT_MFPL'] = 0
    data['opened_last9M_CNT_MFPL'] = 0
    data['opened_last1Y_CNT_MFPL'] = 0
    data['opened_last2Y_CNT_MFPL'] = 0
    data['opened_last3Y_CNT_MFPL'] = 0


    data['opened_last3M_CNT_MFHL'] = 0
    data['opened_last6M_CNT_MFHL'] = 0
    data['opened_last9M_CNT_MFHL'] = 0
    data['opened_last1Y_CNT_MFHL'] = 0
    data['opened_last2Y_CNT_MFHL'] = 0
    data['opened_last3Y_CNT_MFHL'] = 0


    data['opened_last3M_CNT_MFOT'] = 0
    data['opened_last6M_CNT_MFOT'] = 0
    data['opened_last9M_CNT_MFOT'] = 0
    data['opened_last1Y_CNT_MFOT'] = 0
    data['opened_last2Y_CNT_MFOT'] = 0
    data['opened_last3Y_CNT_MFOT'] = 0



    data['opened_last3M_CNT_OTH'] = 0
    data['opened_last6M_CNT_OTH'] = 0
    data['opened_last9M_CNT_OTH'] = 0
    data['opened_last1Y_CNT_OTH'] = 0
    data['opened_last2Y_CNT_OTH'] = 0
    data['opened_last3Y_CNT_OTH'] = 0



    data['opened_last3M_CNT_PLBL'] = 0
    data['opened_last6M_CNT_PLBL'] = 0
    data['opened_last9M_CNT_PLBL'] = 0
    data['opened_last1Y_CNT_PLBL'] = 0
    data['opened_last2Y_CNT_PLBL'] = 0
    data['opened_last3Y_CNT_PLBL'] = 0



    data['opened_last3M_CNT_PLRLBL'] = 0
    data['opened_last6M_CNT_PLRLBL'] = 0
    data['opened_last9M_CNT_PLRLBL'] = 0
    data['opened_last1Y_CNT_PLRLBL'] = 0
    data['opened_last2Y_CNT_PLRLBL'] = 0
    data['opened_last3Y_CNT_PLRLBL'] = 0



    data['opened_last3M_CNT_SEC'] = 0
    data['opened_last6M_CNT_SEC'] = 0
    data['opened_last9M_CNT_SEC'] = 0
    data['opened_last1Y_CNT_SEC'] = 0
    data['opened_last2Y_CNT_SEC'] = 0
    data['opened_last3Y_CNT_SEC'] = 0



    data['opened_last3M_CNT_UNSEC'] = 0
    data['opened_last6M_CNT_UNSEC'] = 0
    data['opened_last9M_CNT_UNSEC'] = 0
    data['opened_last1Y_CNT_UNSEC'] = 0
    data['opened_last2Y_CNT_UNSEC'] = 0
    data['opened_last3Y_CNT_UNSEC'] = 0

    data['opened_last3M_CNT_PL'] = data['opened_last3M_CNT_PL'].astype(object)
    data['opened_last6M_CNT_PL'] = data['opened_last6M_CNT_PL'].astype(object)
    data['opened_last9M_CNT_PL'] = data['opened_last9M_CNT_PL'].astype(object)
    data['opened_last1Y_CNT_PL'] = data['opened_last1Y_CNT_PL'].astype(object)
    data['opened_last2Y_CNT_PL'] = data['opened_last2Y_CNT_PL'].astype(object)
    data['opened_last3Y_CNT_PL'] = data['opened_last3Y_CNT_PL'].astype(object)

    data['opened_last3M_CNT_HL'] = data['opened_last3M_CNT_HL'].astype(object)
    data['opened_last6M_CNT_HL'] = data['opened_last6M_CNT_HL'].astype(object)
    data['opened_last9M_CNT_HL'] = data['opened_last9M_CNT_HL'].astype(object)
    data['opened_last1Y_CNT_HL'] = data['opened_last1Y_CNT_HL'].astype(object)
    data['opened_last2Y_CNT_HL'] = data['opened_last2Y_CNT_HL'].astype(object)
    data['opened_last3Y_CNT_HL'] = data['opened_last3Y_CNT_HL'].astype(object)

    data['opened_last3M_CNT_GL'] = data['opened_last3M_CNT_GL'].astype(object)
    data['opened_last6M_CNT_GL'] = data['opened_last6M_CNT_GL'].astype(object)
    data['opened_last9M_CNT_GL'] = data['opened_last9M_CNT_GL'].astype(object)
    data['opened_last1Y_CNT_GL'] = data['opened_last1Y_CNT_GL'].astype(object)
    data['opened_last2Y_CNT_GL'] = data['opened_last2Y_CNT_GL'].astype(object)
    data['opened_last3Y_CNT_GL'] = data['opened_last3Y_CNT_GL'].astype(object)

    data['opened_last3M_CNT_AL'] = data['opened_last3M_CNT_AL'].astype(object)
    data['opened_last6M_CNT_AL'] = data['opened_last6M_CNT_AL'].astype(object)
    data['opened_last9M_CNT_AL'] = data['opened_last9M_CNT_AL'].astype(object)
    data['opened_last1Y_CNT_AL'] = data['opened_last1Y_CNT_AL'].astype(object)
    data['opened_last2Y_CNT_AL'] = data['opened_last2Y_CNT_AL'].astype(object)
    data['opened_last3Y_CNT_AL'] = data['opened_last3Y_CNT_AL'].astype(object)

    data['opened_last3M_CNT_SEL'] = data['opened_last3M_CNT_SEL'].astype(object)
    data['opened_last6M_CNT_SEL'] = data['opened_last6M_CNT_SEL'].astype(object)
    data['opened_last9M_CNT_SEL'] = data['opened_last9M_CNT_SEL'].astype(object)
    data['opened_last1Y_CNT_SEL'] = data['opened_last1Y_CNT_SEL'].astype(object)
    data['opened_last2Y_CNT_SEL'] = data['opened_last2Y_CNT_SEL'].astype(object)
    data['opened_last3Y_CNT_SEL'] = data['opened_last3Y_CNT_SEL'].astype(object)

    data['opened_last3M_CNT_LAS'] = data['opened_last3M_CNT_LAS'].astype(object)
    data['opened_last6M_CNT_LAS'] = data['opened_last6M_CNT_LAS'].astype(object)
    data['opened_last9M_CNT_LAS'] = data['opened_last9M_CNT_LAS'].astype(object)
    data['opened_last1Y_CNT_LAS'] = data['opened_last1Y_CNT_LAS'].astype(object)
    data['opened_last2Y_CNT_LAS'] = data['opened_last2Y_CNT_LAS'].astype(object)
    data['opened_last3Y_CNT_LAS'] = data['opened_last3Y_CNT_LAS'].astype(object)

    data['opened_last3M_CNT_CD'] = data['opened_last3M_CNT_CD'].astype(object)
    data['opened_last6M_CNT_CD'] = data['opened_last6M_CNT_CD'].astype(object)
    data['opened_last9M_CNT_CD'] = data['opened_last9M_CNT_CD'].astype(object)
    data['opened_last1Y_CNT_CD'] = data['opened_last1Y_CNT_CD'].astype(object)
    data['opened_last2Y_CNT_CD'] = data['opened_last2Y_CNT_CD'].astype(object)
    data['opened_last3Y_CNT_CD'] = data['opened_last3Y_CNT_CD'].astype(object)

    data['opened_last3M_CNT_CC'] = data['opened_last3M_CNT_CC'].astype(object)
    data['opened_last6M_CNT_CC'] = data['opened_last6M_CNT_CC'].astype(object)
    data['opened_last9M_CNT_CC'] = data['opened_last9M_CNT_CC'].astype(object)
    data['opened_last1Y_CNT_CC'] = data['opened_last1Y_CNT_CC'].astype(object)
    data['opened_last2Y_CNT_CC'] = data['opened_last2Y_CNT_CC'].astype(object)
    data['opened_last3Y_CNT_CC'] = data['opened_last3Y_CNT_CC'].astype(object)

    data['opened_last3M_CNT_RL'] = data['opened_last3M_CNT_RL'].astype(object)
    data['opened_last6M_CNT_RL'] = data['opened_last6M_CNT_RL'].astype(object)
    data['opened_last9M_CNT_RL'] = data['opened_last9M_CNT_RL'].astype(object)
    data['opened_last1Y_CNT_RL'] = data['opened_last1Y_CNT_RL'].astype(object)
    data['opened_last2Y_CNT_RL'] = data['opened_last2Y_CNT_RL'].astype(object)
    data['opened_last3Y_CNT_RL'] = data['opened_last3Y_CNT_RL'].astype(object)

    data['opened_last3M_CNT_CV'] = data['opened_last3M_CNT_CV'].astype(object)
    data['opened_last6M_CNT_CV'] = data['opened_last6M_CNT_CV'].astype(object)
    data['opened_last9M_CNT_CV'] = data['opened_last9M_CNT_CV'].astype(object)
    data['opened_last1Y_CNT_CV'] = data['opened_last1Y_CNT_CV'].astype(object)
    data['opened_last2Y_CNT_CV'] = data['opened_last2Y_CNT_CV'].astype(object)
    data['opened_last3Y_CNT_CV'] = data['opened_last3Y_CNT_CV'].astype(object)

    data['opened_last3M_CNT_SCC'] = data['opened_last3M_CNT_SCC'].astype(object)
    data['opened_last6M_CNT_SCC'] = data['opened_last6M_CNT_SCC'].astype(object)
    data['opened_last9M_CNT_SCC'] = data['opened_last9M_CNT_SCC'].astype(object)
    data['opened_last1Y_CNT_SCC'] = data['opened_last1Y_CNT_SCC'].astype(object)
    data['opened_last2Y_CNT_SCC'] = data['opened_last2Y_CNT_SCC'].astype(object)
    data['opened_last3Y_CNT_SCC'] = data['opened_last3Y_CNT_SCC'].astype(object)

    data['opened_last3M_CNT_BL'] = data['opened_last3M_CNT_BL'].astype(object)
    data['opened_last6M_CNT_BL'] = data['opened_last6M_CNT_BL'].astype(object)
    data['opened_last9M_CNT_BL'] = data['opened_last9M_CNT_BL'].astype(object)
    data['opened_last1Y_CNT_BL'] = data['opened_last1Y_CNT_BL'].astype(object)
    data['opened_last2Y_CNT_BL'] = data['opened_last2Y_CNT_BL'].astype(object)
    data['opened_last3Y_CNT_BL'] = data['opened_last3Y_CNT_BL'].astype(object)

    data['opened_last3M_CNT_MFBL'] = data['opened_last3M_CNT_MFBL'].astype(object)
    data['opened_last6M_CNT_MFBL'] = data['opened_last6M_CNT_MFBL'].astype(object)
    data['opened_last9M_CNT_MFBL'] = data['opened_last9M_CNT_MFBL'].astype(object)
    data['opened_last1Y_CNT_MFBL'] = data['opened_last1Y_CNT_MFBL'].astype(object)
    data['opened_last2Y_CNT_MFBL'] = data['opened_last2Y_CNT_MFBL'].astype(object)
    data['opened_last3Y_CNT_MFBL'] = data['opened_last3Y_CNT_MFBL'].astype(object)

    data['opened_last3M_CNT_MFPL'] = data['opened_last3M_CNT_MFPL'].astype(object)
    data['opened_last6M_CNT_MFPL'] = data['opened_last6M_CNT_MFPL'].astype(object)
    data['opened_last9M_CNT_MFPL'] = data['opened_last9M_CNT_MFPL'].astype(object)
    data['opened_last1Y_CNT_MFPL'] = data['opened_last1Y_CNT_MFPL'].astype(object)
    data['opened_last2Y_CNT_MFPL'] = data['opened_last2Y_CNT_MFPL'].astype(object)
    data['opened_last3Y_CNT_MFPL'] = data['opened_last3Y_CNT_MFPL'].astype(object)

    data['opened_last3M_CNT_MFHL'] = data['opened_last3M_CNT_MFHL'].astype(object)
    data['opened_last6M_CNT_MFHL'] = data['opened_last6M_CNT_MFHL'].astype(object)
    data['opened_last9M_CNT_MFHL'] = data['opened_last9M_CNT_MFHL'].astype(object)
    data['opened_last1Y_CNT_MFHL'] = data['opened_last1Y_CNT_MFHL'].astype(object)
    data['opened_last2Y_CNT_MFHL'] = data['opened_last2Y_CNT_MFHL'].astype(object)
    data['opened_last3Y_CNT_MFHL'] = data['opened_last3Y_CNT_MFHL'].astype(object)

    data['opened_last3M_CNT_MFOT'] = data['opened_last3M_CNT_MFOT'].astype(object)
    data['opened_last6M_CNT_MFOT'] = data['opened_last6M_CNT_MFOT'].astype(object)
    data['opened_last9M_CNT_MFOT'] = data['opened_last9M_CNT_MFOT'].astype(object)
    data['opened_last1Y_CNT_MFOT'] = data['opened_last1Y_CNT_MFOT'].astype(object)
    data['opened_last2Y_CNT_MFOT'] = data['opened_last2Y_CNT_MFOT'].astype(object)
    data['opened_last3Y_CNT_MFOT'] = data['opened_last3Y_CNT_MFOT'].astype(object)

    data['opened_last3M_CNT_OTH'] = data['opened_last3M_CNT_OTH'].astype(object)
    data['opened_last6M_CNT_OTH'] = data['opened_last6M_CNT_OTH'].astype(object)
    data['opened_last9M_CNT_OTH'] = data['opened_last9M_CNT_OTH'].astype(object)
    data['opened_last1Y_CNT_OTH'] = data['opened_last1Y_CNT_OTH'].astype(object)
    data['opened_last2Y_CNT_OTH'] = data['opened_last2Y_CNT_OTH'].astype(object)
    data['opened_last3Y_CNT_OTH'] = data['opened_last3Y_CNT_OTH'].astype(object)

    data['opened_last3M_CNT_PLBL'] = data['opened_last3M_CNT_PLBL'].astype(object)
    data['opened_last6M_CNT_PLBL'] = data['opened_last6M_CNT_PLBL'].astype(object)
    data['opened_last9M_CNT_PLBL'] = data['opened_last9M_CNT_PLBL'].astype(object)
    data['opened_last1Y_CNT_PLBL'] = data['opened_last1Y_CNT_PLBL'].astype(object)
    data['opened_last2Y_CNT_PLBL'] = data['opened_last2Y_CNT_PLBL'].astype(object)
    data['opened_last3Y_CNT_PLBL'] = data['opened_last3Y_CNT_PLBL'].astype(object)

    data['opened_last3M_CNT_PLRLBL'] = data['opened_last3M_CNT_PLRLBL'].astype(object)
    data['opened_last6M_CNT_PLRLBL'] = data['opened_last6M_CNT_PLRLBL'].astype(object)
    data['opened_last9M_CNT_PLRLBL'] = data['opened_last9M_CNT_PLRLBL'].astype(object)
    data['opened_last1Y_CNT_PLRLBL'] = data['opened_last1Y_CNT_PLRLBL'].astype(object)
    data['opened_last2Y_CNT_PLRLBL'] = data['opened_last2Y_CNT_PLRLBL'].astype(object)
    data['opened_last3Y_CNT_PLRLBL'] = data['opened_last3Y_CNT_PLRLBL'].astype(object)

    data['opened_last3M_CNT_SEC'] = data['opened_last3M_CNT_SEC'].astype(object)
    data['opened_last6M_CNT_SEC'] = data['opened_last6M_CNT_SEC'].astype(object)
    data['opened_last9M_CNT_SEC'] = data['opened_last9M_CNT_SEC'].astype(object)
    data['opened_last1Y_CNT_SEC'] = data['opened_last1Y_CNT_SEC'].astype(object)
    data['opened_last2Y_CNT_SEC'] = data['opened_last2Y_CNT_SEC'].astype(object)
    data['opened_last3Y_CNT_SEC'] = data['opened_last3Y_CNT_SEC'].astype(object)

    data['opened_last3M_CNT_UNSEC'] = data['opened_last3M_CNT_UNSEC'].astype(object)
    data['opened_last6M_CNT_UNSEC'] = data['opened_last6M_CNT_UNSEC'].astype(object)
    data['opened_last9M_CNT_UNSEC'] = data['opened_last9M_CNT_UNSEC'].astype(object)
    data['opened_last1Y_CNT_UNSEC'] = data['opened_last1Y_CNT_UNSEC'].astype(object)
    data['opened_last2Y_CNT_UNSEC'] = data['opened_last2Y_CNT_UNSEC'].astype(object)
    data['opened_last3Y_CNT_UNSEC'] = data['opened_last3Y_CNT_UNSEC'].astype(object)

    def search_dt_cnt(i, j, accountType_var, startTime_Date, date_before_period, dateOpened_dateClosed_list,
                      accountType_list):
        count = 0
        # print(j)
        for p in range(len(accountType_list)):
            if accountType_list[p] == accountType_var and startTime_Date >= dateOpened_dateClosed_list[
                p] >= date_before_period and dateOpened_dateClosed_list[p] != "NaT":
                count = count + 1
        return count

    for i in range(data.shape[0]):
        opened_last3M_CNT_HL_val = 0
        opened_last6M_CNT_HL_val = 0
        opened_last9M_CNT_HL_val = 0
        opened_last1Y_CNT_HL_val = 0
        opened_last2Y_CNT_HL_val = 0
        opened_last3Y_CNT_HL_val = 0

        opened_last3M_CNT_GL_val = 0
        opened_last6M_CNT_GL_val = 0
        opened_last9M_CNT_GL_val = 0
        opened_last1Y_CNT_GL_val = 0
        opened_last2Y_CNT_GL_val = 0
        opened_last3Y_CNT_GL_val = 0

        opened_last3M_CNT_AL_val = 0
        opened_last6M_CNT_AL_val = 0
        opened_last9M_CNT_AL_val = 0
        opened_last1Y_CNT_AL_val = 0
        opened_last2Y_CNT_AL_val = 0
        opened_last3Y_CNT_AL_val = 0

        opened_last3M_CNT_LAS_val = 0
        opened_last6M_CNT_LAS_val = 0
        opened_last9M_CNT_LAS_val = 0
        opened_last1Y_CNT_LAS_val = 0
        opened_last2Y_CNT_LAS_val = 0
        opened_last3Y_CNT_LAS_val = 0

        opened_last3M_CNT_PL_val = 0
        opened_last6M_CNT_PL_val = 0
        opened_last9M_CNT_PL_val = 0
        opened_last1Y_CNT_PL_val = 0
        opened_last2Y_CNT_PL_val = 0
        opened_last3Y_CNT_PL_val = 0

        opened_last3M_CNT_CD_val = 0
        opened_last6M_CNT_CD_val = 0
        opened_last9M_CNT_CD_val = 0
        opened_last1Y_CNT_CD_val = 0
        opened_last2Y_CNT_CD_val = 0
        opened_last3Y_CNT_CD_val = 0

        opened_last3M_CNT_SEL_val = 0
        opened_last6M_CNT_SEL_val = 0
        opened_last9M_CNT_SEL_val = 0
        opened_last1Y_CNT_SEL_val = 0
        opened_last2Y_CNT_SEL_val = 0
        opened_last3Y_CNT_SEL_val = 0

        opened_last3M_CNT_RL_val = 0
        opened_last6M_CNT_RL_val = 0
        opened_last9M_CNT_RL_val = 0
        opened_last1Y_CNT_RL_val = 0
        opened_last2Y_CNT_RL_val = 0
        opened_last3Y_CNT_RL_val = 0

        opened_last3M_CNT_CV_val = 0
        opened_last6M_CNT_CV_val = 0
        opened_last9M_CNT_CV_val = 0
        opened_last1Y_CNT_CV_val = 0
        opened_last2Y_CNT_CV_val = 0
        opened_last3Y_CNT_CV_val = 0

        opened_last3M_CNT_CC_val = 0
        opened_last6M_CNT_CC_val = 0
        opened_last9M_CNT_CC_val = 0
        opened_last1Y_CNT_CC_val = 0
        opened_last2Y_CNT_CC_val = 0
        opened_last3Y_CNT_CC_val = 0

        opened_last3M_CNT_RL_val = 0
        opened_last6M_CNT_RL_val = 0
        opened_last9M_CNT_RL_val = 0
        opened_last1Y_CNT_RL_val = 0
        opened_last2Y_CNT_RL_val = 0
        opened_last3Y_CNT_RL_val = 0

        opened_last3M_CNT_SCC_val = 0
        opened_last6M_CNT_SCC_val = 0
        opened_last9M_CNT_SCC_val = 0
        opened_last1Y_CNT_SCC_val = 0
        opened_last2Y_CNT_SCC_val = 0
        opened_last3Y_CNT_SCC_val = 0

        opened_last3M_CNT_BL_val = 0
        opened_last6M_CNT_BL_val = 0
        opened_last9M_CNT_BL_val = 0
        opened_last1Y_CNT_BL_val = 0
        opened_last2Y_CNT_BL_val = 0
        opened_last3Y_CNT_BL_val = 0

        opened_last3M_CNT_MFBL_val = 0
        opened_last6M_CNT_MFBL_val = 0
        opened_last9M_CNT_MFBL_val = 0
        opened_last1Y_CNT_MFBL_val = 0
        opened_last2Y_CNT_MFBL_val = 0
        opened_last3Y_CNT_MFBL_val = 0

        opened_last3M_CNT_MFPL_val = 0
        opened_last6M_CNT_MFPL_val = 0
        opened_last9M_CNT_MFPL_val = 0
        opened_last1Y_CNT_MFPL_val = 0
        opened_last2Y_CNT_MFPL_val = 0
        opened_last3Y_CNT_MFPL_val = 0

        opened_last3M_CNT_MFHL_val = 0
        opened_last6M_CNT_MFHL_val = 0
        opened_last9M_CNT_MFHL_val = 0
        opened_last1Y_CNT_MFHL_val = 0
        opened_last2Y_CNT_MFHL_val = 0
        opened_last3Y_CNT_MFHL_val = 0

        opened_last3M_CNT_MFOT_val = 0
        opened_last6M_CNT_MFOT_val = 0
        opened_last9M_CNT_MFOT_val = 0
        opened_last1Y_CNT_MFOT_val = 0
        opened_last2Y_CNT_MFOT_val = 0
        opened_last3Y_CNT_MFOT_val = 0

        opened_last3M_CNT_PLBL_val = 0
        opened_last6M_CNT_PLBL_val = 0
        opened_last9M_CNT_PLBL_val = 0
        opened_last1Y_CNT_PLBL_val = 0
        opened_last2Y_CNT_PLBL_val = 0
        opened_last3Y_CNT_PLBL_val = 0

        opened_last3M_CNT_PLRLBL_val = 0
        opened_last6M_CNT_PLRLBL_val = 0
        opened_last9M_CNT_PLRLBL_val = 0
        opened_last1Y_CNT_PLRLBL_val = 0
        opened_last2Y_CNT_PLRLBL_val = 0
        opened_last3Y_CNT_PLRLBL_val = 0

        opened_last3M_CNT_OTH_val = 0
        opened_last6M_CNT_OTH_val = 0
        opened_last9M_CNT_OTH_val = 0
        opened_last1Y_CNT_OTH_val = 0
        opened_last2Y_CNT_OTH_val = 0
        opened_last3Y_CNT_OTH_val = 0

        opened_last3M_CNT_SEC_val = 0
        opened_last6M_CNT_SEC_val = 0
        opened_last9M_CNT_SEC_val = 0
        opened_last1Y_CNT_SEC_val = 0
        opened_last2Y_CNT_SEC_val = 0
        opened_last3Y_CNT_SEC_val = 0

        opened_last3M_CNT_UNSEC_val = 0
        opened_last6M_CNT_UNSEC_val = 0
        opened_last9M_CNT_UNSEC_val = 0
        opened_last1Y_CNT_UNSEC_val = 0
        opened_last2Y_CNT_UNSEC_val = 0
        opened_last3Y_CNT_UNSEC_val = 0

        for j in range(len(data['dateOpenedOrDisbursed'][i])):
            date_before_3M = data['startTime_Date'][i][j] + three_mon_rel
            date_before_6M = data['startTime_Date'][i][j] + six_mon_rel
            date_before_9M = data['startTime_Date'][i][j] + nine_mon_rel
            date_before_1Y = data['startTime_Date'][i][j] + one_year_rel
            date_before_2Y = data['startTime_Date'][i][j] + two_year_rel
            date_before_3Y = data['startTime_Date'][i][j] + three_year_rel

            if data['accountType'][i][j] == "HL":
                opened_last3M_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_HL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "GL":
                opened_last3M_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_GL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "AL":
                opened_last3M_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_AL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "LAS":
                opened_last3M_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last6M_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last9M_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last1Y_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last2Y_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last3Y_CNT_LAS_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])

            if data['accountType'][i][j] == "PL":
                opened_last3M_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_PL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "CD":
                opened_last3M_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_CD_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "SEL":
                opened_last3M_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last6M_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last9M_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last1Y_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last2Y_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last3Y_CNT_SEL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])

            if data['accountType'][i][j] == "CC":
                opened_last3M_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_CC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "RL":
                opened_last3M_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_RL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "CV":
                opened_last3M_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_CV_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "SCC":
                opened_last3M_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last6M_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last9M_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last1Y_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last2Y_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last3Y_CNT_SCC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])

            if data['accountType'][i][j] == "BL":
                opened_last3M_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last6M_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last9M_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last1Y_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last2Y_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])
                opened_last3Y_CNT_BL_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                         date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                         data['accountType'][i])

            if data['accountType'][i][j] == "MFBL":
                opened_last3M_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_6M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_9M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_1Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_2Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_MFBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][j] == "MFPL":
                opened_last3M_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_6M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_9M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_1Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_2Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_MFPL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][j] == "MFOT":
                opened_last3M_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_6M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_9M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_1Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_2Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_MFOT_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][j] == "PLBL":
                opened_last3M_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_6M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_9M,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_1Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_2Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_PLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                           data['startTime_Date'][i][j], date_before_3Y,
                                                           data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][j] == "PLRLBL":
                opened_last3M_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_3M,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_6M,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_9M,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_1Y,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_2Y,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_PLRLBL_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                             data['startTime_Date'][i][j], date_before_3Y,
                                                             data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][
                j] == "SECFor an applicant, count all the loan accounts which have been opened in last 1 year and gap between the open dates <=3 months":
                opened_last3M_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last6M_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last9M_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last1Y_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last2Y_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last3Y_CNT_SEC_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])

            if data['accountType'][i][j] == "UNSEC":
                opened_last3M_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_3M,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last6M_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_6M,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last9M_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_9M,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last1Y_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_1Y,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last2Y_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_2Y,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])
                opened_last3Y_CNT_UNSEC_val = search_dt_cnt(i, j, data['accountType'][i][j],
                                                            data['startTime_Date'][i][j], date_before_3Y,
                                                            data['dateOpenedOrDisbursed'][i], data['accountType'][i])

            if data['accountType'][i][j] == "OTH":
                opened_last3M_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last6M_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_6M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last9M_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_9M, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last1Y_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_1Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last2Y_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_2Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])
                opened_last3Y_CNT_OTH_val = search_dt_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j],
                                                          date_before_3Y, data['dateOpenedOrDisbursed'][i],
                                                          data['accountType'][i])

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_HL')] = opened_last3M_CNT_HL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_HL')] = opened_last6M_CNT_HL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_HL')] = opened_last9M_CNT_HL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_HL')] = opened_last1Y_CNT_HL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_HL')] = opened_last2Y_CNT_HL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_HL')] = opened_last3Y_CNT_HL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_GL')] = opened_last3M_CNT_GL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_GL')] = opened_last6M_CNT_GL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_GL')] = opened_last9M_CNT_GL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_GL')] = opened_last1Y_CNT_GL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_GL')] = opened_last2Y_CNT_GL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_GL')] = opened_last3Y_CNT_GL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_AL')] = opened_last3M_CNT_AL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_AL')] = opened_last6M_CNT_AL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_AL')] = opened_last9M_CNT_AL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_AL')] = opened_last1Y_CNT_AL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_AL')] = opened_last2Y_CNT_AL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_AL')] = opened_last3Y_CNT_AL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_LAS')] = opened_last3M_CNT_LAS_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_LAS')] = opened_last6M_CNT_LAS_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_LAS')] = opened_last9M_CNT_LAS_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_LAS')] = opened_last1Y_CNT_LAS_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_LAS')] = opened_last2Y_CNT_LAS_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_LAS')] = opened_last3Y_CNT_LAS_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_PL')] = opened_last3M_CNT_PL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_PL')] = opened_last6M_CNT_PL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_PL')] = opened_last9M_CNT_PL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_PL')] = opened_last1Y_CNT_PL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_PL')] = opened_last2Y_CNT_PL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_PL')] = opened_last3Y_CNT_PL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_CD')] = opened_last3M_CNT_CD_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_CD')] = opened_last6M_CNT_CD_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_CD')] = opened_last9M_CNT_CD_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_CD')] = opened_last1Y_CNT_CD_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_CD')] = opened_last2Y_CNT_CD_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_CD')] = opened_last3Y_CNT_CD_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_SEL')] = opened_last3M_CNT_SEL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_SEL')] = opened_last6M_CNT_SEL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_SEL')] = opened_last9M_CNT_SEL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_SEL')] = opened_last1Y_CNT_SEL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_SEL')] = opened_last2Y_CNT_SEL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_SEL')] = opened_last3Y_CNT_SEL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_CC')] = opened_last3M_CNT_CC_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_CC')] = opened_last6M_CNT_CC_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_CC')] = opened_last9M_CNT_CC_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_CC')] = opened_last1Y_CNT_CC_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_CC')] = opened_last2Y_CNT_CC_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_CC')] = opened_last3Y_CNT_CC_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_RL')] = opened_last3M_CNT_RL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_RL')] = opened_last6M_CNT_RL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_RL')] = opened_last9M_CNT_RL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_RL')] = opened_last1Y_CNT_RL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_RL')] = opened_last2Y_CNT_RL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_RL')] = opened_last3Y_CNT_RL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_CV')] = opened_last3M_CNT_CV_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_CV')] = opened_last6M_CNT_CV_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_CV')] = opened_last9M_CNT_CV_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_CV')] = opened_last1Y_CNT_CV_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_CV')] = opened_last2Y_CNT_CV_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_CV')] = opened_last3Y_CNT_CV_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_SCC')] = opened_last3M_CNT_SCC_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_SCC')] = opened_last6M_CNT_SCC_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_SCC')] = opened_last9M_CNT_SCC_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_SCC')] = opened_last1Y_CNT_SCC_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_SCC')] = opened_last2Y_CNT_SCC_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_SCC')] = opened_last3Y_CNT_SCC_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_BL')] = opened_last3M_CNT_BL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_BL')] = opened_last6M_CNT_BL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_BL')] = opened_last9M_CNT_BL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_BL')] = opened_last1Y_CNT_BL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_BL')] = opened_last2Y_CNT_BL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_BL')] = opened_last3Y_CNT_BL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_MFBL')] = opened_last3M_CNT_MFBL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_MFBL')] = opened_last6M_CNT_MFBL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_MFBL')] = opened_last9M_CNT_MFBL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_MFBL')] = opened_last1Y_CNT_MFBL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_MFBL')] = opened_last2Y_CNT_MFBL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_MFBL')] = opened_last3Y_CNT_MFBL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_MFPL')] = opened_last3M_CNT_MFPL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_MFPL')] = opened_last6M_CNT_MFPL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_MFPL')] = opened_last9M_CNT_MFPL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_MFPL')] = opened_last1Y_CNT_MFPL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_MFPL')] = opened_last2Y_CNT_MFPL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_MFPL')] = opened_last3Y_CNT_MFPL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_MFHL')] = opened_last3M_CNT_MFHL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_MFHL')] = opened_last6M_CNT_MFHL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_MFHL')] = opened_last9M_CNT_MFHL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_MFHL')] = opened_last1Y_CNT_MFHL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_MFHL')] = opened_last2Y_CNT_MFHL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_MFHL')] = opened_last3Y_CNT_MFHL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_MFOT')] = opened_last3M_CNT_MFOT_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_MFOT')] = opened_last6M_CNT_MFOT_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_MFOT')] = opened_last9M_CNT_MFOT_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_MFOT')] = opened_last1Y_CNT_MFOT_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_MFOT')] = opened_last2Y_CNT_MFOT_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_MFOT')] = opened_last3Y_CNT_MFOT_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_PLBL')] = opened_last3M_CNT_PLBL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_PLBL')] = opened_last6M_CNT_PLBL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_PLBL')] = opened_last9M_CNT_PLBL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_PLBL')] = opened_last1Y_CNT_PLBL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_PLBL')] = opened_last2Y_CNT_PLBL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_PLBL')] = opened_last3Y_CNT_PLBL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_PLRLBL')] = opened_last3M_CNT_PLRLBL_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_PLRLBL')] = opened_last6M_CNT_PLRLBL_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_PLRLBL')] = opened_last9M_CNT_PLRLBL_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_PLRLBL')] = opened_last1Y_CNT_PLRLBL_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_PLRLBL')] = opened_last2Y_CNT_PLRLBL_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_PLRLBL')] = opened_last3Y_CNT_PLRLBL_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_SEC')] = opened_last3M_CNT_SEC_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_SEC')] = opened_last6M_CNT_SEC_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_SEC')] = opened_last9M_CNT_SEC_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_SEC')] = opened_last1Y_CNT_SEC_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_SEC')] = opened_last2Y_CNT_SEC_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_SEC')] = opened_last3Y_CNT_SEC_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_UNSEC')] = opened_last3M_CNT_UNSEC_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_UNSEC')] = opened_last6M_CNT_UNSEC_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_UNSEC')] = opened_last9M_CNT_UNSEC_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_UNSEC')] = opened_last1Y_CNT_UNSEC_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_UNSEC')] = opened_last2Y_CNT_UNSEC_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_UNSEC')] = opened_last3Y_CNT_UNSEC_val

        data.iat[i, data.columns.get_loc('opened_last3M_CNT_OTH')] = opened_last3M_CNT_OTH_val
        data.iat[i, data.columns.get_loc('opened_last6M_CNT_OTH')] = opened_last6M_CNT_OTH_val
        data.iat[i, data.columns.get_loc('opened_last9M_CNT_OTH')] = opened_last9M_CNT_OTH_val
        data.iat[i, data.columns.get_loc('opened_last1Y_CNT_OTH')] = opened_last1Y_CNT_OTH_val
        data.iat[i, data.columns.get_loc('opened_last2Y_CNT_OTH')] = opened_last2Y_CNT_OTH_val
        data.iat[i, data.columns.get_loc('opened_last3Y_CNT_OTH')] = opened_last3Y_CNT_OTH_val

        data['dateOpened_gap3M_last1Y_CNT'] = 0
        data['dateOpened_gap3M_last2Y_CNT'] = 0
        data['dateOpened_gap3M_last3Y_CNT'] = 0
        data['dateOpened_gap6M_last1Y_CNT'] = 0
        data['dateOpened_gap6M_last2Y_CNT'] = 0
        data['dateOpened_gap6M_last3Y_CNT'] = 0

        data['dateOpened_gap3M_last1Y_CNT'] = data['dateOpened_gap3M_last1Y_CNT'].astype(object)
        data['dateOpened_gap3M_last2Y_CNT'] = data['dateOpened_gap3M_last2Y_CNT'].astype(object)
        data['dateOpened_gap3M_last3Y_CNT'] = data['dateOpened_gap3M_last3Y_CNT'].astype(object)
        data['dateOpened_gap6M_last1Y_CNT'] = data['dateOpened_gap6M_last1Y_CNT'].astype(object)
        data['dateOpened_gap6M_last2Y_CNT'] = data['dateOpened_gap6M_last2Y_CNT'].astype(object)
        data['dateOpened_gap6M_last3Y_CNT'] = data['dateOpened_gap6M_last3Y_CNT'].astype(object)

        gap_three_mon_rel = relativedelta(months=3)
        gap_six_mon_rel = relativedelta(months=6)

        def common_elements(list1, list2):
            return len([element for element in list1 if element in list2])

        def search_dt_gap_cnt(i, j, accountType_var, startTime_Date, date_before_period, dateOpened_dateClosed_list,
                              accountType_list, gap_month_relative):
            opened_last_list = []
            time_range = []
            count = 0

            for p in range(len(accountType_list)):
                if startTime_Date > dateOpened_dateClosed_list[p] >= date_before_period and dateOpened_dateClosed_list[
                    p] != "NaT":
                    opened_last_list.append(dateOpened_dateClosed_list[p])

            opened_last_list = sorted(opened_last_list)
            opened_last_list_len = len(opened_last_list)

            gap_month_relative = relativedelta(months=3)

            # datesx = [[] for i in range(len(opened_last_list))]
            # opened_last_list[q]=str(opened_last_list[q])

            # opened_last_list = [dt.datetime.strptime(date, "%Y-%m-%d").date for date in opened_last_list]

            for q in range(len(opened_last_list)):

                gap_month_period = opened_last_list[q] + gap_month_relative
                # gap_month_period = dt.datetime.strptime(opened_last_list[q], "%Y-%m-%d") + gap_month_relative

                for s in range(q + 1, opened_last_list_len):
                    if opened_last_list[s] != '1111-01-01' and gap_month_period > opened_last_list[s] >= \
                            opened_last_list[q]:
                        opened_last_list[s] = dt.datetime(1111, 1, 1).date
                        count = count + 1

            #         gap_month_period=str(gap_month_period)
            #         opened_last_list[q]=str(opened_last_list[q])
            #         datesx[q] = list(rrule.rrule(rrule.DAILY, dtstart=parser.parse(opened_last_list[q]), until=parser.parse(gap_month_period)))

            #     opened_last_list = [dt.datetime.strptime(date, "%Y-%m-%d") for date in opened_last_list]

            #     date_list = []
            #     for s in range(opened_last_list_len):
            #         date_list = date_list + datesx[s]

            #     date_list.sort()

            #     count = common_elements(opened_last_list,date_list)

            return count

        def diff_month(d1, d2):
            return (d1.year - d2.year) * 12 + d1.month - d2.month

        from itertools import combinations
        month_day_dict = {"1": 30, "2": 60, "3": 90, "4": 120, "5": 150, "6": 180}
        def get_month_gap_cout(year_gap_list, no_of_months, gapMVariable):
            days = month_day_dict[str(no_of_months)]

            datepair = [i for i in combinations(year_gap_list, 2)]
            for pair in datepair:
                diiff_days = (pd.to_datetime(pair[0]) - pd.to_datetime(pair[1])).days
                if (diiff_days >= -90) and (diiff_days <= days):
                    gapMVariable = gapMVariable + 1

            return gapMVariable

        def get_year_mask(datefeatureframe, datetocompaire):
            mask = (pd.to_datetime(datefeatureframe) > pd.to_datetime(datetocompaire)) & (
                        pd.to_datetime(datefeatureframe) != "NaT")
            return mask
        import datetime
        for i in range(data.shape[0]):
            dateOpened_gap3M_last1Y_CNT_val = 0
            dateOpened_gap3M_last2Y_CNT_val = 0
            dateOpened_gap3M_last3Y_CNT_val = 0
            dateOpened_gap6M_last1Y_CNT_val = 0
            dateOpened_gap6M_last2Y_CNT_val = 0
            dateOpened_gap6M_last3Y_CNT_val = 0

            date_data = pd.DataFrame({'dateOpenedOrDisbursed': pd.to_datetime(data['dateOpenedOrDisbursed'][i])})
            date_before_1Y = data['startTime_Date'][i][0] + one_year_rel
            date_before_2Y = data['startTime_Date'][i][0] + two_year_rel
            date_before_3Y = data['startTime_Date'][i][0] + three_year_rel
            # mask = (date_data['dateOpenedOrDisbursed'] < date_before_1Y) & (date_data['dateOpenedOrDisbursed'] != "NaT")
            mask1Y = get_year_mask(data['dateOpenedOrDisbursed'][i], date_before_1Y)
            mask2Y = get_year_mask(data['dateOpenedOrDisbursed'][i], date_before_2Y)
            mask3Y = get_year_mask(data['dateOpenedOrDisbursed'][i], date_before_3Y)

            filtered_df1Y = sorted(
                pd.DataFrame({"dateOpenedOrDisbursed": date_data['dateOpenedOrDisbursed'].loc[mask1Y]})['dateOpenedOrDisbursed'])
            filtered_df2Y = sorted(
                pd.DataFrame({"dateOpenedOrDisbursed": date_data['dateOpenedOrDisbursed'].loc[mask2Y]})['dateOpenedOrDisbursed'])
            filtered_df3Y = sorted(
                pd.DataFrame({"dateOpenedOrDisbursed": date_data['dateOpenedOrDisbursed'].loc[mask3Y]})['dateOpenedOrDisbursed'])

            dateOpened_gap3M_last1Y_CNT_val = get_month_gap_cout(filtered_df1Y, 3, dateOpened_gap3M_last1Y_CNT_val)
            dateOpened_gap3M_last2Y_CNT_val = get_month_gap_cout(filtered_df2Y, 3, dateOpened_gap3M_last2Y_CNT_val)
            dateOpened_gap3M_last3Y_CNT_val = get_month_gap_cout(filtered_df3Y, 3, dateOpened_gap3M_last3Y_CNT_val)
            # from itertools import combinations
            # combinatio= [",".join(map(str, comb)) for comb in combinations(opened_last_list, 2)]

            #print(filtered_df)
            for j in range(len(data['dateOpenedOrDisbursed'][i])):
                date_before_1Y = data['startTime_Date'][i][j] + one_year_rel
                date_before_2Y = data['startTime_Date'][i][j] + two_year_rel
                date_before_3Y = data['startTime_Date'][i][j] + three_year_rel
                date_before_1Y = data['startTime_Date'][i][0] + one_year_rel
                mask = (data['dateOpenedOrDisbursed'] < date_before_1Y) & (data['dateOpenedOrDisbursed'] != "NaT")
                # dateOpened_gap3M_last1Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j], date_before_1Y, data['dateOpenedOrDisbursed'][i], data['accountType'][i], gap_three_mon_rel)
                # dateOpened_gap3M_last2Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j], date_before_2Y, data['dateOpenedOrDisbursed'][i], data['accountType'][i], gap_three_mon_rel)
                # dateOpened_gap3M_last3Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j], date_before_3Y, data['dateOpenedOrDisbursed'][i], data['accountType'][i], gap_three_mon_rel)
                # dateOpened_gap6M_last1Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j], date_before_1Y, data['dateOpenedOrDisbursed'][i], data['accountType'][i], gap_six_mon_rel)
                # dateOpened_gap6M_last2Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j], data['startTime_Date'][i][j], date_before_2Y, data['dateOpenedOrDisbursed'][i], data['accountType'][i], gap_six_mon_rel)
                dateOpened_gap6M_last3Y_CNT_val = search_dt_gap_cnt(i, j, data['accountType'][i][j],
                                                                    data['startTime_Date'][i][j], date_before_3Y,
                                                                    data['dateOpenedOrDisbursed'][i],
                                                                    data['accountType'][i], gap_six_mon_rel)

            data.iat[i, data.columns.get_loc('dateOpened_gap3M_last1Y_CNT')] = dateOpened_gap3M_last1Y_CNT_val
            data.iat[i, data.columns.get_loc('dateOpened_gap3M_last2Y_CNT')] = dateOpened_gap3M_last2Y_CNT_val
            data.iat[i, data.columns.get_loc('dateOpened_gap3M_last3Y_CNT')] = dateOpened_gap3M_last3Y_CNT_val
            data.iat[i, data.columns.get_loc('dateOpened_gap6M_last1Y_CNT')] = dateOpened_gap6M_last1Y_CNT_val
            data.iat[i, data.columns.get_loc('dateOpened_gap6M_last2Y_CNT')] = dateOpened_gap6M_last2Y_CNT_val
            data.iat[i, data.columns.get_loc('dateOpened_gap6M_last3Y_CNT')] = dateOpened_gap6M_last3Y_CNT_val


if __name__ == '__main__':
    run()