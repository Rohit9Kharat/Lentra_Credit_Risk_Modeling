import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
import time
from dask import delayed
import warnings

# Time starts
start_time_ut = time.time()  # You can use time.clock() also

test_df = pd.read_csv('cibil_test.csv')
test_df.shape
df = test_df[test_df['bureauName'] == 'CIBIL']
df.reset_index(drop=True, inplace=True)

warnings.filterwarnings("ignore")

# Function for checking if the string is number


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# Function for calculating the month difference


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# Function for Unique ID list


def get_unique_values(values):
    unique = []
    for piece in values:
        if piece not in unique:
            unique.append(piece)
    return unique

# Function to calculate no. of days


def numOfDays(date1, date2):
    return (date2-date1).days


id_list = list(df['ID'].values)
unq_id_list = get_unique_values(id_list)
# unq_id_list = unq_id_list.compute()


# Filling missing values
df['paymentHist1'].fillna('missing', inplace=True)
df['paymentHist2'].fillna('missing', inplace=True)
df['writtenOffAndSettledStatus'].fillna('unknown', inplace=True)

# Concatenate payment history strings
df['paymentHistComp'] = df['paymentHist1'].map(
    str) + df['paymentHist2'].map(str)

# Handling date fields
df['PHED'] = df['PHED'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
df['PHSD'] = df['PHSD'].apply(lambda x: x if pd.isnull(x) else str(int(x)))
df['dateClosed'] = df['dateClosed'].apply(
    lambda x: x if pd.isnull(x) else str(int(x)))
df['dateReportedAndCertified'] = df['dateReportedAndCertified'].apply(
    lambda x: x if pd.isnull(x) else str(int(x)))
df['dateOpenedOrDisbursed'] = df['dateOpenedOrDisbursed'].apply(
    lambda x: x if pd.isnull(x) else str(int(x)))
df['PHED'] = df['PHED'].astype(str).apply(lambda x: x.zfill(8))
df['PHSD'] = df['PHSD'].astype(str).apply(lambda x: x.zfill(8))
df['dateClosed'] = df['dateClosed'].astype(str).apply(lambda x: x.zfill(8))
df['dateReportedAndCertified'] = df['dateReportedAndCertified'].astype(
    str).apply(lambda x: x.zfill(8))
df['dateOpenedOrDisbursed'] = df['dateOpenedOrDisbursed'].astype(
    str).apply(lambda x: x.zfill(8))
df['PHED'] = df['PHED'].apply(
    lambda x: 'unknown' if x == '00000nan' else dt.datetime.strptime(x, '%d%m%Y'))
df['PHSD'] = df['PHSD'].apply(
    lambda x: 'unknown' if x == '00000nan' else dt.datetime.strptime(x, '%d%m%Y'))
df['dateClosed'] = df['dateClosed'].apply(
    lambda x: 'unknown' if x == '00000nan' else dt.datetime.strptime(x, '%d%m%Y'))
df['dateReportedAndCertified'] = df['dateReportedAndCertified'].apply(
    lambda x: 'unknown' if x == '00000nan' else dt.datetime.strptime(x, '%d%m%Y'))
df['dateOpenedOrDisbursed'] = df['dateOpenedOrDisbursed'].apply(
    lambda x: 'unknown' if x == '00000nan' else dt.datetime.strptime(x, '%d%m%Y'))
df['PHED'] = pd.to_datetime(df['PHED'], errors='coerce').dt.date
df['PHSD'] = pd.to_datetime(df['PHSD'], errors='coerce').dt.date
df['dateClosed'] = pd.to_datetime(df['dateClosed'], errors='coerce').dt.date
df['dateReportedAndCertified'] = pd.to_datetime(
    df['dateReportedAndCertified'], errors='coerce').dt.date
df['dateOpenedOrDisbursed'] = pd.to_datetime(
    df['dateOpenedOrDisbursed'], errors='coerce').dt.date
df['loginDate'] = df['loginDate'].str.replace('Z', '')
df['loginDate'] = df['loginDate'].str.replace('{', '')
df['loginDate'] = df['loginDate'].str.replace('}', '')
df['loginDate'] = df['loginDate'].str.replace('"', '')
df['loginDate'] = df['loginDate'].str.replace('T', '')
df['loginDate'] = pd.to_datetime(df['loginDate'], format='%Y-%m-%d%H:%M:%S.%f')
df['loginDate'] = pd.to_datetime(df['loginDate'], errors='coerce').dt.date

# Sorted Dataframe according to 'dateReportedAndCertified'

df2 = pd.DataFrame()
grp_df = df.groupby('ID')
for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    grp_slice.reset_index(drop=True, inplace=True)
    grp_slice.sort_values(by='dateReportedAndCertified',
                          inplace=True, ascending=False)
    grp_slice.reset_index(drop=True, inplace=True)
    df2 = df2.append(grp_slice)
df = df2.copy()
df.reset_index(drop=True, inplace=True)

# Code for dateClosed_lt_PHED
days_diff = list()
dateClosed_lt_PHED = list()
for x in range(0, df.shape[0]):
    if pd.isnull(df['dateClosed'][x]) or pd.isnull(df['PHED'][x]):
        days_diff.append('unknown')
    else:
        date1 = df['PHED'][x]
        date2 = df['dateClosed'][x]
        days_diff.append(numOfDays(date1, date2))
df['days_diff'] = pd.Series(days_diff).values

for x in range(0, df.shape[0]):
    if pd.isnull(df['dateClosed'][x]) or pd.isnull(df['PHED'][x]):
        dateClosed_lt_PHED.append('unknown')
    elif (df['days_diff'][x] >= 0):
        dateClosed_lt_PHED.append(0)
    else:
        dateClosed_lt_PHED.append(1)
df['dateClosed_lt_PHED'] = pd.Series(dateClosed_lt_PHED).values
df.drop(['days_diff'], axis=1, inplace=True)

# Code for ignore_case
piece = list()
ign_case = list()
for x in range(0, df.shape[0]):
    # df[df['paymentHist1']=='missing']['paymentHist2'].value_counts()
    if df['paymentHist1'][x] == 'missing':
        ign_case.append('unknown')
    elif df['paymentHist2'][x] == 'missing':
        if len(set(df['paymentHist1'][x])) == 1 and (list(set(df['paymentHist1'][x]))[0] == 'X') and (df['dateClosed_lt_PHED'][x] == 1):
            ign_case.append(1)
        else:
            ign_case.append(0)
    elif len(set(df['paymentHistComp'][x])) == 1 and (list(set(df['paymentHistComp'][x]))[0] == 'X') and (df['dateClosed_lt_PHED'][x] == 1):
        ign_case.append(1)
    else:
        ign_case.append(0)
df['ignore_case'] = pd.Series(ign_case).values

# Code for payHistComp
piece = list()
comp_list = list()
for value in df['paymentHistComp']:
    chunks, chunk_size = len(value), 3
    for i in range(0, chunks, chunk_size):
        piece.append(value[i:i+chunk_size])
    comp_list.append(piece)
    piece = list()
df['payHistComp'] = pd.Series(comp_list).values

# Code for writeOff and restructured

start_time = time.time()

writeOff = list()
restructured = list()

for value in df['writtenOffAndSettledStatus']:
    if (value == 0) or (value == 1):
        restructured.append(1)
    elif (value == 'unknown'):
        restructured.append('unknown')
    else:
        restructured.append(0)

    if (value != 0) and (value != 1) and (value != 'unknown'):
        writeOff.append(1)
    elif (value == 'unknown'):
        writeOff.append('unknown')
    else:
        writeOff.append(0)

df['writeOff'] = pd.Series(writeOff).values
df['restructured'] = pd.Series(restructured).values

# Code for month_diff

month_diff = list()
month_diff_ps_pe = list()

for x in range(0, df.shape[0]):
    if (df['dateReportedAndCertified'][x] == 'unknown'):
        month_diff.append('unknown')
    else:
        mo_diff = diff_month(df['loginDate'][x],
                             df['dateReportedAndCertified'][x])
        month_diff.append(mo_diff)

    if pd.isnull(df['PHSD'][x]) or pd.isnull(df['PHED'][x]):
        month_diff_ps_pe.append('unknown')
    else:
        date1 = df['PHED'][x]
        date2 = df['PHSD'][x]
        mo_diff = diff_month(date2, date1)
        month_diff_ps_pe.append(mo_diff)

df['month_diff'] = pd.Series(month_diff).values
df['month_diff_ps_pe'] = pd.Series(month_diff_ps_pe).values


# Handling missing values
df['dateClosed'].fillna('unknown', inplace=True)
df['currentBalance'].fillna('unknown', inplace=True)
df['sanctionAmount'].fillna('unknown', inplace=True)
df['creditLimit'].fillna('unknown', inplace=True)
df['writtenOffAmountPrincipal'].fillna('unknown', inplace=True)
df['dateOpenedOrDisbursed'].fillna('unknown', inplace=True)
df['overdueAmount'].fillna('unknown', inplace=True)
df['suitFiledOrWilfulDefault'].fillna('unknown', inplace=True)

# Code

mo_diff_do_ld = list()
Overdue_Current = list()
Overdue_Disbursed = list()
dateClosed_lt_PHED_wo = list()
dateClosed_lt_PHED_suit = list()
dateClosed_lt_PHED_PH1M = list()
dateClosed_lt_PHED_restruct = list()

for x in range(0, df.shape[0]):
    if (df['dateOpenedOrDisbursed'][x] == 'unknown'):
        mo_diff_do_ld.append('unknown')
    else:
        mo_diff = diff_month(df['loginDate'][x],
                             df['dateOpenedOrDisbursed'][x])
        mo_diff_do_ld.append(mo_diff)

    if (df['overdueAmount'][x] == 'unknown') or (df['currentBalance'][x] == 'unknown') or (df['currentBalance'][x] == 0):
        Overdue_Current.append('unknown')
    else:
        Overdue_Current.append(
            float(df['overdueAmount'][x])/float(df['currentBalance'][x]))

    if (df['overdueAmount'][x] == 'unknown') or (df['sanctionAmount'][x] == 'unknown') or (df['sanctionAmount'][x] == 0):
        Overdue_Disbursed.append('unknown')
    else:
        Overdue_Disbursed.append(
            float(df['overdueAmount'][x])/float(df['sanctionAmount'][x]))

    if (df['dateClosed_lt_PHED'][x] == 1) and (df['writeOff'][x] == 1) and (df['writtenOffAndSettledStatus'][x] != 'unknown'):
        dateClosed_lt_PHED_wo.append(1)
    elif (df['writtenOffAndSettledStatus'][x] == 'unknown'):
        dateClosed_lt_PHED_wo.append('unknown')
    else:
        dateClosed_lt_PHED_wo.append(0)

    if (df['dateClosed_lt_PHED'][x] == 1) and (df['suitFiledOrWilfulDefault'][x] == 1):
        dateClosed_lt_PHED_suit.append(1)
    elif (df['suitFiledOrWilfulDefault'][x] == 'unknown'):
        dateClosed_lt_PHED_suit.append('unknown')
    else:
        dateClosed_lt_PHED_suit.append(0)

    if df['month_diff_ps_pe'][x] == 'unknown':
        dateClosed_lt_PHED_PH1M.append('unknown')
    elif (df['month_diff_ps_pe'][x] == 1) and (df['dateClosed_lt_PHED'][x] == 1):
        dateClosed_lt_PHED_PH1M.append(1)
    else:
        dateClosed_lt_PHED_PH1M.append(0)

    if (df['restructured'][x] == 1) and (df['dateClosed_lt_PHED'][x] == 1):
        dateClosed_lt_PHED_restruct.append(1)
    elif (df['restructured'][x] == 'unknown') or (df['dateClosed_lt_PHED'][x] == 'unknown'):
        dateClosed_lt_PHED_restruct.append('unknown')
    else:
        dateClosed_lt_PHED_restruct.append(0)

df['mo_diff_do_ld'] = pd.Series(mo_diff_do_ld).values
df['Overdue_Current'] = pd.Series(Overdue_Current).values
df['Overdue_Disbursed'] = pd.Series(Overdue_Disbursed).values
df['dateClosed_lt_PHED_wo'] = pd.Series(dateClosed_lt_PHED_wo).values
df['dateClosed_lt_PHED_suit'] = pd.Series(dateClosed_lt_PHED_suit).values
df['dateClosed_lt_PHED_PH1M'] = pd.Series(dateClosed_lt_PHED_PH1M).values
df['dateClosed_lt_PHED_restruct'] = pd.Series(
    dateClosed_lt_PHED_restruct).values

# dictAccountType
sec_L = [0, 1, 2, 3, 4, 7, 11, 13, 15, 16, 17, 31,
         32, 33, 34, 42, 43, 44, 50, 54, 58, 59, 98]
unsec_L = [5, 6, 8, 9, 35, 36, 37, 39, 40, 41, 51, 52, 53, 56, 57, 61, 99]
bureau_accType_dict = {0: "OTH", 1: "AL", 2: "HL", 3: "HL", 4: "LAS", 5: "PL", 6: "CD",
                       7: "GL", 8: "PL", 9: "SEL", 10: "CC", 11: "HL", 12: "RL",
                       13: "AL", 14: "RL", 15: "LAS", 16: "CV", 17: "CV",
                       31: "CC", 32: "AL", 33: "CV", 34: "CV", 35: "SCC", 36: "SCC",
                       37: "PL", 38: "RL", 39: "BL", 40: "MFBL", 41: "MFPL", 42: "MFHL",
                       43: "MFOT", 44: "HL", 50: "BL", 51: "BL", 52: "PLBL", 53: "PLBL",
                       54: "PLBL", 55: "RL", 56: "PLRLBL", 57: "PLRLBL", 58: "PLRLBL",
                       59: "BL", 61: "BL", 98: "SEC", 99: "UNSEC"}

a = np.ones(4462)
df['dictAccountType'] = pd.Series(a).values
df['dictAccountType'] = df.replace(
    {"accountType": bureau_accType_dict})['accountType']
df['dictAccountType'].fillna('unknown', inplace=True)

# First Sequential Code
grp_df = df.groupby('ID')

dateClosed_lt_PHED_CNT = list()
count_list_dt_phed = list()
count_dt_phed = 0

ignore_case_CNT = list()
count_list_ic = list()
count_ic = 0

sumCurrentBalance = list()
sumSanctionAmount = list()
sumCreditLimit = list()

sum_cur_bal = list()
sum_sanc_amt = list()
sum_cred_lmt = list()

curr_bal = 0
sanc_amt = 0
cred_lmt = 0

currentBalance_sanctionedAmount_NCC_L = list()
ratio_list_cu_sa_ncc_l = list()
ratio_cu_sa_ncc_l = 0

mode_util_CC_L = list()
ratio_list_mode_util = list()
ratio_mode_util = 0

mean_util_CC_L = list()
ratio_list_mean_util = list()
ratio_mean_util = 0

median_util_CC_L = list()
ratio_list_med_util = list()
ratio_med_util = 0

min_util_CC_L = list()
ratio_list_min_util = list()
ratio_min_util = 0

mean_util_highCredit_CC_L = list()
ratio_list_mean_util_hi_cred = list()
ratio_mean_util_hi_cred = 0

mode_util_highCredit_CC_L = list()
ratio_list_mode_util_hi_cred = list()
ratio_mode_util_hi_cred = 0

median_util_highCredit_CC_L = list()
ratio_list_med_util_hi_cr = list()
ratio_med_util_hi_cr = 0

min_util_highCredit_CC_L = list()
ratio_list_min_util_hi_cr = list()
ratio_min_util_hi_cr = 0

mean_util_highCredit_CC_A = list()
ratio_list_mean_util_hi_cr_a = list()
ratio_mean_util_hi_cr_a = 0

mode_util_highCredit_CC_A = list()
ratio_list_mode_util_hi_cr_a = list()
ratio_mode_util_hi_cr_a = 0

median_util_highCredit_CC_A = list()
ratio_list_med_util_hi_cr_a = list()
ratio_med_util_hi_cr_a = 0

min_util_highCredit_CC_A = list()
ratio_list_min_util_hi_cr_a = list()
ratio_min_util_hi_cr_a = 0

Mean_SancAmt = list()
sanc_amt_list_mean = list()
sanc_amt_mean = 0

Mean_SancAmt_L = list()
sanc_amt_list_L_mean = list()
sanc_amt_L_mean = 0

Median_SancAmt = list()
sanc_amt_list_med = list()
sanc_amt_med = 0

Median_SancAmt_L = list()
sanc_amt_list_L_med = list()
sanc_amt_L_med = 0

Mode_SancAmt = list()
sanc_amt_list_mode = list()
sanc_amt_mode = 0

Mode_SancAmt_L = list()
sanc_amt_list_L_mode = list()
sanc_amt_L_mode = 0

Secured_CNT = list()
Unsecured_CNT = list()

sec_cnt_list = list()
sec_cnt = 0

unsec_cnt_list = list()
unsec_cnt = 0

Loans_Sec_UnsecwoRLCC_L = list()
Per_Sec_UnsecwoRLCC_L = list()

sec_L_cnt = 0
sec_L_cnt_list = list()

unsec_L_cnt = 0
unsec_L_cnt_list = list()

Mean_SancAmt_AL = list()
Mean_SancAmt_BL = list()
Mean_SancAmt_CD = list()
Mean_SancAmt_CV = list()
Mean_SancAmt_GL = list()
Mean_SancAmt_HL = list()
Mean_SancAmt_LAS = list()
Mean_SancAmt_MFBL = list()
Mean_SancAmt_MFHL = list()
Mean_SancAmt_MFOT = list()
Mean_SancAmt_OTH = list()
Mean_SancAmt_PL = list()
Mean_SancAmt_PLBL = list()
Mean_SancAmt_RL = list()
Mean_SancAmt_SEL = list()

sanc_amt_mean_list_AL = list()
sanc_amt_mean_list_BL = list()
sanc_amt_mean_list_CD = list()
sanc_amt_mean_list_CV = list()
sanc_amt_mean_list_GL = list()
sanc_amt_mean_list_HL = list()
sanc_amt_mean_list_LAS = list()
sanc_amt_mean_list_MFBL = list()
sanc_amt_mean_list_MFHL = list()
sanc_amt_mean_list_MFOT = list()
sanc_amt_mean_list_OTH = list()
sanc_amt_mean_list_PL = list()
sanc_amt_mean_list_PLBL = list()
sanc_amt_mean_list_RL = list()
sanc_amt_mean_list_SEL = list()

sanc_amt_mean_AL = list()
sanc_amt_mean_BL = list()
sanc_amt_mean_CD = list()
sanc_amt_mean_CV = list()
sanc_amt_mean_GL = list()
sanc_amt_mean_HL = list()
sanc_amt_mean_LAS = list()
sanc_amt_mean_MFBL = list()
sanc_amt_mean_MFHL = list()
sanc_amt_mean_MFOT = list()
sanc_amt_mean_OTH = list()
sanc_amt_mean_PL = list()
sanc_amt_mean_PLBL = list()
sanc_amt_mean_RL = list()
sanc_amt_mean_SEL = list()

Mean_SancAmt_L_AL = list()
Mean_SancAmt_L_BL = list()
Mean_SancAmt_L_CD = list()
Mean_SancAmt_L_CV = list()
Mean_SancAmt_L_GL = list()
Mean_SancAmt_L_HL = list()
Mean_SancAmt_L_LAS = list()
Mean_SancAmt_L_MFBL = list()
Mean_SancAmt_L_MFHL = list()
Mean_SancAmt_L_MFOT = list()
Mean_SancAmt_L_OTH = list()
Mean_SancAmt_L_PL = list()
Mean_SancAmt_L_PLBL = list()
Mean_SancAmt_L_RL = list()
Mean_SancAmt_L_SEL = list()

sanc_amt_L_mean_list_AL = list()
sanc_amt_L_mean_list_BL = list()
sanc_amt_L_mean_list_CD = list()
sanc_amt_L_mean_list_CV = list()
sanc_amt_L_mean_list_GL = list()
sanc_amt_L_mean_list_HL = list()
sanc_amt_L_mean_list_LAS = list()
sanc_amt_L_mean_list_MFBL = list()
sanc_amt_L_mean_list_MFHL = list()
sanc_amt_L_mean_list_MFOT = list()
sanc_amt_L_mean_list_OTH = list()
sanc_amt_L_mean_list_PL = list()
sanc_amt_L_mean_list_PLBL = list()
sanc_amt_L_mean_list_RL = list()
sanc_amt_L_mean_list_SEL = list()

sanc_amt_L_mean_AL = list()
sanc_amt_L_mean_BL = list()
sanc_amt_L_mean_CD = list()
sanc_amt_L_mean_CV = list()
sanc_amt_L_mean_GL = list()
sanc_amt_L_mean_HL = list()
sanc_amt_L_mean_LAS = list()
sanc_amt_L_mean_MFBL = list()
sanc_amt_L_mean_MFHL = list()
sanc_amt_L_mean_MFOT = list()
sanc_amt_L_mean_OTH = list()
sanc_amt_L_mean_PL = list()
sanc_amt_L_mean_PLBL = list()
sanc_amt_L_mean_RL = list()
sanc_amt_L_mean_SEL = list()

Med_SancAmt_AL = list()
Med_SancAmt_BL = list()
Med_SancAmt_CD = list()
Med_SancAmt_CV = list()
Med_SancAmt_GL = list()
Med_SancAmt_HL = list()
Med_SancAmt_LAS = list()
Med_SancAmt_MFBL = list()
Med_SancAmt_MFHL = list()
Med_SancAmt_MFOT = list()
Med_SancAmt_OTH = list()
Med_SancAmt_PL = list()
Med_SancAmt_PLBL = list()
Med_SancAmt_RL = list()
Med_SancAmt_SEL = list()

sanc_amt_med_list_AL = list()
sanc_amt_med_list_BL = list()
sanc_amt_med_list_CD = list()
sanc_amt_med_list_CV = list()
sanc_amt_med_list_GL = list()
sanc_amt_med_list_HL = list()
sanc_amt_med_list_LAS = list()
sanc_amt_med_list_MFBL = list()
sanc_amt_med_list_MFHL = list()
sanc_amt_med_list_MFOT = list()
sanc_amt_med_list_OTH = list()
sanc_amt_med_list_PL = list()
sanc_amt_med_list_PLBL = list()
sanc_amt_med_list_RL = list()
sanc_amt_med_list_SEL = list()

sanc_amt_med_AL = list()
sanc_amt_med_BL = list()
sanc_amt_med_CD = list()
sanc_amt_med_CV = list()
sanc_amt_med_GL = list()
sanc_amt_med_HL = list()
sanc_amt_med_LAS = list()
sanc_amt_med_MFBL = list()
sanc_amt_med_MFHL = list()
sanc_amt_med_MFOT = list()
sanc_amt_med_OTH = list()
sanc_amt_med_PL = list()
sanc_amt_med_PLBL = list()
sanc_amt_med_RL = list()
sanc_amt_med_SEL = list()

Med_SancAmt_L_AL = list()
Med_SancAmt_L_BL = list()
Med_SancAmt_L_CD = list()
Med_SancAmt_L_CV = list()
Med_SancAmt_L_GL = list()
Med_SancAmt_L_HL = list()
Med_SancAmt_L_LAS = list()
Med_SancAmt_L_MFBL = list()
Med_SancAmt_L_MFHL = list()
Med_SancAmt_L_MFOT = list()
Med_SancAmt_L_OTH = list()
Med_SancAmt_L_PL = list()
Med_SancAmt_L_PLBL = list()
Med_SancAmt_L_RL = list()
Med_SancAmt_L_SEL = list()

sanc_amt_L_med_list_AL = list()
sanc_amt_L_med_list_BL = list()
sanc_amt_L_med_list_CD = list()
sanc_amt_L_med_list_CV = list()
sanc_amt_L_med_list_GL = list()
sanc_amt_L_med_list_HL = list()
sanc_amt_L_med_list_LAS = list()
sanc_amt_L_med_list_MFBL = list()
sanc_amt_L_med_list_MFHL = list()
sanc_amt_L_med_list_MFOT = list()
sanc_amt_L_med_list_OTH = list()
sanc_amt_L_med_list_PL = list()
sanc_amt_L_med_list_PLBL = list()
sanc_amt_L_med_list_RL = list()
sanc_amt_L_med_list_SEL = list()

sanc_amt_L_med_AL = list()
sanc_amt_L_med_BL = list()
sanc_amt_L_med_CD = list()
sanc_amt_L_med_CV = list()
sanc_amt_L_med_GL = list()
sanc_amt_L_med_HL = list()
sanc_amt_L_med_LAS = list()
sanc_amt_L_med_MFBL = list()
sanc_amt_L_med_MFHL = list()
sanc_amt_L_med_MFOT = list()
sanc_amt_L_med_OTH = list()
sanc_amt_L_med_PL = list()
sanc_amt_L_med_PLBL = list()
sanc_amt_L_med_RL = list()
sanc_amt_L_med_SEL = list()

'''
Mode_SancAmt_AL = list()
Mode_SancAmt_BL = list()
Mode_SancAmt_CD = list()
Mode_SancAmt_CV = list()
Mode_SancAmt_GL = list()
Mode_SancAmt_HL = list()
Mode_SancAmt_LAS = list()
Mode_SancAmt_MFBL = list()
Mode_SancAmt_MFHL = list()
Mode_SancAmt_MFOT = list()
Mode_SancAmt_OTH = list()
Mode_SancAmt_PL = list()
Mode_SancAmt_PLBL = list()
Mode_SancAmt_RL = list()
Mode_SancAmt_SEL = list()

Mode_SancAmt_L_AL = list()
Mode_SancAmt_L_BL = list()
Mode_SancAmt_L_CD = list()
Mode_SancAmt_L_CV = list()
Mode_SancAmt_L_GL = list()
Mode_SancAmt_L_HL = list()
Mode_SancAmt_L_LAS = list()
Mode_SancAmt_L_MFBL = list()
Mode_SancAmt_L_MFHL = list()
Mode_SancAmt_L_MFOT = list()
Mode_SancAmt_L_OTH = list()
Mode_SancAmt_L_PL = list()
Mode_SancAmt_L_PLBL = list()
Mode_SancAmt_L_RL = list()
Mode_SancAmt_L_SEL = list()'''

currentBalance_sanctionedAmount_NCC_L_AL = list()
currentBalance_sanctionedAmount_NCC_L_BL = list()
currentBalance_sanctionedAmount_NCC_L_CD = list()
currentBalance_sanctionedAmount_NCC_L_CV = list()
currentBalance_sanctionedAmount_NCC_L_GL = list()
currentBalance_sanctionedAmount_NCC_L_HL = list()
currentBalance_sanctionedAmount_NCC_L_LAS = list()
currentBalance_sanctionedAmount_NCC_L_MFBL = list()
currentBalance_sanctionedAmount_NCC_L_MFHL = list()
currentBalance_sanctionedAmount_NCC_L_MFOT = list()
currentBalance_sanctionedAmount_NCC_L_OTH = list()
currentBalance_sanctionedAmount_NCC_L_PL = list()
currentBalance_sanctionedAmount_NCC_L_PLBL = list()
currentBalance_sanctionedAmount_NCC_L_RL = list()
currentBalance_sanctionedAmount_NCC_L_SEL = list()

currentBalance_AL = list()
currentBalance_BL = list()
currentBalance_CD = list()
currentBalance_CV = list()
currentBalance_GL = list()
currentBalance_HL = list()
currentBalance_LAS = list()
currentBalance_MFBL = list()
currentBalance_MFHL = list()
currentBalance_MFOT = list()
currentBalance_OTH = list()
currentBalance_PL = list()
currentBalance_PLBL = list()
currentBalance_RL = list()
currentBalance_SEL = list()

sanctionedAmount_AL = list()
sanctionedAmount_BL = list()
sanctionedAmount_CD = list()
sanctionedAmount_CV = list()
sanctionedAmount_GL = list()
sanctionedAmount_HL = list()
sanctionedAmount_LAS = list()
sanctionedAmount_MFBL = list()
sanctionedAmount_MFHL = list()
sanctionedAmount_MFOT = list()
sanctionedAmount_OTH = list()
sanctionedAmount_PL = list()
sanctionedAmount_PLBL = list()
sanctionedAmount_RL = list()
sanctionedAmount_SEL = list()

currBal_ncc_l_AL = 0
currBal_ncc_l_BL = 0
currBal_ncc_l_CD = 0
currBal_ncc_l_CV = 0
currBal_ncc_l_GL = 0
currBal_ncc_l_HL = 0
currBal_ncc_l_LAS = 0
currBal_ncc_l_MFBL = 0
currBal_ncc_l_MFHL = 0
currBal_ncc_l_MFOT = 0
currBal_ncc_l_OTH = 0
currBal_ncc_l_PL = 0
currBal_ncc_l_PLBL = 0
currBal_ncc_l_RL = 0
currBal_ncc_l_SEL = 0

sanc_amt_ncc_l_AL = 0
sanc_amt_ncc_l_BL = 0
sanc_amt_ncc_l_CD = 0
sanc_amt_ncc_l_CV = 0
sanc_amt_ncc_l_GL = 0
sanc_amt_ncc_l_HL = 0
sanc_amt_ncc_l_LAS = 0
sanc_amt_ncc_l_MFBL = 0
sanc_amt_ncc_l_MFHL = 0
sanc_amt_ncc_l_MFOT = 0
sanc_amt_ncc_l_OTH = 0
sanc_amt_ncc_l_PL = 0
sanc_amt_ncc_l_PLBL = 0
sanc_amt_ncc_l_RL = 0
sanc_amt_ncc_l_SEL = 0

totAcc = list()

sanc_amt_grp = list()

sum_sanc_amt_list_AL = list()
sum_sanc_amt_list_BL = list()
sum_sanc_amt_list_CD = list()
sum_sanc_amt_list_CV = list()
sum_sanc_amt_list_GL = list()
sum_sanc_amt_list_HL = list()
sum_sanc_amt_list_LAS = list()
sum_sanc_amt_list_MFBL = list()
sum_sanc_amt_list_MFHL = list()
sum_sanc_amt_list_MFOT = list()
sum_sanc_amt_list_OTH = list()
sum_sanc_amt_list_PL = list()
sum_sanc_amt_list_PLBL = list()
sum_sanc_amt_list_RL = list()
sum_sanc_amt_list_SEL = list()

sum_sanc_amt_AL = 0
sum_sanc_amt_BL = 0
sum_sanc_amt_CD = 0
sum_sanc_amt_CV = 0
sum_sanc_amt_GL = 0
sum_sanc_amt_HL = 0
sum_sanc_amt_LAS = 0
sum_sanc_amt_MFBL = 0
sum_sanc_amt_MFHL = 0
sum_sanc_amt_MFOT = 0
sum_sanc_amt_OTH = 0
sum_sanc_amt_PL = 0
sum_sanc_amt_PLBL = 0
sum_sanc_amt_RL = 0
sum_sanc_amt_SEL = 0

cnt_grp = list()

cnt_list_AL = list()
cnt_list_BL = list()
cnt_list_CD = list()
cnt_list_CV = list()
cnt_list_GL = list()
cnt_list_HL = list()
cnt_list_LAS = list()
cnt_list_MFBL = list()
cnt_list_MFHL = list()
cnt_list_MFOT = list()
cnt_list_OTH = list()
cnt_list_PL = list()
cnt_list_PLBL = list()
cnt_list_RL = list()
cnt_list_SEL = list()

cnt_AL = 0
cnt_BL = 0
cnt_CD = 0
cnt_CV = 0
cnt_GL = 0
cnt_HL = 0
cnt_LAS = 0
cnt_MFBL = 0
cnt_MFHL = 0
cnt_MFOT = 0
cnt_OTH = 0
cnt_PL = 0
cnt_PLBL = 0
cnt_RL = 0
cnt_SEL = 0

df['totAcc_L'] = pd.Series(np.ones(4462)).values
totAcc_L = list()
cnt_L = list()
cnt = 0

sum_L_sanc_amt_grp_L = list()

sum_L_sanc_amt_list_L_AL = list()
sum_L_sanc_amt_list_L_BL = list()
sum_L_sanc_amt_list_L_CD = list()
sum_L_sanc_amt_list_L_CV = list()
sum_L_sanc_amt_list_L_GL = list()
sum_L_sanc_amt_list_L_HL = list()
sum_L_sanc_amt_list_L_LAS = list()
sum_L_sanc_amt_list_L_MFBL = list()
sum_L_sanc_amt_list_L_MFHL = list()
sum_L_sanc_amt_list_L_MFOT = list()
sum_L_sanc_amt_list_L_OTH = list()
sum_L_sanc_amt_list_L_PL = list()
sum_L_sanc_amt_list_L_PLBL = list()
sum_L_sanc_amt_list_L_RL = list()
sum_L_sanc_amt_list_L_SEL = list()

sum_L_sanc_amt_AL = 0
sum_L_sanc_amt_BL = 0
sum_L_sanc_amt_CD = 0
sum_L_sanc_amt_CV = 0
sum_L_sanc_amt_GL = 0
sum_L_sanc_amt_HL = 0
sum_L_sanc_amt_LAS = 0
sum_L_sanc_amt_MFBL = 0
sum_L_sanc_amt_MFHL = 0
sum_L_sanc_amt_MFOT = 0
sum_L_sanc_amt_OTH = 0
sum_L_sanc_amt_PL = 0
sum_L_sanc_amt_PLBL = 0
sum_L_sanc_amt_RL = 0
sum_L_sanc_amt_SEL = 0

cnt_L_grp_L = list()

cnt_L_list_AL = list()
cnt_L_list_BL = list()
cnt_L_list_CD = list()
cnt_L_list_CV = list()
cnt_L_list_GL = list()
cnt_L_list_HL = list()
cnt_L_list_LAS = list()
cnt_L_list_MFBL = list()
cnt_L_list_MFHL = list()
cnt_L_list_MFOT = list()
cnt_L_list_OTH = list()
cnt_L_list_PL = list()
cnt_L_list_PLBL = list()
cnt_L_list_RL = list()
cnt_L_list_SEL = list()

cnt_L_AL = 0
cnt_L_BL = 0
cnt_L_CD = 0
cnt_L_CV = 0
cnt_L_GL = 0
cnt_L_HL = 0
cnt_L_LAS = 0
cnt_L_MFBL = 0
cnt_L_MFHL = 0
cnt_L_MFOT = 0
cnt_L_OTH = 0
cnt_L_PL = 0
cnt_L_PLBL = 0
cnt_L_RL = 0
cnt_L_SEL = 0

curr_bal_grp_L = list()

curr_bal_list_L_AL = list()
curr_bal_list_L_BL = list()
curr_bal_list_L_CD = list()
curr_bal_list_L_CV = list()
curr_bal_list_L_GL = list()
curr_bal_list_L_HL = list()
curr_bal_list_L_LAS = list()
curr_bal_list_L_MFBL = list()
curr_bal_list_L_MFHL = list()
curr_bal_list_L_MFOT = list()
curr_bal_list_L_OTH = list()
curr_bal_list_L_PL = list()
curr_bal_list_L_PLBL = list()
curr_bal_list_L_RL = list()
curr_bal_list_L_SEL = list()

curr_bal_AL = 0
curr_bal_BL = 0
curr_bal_CD = 0
curr_bal_CV = 0
curr_bal_GL = 0
curr_bal_HL = 0
curr_bal_LAS = 0
curr_bal_MFBL = 0
curr_bal_MFHL = 0
curr_bal_MFOT = 0
curr_bal_OTH = 0
curr_bal_PL = 0
curr_bal_PLBL = 0
curr_bal_RL = 0
curr_bal_SEL = 0

DPD30P1M = list()
count_list_30_1m = list()
count_30_1m = 0

DPD60P1M = list()
count_list_60_1m = list()
count_60_1m = 0

DPD90P1M = list()
count_list_90_1m = list()
count_90_1m = 0

writeOff_CNT = list()
count_list_wo = list()
count_wo = 0

restructured_CNT = list()
count_list_re = list()
count_re = 0

writeOff_CNT_AL = list()
writeOff_CNT_BL = list()
writeOff_CNT_CC = list()
writeOff_CNT_CD = list()
writeOff_CNT_CV = list()
writeOff_CNT_GL = list()
writeOff_CNT_HL = list()
writeOff_CNT_LAS = list()
writeOff_CNT_MFBL = list()
writeOff_CNT_MFHL = list()
writeOff_CNT_MFOT = list()
writeOff_CNT_OTH = list()
writeOff_CNT_PL = list()
writeOff_CNT_PLBL = list()
writeOff_CNT_RL = list()
writeOff_CNT_SCC = list()
writeOff_CNT_SEL = list()

count_wo_list_AL = list()
count_wo_list_BL = list()
count_wo_list_CC = list()
count_wo_list_CD = list()
count_wo_list_CV = list()
count_wo_list_GL = list()
count_wo_list_HL = list()
count_wo_list_LAS = list()
count_wo_list_MFBL = list()
count_wo_list_MFHL = list()
count_wo_list_MFOT = list()
count_wo_list_OTH = list()
count_wo_list_PL = list()
count_wo_list_PLBL = list()
count_wo_list_RL = list()
count_wo_list_SCC = list()
count_wo_list_SEL = list()

count_wo_AL = 0
count_wo_BL = 0
count_wo_CC = 0
count_wo_CD = 0
count_wo_CV = 0
count_wo_GL = 0
count_wo_HL = 0
count_wo_LAS = 0
count_wo_MFBL = 0
count_wo_MFHL = 0
count_wo_MFOT = 0
count_wo_OTH = 0
count_wo_PL = 0
count_wo_PLBL = 0
count_wo_RL = 0
count_wo_SCC = 0
count_wo_SEL = 0

restructured_CNT_AL = list()
restructured_CNT_BL = list()
restructured_CNT_CC = list()
restructured_CNT_CD = list()
restructured_CNT_CV = list()
restructured_CNT_GL = list()
restructured_CNT_HL = list()
restructured_CNT_LAS = list()
restructured_CNT_MFBL = list()
restructured_CNT_MFHL = list()
restructured_CNT_MFOT = list()
restructured_CNT_OTH = list()
restructured_CNT_PL = list()
restructured_CNT_PLBL = list()
restructured_CNT_RL = list()
restructured_CNT_SCC = list()
restructured_CNT_SEL = list()

count_re_list_AL = list()
count_re_list_BL = list()
count_re_list_CC = list()
count_re_list_CD = list()
count_re_list_CV = list()
count_re_list_GL = list()
count_re_list_HL = list()
count_re_list_LAS = list()
count_re_list_MFBL = list()
count_re_list_MFHL = list()
count_re_list_MFOT = list()
count_re_list_OTH = list()
count_re_list_PL = list()
count_re_list_PLBL = list()
count_re_list_RL = list()
count_re_list_SCC = list()
count_re_list_SEL = list()

count_re_AL = 0
count_re_BL = 0
count_re_CC = 0
count_re_CD = 0
count_re_CV = 0
count_re_GL = 0
count_re_HL = 0
count_re_LAS = 0
count_re_MFBL = 0
count_re_MFHL = 0
count_re_MFOT = 0
count_re_OTH = 0
count_re_PL = 0
count_re_PLBL = 0
count_re_RL = 0
count_re_SCC = 0
count_re_SEL = 0

writeOff_last3M_CNT = list()
count_wo_l3m_list = list()
count_wo_l3m = 0

writeOff_last3M_CNT_AL = list()
writeOff_last3M_CNT_BL = list()
writeOff_last3M_CNT_CC = list()
writeOff_last3M_CNT_CD = list()
writeOff_last3M_CNT_CV = list()
writeOff_last3M_CNT_GL = list()
writeOff_last3M_CNT_HL = list()
writeOff_last3M_CNT_LAS = list()
writeOff_last3M_CNT_MFBL = list()
writeOff_last3M_CNT_MFHL = list()
writeOff_last3M_CNT_MFOT = list()
writeOff_last3M_CNT_OTH = list()
writeOff_last3M_CNT_PL = list()
writeOff_last3M_CNT_PLBL = list()
writeOff_last3M_CNT_RL = list()
writeOff_last3M_CNT_SCC = list()
writeOff_last3M_CNT_SEL = list()

count_wo_l3m_list_AL = list()
count_wo_l3m_list_BL = list()
count_wo_l3m_list_CC = list()
count_wo_l3m_list_CD = list()
count_wo_l3m_list_CV = list()
count_wo_l3m_list_GL = list()
count_wo_l3m_list_HL = list()
count_wo_l3m_list_LAS = list()
count_wo_l3m_list_MFBL = list()
count_wo_l3m_list_MFHL = list()
count_wo_l3m_list_MFOT = list()
count_wo_l3m_list_OTH = list()
count_wo_l3m_list_PL = list()
count_wo_l3m_list_PLBL = list()
count_wo_l3m_list_RL = list()
count_wo_l3m_list_SCC = list()
count_wo_l3m_list_SEL = list()

count_wo_l3m_AL = 0
count_wo_l3m_BL = 0
count_wo_l3m_CC = 0
count_wo_l3m_CD = 0
count_wo_l3m_CV = 0
count_wo_l3m_GL = 0
count_wo_l3m_HL = 0
count_wo_l3m_LAS = 0
count_wo_l3m_MFBL = 0
count_wo_l3m_MFHL = 0
count_wo_l3m_MFOT = 0
count_wo_l3m_OTH = 0
count_wo_l3m_PL = 0
count_wo_l3m_PLBL = 0
count_wo_l3m_RL = 0
count_wo_l3m_SCC = 0
count_wo_l3m_SEL = 0

writeOff_last6M_CNT = list()
count_wo_l6m_list = list()
count_wo_l6m = 0

writeOff_last6M_CNT_AL = list()
writeOff_last6M_CNT_BL = list()
writeOff_last6M_CNT_CC = list()
writeOff_last6M_CNT_CD = list()
writeOff_last6M_CNT_CV = list()
writeOff_last6M_CNT_GL = list()
writeOff_last6M_CNT_HL = list()
writeOff_last6M_CNT_LAS = list()
writeOff_last6M_CNT_MFBL = list()
writeOff_last6M_CNT_MFHL = list()
writeOff_last6M_CNT_MFOT = list()
writeOff_last6M_CNT_OTH = list()
writeOff_last6M_CNT_PL = list()
writeOff_last6M_CNT_PLBL = list()
writeOff_last6M_CNT_RL = list()
writeOff_last6M_CNT_SCC = list()
writeOff_last6M_CNT_SEL = list()

count_wo_l6m_list_AL = list()
count_wo_l6m_list_BL = list()
count_wo_l6m_list_CC = list()
count_wo_l6m_list_CD = list()
count_wo_l6m_list_CV = list()
count_wo_l6m_list_GL = list()
count_wo_l6m_list_HL = list()
count_wo_l6m_list_LAS = list()
count_wo_l6m_list_MFBL = list()
count_wo_l6m_list_MFHL = list()
count_wo_l6m_list_MFOT = list()
count_wo_l6m_list_OTH = list()
count_wo_l6m_list_PL = list()
count_wo_l6m_list_PLBL = list()
count_wo_l6m_list_RL = list()
count_wo_l6m_list_SCC = list()
count_wo_l6m_list_SEL = list()

count_wo_l6m_AL = 0
count_wo_l6m_BL = 0
count_wo_l6m_CC = 0
count_wo_l6m_CD = 0
count_wo_l6m_CV = 0
count_wo_l6m_GL = 0
count_wo_l6m_HL = 0
count_wo_l6m_LAS = 0
count_wo_l6m_MFBL = 0
count_wo_l6m_MFHL = 0
count_wo_l6m_MFOT = 0
count_wo_l6m_OTH = 0
count_wo_l6m_PL = 0
count_wo_l6m_PLBL = 0
count_wo_l6m_RL = 0
count_wo_l6m_SCC = 0
count_wo_l6m_SEL = 0

writeOff_last9M_CNT = list()
count_wo_l9m_list = list()
count_wo_l9m = 0

writeOff_last9M_CNT_AL = list()
writeOff_last9M_CNT_BL = list()
writeOff_last9M_CNT_CC = list()
writeOff_last9M_CNT_CD = list()
writeOff_last9M_CNT_CV = list()
writeOff_last9M_CNT_GL = list()
writeOff_last9M_CNT_HL = list()
writeOff_last9M_CNT_LAS = list()
writeOff_last9M_CNT_MFBL = list()
writeOff_last9M_CNT_MFHL = list()
writeOff_last9M_CNT_MFOT = list()
writeOff_last9M_CNT_OTH = list()
writeOff_last9M_CNT_PL = list()
writeOff_last9M_CNT_PLBL = list()
writeOff_last9M_CNT_RL = list()
writeOff_last9M_CNT_SCC = list()
writeOff_last9M_CNT_SEL = list()

count_wo_l9m_list_AL = list()
count_wo_l9m_list_BL = list()
count_wo_l9m_list_CC = list()
count_wo_l9m_list_CD = list()
count_wo_l9m_list_CV = list()
count_wo_l9m_list_GL = list()
count_wo_l9m_list_HL = list()
count_wo_l9m_list_LAS = list()
count_wo_l9m_list_MFBL = list()
count_wo_l9m_list_MFHL = list()
count_wo_l9m_list_MFOT = list()
count_wo_l9m_list_OTH = list()
count_wo_l9m_list_PL = list()
count_wo_l9m_list_PLBL = list()
count_wo_l9m_list_RL = list()
count_wo_l9m_list_SCC = list()
count_wo_l9m_list_SEL = list()

count_wo_l9m_AL = 0
count_wo_l9m_BL = 0
count_wo_l9m_CC = 0
count_wo_l9m_CD = 0
count_wo_l9m_CV = 0
count_wo_l9m_GL = 0
count_wo_l9m_HL = 0
count_wo_l9m_LAS = 0
count_wo_l9m_MFBL = 0
count_wo_l9m_MFHL = 0
count_wo_l9m_MFOT = 0
count_wo_l9m_OTH = 0
count_wo_l9m_PL = 0
count_wo_l9m_PLBL = 0
count_wo_l9m_RL = 0
count_wo_l9m_SCC = 0
count_wo_l9m_SEL = 0

writeOff_last1Y_CNT = list()
count_wo_l1y_list = list()
count_wo_l1y = 0

writeOff_last1Y_CNT_AL = list()
writeOff_last1Y_CNT_BL = list()
writeOff_last1Y_CNT_CC = list()
writeOff_last1Y_CNT_CD = list()
writeOff_last1Y_CNT_CV = list()
writeOff_last1Y_CNT_GL = list()
writeOff_last1Y_CNT_HL = list()
writeOff_last1Y_CNT_LAS = list()
writeOff_last1Y_CNT_MFBL = list()
writeOff_last1Y_CNT_MFHL = list()
writeOff_last1Y_CNT_MFOT = list()
writeOff_last1Y_CNT_OTH = list()
writeOff_last1Y_CNT_PL = list()
writeOff_last1Y_CNT_PLBL = list()
writeOff_last1Y_CNT_RL = list()
writeOff_last1Y_CNT_SCC = list()
writeOff_last1Y_CNT_SEL = list()

count_wo_l1y_list_AL = list()
count_wo_l1y_list_BL = list()
count_wo_l1y_list_CC = list()
count_wo_l1y_list_CD = list()
count_wo_l1y_list_CV = list()
count_wo_l1y_list_GL = list()
count_wo_l1y_list_HL = list()
count_wo_l1y_list_LAS = list()
count_wo_l1y_list_MFBL = list()
count_wo_l1y_list_MFHL = list()
count_wo_l1y_list_MFOT = list()
count_wo_l1y_list_OTH = list()
count_wo_l1y_list_PL = list()
count_wo_l1y_list_PLBL = list()
count_wo_l1y_list_RL = list()
count_wo_l1y_list_SCC = list()
count_wo_l1y_list_SEL = list()

count_wo_l1y_AL = 0
count_wo_l1y_BL = 0
count_wo_l1y_CC = 0
count_wo_l1y_CD = 0
count_wo_l1y_CV = 0
count_wo_l1y_GL = 0
count_wo_l1y_HL = 0
count_wo_l1y_LAS = 0
count_wo_l1y_MFBL = 0
count_wo_l1y_MFHL = 0
count_wo_l1y_MFOT = 0
count_wo_l1y_OTH = 0
count_wo_l1y_PL = 0
count_wo_l1y_PLBL = 0
count_wo_l1y_RL = 0
count_wo_l1y_SCC = 0
count_wo_l1y_SEL = 0

writeOff_last2Y_CNT = list()
count_wo_l2y_list = list()
count_wo_l2y = 0

writeOff_last2Y_CNT_AL = list()
writeOff_last2Y_CNT_BL = list()
writeOff_last2Y_CNT_CC = list()
writeOff_last2Y_CNT_CD = list()
writeOff_last2Y_CNT_CV = list()
writeOff_last2Y_CNT_GL = list()
writeOff_last2Y_CNT_HL = list()
writeOff_last2Y_CNT_LAS = list()
writeOff_last2Y_CNT_MFBL = list()
writeOff_last2Y_CNT_MFHL = list()
writeOff_last2Y_CNT_MFOT = list()
writeOff_last2Y_CNT_OTH = list()
writeOff_last2Y_CNT_PL = list()
writeOff_last2Y_CNT_PLBL = list()
writeOff_last2Y_CNT_RL = list()
writeOff_last2Y_CNT_SCC = list()
writeOff_last2Y_CNT_SEL = list()

count_wo_l2y_list_AL = list()
count_wo_l2y_list_BL = list()
count_wo_l2y_list_CC = list()
count_wo_l2y_list_CD = list()
count_wo_l2y_list_CV = list()
count_wo_l2y_list_GL = list()
count_wo_l2y_list_HL = list()
count_wo_l2y_list_LAS = list()
count_wo_l2y_list_MFBL = list()
count_wo_l2y_list_MFHL = list()
count_wo_l2y_list_MFOT = list()
count_wo_l2y_list_OTH = list()
count_wo_l2y_list_PL = list()
count_wo_l2y_list_PLBL = list()
count_wo_l2y_list_RL = list()
count_wo_l2y_list_SCC = list()
count_wo_l2y_list_SEL = list()

count_wo_l2y_AL = 0
count_wo_l2y_BL = 0
count_wo_l2y_CC = 0
count_wo_l2y_CD = 0
count_wo_l2y_CV = 0
count_wo_l2y_GL = 0
count_wo_l2y_HL = 0
count_wo_l2y_LAS = 0
count_wo_l2y_MFBL = 0
count_wo_l2y_MFHL = 0
count_wo_l2y_MFOT = 0
count_wo_l2y_OTH = 0
count_wo_l2y_PL = 0
count_wo_l2y_PLBL = 0
count_wo_l2y_RL = 0
count_wo_l2y_SCC = 0
count_wo_l2y_SEL = 0

writeOff_last3Y_CNT = list()
count_wo_l3y_list = list()
count_wo_l3y = 0

writeOff_last3Y_CNT_AL = list()
writeOff_last3Y_CNT_BL = list()
writeOff_last3Y_CNT_CC = list()
writeOff_last3Y_CNT_CD = list()
writeOff_last3Y_CNT_CV = list()
writeOff_last3Y_CNT_GL = list()
writeOff_last3Y_CNT_HL = list()
writeOff_last3Y_CNT_LAS = list()
writeOff_last3Y_CNT_MFBL = list()
writeOff_last3Y_CNT_MFHL = list()
writeOff_last3Y_CNT_MFOT = list()
writeOff_last3Y_CNT_OTH = list()
writeOff_last3Y_CNT_PL = list()
writeOff_last3Y_CNT_PLBL = list()
writeOff_last3Y_CNT_RL = list()
writeOff_last3Y_CNT_SCC = list()
writeOff_last3Y_CNT_SEL = list()

count_wo_l3y_list_AL = list()
count_wo_l3y_list_BL = list()
count_wo_l3y_list_CC = list()
count_wo_l3y_list_CD = list()
count_wo_l3y_list_CV = list()
count_wo_l3y_list_GL = list()
count_wo_l3y_list_HL = list()
count_wo_l3y_list_LAS = list()
count_wo_l3y_list_MFBL = list()
count_wo_l3y_list_MFHL = list()
count_wo_l3y_list_MFOT = list()
count_wo_l3y_list_OTH = list()
count_wo_l3y_list_PL = list()
count_wo_l3y_list_PLBL = list()
count_wo_l3y_list_RL = list()
count_wo_l3y_list_SCC = list()
count_wo_l3y_list_SEL = list()

count_wo_l3y_AL = 0
count_wo_l3y_BL = 0
count_wo_l3y_CC = 0
count_wo_l3y_CD = 0
count_wo_l3y_CV = 0
count_wo_l3y_GL = 0
count_wo_l3y_HL = 0
count_wo_l3y_LAS = 0
count_wo_l3y_MFBL = 0
count_wo_l3y_MFHL = 0
count_wo_l3y_MFOT = 0
count_wo_l3y_OTH = 0
count_wo_l3y_PL = 0
count_wo_l3y_PLBL = 0
count_wo_l3y_RL = 0
count_wo_l3y_SCC = 0
count_wo_l3y_SEL = 0

writeOff_last1Y_PLT1K_CNT = list()
count_wo_l1y_plt_list = list()
count_wo_l1y_plt = 0

writeOff_last2Y_PLT1K_CNT = list()
count_wo_l2y_plt_list = list()
count_wo_l2y_plt = 0

writeOff_last3Y_PLT1K_CNT = list()
count_wo_l3y_plt_list = list()
count_wo_l3y_plt = 0

opened_last3M_CNT = list()
count_op_l3m_list = list()
count_op_l3m = 0

opened_last3M_CNT_AL = list()
opened_last3M_CNT_BL = list()
opened_last3M_CNT_CC = list()
opened_last3M_CNT_CD = list()
opened_last3M_CNT_CV = list()
opened_last3M_CNT_GL = list()
opened_last3M_CNT_HL = list()
opened_last3M_CNT_LAS = list()
opened_last3M_CNT_MFBL = list()
opened_last3M_CNT_MFHL = list()
opened_last3M_CNT_MFOT = list()
opened_last3M_CNT_OTH = list()
opened_last3M_CNT_PL = list()
opened_last3M_CNT_PLBL = list()
opened_last3M_CNT_RL = list()
opened_last3M_CNT_SCC = list()
opened_last3M_CNT_SEL = list()

count_op_l3m_list_AL = list()
count_op_l3m_list_BL = list()
count_op_l3m_list_CC = list()
count_op_l3m_list_CD = list()
count_op_l3m_list_CV = list()
count_op_l3m_list_GL = list()
count_op_l3m_list_HL = list()
count_op_l3m_list_LAS = list()
count_op_l3m_list_MFBL = list()
count_op_l3m_list_MFHL = list()
count_op_l3m_list_MFOT = list()
count_op_l3m_list_OTH = list()
count_op_l3m_list_PL = list()
count_op_l3m_list_PLBL = list()
count_op_l3m_list_RL = list()
count_op_l3m_list_SCC = list()
count_op_l3m_list_SEL = list()

count_op_l3m_AL = 0
count_op_l3m_BL = 0
count_op_l3m_CC = 0
count_op_l3m_CD = 0
count_op_l3m_CV = 0
count_op_l3m_GL = 0
count_op_l3m_HL = 0
count_op_l3m_LAS = 0
count_op_l3m_MFBL = 0
count_op_l3m_MFHL = 0
count_op_l3m_MFOT = 0
count_op_l3m_OTH = 0
count_op_l3m_PL = 0
count_op_l3m_PLBL = 0
count_op_l3m_RL = 0
count_op_l3m_SCC = 0
count_op_l3m_SEL = 0

opened_last6M_CNT = list()
count_op_l6m_list = list()
count_op_l6m = 0

opened_last6M_CNT_AL = list()
opened_last6M_CNT_BL = list()
opened_last6M_CNT_CC = list()
opened_last6M_CNT_CD = list()
opened_last6M_CNT_CV = list()
opened_last6M_CNT_GL = list()
opened_last6M_CNT_HL = list()
opened_last6M_CNT_LAS = list()
opened_last6M_CNT_MFBL = list()
opened_last6M_CNT_MFHL = list()
opened_last6M_CNT_MFOT = list()
opened_last6M_CNT_OTH = list()
opened_last6M_CNT_PL = list()
opened_last6M_CNT_PLBL = list()
opened_last6M_CNT_RL = list()
opened_last6M_CNT_SCC = list()
opened_last6M_CNT_SEL = list()

count_op_l6m_list_AL = list()
count_op_l6m_list_BL = list()
count_op_l6m_list_CC = list()
count_op_l6m_list_CD = list()
count_op_l6m_list_CV = list()
count_op_l6m_list_GL = list()
count_op_l6m_list_HL = list()
count_op_l6m_list_LAS = list()
count_op_l6m_list_MFBL = list()
count_op_l6m_list_MFHL = list()
count_op_l6m_list_MFOT = list()
count_op_l6m_list_OTH = list()
count_op_l6m_list_PL = list()
count_op_l6m_list_PLBL = list()
count_op_l6m_list_RL = list()
count_op_l6m_list_SCC = list()
count_op_l6m_list_SEL = list()

count_op_l6m_AL = 0
count_op_l6m_BL = 0
count_op_l6m_CC = 0
count_op_l6m_CD = 0
count_op_l6m_CV = 0
count_op_l6m_GL = 0
count_op_l6m_HL = 0
count_op_l6m_LAS = 0
count_op_l6m_MFBL = 0
count_op_l6m_MFHL = 0
count_op_l6m_MFOT = 0
count_op_l6m_OTH = 0
count_op_l6m_PL = 0
count_op_l6m_PLBL = 0
count_op_l6m_RL = 0
count_op_l6m_SCC = 0
count_op_l6m_SEL = 0

opened_last9M_CNT = list()
count_op_l9m_list = list()
count_op_l9m = 0

opened_last9M_CNT_AL = list()
opened_last9M_CNT_BL = list()
opened_last9M_CNT_CC = list()
opened_last9M_CNT_CD = list()
opened_last9M_CNT_CV = list()
opened_last9M_CNT_GL = list()
opened_last9M_CNT_HL = list()
opened_last9M_CNT_LAS = list()
opened_last9M_CNT_MFBL = list()
opened_last9M_CNT_MFHL = list()
opened_last9M_CNT_MFOT = list()
opened_last9M_CNT_OTH = list()
opened_last9M_CNT_PL = list()
opened_last9M_CNT_PLBL = list()
opened_last9M_CNT_RL = list()
opened_last9M_CNT_SCC = list()
opened_last9M_CNT_SEL = list()

count_op_l9m_list_AL = list()
count_op_l9m_list_BL = list()
count_op_l9m_list_CC = list()
count_op_l9m_list_CD = list()
count_op_l9m_list_CV = list()
count_op_l9m_list_GL = list()
count_op_l9m_list_HL = list()
count_op_l9m_list_LAS = list()
count_op_l9m_list_MFBL = list()
count_op_l9m_list_MFHL = list()
count_op_l9m_list_MFOT = list()
count_op_l9m_list_OTH = list()
count_op_l9m_list_PL = list()
count_op_l9m_list_PLBL = list()
count_op_l9m_list_RL = list()
count_op_l9m_list_SCC = list()
count_op_l9m_list_SEL = list()

count_op_l9m_AL = 0
count_op_l9m_BL = 0
count_op_l9m_CC = 0
count_op_l9m_CD = 0
count_op_l9m_CV = 0
count_op_l9m_GL = 0
count_op_l9m_HL = 0
count_op_l9m_LAS = 0
count_op_l9m_MFBL = 0
count_op_l9m_MFHL = 0
count_op_l9m_MFOT = 0
count_op_l9m_OTH = 0
count_op_l9m_PL = 0
count_op_l9m_PLBL = 0
count_op_l9m_RL = 0
count_op_l9m_SCC = 0
count_op_l9m_SEL = 0

opened_last1Y_CNT = list()
count_op_l1y_list = list()
count_op_l1y = 0

opened_last1Y_CNT_AL = list()
opened_last1Y_CNT_BL = list()
opened_last1Y_CNT_CC = list()
opened_last1Y_CNT_CD = list()
opened_last1Y_CNT_CV = list()
opened_last1Y_CNT_GL = list()
opened_last1Y_CNT_HL = list()
opened_last1Y_CNT_LAS = list()
opened_last1Y_CNT_MFBL = list()
opened_last1Y_CNT_MFHL = list()
opened_last1Y_CNT_MFOT = list()
opened_last1Y_CNT_OTH = list()
opened_last1Y_CNT_PL = list()
opened_last1Y_CNT_PLBL = list()
opened_last1Y_CNT_RL = list()
opened_last1Y_CNT_SCC = list()
opened_last1Y_CNT_SEL = list()

count_op_l1y_list_AL = list()
count_op_l1y_list_BL = list()
count_op_l1y_list_CC = list()
count_op_l1y_list_CD = list()
count_op_l1y_list_CV = list()
count_op_l1y_list_GL = list()
count_op_l1y_list_HL = list()
count_op_l1y_list_LAS = list()
count_op_l1y_list_MFBL = list()
count_op_l1y_list_MFHL = list()
count_op_l1y_list_MFOT = list()
count_op_l1y_list_OTH = list()
count_op_l1y_list_PL = list()
count_op_l1y_list_PLBL = list()
count_op_l1y_list_RL = list()
count_op_l1y_list_SCC = list()
count_op_l1y_list_SEL = list()

count_op_l1y_AL = 0
count_op_l1y_BL = 0
count_op_l1y_CC = 0
count_op_l1y_CD = 0
count_op_l1y_CV = 0
count_op_l1y_GL = 0
count_op_l1y_HL = 0
count_op_l1y_LAS = 0
count_op_l1y_MFBL = 0
count_op_l1y_MFHL = 0
count_op_l1y_MFOT = 0
count_op_l1y_OTH = 0
count_op_l1y_PL = 0
count_op_l1y_PLBL = 0
count_op_l1y_RL = 0
count_op_l1y_SCC = 0
count_op_l1y_SEL = 0

opened_last2Y_CNT = list()
count_op_l2y_list = list()
count_op_l2y = 0

opened_last2Y_CNT_AL = list()
opened_last2Y_CNT_BL = list()
opened_last2Y_CNT_CC = list()
opened_last2Y_CNT_CD = list()
opened_last2Y_CNT_CV = list()
opened_last2Y_CNT_GL = list()
opened_last2Y_CNT_HL = list()
opened_last2Y_CNT_LAS = list()
opened_last2Y_CNT_MFBL = list()
opened_last2Y_CNT_MFHL = list()
opened_last2Y_CNT_MFOT = list()
opened_last2Y_CNT_OTH = list()
opened_last2Y_CNT_PL = list()
opened_last2Y_CNT_PLBL = list()
opened_last2Y_CNT_RL = list()
opened_last2Y_CNT_SCC = list()
opened_last2Y_CNT_SEL = list()

count_op_l2y_list_AL = list()
count_op_l2y_list_BL = list()
count_op_l2y_list_CC = list()
count_op_l2y_list_CD = list()
count_op_l2y_list_CV = list()
count_op_l2y_list_GL = list()
count_op_l2y_list_HL = list()
count_op_l2y_list_LAS = list()
count_op_l2y_list_MFBL = list()
count_op_l2y_list_MFHL = list()
count_op_l2y_list_MFOT = list()
count_op_l2y_list_OTH = list()
count_op_l2y_list_PL = list()
count_op_l2y_list_PLBL = list()
count_op_l2y_list_RL = list()
count_op_l2y_list_SCC = list()
count_op_l2y_list_SEL = list()

count_op_l2y_AL = 0
count_op_l2y_BL = 0
count_op_l2y_CC = 0
count_op_l2y_CD = 0
count_op_l2y_CV = 0
count_op_l2y_GL = 0
count_op_l2y_HL = 0
count_op_l2y_LAS = 0
count_op_l2y_MFBL = 0
count_op_l2y_MFHL = 0
count_op_l2y_MFOT = 0
count_op_l2y_OTH = 0
count_op_l2y_PL = 0
count_op_l2y_PLBL = 0
count_op_l2y_RL = 0
count_op_l2y_SCC = 0
count_op_l2y_SEL = 0

opened_last3Y_CNT = list()
count_op_l3y_list = list()
count_op_l3y = 0

opened_last3Y_CNT_AL = list()
opened_last3Y_CNT_BL = list()
opened_last3Y_CNT_CC = list()
opened_last3Y_CNT_CD = list()
opened_last3Y_CNT_CV = list()
opened_last3Y_CNT_GL = list()
opened_last3Y_CNT_HL = list()
opened_last3Y_CNT_LAS = list()
opened_last3Y_CNT_MFBL = list()
opened_last3Y_CNT_MFHL = list()
opened_last3Y_CNT_MFOT = list()
opened_last3Y_CNT_OTH = list()
opened_last3Y_CNT_PL = list()
opened_last3Y_CNT_PLBL = list()
opened_last3Y_CNT_RL = list()
opened_last3Y_CNT_SCC = list()
opened_last3Y_CNT_SEL = list()

count_op_l3y_list_AL = list()
count_op_l3y_list_BL = list()
count_op_l3y_list_CC = list()
count_op_l3y_list_CD = list()
count_op_l3y_list_CV = list()
count_op_l3y_list_GL = list()
count_op_l3y_list_HL = list()
count_op_l3y_list_LAS = list()
count_op_l3y_list_MFBL = list()
count_op_l3y_list_MFHL = list()
count_op_l3y_list_MFOT = list()
count_op_l3y_list_OTH = list()
count_op_l3y_list_PL = list()
count_op_l3y_list_PLBL = list()
count_op_l3y_list_RL = list()
count_op_l3y_list_SCC = list()
count_op_l3y_list_SEL = list()

count_op_l3y_AL = 0
count_op_l3y_BL = 0
count_op_l3y_CC = 0
count_op_l3y_CD = 0
count_op_l3y_CV = 0
count_op_l3y_GL = 0
count_op_l3y_HL = 0
count_op_l3y_LAS = 0
count_op_l3y_MFBL = 0
count_op_l3y_MFHL = 0
count_op_l3y_MFOT = 0
count_op_l3y_OTH = 0
count_op_l3y_PL = 0
count_op_l3y_PLBL = 0
count_op_l3y_RL = 0
count_op_l3y_SCC = 0
count_op_l3y_SEL = 0

overdueAmount_sum_AL = list()
overdueAmount_sum_BL = list()
overdueAmount_sum_CC = list()
overdueAmount_sum_CD = list()
overdueAmount_sum_CV = list()
overdueAmount_sum_GL = list()
overdueAmount_sum_HL = list()
overdueAmount_sum_LAS = list()
overdueAmount_sum_MFBL = list()
overdueAmount_sum_MFHL = list()
overdueAmount_sum_MFOT = list()
overdueAmount_sum_OTH = list()
overdueAmount_sum_PL = list()
overdueAmount_sum_PLBL = list()
overdueAmount_sum_RL = list()
overdueAmount_sum_SCC = list()
overdueAmount_sum_SEL = list()

oa_list_AL = list()
oa_list_BL = list()
oa_list_CC = list()
oa_list_CD = list()
oa_list_CV = list()
oa_list_GL = list()
oa_list_HL = list()
oa_list_LAS = list()
oa_list_MFBL = list()
oa_list_MFHL = list()
oa_list_MFOT = list()
oa_list_OTH = list()
oa_list_PL = list()
oa_list_PLBL = list()
oa_list_RL = list()
oa_list_SCC = list()
oa_list_SEL = list()

oa_AL = 0
oa_BL = 0
oa_CC = 0
oa_CD = 0
oa_CV = 0
oa_GL = 0
oa_HL = 0
oa_LAS = 0
oa_MFBL = 0
oa_MFHL = 0
oa_MFOT = 0
oa_OTH = 0
oa_PL = 0
oa_PLBL = 0
oa_RL = 0
oa_SCC = 0
oa_SEL = 0

Overdue_Current_AL = list()
Overdue_Current_BL = list()
Overdue_Current_CC = list()
Overdue_Current_CD = list()
Overdue_Current_CV = list()
Overdue_Current_GL = list()
Overdue_Current_HL = list()
Overdue_Current_LAS = list()
Overdue_Current_MFBL = list()
Overdue_Current_MFHL = list()
Overdue_Current_MFOT = list()
Overdue_Current_OTH = list()
Overdue_Current_PL = list()
Overdue_Current_PLBL = list()
Overdue_Current_RL = list()
Overdue_Current_SCC = list()
Overdue_Current_SEL = list()

grp_list_oa_AL = list()
grp_list_oa_BL = list()
grp_list_oa_CC = list()
grp_list_oa_CD = list()
grp_list_oa_CV = list()
grp_list_oa_GL = list()
grp_list_oa_HL = list()
grp_list_oa_LAS = list()
grp_list_oa_MFBL = list()
grp_list_oa_MFHL = list()
grp_list_oa_MFOT = list()
grp_list_oa_OTH = list()
grp_list_oa_PL = list()
grp_list_oa_PLBL = list()
grp_list_oa_RL = list()
grp_list_oa_SCC = list()
grp_list_oa_SEL = list()

grp_list_cb_AL = list()
grp_list_cb_BL = list()
grp_list_cb_CC = list()
grp_list_cb_CD = list()
grp_list_cb_CV = list()
grp_list_cb_GL = list()
grp_list_cb_HL = list()
grp_list_cb_LAS = list()
grp_list_cb_MFBL = list()
grp_list_cb_MFHL = list()
grp_list_cb_MFOT = list()
grp_list_cb_OTH = list()
grp_list_cb_PL = list()
grp_list_cb_PLBL = list()
grp_list_cb_RL = list()
grp_list_cb_SCC = list()
grp_list_cb_SEL = list()

grp_oa_AL = 0
grp_oa_BL = 0
grp_oa_CC = 0
grp_oa_CD = 0
grp_oa_CV = 0
grp_oa_GL = 0
grp_oa_HL = 0
grp_oa_LAS = 0
grp_oa_MFBL = 0
grp_oa_MFHL = 0
grp_oa_MFOT = 0
grp_oa_OTH = 0
grp_oa_PL = 0
grp_oa_PLBL = 0
grp_oa_RL = 0
grp_oa_SCC = 0
grp_oa_SEL = 0

grp_cb_AL = 0
grp_cb_BL = 0
grp_cb_CC = 0
grp_cb_CD = 0
grp_cb_CV = 0
grp_cb_GL = 0
grp_cb_HL = 0
grp_cb_LAS = 0
grp_cb_MFBL = 0
grp_cb_MFHL = 0
grp_cb_MFOT = 0
grp_cb_OTH = 0
grp_cb_PL = 0
grp_cb_PLBL = 0
grp_cb_RL = 0
grp_cb_SCC = 0
grp_cb_SEL = 0

Overdue_Disbursed_AL = list()
Overdue_Disbursed_BL = list()
Overdue_Disbursed_CC = list()
Overdue_Disbursed_CD = list()
Overdue_Disbursed_CV = list()
Overdue_Disbursed_GL = list()
Overdue_Disbursed_HL = list()
Overdue_Disbursed_LAS = list()
Overdue_Disbursed_MFBL = list()
Overdue_Disbursed_MFHL = list()
Overdue_Disbursed_MFOT = list()
Overdue_Disbursed_OTH = list()
Overdue_Disbursed_PL = list()
Overdue_Disbursed_PLBL = list()
Overdue_Disbursed_RL = list()
Overdue_Disbursed_SCC = list()
Overdue_Disbursed_SEL = list()

grp_list_oa2_AL = list()
grp_list_oa2_BL = list()
grp_list_oa2_CC = list()
grp_list_oa2_CD = list()
grp_list_oa2_CV = list()
grp_list_oa2_GL = list()
grp_list_oa2_HL = list()
grp_list_oa2_LAS = list()
grp_list_oa2_MFBL = list()
grp_list_oa2_MFHL = list()
grp_list_oa2_MFOT = list()
grp_list_oa2_OTH = list()
grp_list_oa2_PL = list()
grp_list_oa2_PLBL = list()
grp_list_oa2_RL = list()
grp_list_oa2_SCC = list()
grp_list_oa2_SEL = list()

grp_list_da_AL = list()
grp_list_da_BL = list()
grp_list_da_CC = list()
grp_list_da_CD = list()
grp_list_da_CV = list()
grp_list_da_GL = list()
grp_list_da_HL = list()
grp_list_da_LAS = list()
grp_list_da_MFBL = list()
grp_list_da_MFHL = list()
grp_list_da_MFOT = list()
grp_list_da_OTH = list()
grp_list_da_PL = list()
grp_list_da_PLBL = list()
grp_list_da_RL = list()
grp_list_da_SCC = list()
grp_list_da_SEL = list()

grp_oa2_AL = 0
grp_oa2_BL = 0
grp_oa2_CC = 0
grp_oa2_CD = 0
grp_oa2_CV = 0
grp_oa2_GL = 0
grp_oa2_HL = 0
grp_oa2_LAS = 0
grp_oa2_MFBL = 0
grp_oa2_MFHL = 0
grp_oa2_MFOT = 0
grp_oa2_OTH = 0
grp_oa2_PL = 0
grp_oa2_PLBL = 0
grp_oa2_RL = 0
grp_oa2_SCC = 0
grp_oa2_SEL = 0

grp_da_AL = 0
grp_da_BL = 0
grp_da_CC = 0
grp_da_CD = 0
grp_da_CV = 0
grp_da_GL = 0
grp_da_HL = 0
grp_da_LAS = 0
grp_da_MFBL = 0
grp_da_MFHL = 0
grp_da_MFOT = 0
grp_da_OTH = 0
grp_da_PL = 0
grp_da_PLBL = 0
grp_da_RL = 0
grp_da_SCC = 0
grp_da_SEL = 0

dateClosed_lt_PHED_wo_CNT = list()
count_dtCl_wo_list = list()
count_dtCl_wo = 0

dateClosed_lt_PHED_suit_CNT = list()
count_dtCl_suit_list = list()
count_dtCl_suit = 0

dateClosed_lt_PHED_PH1M_CNT = list()
count_dtCl_ph1m_list = list()
count_dtCl_ph1m = 0

dateClosed_lt_PHED_restruct_CNT = list()
count_dtCl_res_list = list()
count_dtCl_res = 0

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    # print(grp_slice)
    grp_slice.reset_index(drop=True, inplace=True)

    for i in range(0, grp_slice.shape[0]):

        totAcc.append(grp_slice.shape[0])

        if (grp_slice['dateClosed_lt_PHED'][i] == 1) or (grp_slice['dateClosed_lt_PHED'][i] == 0):
            count_dt_phed = count_dt_phed + grp_slice['dateClosed_lt_PHED'][i]
        else:
            continue

        if (grp_slice['ignore_case'][i] == 1) or (grp_slice['ignore_case'][i] == 0):
            count_ic = count_ic + grp_slice['ignore_case'][i]
        else:
            continue

        if (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            curr_bal = curr_bal + float(grp_slice['currentBalance'][i])
            sanc_amt = sanc_amt + float(grp_slice['sanctionAmount'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['sumSanctionAmount'][i] == 0) or (grp_slice['sanctionAmount'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown'):
            continue
        else:
            ratio_cu_sa_ncc_l = float(
                grp_slice['sumCurrentBalance'][i])/float(grp_slice['sumSanctionAmount'][i])

        if (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            curr_bal = curr_bal + float(grp_slice['currentBalance'][i])
            cred_lmt = cred_lmt + float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mode_util = float(
                grp_slice['currentBalance'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mean_util = float(
                grp_slice['currentBalance'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_med_util = float(
                grp_slice['currentBalance'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_min_util = float(
                grp_slice['currentBalance'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mean_util_hi_cred = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mode_util_hi_cred = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_med_util_hi_cr = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_min_util_hi_cr = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mean_util_hi_cr_a = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_mode_util_hi_cr_a = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_med_util_hi_cr_a = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            continue
        else:
            ratio_min_util_hi_cr_a = float(
                grp_slice['sanctionAmount'][i])/float(grp_slice['creditLimit'][i])

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_mean = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_L_mean = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_med = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_L_med = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_mode = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        else:
            sanc_amt_L_mode = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['accountType'][i] in sec_L):
            sec_cnt = sec_cnt + 1
        elif (grp_slice['accountType'][i] in unsec_L):
            unsec_cnt = unsec_cnt + 1
        else:
            continue

        if (grp_slice['accountType'][i] in sec_L) and (grp_slice['dateClosed'][i] == 'unknown'):
            sec_L_cnt = sec_L_cnt + 1
        elif (grp_slice['accountType'][i] in unsec_L) and (grp_slice['dateClosed'][i] == 'unknown'):
            unsec_L_cnt = unsec_L_cnt + 1
        else:
            continue

        if (grp_slice['sanctionAmount'][i]=='unknown'):
            continue
        elif (grp_slice['dictAccountType'][i]=='AL'):
            sanc_amt_med_AL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_AL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='BL'):
            sanc_amt_med_BL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_BL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='CD'):
            sanc_amt_med_CD.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_CD.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='CV'):
            sanc_amt_med_CV.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_CV.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='GL'):
            sanc_amt_med_GL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_GL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='HL'):
            sanc_amt_med_HL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_HL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='LAS'):
            sanc_amt_med_LAS.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_LAS.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='MFBL'):
            sanc_amt_med_MFBL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_MFBL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='MFHL'):
            sanc_amt_med_MFHL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_MFHL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='MFOT'):
            sanc_amt_med_MFOT.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_MFOT.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='OTH'):
            sanc_amt_med_OTH.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_OTH.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='PL'):
            sanc_amt_med_PL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_PL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='PLBL'):
            sanc_amt_med_PLBL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_PLBL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='RL'):
            sanc_amt_med_RL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_RL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i]=='SEL'):
            sanc_amt_med_SEL.append(float(grp_slice['sanctionAmount'][i]))
            sanc_amt_mean_SEL.append(float(grp_slice['sanctionAmount'][i]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL'):
            sanc_amt_L_AL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'BL'):
            sanc_amt_L_BL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'CD'):
            sanc_amt_L_CD.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'CV'):
            sanc_amt_L_CV.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'GL'):
            sanc_amt_L_GL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'HL'):
            sanc_amt_L_HL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'LAS'):
            sanc_amt_L_LAS.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'MFBL'):
            sanc_amt_L_MFBL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'MFHL'):
            sanc_amt_L_MFHL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'MFOT'):
            sanc_amt_L_MFOT.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'OTH'):
            sanc_amt_L_OTH.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'PL'):
            sanc_amt_L_PL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'PLBL'):
            sanc_amt_L_PLBL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'RL'):
            sanc_amt_L_RL.append(float(grp_slice['sanctionAmount'][i]))
        elif (grp_slice['dictAccountType'][i] == 'SEL'):
            sanc_amt_L_SEL.append(float(grp_slice['sanctionAmount'][i]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL'):
            currBal_ncc_l_AL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_AL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'BL'):
            currBal_ncc_l_BL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_BL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'CD'):
            currBal_ncc_l_CD = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_CD = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'CV'):
            currBal_ncc_l_CV = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_CV = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'GL'):
            currBal_ncc_l_GL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_GL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'HL'):
            currBal_ncc_l_HL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_HL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'LAS'):
            currBal_ncc_l_LAS = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_LAS = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'MFBL'):
            currBal_ncc_l_MFBL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_MFBL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'MFHL'):
            currBal_ncc_l_MFHL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_MFHL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'MFOT'):
            currBal_ncc_l_MFOT = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_MFOT = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'OTH'):
            currBal_ncc_l_OTH = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_OTH = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'PL'):
            currBal_ncc_l_PL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_PL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'PLBL'):
            currBal_ncc_l_PLBL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_PLBL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'RL'):
            currBal_ncc_l_RL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_RL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['accountType'][i] == 'SEL'):
            currBal_ncc_l_SEL = float(grp_slice['currentBalance'][i])
            sanc_amt_ncc_l_SEL = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['accountType'][i] == 'AL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_AL = sum_sanc_amt_AL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_BL = sum_sanc_amt_BL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_CD = sum_sanc_amt_CD + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_CV = sum_sanc_amt_CV + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_GL = sum_sanc_amt_GL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_HL = sum_sanc_amt_HL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_LAS = sum_sanc_amt_LAS + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_MFBL = sum_sanc_amt_MFBL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_MFHL = sum_sanc_amt_MFHL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_MFOT = sum_sanc_amt_MFOT + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_OTH = sum_sanc_amt_OTH + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_PL = sum_sanc_amt_PL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_PLBL = sum_sanc_amt_PLBL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_RL = sum_sanc_amt_RL + grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['sanctionAmount'][i] != 'unknown'):
            sum_sanc_amt_SEL = sum_sanc_amt_SEL + \
                grp_slice['sanctionAmount'][i]

        if (grp_slice['accountType'][i] == 'AL'):
            cnt_AL = cnt_AL + 1
        elif (grp_slice['accountType'][i] == 'BL'):
            cnt_BL = cnt_BL + 1
        elif (grp_slice['accountType'][i] == 'CD'):
            cnt_CD = cnt_CD + 1
        elif (grp_slice['accountType'][i] == 'CV'):
            cnt_CV = cnt_CV + 1
        elif (grp_slice['accountType'][i] == 'GL'):
            cnt_GL = cnt_GL + 1
        elif (grp_slice['accountType'][i] == 'HL'):
            cnt_HL = cnt_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS'):
            cnt_LAS = cnt_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL'):
            cnt_MFBL = cnt_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL'):
            cnt_MFHL = cnt_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT'):
            cnt_MFOT = cnt_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH'):
            cnt_OTH = cnt_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL'):
            cnt_PL = cnt_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL'):
            cnt_PLBL = cnt_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL'):
            cnt_RL = cnt_RL + 1
        elif (grp_slice['accountType'][i] == 'SEL'):
            cnt_SEL = cnt_SEL + 1

        if (grp_slice['dateClosed'][i] == 'unknown'):
            cnt = cnt + 1
        else:
            continue

        if (grp_slice['accountType'][i] == 'AL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_AL = sum_L_sanc_amt_AL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_BL = sum_L_sanc_amt_BL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_CD = sum_L_sanc_amt_CD + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_CV = sum_L_sanc_amt_CV + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_GL = sum_L_sanc_amt_GL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_HL = sum_L_sanc_amt_HL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_LAS = sum_L_sanc_amt_LAS + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_MFBL = sum_L_sanc_amt_MFBL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_MFHL = sum_L_sanc_amt_MFHL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_MFOT = sum_L_sanc_amt_MFOT + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_OTH = sum_L_sanc_amt_OTH + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_PL = sum_L_sanc_amt_PL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_PLBL = sum_L_sanc_amt_PLBL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_RL = sum_L_sanc_amt_RL + \
                grp_slice['sanctionAmount'][i]
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['sanctionAmount'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_SEL = sum_L_sanc_amt_SEL + \
                grp_slice['sanctionAmount'][i]

        if (grp_slice['accountType'][i] == 'AL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_AL = cnt_L_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_BL = cnt_L_BL + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_CD = cnt_L_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_CV = cnt_L_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_GL = cnt_L_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_HL = cnt_L_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_LAS = cnt_L_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_MFBL = cnt_L_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_MFHL = cnt_L_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_MFOT = cnt_L_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_OTH = cnt_L_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_PL = cnt_L_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_PLBL = cnt_L_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_RL = cnt_L_RL + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_SEL = cnt_L_SEL + 1

        if (grp_slice['accountType'][i] == 'AL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_AL = curr_bal_AL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_BL = curr_bal_BL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_CD = curr_bal_CD + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_CV = curr_bal_CV + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_GL = curr_bal_GL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_HL = curr_bal_HL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_LAS = curr_bal_LAS + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_MFBL = curr_bal_MFBL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_MFHL = curr_bal_MFHL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_MFOT = curr_bal_MFOT + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_OTH = curr_bal_OTH + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_PL = curr_bal_PL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_PLBL = curr_bal_PLBL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_RL = curr_bal_RL + grp_slice['currentBalance'][i]
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['currentBalance'][i] != 'unknown') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_SEL = curr_bal_SEL + grp_slice['currentBalance'][i]

        if (grp_slice['writeOff'][i] == 1) or (grp_slice['writeOff'][i] == 0):
            count_wo = count_wo + grp_slice['writeOff'][i]
        else:
            continue

        if (grp_slice['restructured'][i] == 1) or (grp_slice['restructured'][i] == 0):
            count_re = count_re + grp_slice['restructured'][i]
        else:
            continue

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1):
            count_wo_AL = count_wo_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1):
            count_wo_BL = count_wo_BL + 1
        elif (grp_slice['accountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1):
            count_wo_CC = count_wo_CC + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1):
            count_wo_CD = count_wo_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1):
            count_wo_CV = count_wo_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1):
            count_wo_GL = count_wo_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1):
            count_wo_HL = count_wo_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1):
            count_wo_LAS = count_wo_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1):
            count_wo_MFBL = count_wo_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1):
            count_wo_MFHL = count_wo_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1):
            count_wo_MFOT = count_wo_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1):
            count_wo_OTH = count_wo_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1):
            count_wo_PL = count_wo_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1):
            count_wo_PLBL = count_wo_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1):
            count_wo_RL = count_wo_RL + 1
        elif (grp_slice['accountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1):
            count_wo_SCC = count_wo_SCC + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1):
            count_wo_SEL = count_wo_SEL + 1

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['restructured'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['restructured'][i] == 1):
            count_re_AL = count_re_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['restructured'][i] == 1):
            count_re_BL = count_re_BL + 1
        elif (grp_slice['accountType'][i] == 'CC') and (grp_slice['restructured'][i] == 1):
            count_re_CC = count_re_CC + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['restructured'][i] == 1):
            count_re_CD = count_re_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['restructured'][i] == 1):
            count_re_CV = count_re_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['restructured'][i] == 1):
            count_re_GL = count_re_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['restructured'][i] == 1):
            count_re_HL = count_re_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['restructured'][i] == 1):
            count_re_LAS = count_re_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['restructured'][i] == 1):
            count_re_MFBL = count_re_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['restructured'][i] == 1):
            count_re_MFHL = count_re_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['restructured'][i] == 1):
            count_re_MFOT = count_re_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['restructured'][i] == 1):
            count_re_OTH = count_re_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['restructured'][i] == 1):
            count_re_PL = count_re_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['restructured'][i] == 1):
            count_re_PLBL = count_re_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['restructured'][i] == 1):
            count_re_RL = count_re_RL + 1
        elif (grp_slice['accountType'][i] == 'SCC') and (grp_slice['restructured'][i] == 1):
            count_re_SCC = count_re_SCC + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['restructured'][i] == 1):
            count_re_SEL = count_re_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 3) and (grp_slice['writeOff'][i] == 1):
            count_wo_l3m = count_wo_l3m + 1

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 3):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_AL = count_wo_l3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_BL = count_wo_l3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_CC = count_wo_l3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_CD = count_wo_l3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_CV = count_wo_l3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_GL = count_wo_l3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_HL = count_wo_l3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_LAS = count_wo_l3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_MFBL = count_wo_l3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_MFHL = count_wo_l3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_MFOT = count_wo_l3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_OTH = count_wo_l3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_PL = count_wo_l3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_PLBL = count_wo_l3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_RL = count_wo_l3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_SCC = count_wo_l3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            count_wo_l3m_SEL = count_wo_l3m_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 6) and (grp_slice['writeOff'][i] == 1):
            count_wo_l6m = count_wo_l6m + 1

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 6):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_AL = count_wo_l6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_BL = count_wo_l6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_CC = count_wo_l6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_CD = count_wo_l6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_CV = count_wo_l6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_GL = count_wo_l6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_HL = count_wo_l6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_LAS = count_wo_l6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_MFBL = count_wo_l6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_MFHL = count_wo_l6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_MFOT = count_wo_l6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_OTH = count_wo_l6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_PL = count_wo_l6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_PLBL = count_wo_l6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_RL = count_wo_l6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_SCC = count_wo_l6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            count_wo_l6m_SEL = count_wo_l6m_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 9) and (grp_slice['writeOff'][i] == 1):
            count_wo_l9m = count_wo_l9m + 1

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 9):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_AL = count_wo_l9m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_BL = count_wo_l9m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_CC = count_wo_l9m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_CD = count_wo_l9m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_CV = count_wo_l9m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_GL = count_wo_l9m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_HL = count_wo_l9m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_LAS = count_wo_l9m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_MFBL = count_wo_l9m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_MFHL = count_wo_l9m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_MFOT = count_wo_l9m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_OTH = count_wo_l9m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_PL = count_wo_l9m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_PLBL = count_wo_l9m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_RL = count_wo_l9m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_SCC = count_wo_l9m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            count_wo_l9m_SEL = count_wo_l9m_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 12) and (grp_slice['writeOff'][i] == 1):
            count_wo_l1y = count_wo_l1y + 1

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 12):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_AL = count_wo_l1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_BL = count_wo_l1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_CC = count_wo_l1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_CD = count_wo_l1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_CV = count_wo_l1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_GL = count_wo_l1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_HL = count_wo_l1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_LAS = count_wo_l1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_MFBL = count_wo_l1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_MFHL = count_wo_l1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_MFOT = count_wo_l1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_OTH = count_wo_l1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_PL = count_wo_l1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_PLBL = count_wo_l1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_RL = count_wo_l1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_SCC = count_wo_l1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            count_wo_l1y_SEL = count_wo_l1y_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 24) and (grp_slice['writeOff'][i] == 1):
            count_wo_l2y = count_wo_l2y + 1

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 24):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_AL = count_wo_l2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_BL = count_wo_l2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_CC = count_wo_l2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_CD = count_wo_l2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_CV = count_wo_l2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_GL = count_wo_l2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_HL = count_wo_l2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_LAS = count_wo_l2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_MFBL = count_wo_l2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_MFHL = count_wo_l2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_MFOT = count_wo_l2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_OTH = count_wo_l2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_PL = count_wo_l2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_PLBL = count_wo_l2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_RL = count_wo_l2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_SCC = count_wo_l2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            count_wo_l2y_SEL = count_wo_l2y_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            continue
        elif (grp_slice['month_diff'][i] <= 36) and (grp_slice['writeOff'][i] == 1):
            count_wo_l3y = count_wo_l3y + grp_slice['writeOff'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['month_diff'][i] > 36):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_AL = count_wo_l3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_BL = count_wo_l3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_CC = count_wo_l3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_CD = count_wo_l3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_CV = count_wo_l3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_GL = count_wo_l3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_HL = count_wo_l3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_LAS = count_wo_l3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_MFBL = count_wo_l3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_MFHL = count_wo_l3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_MFOT = count_wo_l3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_OTH = count_wo_l3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_PL = count_wo_l3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_PLBL = count_wo_l3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_RL = count_wo_l3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_SCC = count_wo_l3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            count_wo_l3y_SEL = count_wo_l3y_SEL + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            continue
        elif ((grp_slice['month_diff'][i] <= 12) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            count_wo_l1y_plt = count_wo_l1y_plt + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            continue
        elif ((grp_slice['month_diff'][i] <= 24) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            count_wo_l2y_plt = count_wo_l2y_plt + 1

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            continue
        elif ((grp_slice['month_diff'][i] <= 36) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            count_wo_l3y_plt = count_wo_l3y_plt + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m = count_op_l3m + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_AL = count_op_l3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_BL = count_op_l3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_CC = count_op_l3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_CD = count_op_l3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_CV = count_op_l3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_GL = count_op_l3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_HL = count_op_l3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_LAS = count_op_l3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_MFBL = count_op_l3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_MFHL = count_op_l3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_MFOT = count_op_l3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_OTH = count_op_l3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_PL = count_op_l3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_PLBL = count_op_l3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_RL = count_op_l3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_SCC = count_op_l3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 3):
            count_op_l3m_SEL = count_op_l3m_SEL + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m = count_op_l6m + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_AL = count_op_l6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_BL = count_op_l6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_CC = count_op_l6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_CD = count_op_l6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_CV = count_op_l6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_GL = count_op_l6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_HL = count_op_l6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_LAS = count_op_l6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_MFBL = count_op_l6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_MFHL = count_op_l6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_MFOT = count_op_l6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_OTH = count_op_l6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_PL = count_op_l6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_PLBL = count_op_l6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_RL = count_op_l6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_SCC = count_op_l6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 6):
            count_op_l6m_SEL = count_op_l6m_SEL + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m = count_op_l9m + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_AL = count_op_l9m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_BL = count_op_l9m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_CC = count_op_l9m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_CD = count_op_l9m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_CV = count_op_l9m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_GL = count_op_l9m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_HL = count_op_l9m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_LAS = count_op_l9m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_MFBL = count_op_l9m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_MFHL = count_op_l9m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_MFOT = count_op_l9m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_OTH = count_op_l9m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_PL = count_op_l9m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_PLBL = count_op_l9m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_RL = count_op_l9m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_SCC = count_op_l9m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 9):
            count_op_l9m_SEL = count_op_l9m_SEL + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y = count_op_l1y + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_AL = count_op_l1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_BL = count_op_l1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_CC = count_op_l1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_CD = count_op_l1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_CV = count_op_l1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_GL = count_op_l1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_HL = count_op_l1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_LAS = count_op_l1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_MFBL = count_op_l1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_MFHL = count_op_l1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_MFOT = count_op_l1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_OTH = count_op_l1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_PL = count_op_l1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_PLBL = count_op_l1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_RL = count_op_l1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_SCC = count_op_l1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 12):
            count_op_l1y_SEL = count_op_l1y_SEL + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y = count_op_l2y + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_AL = count_op_l2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_BL = count_op_l2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_CC = count_op_l2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_CD = count_op_l2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_CV = count_op_l2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_GL = count_op_l2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_HL = count_op_l2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_LAS = count_op_l2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_MFBL = count_op_l2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_MFHL = count_op_l2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_MFOT = count_op_l2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_OTH = count_op_l2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_PL = count_op_l2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_PLBL = count_op_l2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_RL = count_op_l2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_SCC = count_op_l2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 24):
            count_op_l2y_SEL = count_op_l2y_SEL + 1

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y = count_op_l3y + 1
        else:
            continue

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_AL = count_op_l3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_BL = count_op_l3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_CC = count_op_l3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_CD = count_op_l3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_CV = count_op_l3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_GL = count_op_l3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_HL = count_op_l3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_LAS = count_op_l3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_MFBL = count_op_l3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_MFHL = count_op_l3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_MFOT = count_op_l3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_OTH = count_op_l3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_PL = count_op_l3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_PLBL = count_op_l3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_RL = count_op_l3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_SCC = count_op_l3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['mo_diff_do_ld'][i] <= 36):
            count_op_l3y_SEL = count_op_l3y_SEL + 1

        if (grp_slice['overdueAmount'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL'):
            oa_AL = oa_AL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'BL'):
            oa_BL = oa_BL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CC'):
            oa_CC = oa_CC + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CD'):
            oa_CD = oa_CD + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CV'):
            oa_CV = oa_CV + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'GL'):
            oa_GL = oa_GL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'HL'):
            oa_HL = oa_HL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'LAS'):
            oa_LAS = oa_LAS + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFBL'):
            oa_MFBL = oa_MFBL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFHL'):
            oa_MFHL = oa_MFHL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFOT'):
            oa_MFOT = oa_MFOT + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'OTH'):
            oa_OTH = oa_OTH + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'PL'):
            oa_PL = oa_PL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'PLBL'):
            oa_PLBL = oa_PLBL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'RL'):
            oa_RL = oa_RL + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'SCC'):
            oa_SCC = oa_SCC + (grp_slice['overdueAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'SEL'):
            oa_SEL = oa_SEL + (grp_slice['overdueAmount'][i])

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 0):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL'):
            grp_oa_AL = float(grp_slice['overdueAmount'][i])
            grp_cb_AL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'BL'):
            grp_oa_BL = float(grp_slice['overdueAmount'][i])
            grp_cb_BL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'CC'):
            grp_oa_CC = float(grp_slice['overdueAmount'][i])
            grp_cb_CC = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'CD'):
            grp_oa_CD = float(grp_slice['overdueAmount'][i])
            grp_cb_CD = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'CV'):
            grp_oa_CV = float(grp_slice['overdueAmount'][i])
            grp_cb_CV = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'GL'):
            grp_oa_GL = float(grp_slice['overdueAmount'][i])
            grp_cb_GL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'HL'):
            grp_oa_HL = float(grp_slice['overdueAmount'][i])
            grp_cb_HL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'LAS'):
            grp_oa_LAS = float(grp_slice['overdueAmount'][i])
            grp_cb_LAS = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFBL'):
            grp_oa_MFBL = float(grp_slice['overdueAmount'][i])
            grp_cb_MFBL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFHL'):
            grp_oa_MFHL = float(grp_slice['overdueAmount'][i])
            grp_cb_MFHL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFOT'):
            grp_oa_MFOT = float(grp_slice['overdueAmount'][i])
            grp_cb_MFOT = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'OTH'):
            grp_oa_OTH = float(grp_slice['overdueAmount'][i])
            grp_cb_OTH = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'PL'):
            grp_oa_PL = float(grp_slice['overdueAmount'][i])
            grp_cb_PL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'PLBL'):
            grp_oa_PLBL = float(grp_slice['overdueAmount'][i])
            grp_cb_PLBL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'RL'):
            grp_oa_RL = float(grp_slice['overdueAmount'][i])
            grp_cb_RL = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'SCC'):
            grp_oa_SCC = float(grp_slice['overdueAmount'][i])
            grp_cb_SCC = float(grp_slice['currentBalance'][i])
        elif (grp_slice['dictAccountType'][i] == 'SEL'):
            grp_oa_SEL = float(grp_slice['overdueAmount'][i])
            grp_cb_SEL = float(grp_slice['currentBalance'][i])

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 0):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL'):
            grp_oa2_AL = float(grp_slice['overdueAmount'][i])
            grp_da_AL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'BL'):
            grp_oa2_BL = float(grp_slice['overdueAmount'][i])
            grp_da_BL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CC'):
            grp_oa2_CC = float(grp_slice['overdueAmount'][i])
            grp_da_CC = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CD'):
            grp_oa2_CD = float(grp_slice['overdueAmount'][i])
            grp_da_CD = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'CV'):
            grp_oa2_CV = float(grp_slice['overdueAmount'][i])
            grp_da_CV = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'GL'):
            grp_oa2_GL = float(grp_slice['overdueAmount'][i])
            grp_da_GL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'HL'):
            grp_oa2_HL = float(grp_slice['overdueAmount'][i])
            grp_da_HL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'LAS'):
            grp_oa2_LAS = float(grp_slice['overdueAmount'][i])
            grp_da_LAS = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFBL'):
            grp_oa2_MFBL = float(grp_slice['overdueAmount'][i])
            grp_da_MFBL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFHL'):
            grp_oa2_MFHL = float(grp_slice['overdueAmount'][i])
            grp_da_MFHL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'MFOT'):
            grp_oa2_MFOT = float(grp_slice['overdueAmount'][i])
            grp_da_MFOT = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'OTH'):
            grp_oa2_OTH = float(grp_slice['overdueAmount'][i])
            grp_da_OTH = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'PL'):
            grp_oa2_PL = float(grp_slice['overdueAmount'][i])
            grp_da_PL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'PLBL'):
            grp_oa2_PLBL = float(grp_slice['overdueAmount'][i])
            grp_da_PLBL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'RL'):
            grp_oa2_RL = float(grp_slice['overdueAmount'][i])
            grp_da_RL = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'SCC'):
            grp_oa2_SCC = float(grp_slice['overdueAmount'][i])
            grp_da_SCC = float(grp_slice['sanctionAmount'][i])
        elif (grp_slice['dictAccountType'][i] == 'SEL'):
            grp_oa2_SEL = float(grp_slice['overdueAmount'][i])
            grp_da_SEL = float(grp_slice['sanctionAmount'][i])

        if (grp_slice['dateClosed_lt_PHED_wo'][i] == 1) or (grp_slice['dateClosed_lt_PHED_wo'][i] == 0):
            count_dtCl_wo = count_dtCl_wo + \
                grp_slice['dateClosed_lt_PHED_wo'][i]
        else:
            continue

        if (grp_slice['dateClosed_lt_PHED_suit'][i] == 1) or (grp_slice['dateClosed_lt_PHED_suit'][i] == 0):
            count_dtCl_suit = count_dtCl_suit + \
                grp_slice['dateClosed_lt_PHED_suit'][i]
        else:
            continue

        if (grp_slice['dateClosed_lt_PHED_PH1M'][i] == 1) or (grp_slice['dateClosed_lt_PHED_PH1M'][i] == 0):
            count_dtCl_ph1m = count_dtCl_ph1m + \
                grp_slice['dateClosed_lt_PHED_PH1M'][i]
        else:
            continue

        if (grp_slice['dateClosed_lt_PHED_restruct'][i] == 1) or (grp_slice['dateClosed_lt_PHED_restruct'][i] == 0):
            count_dtCl_res = count_dtCl_res + \
                grp_slice['dateClosed_lt_PHED_restruct'][i]
        else:
            continue

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['dateClosed'][i] == 'unknown'):
            grp_slice['totAcc_L'][i] = cnt
        else:
            grp_slice['totAcc_L'][i] = 0

    count_list_dt_phed.append(count_dt_phed)
    count_dt_phed = 0

    count_list_ic.append(count_ic)
    count_ic = 0

    sum_cur_bal.append(curr_bal)
    sum_sanc_amt.append(sanc_amt)
    sum_cred_lmt.append(cred_lmt)

    curr_bal = 0
    sanc_amt = 0
    cred_lmt = 0

    ratio_list_cu_sa_ncc_l.append(ratio_cu_sa_ncc_l)
    ratio_cu_sa_ncc_l = 0

    ratio_list_mode_util.append(ratio_mode_util)
    ratio_mode_util = 0

    ratio_list_mean_util.append(ratio_mean_util)
    ratio_mean_util = 0

    ratio_list_med_util.append(ratio_med_util)
    ratio_med_util = 0

    ratio_list_min_util.append(ratio_min_util)
    ratio_min_util = 0

    ratio_list_mean_util_hi_cred.append(ratio_mean_util_hi_cred)
    ratio_mean_util_hi_cred = 0

    ratio_list_mode_util_hi_cred.append(ratio_mode_util_hi_cred)
    ratio_mode_util_hi_cred = 0

    ratio_list_med_util_hi_cr.append(ratio_med_util_hi_cr)
    ratio_med_util_hi_cr = 0

    ratio_list_min_util_hi_cr.append(ratio_min_util_hi_cr)
    ratio_min_util_hi_cr = 0

    ratio_list_mean_util_hi_cr_a.append(ratio_mean_util_hi_cr_a)
    ratio_mean_util_hi_cr_a = 0

    ratio_list_mode_util_hi_cr_a.append(ratio_mode_util_hi_cr_a)
    ratio_mode_util_hi_cr_a = 0

    ratio_list_med_util_hi_cr_a.append(ratio_med_util_hi_cr_a)
    ratio_med_util_hi_cr_a = 0

    ratio_list_min_util_hi_cr_a.append(ratio_min_util_hi_cr_a)
    ratio_min_util_hi_cr_a = 0

    sanc_amt_list_mean.append(sanc_amt_mean)
    sanc_amt_mean = 0

    sanc_amt_list_L_mean.append(sanc_amt_L_mean)
    sanc_amt_L_mean = 0

    sanc_amt_list_med.append(sanc_amt_med)
    sanc_amt_med = 0

    sanc_amt_list_L_med.append(sanc_amt_L_med)
    sanc_amt_L_med = 0

    sanc_amt_list_mode.append(sanc_amt_mode)
    sanc_amt_mode = 0

    sanc_amt_list_L_mode.append(sanc_amt_L_mode)
    sanc_amt_L_mode = 0

    sec_cnt_list.append(sec_cnt)
    sec_cnt = 0

    unsec_cnt_list.append(unsec_cnt)
    unsec_cnt = 0

    sec_L_cnt_list.append(sec_L_cnt)
    unsec_L_cnt_list.append(unsec_L_cnt)

    sec_L_cnt = 0
    unsec_L_cnt = 0

    sanc_amt_med_list_AL.append(sanc_amt_med_AL)
    sanc_amt_med_list_BL.append(sanc_amt_med_BL)
    sanc_amt_med_list_CD.append(sanc_amt_med_CD)
    sanc_amt_med_list_CV.append(sanc_amt_med_CV)
    sanc_amt_med_list_GL.append(sanc_amt_med_GL)
    sanc_amt_med_list_HL.append(sanc_amt_med_HL)
    sanc_amt_med_list_LAS.append(sanc_amt_med_LAS)
    sanc_amt_med_list_MFBL.append(sanc_amt_med_MFBL)
    sanc_amt_med_list_MFHL.append(sanc_amt_med_MFHL)
    sanc_amt_med_list_MFOT.append(sanc_amt_med_MFOT)
    sanc_amt_med_list_OTH.append(sanc_amt_med_OTH)
    sanc_amt_med_list_PL.append(sanc_amt_med_PL)
    sanc_amt_med_list_PLBL.append(sanc_amt_med_PLBL)
    sanc_amt_med_list_RL.append(sanc_amt_med_RL)
    sanc_amt_med_list_SEL.append(sanc_amt_med_SEL)
    
    sanc_amt_med_AL = list()
    sanc_amt_med_BL = list()
    sanc_amt_med_CD = list()
    sanc_amt_med_CV = list()
    sanc_amt_med_GL = list()
    sanc_amt_med_HL = list()
    sanc_amt_med_LAS = list()
    sanc_amt_med_MFBL = list()
    sanc_amt_med_MFHL = list()
    sanc_amt_med_MFOT = list()
    sanc_amt_med_OTH = list()
    sanc_amt_med_PL = list()
    sanc_amt_med_PLBL = list()
    sanc_amt_med_RL = list()
    sanc_amt_med_SEL = list()

    sanc_amt_mean_list_AL.append(sanc_amt_mean_AL)
    sanc_amt_mean_list_BL.append(sanc_amt_mean_BL)
    sanc_amt_mean_list_CD.append(sanc_amt_mean_CD)
    sanc_amt_mean_list_CV.append(sanc_amt_mean_CV)
    sanc_amt_mean_list_GL.append(sanc_amt_mean_GL)
    sanc_amt_mean_list_HL.append(sanc_amt_mean_HL)
    sanc_amt_mean_list_LAS.append(sanc_amt_mean_LAS)
    sanc_amt_mean_list_MFBL.append(sanc_amt_mean_MFBL)
    sanc_amt_mean_list_MFHL.append(sanc_amt_mean_MFHL)
    sanc_amt_mean_list_MFOT.append(sanc_amt_mean_MFOT)
    sanc_amt_mean_list_OTH.append(sanc_amt_mean_OTH)
    sanc_amt_mean_list_PL.append(sanc_amt_mean_PL)
    sanc_amt_mean_list_PLBL.append(sanc_amt_mean_PLBL)
    sanc_amt_mean_list_RL.append(sanc_amt_mean_RL)
    sanc_amt_mean_list_SEL.append(sanc_amt_mean_SEL)
    
    sanc_amt_mean_AL = list()
    sanc_amt_mean_BL = list()
    sanc_amt_mean_CD = list()
    sanc_amt_mean_CV = list()
    sanc_amt_mean_GL = list()
    sanc_amt_mean_HL = list()
    sanc_amt_mean_LAS = list()
    sanc_amt_mean_MFBL = list()
    sanc_amt_mean_MFHL = list()
    sanc_amt_mean_MFOT = list()
    sanc_amt_mean_OTH = list()
    sanc_amt_mean_PL = list()
    sanc_amt_mean_PLBL = list()
    sanc_amt_mean_RL = list()
    sanc_amt_mean_SEL = list()

    sanc_amt_L_list_AL.append(sanc_amt_L_AL)
    sanc_amt_L_list_BL.append(sanc_amt_L_BL)
    sanc_amt_L_list_CD.append(sanc_amt_L_CD)
    sanc_amt_L_list_CV.append(sanc_amt_L_CV)
    sanc_amt_L_list_GL.append(sanc_amt_L_GL)
    sanc_amt_L_list_HL.append(sanc_amt_L_HL)
    sanc_amt_L_list_LAS.append(sanc_amt_L_LAS)
    sanc_amt_L_list_MFBL.append(sanc_amt_L_MFBL)
    sanc_amt_L_list_MFHL.append(sanc_amt_L_MFHL)
    sanc_amt_L_list_MFOT.append(sanc_amt_L_MFOT)
    sanc_amt_L_list_OTH.append(sanc_amt_L_OTH)
    sanc_amt_L_list_PL.append(sanc_amt_L_PL)
    sanc_amt_L_list_PLBL.append(sanc_amt_L_PLBL)
    sanc_amt_L_list_RL.append(sanc_amt_L_RL)
    sanc_amt_L_list_SEL.append(sanc_amt_L_SEL)

    sanc_amt_L_AL = list()
    sanc_amt_L_BL = list()
    sanc_amt_L_CD = list()
    sanc_amt_L_CV = list()
    sanc_amt_L_GL = list()
    sanc_amt_L_HL = list()
    sanc_amt_L_LAS = list()
    sanc_amt_L_MFBL = list()
    sanc_amt_L_MFHL = list()
    sanc_amt_L_MFOT = list()
    sanc_amt_L_OTH = list()
    sanc_amt_L_PL = list()
    sanc_amt_L_PLBL = list()
    sanc_amt_L_RL = list()
    sanc_amt_L_SEL = list()

    currentBalance_AL.append(currBal_ncc_l_AL)
    currentBalance_BL.append(currBal_ncc_l_BL)
    currentBalance_CD.append(currBal_ncc_l_CD)
    currentBalance_CV.append(currBal_ncc_l_CV)
    currentBalance_GL.append(currBal_ncc_l_GL)
    currentBalance_HL.append(currBal_ncc_l_HL)
    currentBalance_LAS.append(currBal_ncc_l_LAS)
    currentBalance_MFBL.append(currBal_ncc_l_MFBL)
    currentBalance_MFHL.append(currBal_ncc_l_MFHL)
    currentBalance_MFOT.append(currBal_ncc_l_MFOT)
    currentBalance_OTH.append(currBal_ncc_l_OTH)
    currentBalance_PL.append(currBal_ncc_l_PL)
    currentBalance_PLBL.append(currBal_ncc_l_PLBL)
    currentBalance_RL.append(currBal_ncc_l_RL)
    currentBalance_SEL.append(currBal_ncc_l_SEL)

    sanctionedAmount_AL.append(sanc_amt_ncc_l_AL)
    sanctionedAmount_BL.append(sanc_amt_ncc_l_BL)
    sanctionedAmount_CD.append(sanc_amt_ncc_l_CD)
    sanctionedAmount_CV.append(sanc_amt_ncc_l_CV)
    sanctionedAmount_GL.append(sanc_amt_ncc_l_GL)
    sanctionedAmount_HL.append(sanc_amt_ncc_l_HL)
    sanctionedAmount_LAS.append(sanc_amt_ncc_l_LAS)
    sanctionedAmount_MFBL.append(sanc_amt_ncc_l_MFBL)
    sanctionedAmount_MFHL.append(sanc_amt_ncc_l_MFHL)
    sanctionedAmount_MFOT.append(sanc_amt_ncc_l_MFOT)
    sanctionedAmount_OTH.append(sanc_amt_ncc_l_OTH)
    sanctionedAmount_PL.append(sanc_amt_ncc_l_PL)
    sanctionedAmount_PLBL.append(sanc_amt_ncc_l_PLBL)
    sanctionedAmount_RL.append(sanc_amt_ncc_l_RL)
    sanctionedAmount_SEL.append(sanc_amt_ncc_l_SEL)

    currBal_ncc_l_AL = 0
    currBal_ncc_l_BL = 0
    currBal_ncc_l_CD = 0
    currBal_ncc_l_CV = 0
    currBal_ncc_l_GL = 0
    currBal_ncc_l_HL = 0
    currBal_ncc_l_LAS = 0
    currBal_ncc_l_MFBL = 0
    currBal_ncc_l_MFHL = 0
    currBal_ncc_l_MFOT = 0
    currBal_ncc_l_OTH = 0
    currBal_ncc_l_PL = 0
    currBal_ncc_l_PLBL = 0
    currBal_ncc_l_RL = 0
    currBal_ncc_l_SEL = 0

    sanc_amt_ncc_l_AL = 0
    sanc_amt_ncc_l_BL = 0
    sanc_amt_ncc_l_CD = 0
    sanc_amt_ncc_l_CV = 0
    sanc_amt_ncc_l_GL = 0
    sanc_amt_ncc_l_HL = 0
    sanc_amt_ncc_l_LAS = 0
    sanc_amt_ncc_l_MFBL = 0
    sanc_amt_ncc_l_MFHL = 0
    sanc_amt_ncc_l_MFOT = 0
    sanc_amt_ncc_l_OTH = 0
    sanc_amt_ncc_l_PL = 0
    sanc_amt_ncc_l_PLBL = 0
    sanc_amt_ncc_l_RL = 0
    sanc_amt_ncc_l_SEL = 0

    sum_sanc_amt_list_AL.append(sum_sanc_amt_AL)
    sum_sanc_amt_list_BL.append(sum_sanc_amt_BL)
    sum_sanc_amt_list_CD.append(sum_sanc_amt_CD)
    sum_sanc_amt_list_CV.append(sum_sanc_amt_CV)
    sum_sanc_amt_list_GL.append(sum_sanc_amt_GL)
    sum_sanc_amt_list_HL.append(sum_sanc_amt_HL)
    sum_sanc_amt_list_LAS.append(sum_sanc_amt_LAS)
    sum_sanc_amt_list_MFBL.append(sum_sanc_amt_MFBL)
    sum_sanc_amt_list_MFHL.append(sum_sanc_amt_MFHL)
    sum_sanc_amt_list_MFOT.append(sum_sanc_amt_MFOT)
    sum_sanc_amt_list_OTH.append(sum_sanc_amt_OTH)
    sum_sanc_amt_list_PL.append(sum_sanc_amt_PL)
    sum_sanc_amt_list_PLBL.append(sum_sanc_amt_PLBL)
    sum_sanc_amt_list_RL.append(sum_sanc_amt_RL)
    sum_sanc_amt_list_SEL.append(sum_sanc_amt_SEL)

    sum_sanc_amt_AL = 0
    sum_sanc_amt_BL = 0
    sum_sanc_amt_CD = 0
    sum_sanc_amt_CV = 0
    sum_sanc_amt_GL = 0
    sum_sanc_amt_HL = 0
    sum_sanc_amt_LAS = 0
    sum_sanc_amt_MFBL = 0
    sum_sanc_amt_MFHL = 0
    sum_sanc_amt_MFOT = 0
    sum_sanc_amt_OTH = 0
    sum_sanc_amt_PL = 0
    sum_sanc_amt_PLBL = 0
    sum_sanc_amt_RL = 0
    sum_sanc_amt_SEL = 0

    cnt_list_AL.append(cnt_AL)
    cnt_list_BL.append(cnt_BL)
    cnt_list_CD.append(cnt_CD)
    cnt_list_CV.append(cnt_CV)
    cnt_list_GL.append(cnt_GL)
    cnt_list_HL.append(cnt_HL)
    cnt_list_LAS.append(cnt_LAS)
    cnt_list_MFBL.append(cnt_MFBL)
    cnt_list_MFHL.append(cnt_MFHL)
    cnt_list_MFOT.append(cnt_MFOT)
    cnt_list_OTH.append(cnt_OTH)
    cnt_list_PL.append(cnt_PL)
    cnt_list_PLBL.append(cnt_PLBL)
    cnt_list_RL.append(cnt_RL)
    cnt_list_SEL.append(cnt_SEL)

    cnt_AL = 0
    cnt_BL = 0
    cnt_CD = 0
    cnt_CV = 0
    cnt_GL = 0
    cnt_HL = 0
    cnt_LAS = 0
    cnt_MFBL = 0
    cnt_MFHL = 0
    cnt_MFOT = 0
    cnt_OTH = 0
    cnt_PL = 0
    cnt_PLBL = 0
    cnt_RL = 0

    cnt = 0

    sum_L_sanc_amt_list_L_AL.append(sum_L_sanc_amt_AL)
    sum_L_sanc_amt_list_L_BL.append(sum_L_sanc_amt_BL)
    sum_L_sanc_amt_list_L_CD.append(sum_L_sanc_amt_CD)
    sum_L_sanc_amt_list_L_CV.append(sum_L_sanc_amt_CV)
    sum_L_sanc_amt_list_L_GL.append(sum_L_sanc_amt_GL)
    sum_L_sanc_amt_list_L_HL.append(sum_L_sanc_amt_HL)
    sum_L_sanc_amt_list_L_LAS.append(sum_L_sanc_amt_LAS)
    sum_L_sanc_amt_list_L_MFBL.append(sum_L_sanc_amt_MFBL)
    sum_L_sanc_amt_list_L_MFHL.append(sum_L_sanc_amt_MFHL)
    sum_L_sanc_amt_list_L_MFOT.append(sum_L_sanc_amt_MFOT)
    sum_L_sanc_amt_list_L_OTH.append(sum_L_sanc_amt_OTH)
    sum_L_sanc_amt_list_L_PL.append(sum_L_sanc_amt_PL)
    sum_L_sanc_amt_list_L_PLBL.append(sum_L_sanc_amt_PLBL)
    sum_L_sanc_amt_list_L_RL.append(sum_L_sanc_amt_RL)
    sum_L_sanc_amt_list_L_SEL.append(sum_L_sanc_amt_SEL)

    sum_L_sanc_amt_AL = 0
    sum_L_sanc_amt_BL = 0
    sum_L_sanc_amt_CD = 0
    sum_L_sanc_amt_CV = 0
    sum_L_sanc_amt_GL = 0
    sum_L_sanc_amt_HL = 0
    sum_L_sanc_amt_LAS = 0
    sum_L_sanc_amt_MFBL = 0
    sum_L_sanc_amt_MFHL = 0
    sum_L_sanc_amt_MFOT = 0
    sum_L_sanc_amt_OTH = 0
    sum_L_sanc_amt_PL = 0
    sum_L_sanc_amt_PLBL = 0
    sum_L_sanc_amt_RL = 0
    sum_L_sanc_amt_SEL = 0

    cnt_L_list_AL.append(cnt_L_AL)
    cnt_L_list_BL.append(cnt_L_BL)
    cnt_L_list_CD.append(cnt_L_CD)
    cnt_L_list_CV.append(cnt_L_CV)
    cnt_L_list_GL.append(cnt_L_GL)
    cnt_L_list_HL.append(cnt_L_HL)
    cnt_L_list_LAS.append(cnt_L_LAS)
    cnt_L_list_MFBL.append(cnt_L_MFBL)
    cnt_L_list_MFHL.append(cnt_L_MFHL)
    cnt_L_list_MFOT.append(cnt_L_MFOT)
    cnt_L_list_OTH.append(cnt_L_OTH)
    cnt_L_list_PL.append(cnt_L_PL)
    cnt_L_list_PLBL.append(cnt_L_PLBL)
    cnt_L_list_RL.append(cnt_L_RL)
    cnt_L_list_SEL.append(cnt_L_SEL)

    cnt_L_AL = 0
    cnt_L_BL = 0
    cnt_L_CD = 0
    cnt_L_CV = 0
    cnt_L_GL = 0
    cnt_L_HL = 0
    cnt_L_LAS = 0
    cnt_L_MFBL = 0
    cnt_L_MFHL = 0
    cnt_L_MFOT = 0
    cnt_L_OTH = 0
    cnt_L_PL = 0
    cnt_L_PLBL = 0
    cnt_L_RL = 0
    cnt_L_SEL = 0

    curr_bal_list_L_AL.append(curr_bal_AL)
    curr_bal_list_L_BL.append(curr_bal_BL)
    curr_bal_list_L_CD.append(curr_bal_CD)
    curr_bal_list_L_CV.append(curr_bal_CV)
    curr_bal_list_L_GL.append(curr_bal_GL)
    curr_bal_list_L_HL.append(curr_bal_HL)
    curr_bal_list_L_LAS.append(curr_bal_LAS)
    curr_bal_list_L_MFBL.append(curr_bal_MFBL)
    curr_bal_list_L_MFHL.append(curr_bal_MFHL)
    curr_bal_list_L_MFOT.append(curr_bal_MFOT)
    curr_bal_list_L_OTH.append(curr_bal_OTH)
    curr_bal_list_L_PL.append(curr_bal_PL)
    curr_bal_list_L_PLBL.append(curr_bal_PLBL)
    curr_bal_list_L_RL.append(curr_bal_RL)
    curr_bal_list_L_SEL.append(curr_bal_SEL)

    curr_bal_AL = 0
    curr_bal_BL = 0
    curr_bal_CD = 0
    curr_bal_CV = 0
    curr_bal_GL = 0
    curr_bal_HL = 0
    curr_bal_LAS = 0
    curr_bal_MFBL = 0
    curr_bal_MFHL = 0
    curr_bal_MFOT = 0
    curr_bal_OTH = 0
    curr_bal_PL = 0
    curr_bal_PLBL = 0
    curr_bal_RL = 0
    curr_bal_SEL = 0

    count_list_wo.append(count_wo)
    count_wo = 0

    count_list_re.append(count_re)
    count_re = 0

    count_wo_list_AL.append(count_wo_AL)
    count_wo_list_BL.append(count_wo_BL)
    count_wo_list_CC.append(count_wo_CC)
    count_wo_list_CD.append(count_wo_CD)
    count_wo_list_CV.append(count_wo_CV)
    count_wo_list_GL.append(count_wo_GL)
    count_wo_list_HL.append(count_wo_HL)
    count_wo_list_LAS.append(count_wo_LAS)
    count_wo_list_MFBL.append(count_wo_MFBL)
    count_wo_list_MFHL.append(count_wo_MFHL)
    count_wo_list_MFOT.append(count_wo_MFOT)
    count_wo_list_OTH.append(count_wo_OTH)
    count_wo_list_PL.append(count_wo_PL)
    count_wo_list_PLBL.append(count_wo_PLBL)
    count_wo_list_RL.append(count_wo_RL)
    count_wo_list_SCC.append(count_wo_SCC)
    count_wo_list_SEL.append(count_wo_SEL)

    count_wo_AL = 0
    count_wo_BL = 0
    count_wo_CC = 0
    count_wo_CD = 0
    count_wo_CV = 0
    count_wo_GL = 0
    count_wo_HL = 0
    count_wo_LAS = 0
    count_wo_MFBL = 0
    count_wo_MFHL = 0
    count_wo_MFOT = 0
    count_wo_OTH = 0
    count_wo_PL = 0
    count_wo_PLBL = 0
    count_wo_RL = 0
    count_wo_SCC = 0
    count_wo_SEL = 0

    count_re_list_AL.append(count_re_AL)
    count_re_list_BL.append(count_re_BL)
    count_re_list_CC.append(count_re_CC)
    count_re_list_CD.append(count_re_CD)
    count_re_list_CV.append(count_re_CV)
    count_re_list_GL.append(count_re_GL)
    count_re_list_HL.append(count_re_HL)
    count_re_list_LAS.append(count_re_LAS)
    count_re_list_MFBL.append(count_re_MFBL)
    count_re_list_MFHL.append(count_re_MFHL)
    count_re_list_MFOT.append(count_re_MFOT)
    count_re_list_OTH.append(count_re_OTH)
    count_re_list_PL.append(count_re_PL)
    count_re_list_PLBL.append(count_re_PLBL)
    count_re_list_RL.append(count_re_RL)
    count_re_list_SCC.append(count_re_SCC)
    count_re_list_SEL.append(count_re_SEL)

    count_re_AL = 0
    count_re_BL = 0
    count_re_CC = 0
    count_re_CD = 0
    count_re_CV = 0
    count_re_GL = 0
    count_re_HL = 0
    count_re_LAS = 0
    count_re_MFBL = 0
    count_re_MFHL = 0
    count_re_MFOT = 0
    count_re_OTH = 0
    count_re_PL = 0
    count_re_PLBL = 0
    count_re_RL = 0
    count_re_SCC = 0
    count_re_SEL = 0

    count_wo_l3m_list.append(count_wo_l3m)
    count_wo_l3m = 0

    count_wo_l3m_list_AL.append(count_wo_l3m_AL)
    count_wo_l3m_list_BL.append(count_wo_l3m_BL)
    count_wo_l3m_list_CC.append(count_wo_l3m_CC)
    count_wo_l3m_list_CD.append(count_wo_l3m_CD)
    count_wo_l3m_list_CV.append(count_wo_l3m_CV)
    count_wo_l3m_list_GL.append(count_wo_l3m_GL)
    count_wo_l3m_list_HL.append(count_wo_l3m_HL)
    count_wo_l3m_list_LAS.append(count_wo_l3m_LAS)
    count_wo_l3m_list_MFBL.append(count_wo_l3m_MFBL)
    count_wo_l3m_list_MFHL.append(count_wo_l3m_MFHL)
    count_wo_l3m_list_MFOT.append(count_wo_l3m_MFOT)
    count_wo_l3m_list_OTH.append(count_wo_l3m_OTH)
    count_wo_l3m_list_PL.append(count_wo_l3m_PL)
    count_wo_l3m_list_PLBL.append(count_wo_l3m_PLBL)
    count_wo_l3m_list_RL.append(count_wo_l3m_RL)
    count_wo_l3m_list_SCC.append(count_wo_l3m_SCC)
    count_wo_l3m_list_SEL.append(count_wo_l3m_SEL)

    count_wo_l3m_AL = 0
    count_wo_l3m_BL = 0
    count_wo_l3m_CC = 0
    count_wo_l3m_CD = 0
    count_wo_l3m_CV = 0
    count_wo_l3m_GL = 0
    count_wo_l3m_HL = 0
    count_wo_l3m_LAS = 0
    count_wo_l3m_MFBL = 0
    count_wo_l3m_MFHL = 0
    count_wo_l3m_MFOT = 0
    count_wo_l3m_OTH = 0
    count_wo_l3m_PL = 0
    count_wo_l3m_PLBL = 0
    count_wo_l3m_RL = 0
    count_wo_l3m_SCC = 0
    count_wo_l3m_SEL = 0

    count_wo_l6m_list.append(count_wo_l6m)
    count_wo_l6m = 0

    count_wo_l6m_list_AL.append(count_wo_l6m_AL)
    count_wo_l6m_list_BL.append(count_wo_l6m_BL)
    count_wo_l6m_list_CC.append(count_wo_l6m_CC)
    count_wo_l6m_list_CD.append(count_wo_l6m_CD)
    count_wo_l6m_list_CV.append(count_wo_l6m_CV)
    count_wo_l6m_list_GL.append(count_wo_l6m_GL)
    count_wo_l6m_list_HL.append(count_wo_l6m_HL)
    count_wo_l6m_list_LAS.append(count_wo_l6m_LAS)
    count_wo_l6m_list_MFBL.append(count_wo_l6m_MFBL)
    count_wo_l6m_list_MFHL.append(count_wo_l6m_MFHL)
    count_wo_l6m_list_MFOT.append(count_wo_l6m_MFOT)
    count_wo_l6m_list_OTH.append(count_wo_l6m_OTH)
    count_wo_l6m_list_PL.append(count_wo_l6m_PL)
    count_wo_l6m_list_PLBL.append(count_wo_l6m_PLBL)
    count_wo_l6m_list_RL.append(count_wo_l6m_RL)
    count_wo_l6m_list_SCC.append(count_wo_l6m_SCC)
    count_wo_l6m_list_SEL.append(count_wo_l6m_SEL)

    count_wo_l6m_AL = 0
    count_wo_l6m_BL = 0
    count_wo_l6m_CC = 0
    count_wo_l6m_CD = 0
    count_wo_l6m_CV = 0
    count_wo_l6m_GL = 0
    count_wo_l6m_HL = 0
    count_wo_l6m_LAS = 0
    count_wo_l6m_MFBL = 0
    count_wo_l6m_MFHL = 0
    count_wo_l6m_MFOT = 0
    count_wo_l6m_OTH = 0
    count_wo_l6m_PL = 0
    count_wo_l6m_PLBL = 0
    count_wo_l6m_RL = 0
    count_wo_l6m_SCC = 0
    count_wo_l6m_SEL = 0

    count_wo_l9m_list.append(count_wo_l9m)
    count_wo_l9m = 0

    count_wo_l9m_list_AL.append(count_wo_l9m_AL)
    count_wo_l9m_list_BL.append(count_wo_l9m_BL)
    count_wo_l9m_list_CC.append(count_wo_l9m_CC)
    count_wo_l9m_list_CD.append(count_wo_l9m_CD)
    count_wo_l9m_list_CV.append(count_wo_l9m_CV)
    count_wo_l9m_list_GL.append(count_wo_l9m_GL)
    count_wo_l9m_list_HL.append(count_wo_l9m_HL)
    count_wo_l9m_list_LAS.append(count_wo_l9m_LAS)
    count_wo_l9m_list_MFBL.append(count_wo_l9m_MFBL)
    count_wo_l9m_list_MFHL.append(count_wo_l9m_MFHL)
    count_wo_l9m_list_MFOT.append(count_wo_l9m_MFOT)
    count_wo_l9m_list_OTH.append(count_wo_l9m_OTH)
    count_wo_l9m_list_PL.append(count_wo_l9m_PL)
    count_wo_l9m_list_PLBL.append(count_wo_l9m_PLBL)
    count_wo_l9m_list_RL.append(count_wo_l9m_RL)
    count_wo_l9m_list_SCC.append(count_wo_l9m_SCC)
    count_wo_l9m_list_SEL.append(count_wo_l9m_SEL)

    count_wo_l9m_AL = 0
    count_wo_l9m_BL = 0
    count_wo_l9m_CC = 0
    count_wo_l9m_CD = 0
    count_wo_l9m_CV = 0
    count_wo_l9m_GL = 0
    count_wo_l9m_HL = 0
    count_wo_l9m_LAS = 0
    count_wo_l9m_MFBL = 0
    count_wo_l9m_MFHL = 0
    count_wo_l9m_MFOT = 0
    count_wo_l9m_OTH = 0
    count_wo_l9m_PL = 0
    count_wo_l9m_PLBL = 0
    count_wo_l9m_RL = 0
    count_wo_l9m_SCC = 0
    count_wo_l9m_SEL = 0

    count_wo_l1y_list.append(count_wo_l1y)
    count_wo_l1y = 0

    count_wo_l1y_list_AL.append(count_wo_l1y_AL)
    count_wo_l1y_list_BL.append(count_wo_l1y_BL)
    count_wo_l1y_list_CC.append(count_wo_l1y_CC)
    count_wo_l1y_list_CD.append(count_wo_l1y_CD)
    count_wo_l1y_list_CV.append(count_wo_l1y_CV)
    count_wo_l1y_list_GL.append(count_wo_l1y_GL)
    count_wo_l1y_list_HL.append(count_wo_l1y_HL)
    count_wo_l1y_list_LAS.append(count_wo_l1y_LAS)
    count_wo_l1y_list_MFBL.append(count_wo_l1y_MFBL)
    count_wo_l1y_list_MFHL.append(count_wo_l1y_MFHL)
    count_wo_l1y_list_MFOT.append(count_wo_l1y_MFOT)
    count_wo_l1y_list_OTH.append(count_wo_l1y_OTH)
    count_wo_l1y_list_PL.append(count_wo_l1y_PL)
    count_wo_l1y_list_PLBL.append(count_wo_l1y_PLBL)
    count_wo_l1y_list_RL.append(count_wo_l1y_RL)
    count_wo_l1y_list_SCC.append(count_wo_l1y_SCC)
    count_wo_l1y_list_SEL.append(count_wo_l1y_SEL)

    count_wo_l1y_AL = 0
    count_wo_l1y_BL = 0
    count_wo_l1y_CC = 0
    count_wo_l1y_CD = 0
    count_wo_l1y_CV = 0
    count_wo_l1y_GL = 0
    count_wo_l1y_HL = 0
    count_wo_l1y_LAS = 0
    count_wo_l1y_MFBL = 0
    count_wo_l1y_MFHL = 0
    count_wo_l1y_MFOT = 0
    count_wo_l1y_OTH = 0
    count_wo_l1y_PL = 0
    count_wo_l1y_PLBL = 0
    count_wo_l1y_RL = 0
    count_wo_l1y_SCC = 0
    count_wo_l1y_SEL = 0

    count_wo_l2y_list.append(count_wo_l2y)
    count_wo_l2y = 0

    count_wo_l2y_list_AL.append(count_wo_l2y_AL)
    count_wo_l2y_list_BL.append(count_wo_l2y_BL)
    count_wo_l2y_list_CC.append(count_wo_l2y_CC)
    count_wo_l2y_list_CD.append(count_wo_l2y_CD)
    count_wo_l2y_list_CV.append(count_wo_l2y_CV)
    count_wo_l2y_list_GL.append(count_wo_l2y_GL)
    count_wo_l2y_list_HL.append(count_wo_l2y_HL)
    count_wo_l2y_list_LAS.append(count_wo_l2y_LAS)
    count_wo_l2y_list_MFBL.append(count_wo_l2y_MFBL)
    count_wo_l2y_list_MFHL.append(count_wo_l2y_MFHL)
    count_wo_l2y_list_MFOT.append(count_wo_l2y_MFOT)
    count_wo_l2y_list_OTH.append(count_wo_l2y_OTH)
    count_wo_l2y_list_PL.append(count_wo_l2y_PL)
    count_wo_l2y_list_PLBL.append(count_wo_l2y_PLBL)
    count_wo_l2y_list_RL.append(count_wo_l2y_RL)
    count_wo_l2y_list_SCC.append(count_wo_l2y_SCC)
    count_wo_l2y_list_SEL.append(count_wo_l2y_SEL)

    count_wo_l2y_AL = 0
    count_wo_l2y_BL = 0
    count_wo_l2y_CC = 0
    count_wo_l2y_CD = 0
    count_wo_l2y_CV = 0
    count_wo_l2y_GL = 0
    count_wo_l2y_HL = 0
    count_wo_l2y_LAS = 0
    count_wo_l2y_MFBL = 0
    count_wo_l2y_MFHL = 0
    count_wo_l2y_MFOT = 0
    count_wo_l2y_OTH = 0
    count_wo_l2y_PL = 0
    count_wo_l2y_PLBL = 0
    count_wo_l2y_RL = 0
    count_wo_l2y_SCC = 0
    count_wo_l2y_SEL = 0

    count_wo_l3y_list.append(count_wo_l3y)
    count_wo_l3y = 0

    count_wo_l3y_list_AL.append(count_wo_l3y_AL)
    count_wo_l3y_list_BL.append(count_wo_l3y_BL)
    count_wo_l3y_list_CC.append(count_wo_l3y_CC)
    count_wo_l3y_list_CD.append(count_wo_l3y_CD)
    count_wo_l3y_list_CV.append(count_wo_l3y_CV)
    count_wo_l3y_list_GL.append(count_wo_l3y_GL)
    count_wo_l3y_list_HL.append(count_wo_l3y_HL)
    count_wo_l3y_list_LAS.append(count_wo_l3y_LAS)
    count_wo_l3y_list_MFBL.append(count_wo_l3y_MFBL)
    count_wo_l3y_list_MFHL.append(count_wo_l3y_MFHL)
    count_wo_l3y_list_MFOT.append(count_wo_l3y_MFOT)
    count_wo_l3y_list_OTH.append(count_wo_l3y_OTH)
    count_wo_l3y_list_PL.append(count_wo_l3y_PL)
    count_wo_l3y_list_PLBL.append(count_wo_l3y_PLBL)
    count_wo_l3y_list_RL.append(count_wo_l3y_RL)
    count_wo_l3y_list_SCC.append(count_wo_l3y_SCC)
    count_wo_l3y_list_SEL.append(count_wo_l3y_SEL)

    count_wo_l3y_AL = 0
    count_wo_l3y_BL = 0
    count_wo_l3y_CC = 0
    count_wo_l3y_CD = 0
    count_wo_l3y_CV = 0
    count_wo_l3y_GL = 0
    count_wo_l3y_HL = 0
    count_wo_l3y_LAS = 0
    count_wo_l3y_MFBL = 0
    count_wo_l3y_MFHL = 0
    count_wo_l3y_MFOT = 0
    count_wo_l3y_OTH = 0
    count_wo_l3y_PL = 0
    count_wo_l3y_PLBL = 0
    count_wo_l3y_RL = 0
    count_wo_l3y_SCC = 0
    count_wo_l3y_SEL = 0

    count_wo_l1y_plt_list.append(count_wo_l1y_plt)
    count_wo_l1y_plt = 0

    count_wo_l2y_plt_list.append(count_wo_l2y_plt)
    count_wo_l2y_plt = 0

    count_wo_l3y_plt_list.append(count_wo_l3y_plt)
    count_wo_l3y_plt = 0

    count_op_l3m_list.append(count_op_l3m)
    count_op_l3m = 0

    count_op_l3m_list_AL.append(count_op_l3m_AL)
    count_op_l3m_list_BL.append(count_op_l3m_BL)
    count_op_l3m_list_CC.append(count_op_l3m_CC)
    count_op_l3m_list_CD.append(count_op_l3m_CD)
    count_op_l3m_list_CV.append(count_op_l3m_CV)
    count_op_l3m_list_GL.append(count_op_l3m_GL)
    count_op_l3m_list_HL.append(count_op_l3m_HL)
    count_op_l3m_list_LAS.append(count_op_l3m_LAS)
    count_op_l3m_list_MFBL.append(count_op_l3m_MFBL)
    count_op_l3m_list_MFHL.append(count_op_l3m_MFHL)
    count_op_l3m_list_MFOT.append(count_op_l3m_MFOT)
    count_op_l3m_list_OTH.append(count_op_l3m_OTH)
    count_op_l3m_list_PL.append(count_op_l3m_PL)
    count_op_l3m_list_PLBL.append(count_op_l3m_PLBL)
    count_op_l3m_list_RL.append(count_op_l3m_RL)
    count_op_l3m_list_SCC.append(count_op_l3m_SCC)
    count_op_l3m_list_SEL.append(count_op_l3m_SEL)

    count_op_l3m_AL = 0
    count_op_l3m_BL = 0
    count_op_l3m_CC = 0
    count_op_l3m_CD = 0
    count_op_l3m_CV = 0
    count_op_l3m_GL = 0
    count_op_l3m_HL = 0
    count_op_l3m_LAS = 0
    count_op_l3m_MFBL = 0
    count_op_l3m_MFHL = 0
    count_op_l3m_MFOT = 0
    count_op_l3m_OTH = 0
    count_op_l3m_PL = 0
    count_op_l3m_PLBL = 0
    count_op_l3m_RL = 0
    count_op_l3m_SCC = 0
    count_op_l3m_SEL = 0

    count_op_l6m_list.append(count_op_l6m)
    count_op_l6m = 0

    count_op_l6m_list_AL.append(count_op_l6m_AL)
    count_op_l6m_list_BL.append(count_op_l6m_BL)
    count_op_l6m_list_CC.append(count_op_l6m_CC)
    count_op_l6m_list_CD.append(count_op_l6m_CD)
    count_op_l6m_list_CV.append(count_op_l6m_CV)
    count_op_l6m_list_GL.append(count_op_l6m_GL)
    count_op_l6m_list_HL.append(count_op_l6m_HL)
    count_op_l6m_list_LAS.append(count_op_l6m_LAS)
    count_op_l6m_list_MFBL.append(count_op_l6m_MFBL)
    count_op_l6m_list_MFHL.append(count_op_l6m_MFHL)
    count_op_l6m_list_MFOT.append(count_op_l6m_MFOT)
    count_op_l6m_list_OTH.append(count_op_l6m_OTH)
    count_op_l6m_list_PL.append(count_op_l6m_PL)
    count_op_l6m_list_PLBL.append(count_op_l6m_PLBL)
    count_op_l6m_list_RL.append(count_op_l6m_RL)
    count_op_l6m_list_SCC.append(count_op_l6m_SCC)
    count_op_l6m_list_SEL.append(count_op_l6m_SEL)

    count_op_l6m_AL = 0
    count_op_l6m_BL = 0
    count_op_l6m_CC = 0
    count_op_l6m_CD = 0
    count_op_l6m_CV = 0
    count_op_l6m_GL = 0
    count_op_l6m_HL = 0
    count_op_l6m_LAS = 0
    count_op_l6m_MFBL = 0
    count_op_l6m_MFHL = 0
    count_op_l6m_MFOT = 0
    count_op_l6m_OTH = 0
    count_op_l6m_PL = 0
    count_op_l6m_PLBL = 0
    count_op_l6m_RL = 0
    count_op_l6m_SCC = 0
    count_op_l6m_SEL = 0

    count_op_l9m_list.append(count_op_l9m)
    count_op_l9m = 0

    count_op_l9m_list_AL.append(count_op_l9m_AL)
    count_op_l9m_list_BL.append(count_op_l9m_BL)
    count_op_l9m_list_CC.append(count_op_l9m_CC)
    count_op_l9m_list_CD.append(count_op_l9m_CD)
    count_op_l9m_list_CV.append(count_op_l9m_CV)
    count_op_l9m_list_GL.append(count_op_l9m_GL)
    count_op_l9m_list_HL.append(count_op_l9m_HL)
    count_op_l9m_list_LAS.append(count_op_l9m_LAS)
    count_op_l9m_list_MFBL.append(count_op_l9m_MFBL)
    count_op_l9m_list_MFHL.append(count_op_l9m_MFHL)
    count_op_l9m_list_MFOT.append(count_op_l9m_MFOT)
    count_op_l9m_list_OTH.append(count_op_l9m_OTH)
    count_op_l9m_list_PL.append(count_op_l9m_PL)
    count_op_l9m_list_PLBL.append(count_op_l9m_PLBL)
    count_op_l9m_list_RL.append(count_op_l9m_RL)
    count_op_l9m_list_SCC.append(count_op_l9m_SCC)
    count_op_l9m_list_SEL.append(count_op_l9m_SEL)

    count_op_l9m_AL = 0
    count_op_l9m_BL = 0
    count_op_l9m_CC = 0
    count_op_l9m_CD = 0
    count_op_l9m_CV = 0
    count_op_l9m_GL = 0
    count_op_l9m_HL = 0
    count_op_l9m_LAS = 0
    count_op_l9m_MFBL = 0
    count_op_l9m_MFHL = 0
    count_op_l9m_MFOT = 0
    count_op_l9m_OTH = 0
    count_op_l9m_PL = 0
    count_op_l9m_PLBL = 0
    count_op_l9m_RL = 0
    count_op_l9m_SCC = 0
    count_op_l9m_SEL = 0

    count_op_l1y_list.append(count_op_l1y)
    count_op_l1y = 0

    count_op_l1y_list_AL.append(count_op_l1y_AL)
    count_op_l1y_list_BL.append(count_op_l1y_BL)
    count_op_l1y_list_CC.append(count_op_l1y_CC)
    count_op_l1y_list_CD.append(count_op_l1y_CD)
    count_op_l1y_list_CV.append(count_op_l1y_CV)
    count_op_l1y_list_GL.append(count_op_l1y_GL)
    count_op_l1y_list_HL.append(count_op_l1y_HL)
    count_op_l1y_list_LAS.append(count_op_l1y_LAS)
    count_op_l1y_list_MFBL.append(count_op_l1y_MFBL)
    count_op_l1y_list_MFHL.append(count_op_l1y_MFHL)
    count_op_l1y_list_MFOT.append(count_op_l1y_MFOT)
    count_op_l1y_list_OTH.append(count_op_l1y_OTH)
    count_op_l1y_list_PL.append(count_op_l1y_PL)
    count_op_l1y_list_PLBL.append(count_op_l1y_PLBL)
    count_op_l1y_list_RL.append(count_op_l1y_RL)
    count_op_l1y_list_SCC.append(count_op_l1y_SCC)
    count_op_l1y_list_SEL.append(count_op_l1y_SEL)

    count_op_l1y_AL = 0
    count_op_l1y_BL = 0
    count_op_l1y_CC = 0
    count_op_l1y_CD = 0
    count_op_l1y_CV = 0
    count_op_l1y_GL = 0
    count_op_l1y_HL = 0
    count_op_l1y_LAS = 0
    count_op_l1y_MFBL = 0
    count_op_l1y_MFHL = 0
    count_op_l1y_MFOT = 0
    count_op_l1y_OTH = 0
    count_op_l1y_PL = 0
    count_op_l1y_PLBL = 0
    count_op_l1y_RL = 0
    count_op_l1y_SCC = 0
    count_op_l1y_SEL = 0

    count_op_l2y_list.append(count_op_l2y)
    count_op_l2y = 0

    count_op_l2y_list_AL.append(count_op_l2y_AL)
    count_op_l2y_list_BL.append(count_op_l2y_BL)
    count_op_l2y_list_CC.append(count_op_l2y_CC)
    count_op_l2y_list_CD.append(count_op_l2y_CD)
    count_op_l2y_list_CV.append(count_op_l2y_CV)
    count_op_l2y_list_GL.append(count_op_l2y_GL)
    count_op_l2y_list_HL.append(count_op_l2y_HL)
    count_op_l2y_list_LAS.append(count_op_l2y_LAS)
    count_op_l2y_list_MFBL.append(count_op_l2y_MFBL)
    count_op_l2y_list_MFHL.append(count_op_l2y_MFHL)
    count_op_l2y_list_MFOT.append(count_op_l2y_MFOT)
    count_op_l2y_list_OTH.append(count_op_l2y_OTH)
    count_op_l2y_list_PL.append(count_op_l2y_PL)
    count_op_l2y_list_PLBL.append(count_op_l2y_PLBL)
    count_op_l2y_list_RL.append(count_op_l2y_RL)
    count_op_l2y_list_SCC.append(count_op_l2y_SCC)
    count_op_l2y_list_SEL.append(count_op_l2y_SEL)

    count_op_l2y_AL = 0
    count_op_l2y_BL = 0
    count_op_l2y_CC = 0
    count_op_l2y_CD = 0
    count_op_l2y_CV = 0
    count_op_l2y_GL = 0
    count_op_l2y_HL = 0
    count_op_l2y_LAS = 0
    count_op_l2y_MFBL = 0
    count_op_l2y_MFHL = 0
    count_op_l2y_MFOT = 0
    count_op_l2y_OTH = 0
    count_op_l2y_PL = 0
    count_op_l2y_PLBL = 0
    count_op_l2y_RL = 0
    count_op_l2y_SCC = 0
    count_op_l2y_SEL = 0

    count_op_l3y_list.append(count_op_l3y)
    count_op_l3y = 0

    count_op_l3y_list_AL.append(count_op_l3y_AL)
    count_op_l3y_list_BL.append(count_op_l3y_BL)
    count_op_l3y_list_CC.append(count_op_l3y_CC)
    count_op_l3y_list_CD.append(count_op_l3y_CD)
    count_op_l3y_list_CV.append(count_op_l3y_CV)
    count_op_l3y_list_GL.append(count_op_l3y_GL)
    count_op_l3y_list_HL.append(count_op_l3y_HL)
    count_op_l3y_list_LAS.append(count_op_l3y_LAS)
    count_op_l3y_list_MFBL.append(count_op_l3y_MFBL)
    count_op_l3y_list_MFHL.append(count_op_l3y_MFHL)
    count_op_l3y_list_MFOT.append(count_op_l3y_MFOT)
    count_op_l3y_list_OTH.append(count_op_l3y_OTH)
    count_op_l3y_list_PL.append(count_op_l3y_PL)
    count_op_l3y_list_PLBL.append(count_op_l3y_PLBL)
    count_op_l3y_list_RL.append(count_op_l3y_RL)
    count_op_l3y_list_SCC.append(count_op_l3y_SCC)
    count_op_l3y_list_SEL.append(count_op_l3y_SEL)

    count_op_l3y_AL = 0
    count_op_l3y_BL = 0
    count_op_l3y_CC = 0
    count_op_l3y_CD = 0
    count_op_l3y_CV = 0
    count_op_l3y_GL = 0
    count_op_l3y_HL = 0
    count_op_l3y_LAS = 0
    count_op_l3y_MFBL = 0
    count_op_l3y_MFHL = 0
    count_op_l3y_MFOT = 0
    count_op_l3y_OTH = 0
    count_op_l3y_PL = 0
    count_op_l3y_PLBL = 0
    count_op_l3y_RL = 0
    count_op_l3y_SCC = 0
    count_op_l3y_SEL = 0

    oa_list_AL.append(oa_AL)
    oa_list_BL.append(oa_BL)
    oa_list_CC.append(oa_CC)
    oa_list_CD.append(oa_CD)
    oa_list_CV.append(oa_CV)
    oa_list_GL.append(oa_GL)
    oa_list_HL.append(oa_HL)
    oa_list_LAS.append(oa_LAS)
    oa_list_MFBL.append(oa_MFBL)
    oa_list_MFHL.append(oa_MFHL)
    oa_list_MFOT.append(oa_MFOT)
    oa_list_OTH.append(oa_OTH)
    oa_list_PL.append(oa_PL)
    oa_list_PLBL.append(oa_PLBL)
    oa_list_RL.append(oa_RL)
    oa_list_SCC.append(oa_SCC)
    oa_list_SEL.append(oa_SEL)

    oa_AL = 0
    oa_BL = 0
    oa_CC = 0
    oa_CD = 0
    oa_CV = 0
    oa_GL = 0
    oa_HL = 0
    oa_LAS = 0
    oa_MFBL = 0
    oa_MFHL = 0
    oa_MFOT = 0
    oa_OTH = 0
    oa_PL = 0
    oa_PLBL = 0
    oa_RL = 0
    oa_SCC = 0
    oa_SEL = 0

    grp_list_oa_AL.append(grp_oa_AL)
    grp_list_oa_BL.append(grp_oa_BL)
    grp_list_oa_CC.append(grp_oa_CC)
    grp_list_oa_CD.append(grp_oa_CD)
    grp_list_oa_CV.append(grp_oa_CV)
    grp_list_oa_GL.append(grp_oa_GL)
    grp_list_oa_HL.append(grp_oa_HL)
    grp_list_oa_LAS.append(grp_oa_LAS)
    grp_list_oa_MFBL.append(grp_oa_MFBL)
    grp_list_oa_MFHL.append(grp_oa_MFHL)
    grp_list_oa_MFOT.append(grp_oa_MFOT)
    grp_list_oa_OTH.append(grp_oa_OTH)
    grp_list_oa_PL.append(grp_oa_PL)
    grp_list_oa_PLBL.append(grp_oa_PLBL)
    grp_list_oa_RL.append(grp_oa_RL)
    grp_list_oa_SCC.append(grp_oa_SCC)
    grp_list_oa_SEL.append(grp_oa_SEL)

    grp_list_cb_AL.append(grp_cb_AL)
    grp_list_cb_BL.append(grp_cb_BL)
    grp_list_cb_CC.append(grp_cb_CC)
    grp_list_cb_CD.append(grp_cb_CD)
    grp_list_cb_CV.append(grp_cb_CV)
    grp_list_cb_GL.append(grp_cb_GL)
    grp_list_cb_HL.append(grp_cb_HL)
    grp_list_cb_LAS.append(grp_cb_LAS)
    grp_list_cb_MFBL.append(grp_cb_MFBL)
    grp_list_cb_MFHL.append(grp_cb_MFHL)
    grp_list_cb_MFOT.append(grp_cb_MFOT)
    grp_list_cb_OTH.append(grp_cb_OTH)
    grp_list_cb_PL.append(grp_cb_PL)
    grp_list_cb_PLBL.append(grp_cb_PLBL)
    grp_list_cb_RL.append(grp_cb_RL)
    grp_list_cb_SCC.append(grp_cb_SCC)
    grp_list_cb_SEL.append(grp_cb_SEL)

    grp_oa_AL = 0
    grp_oa_BL = 0
    grp_oa_CC = 0
    grp_oa_CD = 0
    grp_oa_CV = 0
    grp_oa_GL = 0
    grp_oa_HL = 0
    grp_oa_LAS = 0
    grp_oa_MFBL = 0
    grp_oa_MFHL = 0
    grp_oa_MFOT = 0
    grp_oa_OTH = 0
    grp_oa_PL = 0
    grp_oa_PLBL = 0
    grp_oa_RL = 0
    grp_oa_SCC = 0
    grp_oa_SEL = 0

    grp_cb_BL = 0
    grp_cb_CC = 0
    grp_cb_CD = 0
    grp_cb_CV = 0
    grp_cb_GL = 0
    grp_cb_HL = 0
    grp_cb_LAS = 0
    grp_cb_MFBL = 0
    grp_cb_MFHL = 0
    grp_cb_MFOT = 0
    grp_cb_OTH = 0
    grp_cb_PL = 0
    grp_cb_PLBL = 0
    grp_cb_RL = 0
    grp_cb_SCC = 0
    grp_cb_SEL = 0

    grp_list_oa2_AL.append(grp_oa2_AL)
    grp_list_oa2_BL.append(grp_oa2_BL)
    grp_list_oa2_CC.append(grp_oa2_CC)
    grp_list_oa2_CD.append(grp_oa2_CD)
    grp_list_oa2_CV.append(grp_oa2_CV)
    grp_list_oa2_GL.append(grp_oa2_GL)
    grp_list_oa2_HL.append(grp_oa2_HL)
    grp_list_oa2_LAS.append(grp_oa2_LAS)
    grp_list_oa2_MFBL.append(grp_oa2_MFBL)
    grp_list_oa2_MFHL.append(grp_oa2_MFHL)
    grp_list_oa2_MFOT.append(grp_oa2_MFOT)
    grp_list_oa2_OTH.append(grp_oa2_OTH)
    grp_list_oa2_PL.append(grp_oa2_PL)
    grp_list_oa2_PLBL.append(grp_oa2_PLBL)
    grp_list_oa2_RL.append(grp_oa2_RL)
    grp_list_oa2_SCC.append(grp_oa2_SCC)
    grp_list_oa2_SEL.append(grp_oa2_SEL)

    grp_list_da_AL.append(grp_da_AL)
    grp_list_da_BL.append(grp_da_BL)
    grp_list_da_CC.append(grp_da_CC)
    grp_list_da_CD.append(grp_da_CD)
    grp_list_da_CV.append(grp_da_CV)
    grp_list_da_GL.append(grp_da_GL)
    grp_list_da_HL.append(grp_da_HL)
    grp_list_da_LAS.append(grp_da_LAS)
    grp_list_da_MFBL.append(grp_da_MFBL)
    grp_list_da_MFHL.append(grp_da_MFHL)
    grp_list_da_MFOT.append(grp_da_MFOT)
    grp_list_da_OTH.append(grp_da_OTH)
    grp_list_da_PL.append(grp_da_PL)
    grp_list_da_PLBL.append(grp_da_PLBL)
    grp_list_da_RL.append(grp_da_RL)
    grp_list_da_SCC.append(grp_da_SCC)
    grp_list_da_SEL.append(grp_da_SEL)

    grp_oa2_AL = 0
    grp_oa2_BL = 0
    grp_oa2_CC = 0
    grp_oa2_CD = 0
    grp_oa2_CV = 0
    grp_oa2_GL = 0
    grp_oa2_HL = 0
    grp_oa2_LAS = 0
    grp_oa2_MFBL = 0
    grp_oa2_MFHL = 0
    grp_oa2_MFOT = 0
    grp_oa2_OTH = 0
    grp_oa2_PL = 0
    grp_oa2_PLBL = 0
    grp_oa2_RL = 0
    grp_oa2_SCC = 0
    grp_oa2_SEL = 0

    grp_da_BL = 0
    grp_da_CC = 0
    grp_da_CD = 0
    grp_da_CV = 0
    grp_da_GL = 0
    grp_da_HL = 0
    grp_da_LAS = 0
    grp_da_MFBL = 0
    grp_da_MFHL = 0
    grp_da_MFOT = 0
    grp_da_OTH = 0
    grp_da_PL = 0
    grp_da_PLBL = 0
    grp_da_RL = 0
    grp_da_SCC = 0
    grp_da_SEL = 0

    count_dtCl_wo_list.append(count_dtCl_wo)
    count_dtCl_wo = 0

    count_dtCl_suit_list.append(count_dtCl_suit)
    count_dtCl_suit = 0

    count_dtCl_ph1m_list.append(count_dtCl_ph1m)
    count_dtCl_ph1m = 0

    count_dtCl_res_list.append(count_dtCl_res)
    count_dtCl_res = 0

    for i in range(0, grp_slice.shape[0]):

        if (grp_slice['dateClosed_lt_PHED'][i] == 1) or (grp_slice['dateClosed_lt_PHED'][i] == 0):
            dateClosed_lt_PHED_CNT.append(count_list_dt_phed[x])
        else:
            dateClosed_lt_PHED_CNT.append('unknown')

        if (grp_slice['ignore_case'][i] == 1) or (grp_slice['ignore_case'][i] == 0):
            ignore_case_CNT.append(count_list_ic[x])
        else:
            ignore_case_CNT.append('unknown')

        if (grp_slice['currentBalance'][i] == 'unknown') and (grp_slice['sanctionAmount'][i] == 'unknown'):
            sumCurrentBalance.append('unknown')
            sumSanctionAmount.append('unknown')
        else:
            sumCurrentBalance.append(sum_cur_bal[x])
            sumSanctionAmount.append(sum_sanc_amt[x])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == '36') or (grp_slice['currentBalance'][i] == 'unknown'):
            currentBalance_sanctionedAmount_NCC_L.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L.append(
                ratio_list_cu_sa_ncc_l[x])

        if (grp_slice['currentBalance'][i] == 'unknown') and (grp_slice['creditLimit'][i] == 'unknown'):
            sumCreditLimit.append('unknown')
        else:
            sumCreditLimit.append(sum_cred_lmt[x])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mode_util_CC_L.append('unknown')
        else:
            mode_util_CC_L.append(np.max(ratio_list_mode_util[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mean_util_CC_L.append('unknown')
        else:
            mean_util_CC_L.append(np.mean(ratio_list_mean_util[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            median_util_CC_L.append('unknown')
        else:
            median_util_CC_L.append(np.median(ratio_list_med_util[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            min_util_CC_L.append('unknown')
        else:
            min_util_CC_L.append(np.min(ratio_list_min_util[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mean_util_highCredit_CC_L.append('unknown')
        else:
            mean_util_highCredit_CC_L.append(
                np.mean(ratio_list_mean_util_hi_cred[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mode_util_highCredit_CC_L.append('unknown')
        else:
            mode_util_highCredit_CC_L.append(
                np.max(ratio_list_mode_util_hi_cred[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            median_util_highCredit_CC_L.append('unknown')
        else:
            median_util_highCredit_CC_L.append(
                np.median(ratio_list_med_util_hi_cr[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            min_util_highCredit_CC_L.append('unknown')
        else:
            min_util_highCredit_CC_L.append(
                np.min(ratio_list_min_util_hi_cr[x]))

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mean_util_highCredit_CC_A.append('unknown')
        else:
            mean_util_highCredit_CC_A.append(
                np.mean(ratio_list_mean_util_hi_cr_a[x]))

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            mode_util_highCredit_CC_A.append('unknown')
        else:
            mode_util_highCredit_CC_A.append(
                np.max(ratio_list_mode_util_hi_cr_a[x]))

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            median_util_highCredit_CC_A.append('unknown')
        else:
            median_util_highCredit_CC_A.append(
                np.median(ratio_list_med_util_hi_cr_a[x]))

        if (grp_slice['accountType'][i] != 10) or (grp_slice['creditLimit'][i] == 0) or (grp_slice['sanctionAmount'][i] == 'unknown') or (grp_slice['creditLimit'][i] == 'unknown'):
            min_util_highCredit_CC_A.append('unknown')
        else:
            min_util_highCredit_CC_A.append(
                np.median(ratio_list_min_util_hi_cr_a[x]))

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mean_SancAmt.append('unknown')
        else:
            Mean_SancAmt.append(np.mean(sanc_amt_list_mean[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mean_SancAmt_L.append('unknown')
        else:
            Mean_SancAmt_L.append(np.mean(sanc_amt_list_L_mean[x]))

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Median_SancAmt.append('unknown')
        else:
            Median_SancAmt.append(np.median(sanc_amt_list_med[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Median_SancAmt_L.append('unknown')
        else:
            Median_SancAmt_L.append(np.median(sanc_amt_list_L_med[x]))

        if (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mode_SancAmt.append('unknown')
        else:
            Mode_SancAmt.append(np.max(sanc_amt_list_mode[x]))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 10) or (grp_slice['accountType'][i] == 35) or (grp_slice['accountType'][i] == 36) or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mode_SancAmt_L.append('unknown')
        else:
            Mode_SancAmt_L.append(np.max(sanc_amt_list_L_mode[x]))

        if (pd.isnull(grp_slice['accountType'][i])):
            Secured_CNT.append('unknown')
        else:
            Secured_CNT.append(sec_cnt_list[x])

        if (pd.isnull(grp_slice['accountType'][i])):
            Unsecured_CNT.append('unknown')
        else:
            Unsecured_CNT.append(unsec_cnt_list[x])

        if (pd.isnull(grp_slice['accountType'][i])) or (unsec_L_cnt_list[0] == 0):
            Loans_Sec_UnsecwoRLCC_L.append('unknown')
            Per_Sec_UnsecwoRLCC_L.append('unknown')
        else:
            Loans_Sec_UnsecwoRLCC_L.append(
                sec_L_cnt_list[0]/unsec_L_cnt_list[0])
            Per_Sec_UnsecwoRLCC_L.append(
                sec_L_cnt_list[0]/(unsec_L_cnt_list[0]+sec_L_cnt_list[0]))

        if (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mean_SancAmt_AL.append('unknown')
            Mean_SancAmt_BL.append('unknown')
            Mean_SancAmt_CD.append('unknown')
            Mean_SancAmt_CV.append('unknown')
            Mean_SancAmt_GL.append('unknown')
            Mean_SancAmt_HL.append('unknown')
            Mean_SancAmt_LAS.append('unknown')
            Mean_SancAmt_MFBL.append('unknown')
            Mean_SancAmt_MFHL.append('unknown')
            Mean_SancAmt_MFOT.append('unknown')
            Mean_SancAmt_OTH.append('unknown')
            Mean_SancAmt_PL.append('unknown')
            Mean_SancAmt_PLBL.append('unknown')
            Mean_SancAmt_RL.append('unknown')
            Mean_SancAmt_SEL.append('unknown')

            Med_SancAmt_AL.append('unknown')
            Med_SancAmt_BL.append('unknown')
            Med_SancAmt_CD.append('unknown')
            Med_SancAmt_CV.append('unknown')
            Med_SancAmt_GL.append('unknown')
            Med_SancAmt_HL.append('unknown')
            Med_SancAmt_LAS.append('unknown')
            Med_SancAmt_MFBL.append('unknown')
            Med_SancAmt_MFHL.append('unknown')
            Med_SancAmt_MFOT.append('unknown')
            Med_SancAmt_OTH.append('unknown')
            Med_SancAmt_PL.append('unknown')
            Med_SancAmt_PLBL.append('unknown')
            Med_SancAmt_RL.append('unknown')
            Med_SancAmt_SEL.append('unknown')
            '''
            Mode_SancAmt_AL.append('unknown')
            Mode_SancAmt_BL.append('unknown')
            Mode_SancAmt_CD.append('unknown')
            Mode_SancAmt_CV.append('unknown')
            Mode_SancAmt_GL.append('unknown')
            Mode_SancAmt_HL.append('unknown')
            Mode_SancAmt_LAS.append('unknown')
            Mode_SancAmt_MFBL.append('unknown')
            Mode_SancAmt_MFHL.append('unknown')
            Mode_SancAmt_MFOT.append('unknown')
            Mode_SancAmt_OTH.append('unknown')
            Mode_SancAmt_PL.append('unknown')
            Mode_SancAmt_PLBL.append('unknown')
            Mode_SancAmt_RL.append('unknown')
            Mode_SancAmt_SEL.append('unknown')'''

        else:
            Mean_SancAmt_AL.append(np.median(sanc_amt_mean_list_AL[x]))
            Mean_SancAmt_BL.append(np.median(sanc_amt_mean_list_BL[x]))
            Mean_SancAmt_CD.append(np.median(sanc_amt_mean_list_CD[x]))
            Mean_SancAmt_CV.append(np.median(sanc_amt_mean_list_CV[x]))
            Mean_SancAmt_GL.append(np.median(sanc_amt_mean_list_GL[x]))
            Mean_SancAmt_HL.append(np.median(sanc_amt_mean_list_HL[x]))
            Mean_SancAmt_LAS.append(np.median(sanc_amt_mean_list_LAS[x]))
            Mean_SancAmt_MFBL.append(np.median(sanc_amt_mean_list_MFBL[x]))
            Mean_SancAmt_MFHL.append(np.median(sanc_amt_mean_list_MFHL[x]))
            Mean_SancAmt_MFOT.append(np.median(sanc_amt_mean_list_MFOT[x]))
            Mean_SancAmt_OTH.append(np.median(sanc_amt_mean_list_OTH[x]))
            Mean_SancAmt_PL.append(np.median(sanc_amt_mean_list_PL[x]))
            Mean_SancAmt_PLBL.append(np.median(sanc_amt_mean_list_PLBL[x]))
            Mean_SancAmt_RL.append(np.median(sanc_amt_mean_list_RL[x]))
            Mean_SancAmt_SEL.append(np.median(sanc_amt_mean_list_SEL[x]))

            Med_SancAmt_AL.append(np.median(sanc_amt_med_list_AL[x]))
            Med_SancAmt_BL.append(np.median(sanc_amt_med_list_BL[x]))
            Med_SancAmt_CD.append(np.median(sanc_amt_med_list_CD[x]))
            Med_SancAmt_CV.append(np.median(sanc_amt_med_list_CV[x]))
            Med_SancAmt_GL.append(np.median(sanc_amt_med_list_GL[x]))
            Med_SancAmt_HL.append(np.median(sanc_amt_med_list_HL[x]))
            Med_SancAmt_LAS.append(np.median(sanc_amt_med_list_LAS[x]))
            Med_SancAmt_MFBL.append(np.median(sanc_amt_med_list_MFBL[x]))
            Med_SancAmt_MFHL.append(np.median(sanc_amt_med_list_MFHL[x]))
            Med_SancAmt_MFOT.append(np.median(sanc_amt_med_list_MFOT[x]))
            Med_SancAmt_OTH.append(np.median(sanc_amt_med_list_OTH[x]))
            Med_SancAmt_PL.append(np.median(sanc_amt_med_list_PL[x]))
            Med_SancAmt_PLBL.append(np.median(sanc_amt_med_list_PLBL[x]))
            Med_SancAmt_RL.append(np.median(sanc_amt_med_list_RL[x]))
            Med_SancAmt_SEL.append(np.median(sanc_amt_med_list_SEL[x]))

            '''
            Mode_SancAmt_AL.append(np.max(sanc_amt_list_AL[x]))
            Mode_SancAmt_BL.append(np.max(sanc_amt_list_BL[x]))
            Mode_SancAmt_CD.append(np.max(sanc_amt_list_CD[x]))
            Mode_SancAmt_CV.append(np.max(sanc_amt_list_CV[x]))
            Mode_SancAmt_GL.append(np.max(sanc_amt_list_GL[x]))
            Mode_SancAmt_HL.append(np.max(sanc_amt_list_HL[x]))
            Mode_SancAmt_LAS.append(np.max(sanc_amt_list_LAS[x]))
            Mode_SancAmt_MFBL.append(np.max(sanc_amt_list_MFBL[x]))
            Mode_SancAmt_MFHL.append(np.max(sanc_amt_list_MFHL[x]))
            Mode_SancAmt_MFOT.append(np.max(sanc_amt_list_MFOT[x]))
            Mode_SancAmt_OTH.append(np.max(sanc_amt_list_OTH[x]))
            Mode_SancAmt_PL.append(np.max(sanc_amt_list_PL[x]))
            Mode_SancAmt_PLBL.append(np.max(sanc_amt_list_PLBL[x]))
            Mode_SancAmt_RL.append(np.max(sanc_amt_list_RL[x]))
            Mode_SancAmt_SEL.append(np.max(sanc_amt_list_SEL[x]))'''

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            Mean_SancAmt_L_AL.append('unknown')
            Mean_SancAmt_L_BL.append('unknown')
            Mean_SancAmt_L_CD.append('unknown')
            Mean_SancAmt_L_CV.append('unknown')
            Mean_SancAmt_L_GL.append('unknown')
            Mean_SancAmt_L_HL.append('unknown')
            Mean_SancAmt_L_LAS.append('unknown')
            Mean_SancAmt_L_MFBL.append('unknown')
            Mean_SancAmt_L_MFHL.append('unknown')
            Mean_SancAmt_L_MFOT.append('unknown')
            Mean_SancAmt_L_OTH.append('unknown')
            Mean_SancAmt_L_PL.append('unknown')
            Mean_SancAmt_L_PLBL.append('unknown')
            Mean_SancAmt_L_RL.append('unknown')
            Mean_SancAmt_L_SEL.append('unknown')

            Med_SancAmt_L_AL.append('unknown')
            Med_SancAmt_L_BL.append('unknown')
            Med_SancAmt_L_CD.append('unknown')
            Med_SancAmt_L_CV.append('unknown')
            Med_SancAmt_L_GL.append('unknown')
            Med_SancAmt_L_HL.append('unknown')
            Med_SancAmt_L_LAS.append('unknown')
            Med_SancAmt_L_MFBL.append('unknown')
            Med_SancAmt_L_MFHL.append('unknown')
            Med_SancAmt_L_MFOT.append('unknown')
            Med_SancAmt_L_OTH.append('unknown')
            Med_SancAmt_L_PL.append('unknown')
            Med_SancAmt_L_PLBL.append('unknown')
            Med_SancAmt_L_RL.append('unknown')
            Med_SancAmt_L_SEL.append('unknown')

            '''
            Mode_SancAmt_L_AL.append('unknown')
            Mode_SancAmt_L_BL.append('unknown')
            Mode_SancAmt_L_CD.append('unknown')
            Mode_SancAmt_L_CV.append('unknown')
            Mode_SancAmt_L_GL.append('unknown')
            Mode_SancAmt_L_HL.append('unknown')
            Mode_SancAmt_L_LAS.append('unknown')
            Mode_SancAmt_L_MFBL.append('unknown')
            Mode_SancAmt_L_MFHL.append('unknown')
            Mode_SancAmt_L_MFOT.append('unknown')
            Mode_SancAmt_L_OTH.append('unknown')
            Mode_SancAmt_L_PL.append('unknown')
            Mode_SancAmt_L_PLBL.append('unknown')
            Mode_SancAmt_L_RL.append('unknown')
            Mode_SancAmt_L_SEL.append('unknown')'''

        else:
            Mean_SancAmt_L_AL.append(np.mean(sanc_amt_L_list_AL[x]))
            Mean_SancAmt_L_BL.append(np.mean(sanc_amt_L_list_BL[x]))
            Mean_SancAmt_L_CD.append(np.mean(sanc_amt_L_list_CD[x]))
            Mean_SancAmt_L_CV.append(np.mean(sanc_amt_L_list_CV[x]))
            Mean_SancAmt_L_GL.append(np.mean(sanc_amt_L_list_GL[x]))
            Mean_SancAmt_L_HL.append(np.mean(sanc_amt_L_list_HL[x]))
            Mean_SancAmt_L_LAS.append(np.mean(sanc_amt_L_list_LAS[x]))
            Mean_SancAmt_L_MFBL.append(np.mean(sanc_amt_L_list_MFBL[x]))
            Mean_SancAmt_L_MFHL.append(np.mean(sanc_amt_L_list_MFHL[x]))
            Mean_SancAmt_L_MFOT.append(np.mean(sanc_amt_L_list_MFOT[x]))
            Mean_SancAmt_L_OTH.append(np.mean(sanc_amt_L_list_OTH[x]))
            Mean_SancAmt_L_PL.append(np.mean(sanc_amt_L_list_PL[x]))
            Mean_SancAmt_L_PLBL.append(np.mean(sanc_amt_L_list_PLBL[x]))
            Mean_SancAmt_L_RL.append(np.mean(sanc_amt_L_list_RL[x]))
            Mean_SancAmt_L_SEL.append(np.mean(sanc_amt_L_list_SEL[x]))

            Med_SancAmt_L_AL.append(np.median(sanc_amt_list_AL[x]))
            Med_SancAmt_L_BL.append(np.median(sanc_amt_list_BL[x]))
            Med_SancAmt_L_CD.append(np.median(sanc_amt_list_CD[x]))
            Med_SancAmt_L_CV.append(np.median(sanc_amt_list_CV[x]))
            Med_SancAmt_L_GL.append(np.median(sanc_amt_list_GL[x]))
            Med_SancAmt_L_HL.append(np.median(sanc_amt_list_HL[x]))
            Med_SancAmt_L_LAS.append(np.median(sanc_amt_list_LAS[x]))
            Med_SancAmt_L_MFBL.append(np.median(sanc_amt_list_MFBL[x]))
            Med_SancAmt_L_MFHL.append(np.median(sanc_amt_list_MFHL[x]))
            Med_SancAmt_L_MFOT.append(np.median(sanc_amt_list_MFOT[x]))
            Med_SancAmt_L_OTH.append(np.median(sanc_amt_list_OTH[x]))
            Med_SancAmt_L_PL.append(np.median(sanc_amt_list_PL[x]))
            Med_SancAmt_L_PLBL.append(np.median(sanc_amt_list_PLBL[x]))
            Med_SancAmt_L_RL.append(np.median(sanc_amt_list_RL[x]))
            Med_SancAmt_L_SEL.append(np.median(sanc_amt_list_SEL[x]))

            '''
            Mode_SancAmt_L_AL.append(np.max(sanc_amt_list_AL[x]))
            Mode_SancAmt_L_BL.append(np.max(sanc_amt_list_BL[x]))
            Mode_SancAmt_L_CD.append(np.max(sanc_amt_list_CD[x]))
            Mode_SancAmt_L_CV.append(np.max(sanc_amt_list_CV[x]))
            Mode_SancAmt_L_GL.append(np.max(sanc_amt_list_GL[x]))
            Mode_SancAmt_L_HL.append(np.max(sanc_amt_list_HL[x]))
            Mode_SancAmt_L_LAS.append(np.max(sanc_amt_list_LAS[x]))
            Mode_SancAmt_L_MFBL.append(np.max(sanc_amt_list_MFBL[x]))
            Mode_SancAmt_L_MFHL.append(np.max(sanc_amt_list_MFHL[x]))
            Mode_SancAmt_L_MFOT.append(np.max(sanc_amt_list_MFOT[x]))
            Mode_SancAmt_L_OTH.append(np.max(sanc_amt_list_OTH[x]))
            Mode_SancAmt_L_PL.append(np.max(sanc_amt_list_PL[x]))
            Mode_SancAmt_L_PLBL.append(np.max(sanc_amt_list_PLBL[x]))
            Mode_SancAmt_L_RL.append(np.max(sanc_amt_list_RL[x]))
            Mode_SancAmt_L_SEL.append(np.max(sanc_amt_list_SEL[x]))'''

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_AL) == 0):
            currentBalance_sanctionedAmount_NCC_L_AL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_AL.append(
                sum(currentBalance_AL)/sum(sanctionedAmount_AL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_BL) == 0):
            currentBalance_sanctionedAmount_NCC_L_BL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_BL.append(
                sum(currentBalance_BL)/sum(sanctionedAmount_BL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_CD) == 0):
            currentBalance_sanctionedAmount_NCC_L_CD.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_CD.append(
                sum(currentBalance_CD)/sum(sanctionedAmount_CD))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_CV) == 0):
            currentBalance_sanctionedAmount_NCC_L_CV.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_CV.append(
                sum(currentBalance_CV)/sum(sanctionedAmount_CV))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_GL) == 0):
            currentBalance_sanctionedAmount_NCC_L_GL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_GL.append(
                sum(currentBalance_GL)/sum(sanctionedAmount_GL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_HL) == 0):
            currentBalance_sanctionedAmount_NCC_L_HL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_HL.append(
                sum(currentBalance_HL)/sum(sanctionedAmount_HL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_LAS) == 0):
            currentBalance_sanctionedAmount_NCC_L_LAS.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_LAS.append(
                sum(currentBalance_LAS)/sum(sanctionedAmount_LAS))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_MFBL) == 0):
            currentBalance_sanctionedAmount_NCC_L_MFBL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_MFBL.append(
                sum(currentBalance_MFBL)/sum(sanctionedAmount_MFBL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_MFHL) == 0):
            currentBalance_sanctionedAmount_NCC_L_MFHL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_MFHL.append(
                sum(currentBalance_MFHL)/sum(sanctionedAmount_MFHL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_MFOT) == 0):
            currentBalance_sanctionedAmount_NCC_L_MFOT.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_MFOT.append(
                sum(currentBalance_MFOT)/sum(sanctionedAmount_MFOT))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_OTH) == 0):
            currentBalance_sanctionedAmount_NCC_L_OTH.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_OTH.append(
                sum(currentBalance_OTH)/sum(sanctionedAmount_OTH))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_PL) == 0):
            currentBalance_sanctionedAmount_NCC_L_PL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_PL.append(
                sum(currentBalance_PL)/sum(sanctionedAmount_PL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_PLBL) == 0):
            currentBalance_sanctionedAmount_NCC_L_PLBL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_PLBL.append(
                sum(currentBalance_PLBL)/sum(sanctionedAmount_PLBL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_RL) == 0):
            currentBalance_sanctionedAmount_NCC_L_RL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_RL.append(
                sum(currentBalance_RL)/sum(sanctionedAmount_RL))

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] == 'CC') or (grp_slice['accountType'][i] == 'SCC') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(sanctionedAmount_SEL) == 0):
            currentBalance_sanctionedAmount_NCC_L_SEL.append('unknown')
        else:
            currentBalance_sanctionedAmount_NCC_L_SEL.append(
                sum(currentBalance_SEL)/sum(sanctionedAmount_SEL))

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            sanc_amt_grp.append('unknown')

        elif (grp_slice['accountType'][i] == 'AL'):
            sanc_amt_grp.append(sanc_amt_list_AL[x])

        elif (grp_slice['accountType'][i] == 'BL'):
            sanc_amt_grp.append(sanc_amt_list_BL[x])

        elif (grp_slice['accountType'][i] == 'CD'):
            sanc_amt_grp.append(sanc_amt_list_CD[x])

        elif (grp_slice['accountType'][i] == 'CV'):
            sanc_amt_grp.append(sanc_amt_list_CV[x])

        elif (grp_slice['accountType'][i] == 'GL'):
            sanc_amt_grp.append(sanc_amt_list_GL[x])

        elif (grp_slice['accountType'][i] == 'HL'):
            sanc_amt_grp.append(sanc_amt_list_HL[x])

        elif (grp_slice['accountType'][i] == 'LAS'):
            sanc_amt_grp.append(sanc_amt_list_LAS[x])

        elif (grp_slice['accountType'][i] == 'MFBL'):
            sanc_amt_grp.append(sanc_amt_list_MFBL[x])

        elif (grp_slice['accountType'][i] == 'MFHL'):
            sanc_amt_grp.append(sanc_amt_list_MFHL[x])

        elif (grp_slice['accountType'][i] == 'MFOT'):
            sanc_amt_grp.append(sanc_amt_list_MFOT[x])

        elif (grp_slice['accountType'][i] == 'OTH'):
            sanc_amt_grp.append(sanc_amt_list_OTH[x])

        elif (grp_slice['accountType'][i] == 'PL'):
            sanc_amt_grp.append(sanc_amt_list_PL[x])

        elif (grp_slice['accountType'][i] == 'PLBL'):
            sanc_amt_grp.append(sanc_amt_list_PLBL[x])

        elif (grp_slice['accountType'][i] == 'RL'):
            sanc_amt_grp.append(sanc_amt_list_RL[x])

        elif (grp_slice['accountType'][i] == 'SEL'):
            sanc_amt_grp.append(sanc_amt_list_SEL[x])

        else:
            sanc_amt_grp.append('unknown')

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            cnt_grp.append('unknown')

        elif (grp_slice['accountType'][i] == 'AL'):
            cnt_grp.append(cnt_list_AL[x])

        elif (grp_slice['accountType'][i] == 'BL'):
            cnt_grp.append(cnt_list_BL[x])

        elif (grp_slice['accountType'][i] == 'CD'):
            cnt_grp.append(cnt_list_CD[x])

        elif (grp_slice['accountType'][i] == 'CV'):
            cnt_grp.append(cnt_list_CV[x])

        elif (grp_slice['accountType'][i] == 'GL'):
            cnt_grp.append(cnt_list_GL[x])

        elif (grp_slice['accountType'][i] == 'HL'):
            cnt_grp.append(cnt_list_HL[x])

        elif (grp_slice['accountType'][i] == 'LAS'):
            cnt_grp.append(cnt_list_LAS[x])

        elif (grp_slice['accountType'][i] == 'MFBL'):
            cnt_grp.append(cnt_list_MFBL[x])

        elif (grp_slice['accountType'][i] == 'MFHL'):
            cnt_grp.append(cnt_list_MFHL[x])

        elif (grp_slice['accountType'][i] == 'MFOT'):
            cnt_grp.append(cnt_list_MFOT[x])

        elif (grp_slice['accountType'][i] == 'OTH'):
            cnt_grp.append(cnt_list_OTH[x])

        elif (grp_slice['accountType'][i] == 'PL'):
            cnt_grp.append(cnt_list_PL[x])

        elif (grp_slice['accountType'][i] == 'PLBL'):
            cnt_grp.append(cnt_list_PLBL[x])

        elif (grp_slice['accountType'][i] == 'RL'):
            cnt_grp.append(cnt_list_RL[x])

        elif (grp_slice['accountType'][i] == 'SEL'):
            cnt_grp.append(cnt_list_SEL[x])

        else:
            cnt_grp.append('unknown')

        if (grp_slice['dateClosed'][i] == 'unknown'):
            totAcc_L.append(grp_slice['totAcc_L'][0])
        else:
            totAcc_L.append(0)

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append('unknown')
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_AL[x])

        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_BL[x])

        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_CD[x])

        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_CV[x])

        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_GL[x])

        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_HL[x])

        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_LAS[x])

        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_MFBL[x])

        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_MFHL[x])

        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_MFOT[x])

        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_OTH[x])

        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_PL[x])

        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_PLBL[x])

        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_RL[x])

        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['dateClosed'][i] == 'unknown'):
            sum_L_sanc_amt_grp_L.append(sum_L_sanc_amt_list_L_SEL[x])

        else:
            sum_L_sanc_amt_grp_L.append('unknown')

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown'):
            cnt_L_grp_L.append('unknown')

        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_AL[x])

        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_BL[x])

        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_CD[x])

        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_CV[x])

        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_GL[x])

        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_HL[x])

        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_LAS[x])

        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_MFBL[x])

        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_MFHL[x])

        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_MFOT[x])

        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_OTH[x])

        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_PL[x])

        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_PLBL[x])

        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_RL[x])

        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['dateClosed'][i] == 'unknown'):
            cnt_L_grp_L.append(cnt_L_list_SEL[x])

        else:
            cnt_L_grp_L.append('unknown')

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown'):
            curr_bal_grp_L.append('unknown')

        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_AL[x])

        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_BL[x])

        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_CD[x])

        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_CV[x])

        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_GL[x])

        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_HL[x])

        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_LAS[x])

        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_MFBL[x])

        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_MFHL[x])

        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_MFOT[x])

        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_OTH[x])

        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_PL[x])

        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_PLBL[x])

        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_RL[x])

        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['dateClosed'][i] == 'unknown') and (grp_slice['currentBalance'][i] >= 0):
            curr_bal_grp_L.append(curr_bal_list_L_SEL[x])

        else:
            curr_bal_grp_L.append('unknown')

        if (grp_slice['writeOff'][i] == 1) or (grp_slice['writeOff'][i] == 0):
            writeOff_CNT.append(count_list_wo[x])
        else:
            writeOff_CNT.append('unknown')

        if (grp_slice['restructured'][i] == 1) or (grp_slice['restructured'][i] == 0):
            restructured_CNT.append(count_list_re[x])
        else:
            restructured_CNT.append('unknown')

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_CNT_AL.append('unknown')
            writeOff_CNT_BL.append('unknown')
            writeOff_CNT_CC.append('unknown')
            writeOff_CNT_CD.append('unknown')
            writeOff_CNT_CV.append('unknown')
            writeOff_CNT_GL.append('unknown')
            writeOff_CNT_HL.append('unknown')
            writeOff_CNT_LAS.append('unknown')
            writeOff_CNT_MFBL.append('unknown')
            writeOff_CNT_MFHL.append('unknown')
            writeOff_CNT_MFOT.append('unknown')
            writeOff_CNT_OTH.append('unknown')
            writeOff_CNT_PL.append('unknown')
            writeOff_CNT_PLBL.append('unknown')
            writeOff_CNT_RL.append('unknown')
            writeOff_CNT_SCC.append('unknown')
            writeOff_CNT_SEL.append('unknown')
        else:
            writeOff_CNT_AL.append(count_wo_list_AL[x])
            writeOff_CNT_BL.append(count_wo_list_BL[x])
            writeOff_CNT_CC.append(count_wo_list_CC[x])
            writeOff_CNT_CD.append(count_wo_list_CD[x])
            writeOff_CNT_CV.append(count_wo_list_CV[x])
            writeOff_CNT_GL.append(count_wo_list_GL[x])
            writeOff_CNT_HL.append(count_wo_list_HL[x])
            writeOff_CNT_LAS.append(count_wo_list_LAS[x])
            writeOff_CNT_MFBL.append(count_wo_list_MFBL[x])
            writeOff_CNT_MFHL.append(count_wo_list_MFHL[x])
            writeOff_CNT_MFOT.append(count_wo_list_MFOT[x])
            writeOff_CNT_OTH.append(count_wo_list_OTH[x])
            writeOff_CNT_PL.append(count_wo_list_PL[x])
            writeOff_CNT_PLBL.append(count_wo_list_PLBL[x])
            writeOff_CNT_RL.append(count_wo_list_RL[x])
            writeOff_CNT_SCC.append(count_wo_list_SCC[x])
            writeOff_CNT_SEL.append(count_wo_list_SEL[x])

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['restructured'][i] == 'unknown'):
            restructured_CNT_AL.append('unknown')
            restructured_CNT_BL.append('unknown')
            restructured_CNT_CC.append('unknown')
            restructured_CNT_CD.append('unknown')
            restructured_CNT_CV.append('unknown')
            restructured_CNT_GL.append('unknown')
            restructured_CNT_HL.append('unknown')
            restructured_CNT_LAS.append('unknown')
            restructured_CNT_MFBL.append('unknown')
            restructured_CNT_MFHL.append('unknown')
            restructured_CNT_MFOT.append('unknown')
            restructured_CNT_OTH.append('unknown')
            restructured_CNT_PL.append('unknown')
            restructured_CNT_PLBL.append('unknown')
            restructured_CNT_RL.append('unknown')
            restructured_CNT_SCC.append('unknown')
            restructured_CNT_SEL.append('unknown')
        else:
            restructured_CNT_AL.append(count_re_list_AL[x])
            restructured_CNT_BL.append(count_re_list_BL[x])
            restructured_CNT_CC.append(count_re_list_CC[x])
            restructured_CNT_CD.append(count_re_list_CD[x])
            restructured_CNT_CV.append(count_re_list_CV[x])
            restructured_CNT_GL.append(count_re_list_GL[x])
            restructured_CNT_HL.append(count_re_list_HL[x])
            restructured_CNT_LAS.append(count_re_list_LAS[x])
            restructured_CNT_MFBL.append(count_re_list_MFBL[x])
            restructured_CNT_MFHL.append(count_re_list_MFHL[x])
            restructured_CNT_MFOT.append(count_re_list_MFOT[x])
            restructured_CNT_OTH.append(count_re_list_OTH[x])
            restructured_CNT_PL.append(count_re_list_PL[x])
            restructured_CNT_PLBL.append(count_re_list_PLBL[x])
            restructured_CNT_RL.append(count_re_list_RL[x])
            restructured_CNT_SCC.append(count_re_list_SCC[x])
            restructured_CNT_SEL.append(count_re_list_SEL[x])

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last3M_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 3) and (grp_slice['writeOff'][i] == 1):
            writeOff_last3M_CNT.append(count_wo_l3m_list[x])
        else:
            writeOff_last3M_CNT.append(0)

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last3M_CNT_AL.append('unknown')
            writeOff_last3M_CNT_BL.append('unknown')
            writeOff_last3M_CNT_CC.append('unknown')
            writeOff_last3M_CNT_CD.append('unknown')
            writeOff_last3M_CNT_CV.append('unknown')
            writeOff_last3M_CNT_GL.append('unknown')
            writeOff_last3M_CNT_HL.append('unknown')
            writeOff_last3M_CNT_LAS.append('unknown')
            writeOff_last3M_CNT_MFBL.append('unknown')
            writeOff_last3M_CNT_MFHL.append('unknown')
            writeOff_last3M_CNT_MFOT.append('unknown')
            writeOff_last3M_CNT_OTH.append('unknown')
            writeOff_last3M_CNT_PL.append('unknown')
            writeOff_last3M_CNT_PLBL.append('unknown')
            writeOff_last3M_CNT_RL.append('unknown')
            writeOff_last3M_CNT_SCC.append('unknown')
            writeOff_last3M_CNT_SEL.append('unknown')

        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 3):
            writeOff_last3M_CNT_AL.append(count_wo_l3m_list_AL[x])
            writeOff_last3M_CNT_BL.append(count_wo_l3m_list_BL[x])
            writeOff_last3M_CNT_CC.append(count_wo_l3m_list_CC[x])
            writeOff_last3M_CNT_CD.append(count_wo_l3m_list_CD[x])
            writeOff_last3M_CNT_CV.append(count_wo_l3m_list_CV[x])
            writeOff_last3M_CNT_GL.append(count_wo_l3m_list_GL[x])
            writeOff_last3M_CNT_HL.append(count_wo_l3m_list_HL[x])
            writeOff_last3M_CNT_LAS.append(count_wo_l3m_list_LAS[x])
            writeOff_last3M_CNT_MFBL.append(count_wo_l3m_list_MFBL[x])
            writeOff_last3M_CNT_MFHL.append(count_wo_l3m_list_MFHL[x])
            writeOff_last3M_CNT_MFOT.append(count_wo_l3m_list_MFOT[x])
            writeOff_last3M_CNT_OTH.append(count_wo_l3m_list_OTH[x])
            writeOff_last3M_CNT_PL.append(count_wo_l3m_list_PL[x])
            writeOff_last3M_CNT_PLBL.append(count_wo_l3m_list_PLBL[x])
            writeOff_last3M_CNT_RL.append(count_wo_l3m_list_RL[x])
            writeOff_last3M_CNT_SCC.append(count_wo_l3m_list_SCC[x])
            writeOff_last3M_CNT_SEL.append(count_wo_l3m_list_SEL[x])

        else:
            writeOff_last3M_CNT_AL.append(0)
            writeOff_last3M_CNT_BL.append(0)
            writeOff_last3M_CNT_CC.append(0)
            writeOff_last3M_CNT_CD.append(0)
            writeOff_last3M_CNT_CV.append(0)
            writeOff_last3M_CNT_GL.append(0)
            writeOff_last3M_CNT_HL.append(0)
            writeOff_last3M_CNT_LAS.append(0)
            writeOff_last3M_CNT_MFBL.append(0)
            writeOff_last3M_CNT_MFHL.append(0)
            writeOff_last3M_CNT_MFOT.append(0)
            writeOff_last3M_CNT_OTH.append(0)
            writeOff_last3M_CNT_PL.append(0)
            writeOff_last3M_CNT_PLBL.append(0)
            writeOff_last3M_CNT_RL.append(0)
            writeOff_last3M_CNT_SCC.append(0)
            writeOff_last3M_CNT_SEL.append(0)

        if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last6M_CNT_AL.append('unknown')
            writeOff_last6M_CNT_BL.append('unknown')
            writeOff_last6M_CNT_CC.append('unknown')
            writeOff_last6M_CNT_CD.append('unknown')
            writeOff_last6M_CNT_CV.append('unknown')
            writeOff_last6M_CNT_GL.append('unknown')
            writeOff_last6M_CNT_HL.append('unknown')
            writeOff_last6M_CNT_LAS.append('unknown')
            writeOff_last6M_CNT_MFBL.append('unknown')
            writeOff_last6M_CNT_MFHL.append('unknown')
            writeOff_last6M_CNT_MFOT.append('unknown')
            writeOff_last6M_CNT_OTH.append('unknown')
            writeOff_last6M_CNT_PL.append('unknown')
            writeOff_last6M_CNT_PLBL.append('unknown')
            writeOff_last6M_CNT_RL.append('unknown')
            writeOff_last6M_CNT_SCC.append('unknown')
            writeOff_last6M_CNT_SEL.append('unknown')
        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 6):
            writeOff_last6M_CNT_AL.append(count_wo_l6m_list_AL[x])
            writeOff_last6M_CNT_BL.append(count_wo_l6m_list_BL[x])
            writeOff_last6M_CNT_CC.append(count_wo_l6m_list_CC[x])
            writeOff_last6M_CNT_CD.append(count_wo_l6m_list_CD[x])
            writeOff_last6M_CNT_CV.append(count_wo_l6m_list_CV[x])
            writeOff_last6M_CNT_GL.append(count_wo_l6m_list_GL[x])
            writeOff_last6M_CNT_HL.append(count_wo_l6m_list_HL[x])
            writeOff_last6M_CNT_LAS.append(count_wo_l6m_list_LAS[x])
            writeOff_last6M_CNT_MFBL.append(count_wo_l6m_list_MFBL[x])
            writeOff_last6M_CNT_MFHL.append(count_wo_l6m_list_MFHL[x])
            writeOff_last6M_CNT_MFOT.append(count_wo_l6m_list_MFOT[x])
            writeOff_last6M_CNT_OTH.append(count_wo_l6m_list_OTH[x])
            writeOff_last6M_CNT_PL.append(count_wo_l6m_list_PL[x])
            writeOff_last6M_CNT_PLBL.append(count_wo_l6m_list_PLBL[x])
            writeOff_last6M_CNT_RL.append(count_wo_l6m_list_RL[x])
            writeOff_last6M_CNT_SCC.append(count_wo_l6m_list_SCC[x])
            writeOff_last6M_CNT_SEL.append(count_wo_l6m_list_SEL[x])
        else:
            writeOff_last6M_CNT_AL.append(0)
            writeOff_last6M_CNT_BL.append(0)
            writeOff_last6M_CNT_CC.append(0)
            writeOff_last6M_CNT_CD.append(0)
            writeOff_last6M_CNT_CV.append(0)
            writeOff_last6M_CNT_GL.append(0)
            writeOff_last6M_CNT_HL.append(0)
            writeOff_last6M_CNT_LAS.append(0)
            writeOff_last6M_CNT_MFBL.append(0)
            writeOff_last6M_CNT_MFHL.append(0)
            writeOff_last6M_CNT_MFOT.append(0)
            writeOff_last6M_CNT_OTH.append(0)
            writeOff_last6M_CNT_PL.append(0)
            writeOff_last6M_CNT_PLBL.append(0)
            writeOff_last6M_CNT_RL.append(0)
            writeOff_last6M_CNT_SCC.append(0)
            writeOff_last6M_CNT_SEL.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last6M_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 6) and (grp_slice['writeOff'][i] == 1):
            writeOff_last6M_CNT.append(count_wo_l6m_list[x])
        else:
            writeOff_last6M_CNT.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last9M_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 9) and (grp_slice['writeOff'][i] == 1):
            writeOff_last9M_CNT.append(count_wo_l9m_list[x])
        else:
            writeOff_last9M_CNT.append(0)

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last9M_CNT_AL.append('unknown')
            writeOff_last9M_CNT_BL.append('unknown')
            writeOff_last9M_CNT_CC.append('unknown')
            writeOff_last9M_CNT_CD.append('unknown')
            writeOff_last9M_CNT_CV.append('unknown')
            writeOff_last9M_CNT_GL.append('unknown')
            writeOff_last9M_CNT_HL.append('unknown')
            writeOff_last9M_CNT_LAS.append('unknown')
            writeOff_last9M_CNT_MFBL.append('unknown')
            writeOff_last9M_CNT_MFHL.append('unknown')
            writeOff_last9M_CNT_MFOT.append('unknown')
            writeOff_last9M_CNT_OTH.append('unknown')
            writeOff_last9M_CNT_PL.append('unknown')
            writeOff_last9M_CNT_PLBL.append('unknown')
            writeOff_last9M_CNT_RL.append('unknown')
            writeOff_last9M_CNT_SCC.append('unknown')
            writeOff_last9M_CNT_SEL.append('unknown')
        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 9):
            writeOff_last9M_CNT_AL.append(count_wo_l9m_list_AL[x])
            writeOff_last9M_CNT_BL.append(count_wo_l9m_list_BL[x])
            writeOff_last9M_CNT_CC.append(count_wo_l9m_list_CC[x])
            writeOff_last9M_CNT_CD.append(count_wo_l9m_list_CD[x])
            writeOff_last9M_CNT_CV.append(count_wo_l9m_list_CV[x])
            writeOff_last9M_CNT_GL.append(count_wo_l9m_list_GL[x])
            writeOff_last9M_CNT_HL.append(count_wo_l9m_list_HL[x])
            writeOff_last9M_CNT_LAS.append(count_wo_l9m_list_LAS[x])
            writeOff_last9M_CNT_MFBL.append(count_wo_l9m_list_MFBL[x])
            writeOff_last9M_CNT_MFHL.append(count_wo_l9m_list_MFHL[x])
            writeOff_last9M_CNT_MFOT.append(count_wo_l9m_list_MFOT[x])
            writeOff_last9M_CNT_OTH.append(count_wo_l9m_list_OTH[x])
            writeOff_last9M_CNT_PL.append(count_wo_l9m_list_PL[x])
            writeOff_last9M_CNT_PLBL.append(count_wo_l9m_list_PLBL[x])
            writeOff_last9M_CNT_RL.append(count_wo_l9m_list_RL[x])
            writeOff_last9M_CNT_SCC.append(count_wo_l9m_list_SCC[x])
            writeOff_last9M_CNT_SEL.append(count_wo_l9m_list_SEL[x])
        else:
            writeOff_last9M_CNT_AL.append(0)
            writeOff_last9M_CNT_BL.append(0)
            writeOff_last9M_CNT_CC.append(0)
            writeOff_last9M_CNT_CD.append(0)
            writeOff_last9M_CNT_CV.append(0)
            writeOff_last9M_CNT_GL.append(0)
            writeOff_last9M_CNT_HL.append(0)
            writeOff_last9M_CNT_LAS.append(0)
            writeOff_last9M_CNT_MFBL.append(0)
            writeOff_last9M_CNT_MFHL.append(0)
            writeOff_last9M_CNT_MFOT.append(0)
            writeOff_last9M_CNT_OTH.append(0)
            writeOff_last9M_CNT_PL.append(0)
            writeOff_last9M_CNT_PLBL.append(0)
            writeOff_last9M_CNT_RL.append(0)
            writeOff_last9M_CNT_SCC.append(0)
            writeOff_last9M_CNT_SEL.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last1Y_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 12) and (grp_slice['writeOff'][i] == 1):
            writeOff_last1Y_CNT.append(count_wo_l1y_list[x])
        else:
            writeOff_last1Y_CNT.append(0)

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last1Y_CNT_AL.append('unknown')
            writeOff_last1Y_CNT_BL.append('unknown')
            writeOff_last1Y_CNT_CC.append('unknown')
            writeOff_last1Y_CNT_CD.append('unknown')
            writeOff_last1Y_CNT_CV.append('unknown')
            writeOff_last1Y_CNT_GL.append('unknown')
            writeOff_last1Y_CNT_HL.append('unknown')
            writeOff_last1Y_CNT_LAS.append('unknown')
            writeOff_last1Y_CNT_MFBL.append('unknown')
            writeOff_last1Y_CNT_MFHL.append('unknown')
            writeOff_last1Y_CNT_MFOT.append('unknown')
            writeOff_last1Y_CNT_OTH.append('unknown')
            writeOff_last1Y_CNT_PL.append('unknown')
            writeOff_last1Y_CNT_PLBL.append('unknown')
            writeOff_last1Y_CNT_RL.append('unknown')
            writeOff_last1Y_CNT_SCC.append('unknown')
            writeOff_last1Y_CNT_SEL.append('unknown')
        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 12):
            writeOff_last1Y_CNT_AL.append(count_wo_l1y_list_AL[x])
            writeOff_last1Y_CNT_BL.append(count_wo_l1y_list_BL[x])
            writeOff_last1Y_CNT_CC.append(count_wo_l1y_list_CC[x])
            writeOff_last1Y_CNT_CD.append(count_wo_l1y_list_CD[x])
            writeOff_last1Y_CNT_CV.append(count_wo_l1y_list_CV[x])
            writeOff_last1Y_CNT_GL.append(count_wo_l1y_list_GL[x])
            writeOff_last1Y_CNT_HL.append(count_wo_l1y_list_HL[x])
            writeOff_last1Y_CNT_LAS.append(count_wo_l1y_list_LAS[x])
            writeOff_last1Y_CNT_MFBL.append(count_wo_l1y_list_MFBL[x])
            writeOff_last1Y_CNT_MFHL.append(count_wo_l1y_list_MFHL[x])
            writeOff_last1Y_CNT_MFOT.append(count_wo_l1y_list_MFOT[x])
            writeOff_last1Y_CNT_OTH.append(count_wo_l1y_list_OTH[x])
            writeOff_last1Y_CNT_PL.append(count_wo_l1y_list_PL[x])
            writeOff_last1Y_CNT_PLBL.append(count_wo_l1y_list_PLBL[x])
            writeOff_last1Y_CNT_RL.append(count_wo_l1y_list_RL[x])
            writeOff_last1Y_CNT_SCC.append(count_wo_l1y_list_SCC[x])
            writeOff_last1Y_CNT_SEL.append(count_wo_l1y_list_SEL[x])
        else:
            writeOff_last1Y_CNT_AL.append(0)
            writeOff_last1Y_CNT_BL.append(0)
            writeOff_last1Y_CNT_CC.append(0)
            writeOff_last1Y_CNT_CD.append(0)
            writeOff_last1Y_CNT_CV.append(0)
            writeOff_last1Y_CNT_GL.append(0)
            writeOff_last1Y_CNT_HL.append(0)
            writeOff_last1Y_CNT_LAS.append(0)
            writeOff_last1Y_CNT_MFBL.append(0)
            writeOff_last1Y_CNT_MFHL.append(0)
            writeOff_last1Y_CNT_MFOT.append(0)
            writeOff_last1Y_CNT_OTH.append(0)
            writeOff_last1Y_CNT_PL.append(0)
            writeOff_last1Y_CNT_PLBL.append(0)
            writeOff_last1Y_CNT_RL.append(0)
            writeOff_last1Y_CNT_SCC.append(0)
            writeOff_last1Y_CNT_SEL.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last2Y_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 24) and (grp_slice['writeOff'][i] == 1):
            writeOff_last2Y_CNT.append(count_wo_l2y_list[x])
        else:
            writeOff_last2Y_CNT.append(0)

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last2Y_CNT_AL.append('unknown')
            writeOff_last2Y_CNT_BL.append('unknown')
            writeOff_last2Y_CNT_CC.append('unknown')
            writeOff_last2Y_CNT_CD.append('unknown')
            writeOff_last2Y_CNT_CV.append('unknown')
            writeOff_last2Y_CNT_GL.append('unknown')
            writeOff_last2Y_CNT_HL.append('unknown')
            writeOff_last2Y_CNT_LAS.append('unknown')
            writeOff_last2Y_CNT_MFBL.append('unknown')
            writeOff_last2Y_CNT_MFHL.append('unknown')
            writeOff_last2Y_CNT_MFOT.append('unknown')
            writeOff_last2Y_CNT_OTH.append('unknown')
            writeOff_last2Y_CNT_PL.append('unknown')
            writeOff_last2Y_CNT_PLBL.append('unknown')
            writeOff_last2Y_CNT_RL.append('unknown')
            writeOff_last2Y_CNT_SCC.append('unknown')
            writeOff_last2Y_CNT_SEL.append('unknown')
        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 24):
            writeOff_last2Y_CNT_AL.append(count_wo_l2y_list_AL[x])
            writeOff_last2Y_CNT_BL.append(count_wo_l2y_list_BL[x])
            writeOff_last2Y_CNT_CC.append(count_wo_l2y_list_CC[x])
            writeOff_last2Y_CNT_CD.append(count_wo_l2y_list_CD[x])
            writeOff_last2Y_CNT_CV.append(count_wo_l2y_list_CV[x])
            writeOff_last2Y_CNT_GL.append(count_wo_l2y_list_GL[x])
            writeOff_last2Y_CNT_HL.append(count_wo_l2y_list_HL[x])
            writeOff_last2Y_CNT_LAS.append(count_wo_l2y_list_LAS[x])
            writeOff_last2Y_CNT_MFBL.append(count_wo_l2y_list_MFBL[x])
            writeOff_last2Y_CNT_MFHL.append(count_wo_l2y_list_MFHL[x])
            writeOff_last2Y_CNT_MFOT.append(count_wo_l2y_list_MFOT[x])
            writeOff_last2Y_CNT_OTH.append(count_wo_l2y_list_OTH[x])
            writeOff_last2Y_CNT_PL.append(count_wo_l2y_list_PL[x])
            writeOff_last2Y_CNT_PLBL.append(count_wo_l2y_list_PLBL[x])
            writeOff_last2Y_CNT_RL.append(count_wo_l2y_list_RL[x])
            writeOff_last2Y_CNT_SCC.append(count_wo_l2y_list_SCC[x])
            writeOff_last2Y_CNT_SEL.append(count_wo_l2y_list_SEL[x])
        else:
            writeOff_last2Y_CNT_AL.append(0)
            writeOff_last2Y_CNT_BL.append(0)
            writeOff_last2Y_CNT_CC.append(0)
            writeOff_last2Y_CNT_CD.append(0)
            writeOff_last2Y_CNT_CV.append(0)
            writeOff_last2Y_CNT_GL.append(0)
            writeOff_last2Y_CNT_HL.append(0)
            writeOff_last2Y_CNT_LAS.append(0)
            writeOff_last2Y_CNT_MFBL.append(0)
            writeOff_last2Y_CNT_MFHL.append(0)
            writeOff_last2Y_CNT_MFOT.append(0)
            writeOff_last2Y_CNT_OTH.append(0)
            writeOff_last2Y_CNT_PL.append(0)
            writeOff_last2Y_CNT_PLBL.append(0)
            writeOff_last2Y_CNT_RL.append(0)
            writeOff_last2Y_CNT_SCC.append(0)
            writeOff_last2Y_CNT_SEL.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last3Y_CNT.append('unknown')
        elif (grp_slice['month_diff'][i] <= 36) and (grp_slice['writeOff'][i] == 1):
            writeOff_last3Y_CNT.append(count_wo_l3y_list[x])
        else:
            writeOff_last3Y_CNT.append(0)

        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
            writeOff_last3Y_CNT_AL.append('unknown')
            writeOff_last3Y_CNT_BL.append('unknown')
            writeOff_last3Y_CNT_CC.append('unknown')
            writeOff_last3Y_CNT_CD.append('unknown')
            writeOff_last3Y_CNT_CV.append('unknown')
            writeOff_last3Y_CNT_GL.append('unknown')
            writeOff_last3Y_CNT_HL.append('unknown')
            writeOff_last3Y_CNT_LAS.append('unknown')
            writeOff_last3Y_CNT_MFBL.append('unknown')
            writeOff_last3Y_CNT_MFHL.append('unknown')
            writeOff_last3Y_CNT_MFOT.append('unknown')
            writeOff_last3Y_CNT_OTH.append('unknown')
            writeOff_last3Y_CNT_PL.append('unknown')
            writeOff_last3Y_CNT_PLBL.append('unknown')
            writeOff_last3Y_CNT_RL.append('unknown')
            writeOff_last3Y_CNT_SCC.append('unknown')
            writeOff_last3Y_CNT_SEL.append('unknown')
        elif (grp_slice['writeOff'][i] == 1) and (grp_slice['month_diff'][i] <= 36):
            writeOff_last3Y_CNT_AL.append(count_wo_l3y_list_AL[x])
            writeOff_last3Y_CNT_BL.append(count_wo_l3y_list_BL[x])
            writeOff_last3Y_CNT_CC.append(count_wo_l3y_list_CC[x])
            writeOff_last3Y_CNT_CD.append(count_wo_l3y_list_CD[x])
            writeOff_last3Y_CNT_CV.append(count_wo_l3y_list_CV[x])
            writeOff_last3Y_CNT_GL.append(count_wo_l3y_list_GL[x])
            writeOff_last3Y_CNT_HL.append(count_wo_l3y_list_HL[x])
            writeOff_last3Y_CNT_LAS.append(count_wo_l3y_list_LAS[x])
            writeOff_last3Y_CNT_MFBL.append(count_wo_l3y_list_MFBL[x])
            writeOff_last3Y_CNT_MFHL.append(count_wo_l3y_list_MFHL[x])
            writeOff_last3Y_CNT_MFOT.append(count_wo_l3y_list_MFOT[x])
            writeOff_last3Y_CNT_OTH.append(count_wo_l3y_list_OTH[x])
            writeOff_last3Y_CNT_PL.append(count_wo_l3y_list_PL[x])
            writeOff_last3Y_CNT_PLBL.append(count_wo_l3y_list_PLBL[x])
            writeOff_last3Y_CNT_RL.append(count_wo_l3y_list_RL[x])
            writeOff_last3Y_CNT_SCC.append(count_wo_l3y_list_SCC[x])
            writeOff_last3Y_CNT_SEL.append(count_wo_l3y_list_SEL[x])
        else:
            writeOff_last3Y_CNT_AL.append(0)
            writeOff_last3Y_CNT_BL.append(0)
            writeOff_last3Y_CNT_CC.append(0)
            writeOff_last3Y_CNT_CD.append(0)
            writeOff_last3Y_CNT_CV.append(0)
            writeOff_last3Y_CNT_GL.append(0)
            writeOff_last3Y_CNT_HL.append(0)
            writeOff_last3Y_CNT_LAS.append(0)
            writeOff_last3Y_CNT_MFBL.append(0)
            writeOff_last3Y_CNT_MFHL.append(0)
            writeOff_last3Y_CNT_MFOT.append(0)
            writeOff_last3Y_CNT_OTH.append(0)
            writeOff_last3Y_CNT_PL.append(0)
            writeOff_last3Y_CNT_PLBL.append(0)
            writeOff_last3Y_CNT_RL.append(0)
            writeOff_last3Y_CNT_SCC.append(0)
            writeOff_last3Y_CNT_SEL.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            writeOff_last1Y_PLT1K_CNT.append('unknown')
        elif ((grp_slice['month_diff'][i] <= 12) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            writeOff_last1Y_PLT1K_CNT.append(count_wo_l1y_plt_list[x])
        else:
            writeOff_last1Y_PLT1K_CNT.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            writeOff_last2Y_PLT1K_CNT.append('unknown')
        elif ((grp_slice['month_diff'][i] <= 24) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            writeOff_last2Y_PLT1K_CNT.append(count_wo_l2y_plt_list[x])
        else:
            writeOff_last2Y_PLT1K_CNT.append(0)

        if (grp_slice['month_diff'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown') or (grp_slice['writtenOffAmountPrincipal'][i] == 'unknown'):
            writeOff_last3Y_PLT1K_CNT.append('unknown')
        elif ((grp_slice['month_diff'][i] <= 36) and (grp_slice['writeOff'][i] == 1) and (grp_slice['writtenOffAmountPrincipal'][i] >= 1000)):
            writeOff_last3Y_PLT1K_CNT.append(count_wo_l3y_plt_list[x])
        else:
            writeOff_last3Y_PLT1K_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last3M_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 3):
            opened_last3M_CNT.append(count_op_l3m_list[x])
        else:
            opened_last3M_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last3M_CNT_AL.append('unknown')
            opened_last3M_CNT_BL.append('unknown')
            opened_last3M_CNT_CC.append('unknown')
            opened_last3M_CNT_CD.append('unknown')
            opened_last3M_CNT_CV.append('unknown')
            opened_last3M_CNT_GL.append('unknown')
            opened_last3M_CNT_HL.append('unknown')
            opened_last3M_CNT_LAS.append('unknown')
            opened_last3M_CNT_MFBL.append('unknown')
            opened_last3M_CNT_MFHL.append('unknown')
            opened_last3M_CNT_MFOT.append('unknown')
            opened_last3M_CNT_OTH.append('unknown')
            opened_last3M_CNT_PL.append('unknown')
            opened_last3M_CNT_PLBL.append('unknown')
            opened_last3M_CNT_RL.append('unknown')
            opened_last3M_CNT_SCC.append('unknown')
            opened_last3M_CNT_SEL.append('unknown')

            opened_last6M_CNT_AL.append('unknown')
            opened_last6M_CNT_BL.append('unknown')
            opened_last6M_CNT_CC.append('unknown')
            opened_last6M_CNT_CD.append('unknown')
            opened_last6M_CNT_CV.append('unknown')
            opened_last6M_CNT_GL.append('unknown')
            opened_last6M_CNT_HL.append('unknown')
            opened_last6M_CNT_LAS.append('unknown')
            opened_last6M_CNT_MFBL.append('unknown')
            opened_last6M_CNT_MFHL.append('unknown')
            opened_last6M_CNT_MFOT.append('unknown')
            opened_last6M_CNT_OTH.append('unknown')
            opened_last6M_CNT_PL.append('unknown')
            opened_last6M_CNT_PLBL.append('unknown')
            opened_last6M_CNT_RL.append('unknown')
            opened_last6M_CNT_SCC.append('unknown')
            opened_last6M_CNT_SEL.append('unknown')

            opened_last9M_CNT_AL.append('unknown')
            opened_last9M_CNT_BL.append('unknown')
            opened_last9M_CNT_CC.append('unknown')
            opened_last9M_CNT_CD.append('unknown')
            opened_last9M_CNT_CV.append('unknown')
            opened_last9M_CNT_GL.append('unknown')
            opened_last9M_CNT_HL.append('unknown')
            opened_last9M_CNT_LAS.append('unknown')
            opened_last9M_CNT_MFBL.append('unknown')
            opened_last9M_CNT_MFHL.append('unknown')
            opened_last9M_CNT_MFOT.append('unknown')
            opened_last9M_CNT_OTH.append('unknown')
            opened_last9M_CNT_PL.append('unknown')
            opened_last9M_CNT_PLBL.append('unknown')
            opened_last9M_CNT_RL.append('unknown')
            opened_last9M_CNT_SCC.append('unknown')
            opened_last9M_CNT_SEL.append('unknown')

            opened_last1Y_CNT_AL.append('unknown')
            opened_last1Y_CNT_BL.append('unknown')
            opened_last1Y_CNT_CC.append('unknown')
            opened_last1Y_CNT_CD.append('unknown')
            opened_last1Y_CNT_CV.append('unknown')
            opened_last1Y_CNT_GL.append('unknown')
            opened_last1Y_CNT_HL.append('unknown')
            opened_last1Y_CNT_LAS.append('unknown')
            opened_last1Y_CNT_MFBL.append('unknown')
            opened_last1Y_CNT_MFHL.append('unknown')
            opened_last1Y_CNT_MFOT.append('unknown')
            opened_last1Y_CNT_OTH.append('unknown')
            opened_last1Y_CNT_PL.append('unknown')
            opened_last1Y_CNT_PLBL.append('unknown')
            opened_last1Y_CNT_RL.append('unknown')
            opened_last1Y_CNT_SCC.append('unknown')
            opened_last1Y_CNT_SEL.append('unknown')

            opened_last2Y_CNT_AL.append('unknown')
            opened_last2Y_CNT_BL.append('unknown')
            opened_last2Y_CNT_CC.append('unknown')
            opened_last2Y_CNT_CD.append('unknown')
            opened_last2Y_CNT_CV.append('unknown')
            opened_last2Y_CNT_GL.append('unknown')
            opened_last2Y_CNT_HL.append('unknown')
            opened_last2Y_CNT_LAS.append('unknown')
            opened_last2Y_CNT_MFBL.append('unknown')
            opened_last2Y_CNT_MFHL.append('unknown')
            opened_last2Y_CNT_MFOT.append('unknown')
            opened_last2Y_CNT_OTH.append('unknown')
            opened_last2Y_CNT_PL.append('unknown')
            opened_last2Y_CNT_PLBL.append('unknown')
            opened_last2Y_CNT_RL.append('unknown')
            opened_last2Y_CNT_SCC.append('unknown')
            opened_last2Y_CNT_SEL.append('unknown')

            opened_last3Y_CNT_AL.append('unknown')
            opened_last3Y_CNT_BL.append('unknown')
            opened_last3Y_CNT_CC.append('unknown')
            opened_last3Y_CNT_CD.append('unknown')
            opened_last3Y_CNT_CV.append('unknown')
            opened_last3Y_CNT_GL.append('unknown')
            opened_last3Y_CNT_HL.append('unknown')
            opened_last3Y_CNT_LAS.append('unknown')
            opened_last3Y_CNT_MFBL.append('unknown')
            opened_last3Y_CNT_MFHL.append('unknown')
            opened_last3Y_CNT_MFOT.append('unknown')
            opened_last3Y_CNT_OTH.append('unknown')
            opened_last3Y_CNT_PL.append('unknown')
            opened_last3Y_CNT_PLBL.append('unknown')
            opened_last3Y_CNT_RL.append('unknown')
            opened_last3Y_CNT_SCC.append('unknown')
            opened_last3Y_CNT_SEL.append('unknown')

        else:
            opened_last3M_CNT_AL.append(count_op_l3m_list_AL[x])
            opened_last3M_CNT_BL.append(count_op_l3m_list_BL[x])
            opened_last3M_CNT_CC.append(count_op_l3m_list_CC[x])
            opened_last3M_CNT_CD.append(count_op_l3m_list_CD[x])
            opened_last3M_CNT_CV.append(count_op_l3m_list_CV[x])
            opened_last3M_CNT_GL.append(count_op_l3m_list_GL[x])
            opened_last3M_CNT_HL.append(count_op_l3m_list_HL[x])
            opened_last3M_CNT_LAS.append(count_op_l3m_list_LAS[x])
            opened_last3M_CNT_MFBL.append(count_op_l3m_list_MFBL[x])
            opened_last3M_CNT_MFHL.append(count_op_l3m_list_MFHL[x])
            opened_last3M_CNT_MFOT.append(count_op_l3m_list_MFOT[x])
            opened_last3M_CNT_OTH.append(count_op_l3m_list_OTH[x])
            opened_last3M_CNT_PL.append(count_op_l3m_list_PL[x])
            opened_last3M_CNT_PLBL.append(count_op_l3m_list_PLBL[x])
            opened_last3M_CNT_RL.append(count_op_l3m_list_RL[x])
            opened_last3M_CNT_SCC.append(count_op_l3m_list_SCC[x])
            opened_last3M_CNT_SEL.append(count_op_l3m_list_SEL[x])

            opened_last6M_CNT_AL.append(count_op_l6m_list_AL[x])
            opened_last6M_CNT_BL.append(count_op_l6m_list_BL[x])
            opened_last6M_CNT_CC.append(count_op_l6m_list_CC[x])
            opened_last6M_CNT_CD.append(count_op_l6m_list_CD[x])
            opened_last6M_CNT_CV.append(count_op_l6m_list_CV[x])
            opened_last6M_CNT_GL.append(count_op_l6m_list_GL[x])
            opened_last6M_CNT_HL.append(count_op_l6m_list_HL[x])
            opened_last6M_CNT_LAS.append(count_op_l6m_list_LAS[x])
            opened_last6M_CNT_MFBL.append(count_op_l6m_list_MFBL[x])
            opened_last6M_CNT_MFHL.append(count_op_l6m_list_MFHL[x])
            opened_last6M_CNT_MFOT.append(count_op_l6m_list_MFOT[x])
            opened_last6M_CNT_OTH.append(count_op_l6m_list_OTH[x])
            opened_last6M_CNT_PL.append(count_op_l6m_list_PL[x])
            opened_last6M_CNT_PLBL.append(count_op_l6m_list_PLBL[x])
            opened_last6M_CNT_RL.append(count_op_l6m_list_RL[x])
            opened_last6M_CNT_SCC.append(count_op_l6m_list_SCC[x])
            opened_last6M_CNT_SEL.append(count_op_l6m_list_SEL[x])

            opened_last9M_CNT_AL.append(count_op_l9m_list_AL[x])
            opened_last9M_CNT_BL.append(count_op_l9m_list_BL[x])
            opened_last9M_CNT_CC.append(count_op_l9m_list_CC[x])
            opened_last9M_CNT_CD.append(count_op_l9m_list_CD[x])
            opened_last9M_CNT_CV.append(count_op_l9m_list_CV[x])
            opened_last9M_CNT_GL.append(count_op_l9m_list_GL[x])
            opened_last9M_CNT_HL.append(count_op_l9m_list_HL[x])
            opened_last9M_CNT_LAS.append(count_op_l9m_list_LAS[x])
            opened_last9M_CNT_MFBL.append(count_op_l9m_list_MFBL[x])
            opened_last9M_CNT_MFHL.append(count_op_l9m_list_MFHL[x])
            opened_last9M_CNT_MFOT.append(count_op_l9m_list_MFOT[x])
            opened_last9M_CNT_OTH.append(count_op_l9m_list_OTH[x])
            opened_last9M_CNT_PL.append(count_op_l9m_list_PL[x])
            opened_last9M_CNT_PLBL.append(count_op_l9m_list_PLBL[x])
            opened_last9M_CNT_RL.append(count_op_l9m_list_RL[x])
            opened_last9M_CNT_SCC.append(count_op_l9m_list_SCC[x])
            opened_last9M_CNT_SEL.append(count_op_l9m_list_SEL[x])

            opened_last1Y_CNT_AL.append(count_op_l1y_list_AL[x])
            opened_last1Y_CNT_BL.append(count_op_l1y_list_BL[x])
            opened_last1Y_CNT_CC.append(count_op_l1y_list_CC[x])
            opened_last1Y_CNT_CD.append(count_op_l1y_list_CD[x])
            opened_last1Y_CNT_CV.append(count_op_l1y_list_CV[x])
            opened_last1Y_CNT_GL.append(count_op_l1y_list_GL[x])
            opened_last1Y_CNT_HL.append(count_op_l1y_list_HL[x])
            opened_last1Y_CNT_LAS.append(count_op_l1y_list_LAS[x])
            opened_last1Y_CNT_MFBL.append(count_op_l1y_list_MFBL[x])
            opened_last1Y_CNT_MFHL.append(count_op_l1y_list_MFHL[x])
            opened_last1Y_CNT_MFOT.append(count_op_l1y_list_MFOT[x])
            opened_last1Y_CNT_OTH.append(count_op_l1y_list_OTH[x])
            opened_last1Y_CNT_PL.append(count_op_l1y_list_PL[x])
            opened_last1Y_CNT_PLBL.append(count_op_l1y_list_PLBL[x])
            opened_last1Y_CNT_RL.append(count_op_l1y_list_RL[x])
            opened_last1Y_CNT_SCC.append(count_op_l1y_list_SCC[x])
            opened_last1Y_CNT_SEL.append(count_op_l1y_list_SEL[x])

            opened_last2Y_CNT_AL.append(count_op_l2y_list_AL[x])
            opened_last2Y_CNT_BL.append(count_op_l2y_list_BL[x])
            opened_last2Y_CNT_CC.append(count_op_l2y_list_CC[x])
            opened_last2Y_CNT_CD.append(count_op_l2y_list_CD[x])
            opened_last2Y_CNT_CV.append(count_op_l2y_list_CV[x])
            opened_last2Y_CNT_GL.append(count_op_l2y_list_GL[x])
            opened_last2Y_CNT_HL.append(count_op_l2y_list_HL[x])
            opened_last2Y_CNT_LAS.append(count_op_l2y_list_LAS[x])
            opened_last2Y_CNT_MFBL.append(count_op_l2y_list_MFBL[x])
            opened_last2Y_CNT_MFHL.append(count_op_l2y_list_MFHL[x])
            opened_last2Y_CNT_MFOT.append(count_op_l2y_list_MFOT[x])
            opened_last2Y_CNT_OTH.append(count_op_l2y_list_OTH[x])
            opened_last2Y_CNT_PL.append(count_op_l2y_list_PL[x])
            opened_last2Y_CNT_PLBL.append(count_op_l2y_list_PLBL[x])
            opened_last2Y_CNT_RL.append(count_op_l2y_list_RL[x])
            opened_last2Y_CNT_SCC.append(count_op_l2y_list_SCC[x])
            opened_last2Y_CNT_SEL.append(count_op_l2y_list_SEL[x])

            opened_last3Y_CNT_AL.append(count_op_l3y_list_AL[x])
            opened_last3Y_CNT_BL.append(count_op_l3y_list_BL[x])
            opened_last3Y_CNT_CC.append(count_op_l3y_list_CC[x])
            opened_last3Y_CNT_CD.append(count_op_l3y_list_CD[x])
            opened_last3Y_CNT_CV.append(count_op_l3y_list_CV[x])
            opened_last3Y_CNT_GL.append(count_op_l3y_list_GL[x])
            opened_last3Y_CNT_HL.append(count_op_l3y_list_HL[x])
            opened_last3Y_CNT_LAS.append(count_op_l3y_list_LAS[x])
            opened_last3Y_CNT_MFBL.append(count_op_l3y_list_MFBL[x])
            opened_last3Y_CNT_MFHL.append(count_op_l3y_list_MFHL[x])
            opened_last3Y_CNT_MFOT.append(count_op_l3y_list_MFOT[x])
            opened_last3Y_CNT_OTH.append(count_op_l3y_list_OTH[x])
            opened_last3Y_CNT_PL.append(count_op_l3y_list_PL[x])
            opened_last3Y_CNT_PLBL.append(count_op_l3y_list_PLBL[x])
            opened_last3Y_CNT_RL.append(count_op_l3y_list_RL[x])
            opened_last3Y_CNT_SCC.append(count_op_l3y_list_SCC[x])
            opened_last3Y_CNT_SEL.append(count_op_l3y_list_SEL[x])

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last6M_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 6):
            opened_last6M_CNT.append(count_op_l6m_list[x])
        else:
            opened_last6M_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last9M_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 9):
            opened_last9M_CNT.append(count_op_l9m_list[x])
        else:
            opened_last9M_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last1Y_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 12):
            opened_last1Y_CNT.append(count_op_l1y_list[x])
        else:
            opened_last1Y_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last2Y_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 24):
            opened_last2Y_CNT.append(count_op_l2y_list[x])
        else:
            opened_last2Y_CNT.append(0)

        if (grp_slice['mo_diff_do_ld'][i] == 'unknown'):
            opened_last3Y_CNT.append('unknown')
        elif (grp_slice['mo_diff_do_ld'][i] <= 36):
            opened_last3Y_CNT.append(count_op_l3y_list[x])
        else:
            opened_last3Y_CNT.append(0)

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'AL'):
            overdueAmount_sum_AL.append(sum(oa_list_AL))
        else:
            overdueAmount_sum_AL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'BL'):
            overdueAmount_sum_BL.append(sum(oa_list_BL))
        else:
            overdueAmount_sum_BL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'CC'):
            overdueAmount_sum_CC.append(sum(oa_list_CC))
        else:
            overdueAmount_sum_CC.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'CD'):
            overdueAmount_sum_CD.append(sum(oa_list_CD))
        else:
            overdueAmount_sum_CD.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'CV'):
            overdueAmount_sum_CV.append(sum(oa_list_CV))
        else:
            overdueAmount_sum_CV.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'GL'):
            overdueAmount_sum_GL.append(sum(oa_list_GL))
        else:
            overdueAmount_sum_GL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'HL'):
            overdueAmount_sum_HL.append(sum(oa_list_HL))
        else:
            overdueAmount_sum_HL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'LAS'):
            overdueAmount_sum_LAS.append(sum(oa_list_LAS))
        else:
            overdueAmount_sum_LAS.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'MFBL'):
            overdueAmount_sum_MFBL.append(sum(oa_list_MFBL))
        else:
            overdueAmount_sum_MFBL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'MFHL'):
            overdueAmount_sum_MFHL.append(sum(oa_list_MFHL))
        else:
            overdueAmount_sum_MFHL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'MFOT'):
            overdueAmount_sum_MFOT.append(sum(oa_list_MFOT))
        else:
            overdueAmount_sum_MFOT.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'OTH'):
            overdueAmount_sum_OTH.append(sum(oa_list_OTH))
        else:
            overdueAmount_sum_OTH.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'PL'):
            overdueAmount_sum_PL.append(sum(oa_list_PL))
        else:
            overdueAmount_sum_PL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'PLBL'):
            overdueAmount_sum_PLBL.append(sum(oa_list_PLBL))
        else:
            overdueAmount_sum_PLBL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'RL'):
            overdueAmount_sum_RL.append(sum(oa_list_RL))
        else:
            overdueAmount_sum_RL.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'SCC'):
            overdueAmount_sum_SCC.append(sum(oa_list_SCC))
        else:
            overdueAmount_sum_SCC.append('unknown')

        if (grp_slice['overdueAmount'][i] != 'unknown') and (grp_slice['dictAccountType'][i] == 'SEL'):
            overdueAmount_sum_SEL.append(sum(oa_list_SEL))
        else:
            overdueAmount_sum_SEL.append('unknown')

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_AL) == 0):
            Overdue_Current_AL.append('unknown')
        else:
            Overdue_Current_AL.append(
                sum(grp_list_oa_AL)/sum(grp_list_cb_AL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_BL) == 0):
            Overdue_Current_BL.append('unknown')
        else:
            Overdue_Current_BL.append(
                sum(grp_list_oa_BL)/sum(grp_list_cb_BL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_CC) == 0):
            Overdue_Current_CC.append('unknown')
        else:
            Overdue_Current_CC.append(
                sum(grp_list_oa_CC)/sum(grp_list_cb_CC))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_CD) == 0):
            Overdue_Current_CD.append('unknown')
        else:
            Overdue_Current_CD.append(
                sum(grp_list_oa_CD)/sum(grp_list_cb_CD))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_CV) == 0):
            Overdue_Current_CV.append('unknown')
        else:
            Overdue_Current_CV.append(
                sum(grp_list_oa_CV)/sum(grp_list_cb_CV))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_GL) == 0):
            Overdue_Current_GL.append('unknown')
        else:
            Overdue_Current_GL.append(
                sum(grp_list_oa_GL)/sum(grp_list_cb_GL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_HL) == 0):
            Overdue_Current_HL.append('unknown')
        else:
            Overdue_Current_HL.append(
                sum(grp_list_oa_HL)/sum(grp_list_cb_HL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_LAS) == 0):
            Overdue_Current_LAS.append('unknown')
        else:
            Overdue_Current_LAS.append(
                sum(grp_list_oa_LAS)/sum(grp_list_cb_LAS))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_MFBL) == 0):
            Overdue_Current_MFBL.append('unknown')
        else:
            Overdue_Current_MFBL.append(
                sum(grp_list_oa_MFBL)/sum(grp_list_cb_MFBL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_MFHL) == 0):
            Overdue_Current_MFHL.append('unknown')
        else:
            Overdue_Current_MFHL.append(
                sum(grp_list_oa_MFHL)/sum(grp_list_cb_MFHL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_MFOT) == 0):
            Overdue_Current_MFOT.append('unknown')
        else:
            Overdue_Current_MFOT.append(
                sum(grp_list_oa_MFOT)/sum(grp_list_cb_MFOT))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_OTH) == 0):
            Overdue_Current_OTH.append('unknown')
        else:
            Overdue_Current_OTH.append(
                sum(grp_list_oa_OTH)/sum(grp_list_cb_OTH))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_PL) == 0):
            Overdue_Current_PL.append('unknown')
        else:
            Overdue_Current_PL.append(
                sum(grp_list_oa_PL)/sum(grp_list_cb_PL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_PLBL) == 0):
            Overdue_Current_PLBL.append('unknown')
        else:
            Overdue_Current_PLBL.append(
                sum(grp_list_oa_PLBL)/sum(grp_list_cb_PLBL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_RL) == 0):
            Overdue_Current_RL.append('unknown')
        else:
            Overdue_Current_RL.append(
                sum(grp_list_oa_RL)/sum(grp_list_cb_RL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_SCC) == 0):
            Overdue_Current_SCC.append('unknown')
        else:
            Overdue_Current_SCC.append(
                sum(grp_list_oa_SCC)/sum(grp_list_cb_SCC))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (sum(grp_list_cb_SEL) == 0):
            Overdue_Current_SEL.append('unknown')
        else:
            Overdue_Current_SEL.append(
                sum(grp_list_oa_SEL)/sum(grp_list_cb_SEL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_AL) == 0):
            Overdue_Disbursed_AL.append('unknown')
        else:
            Overdue_Disbursed_AL.append(
                sum(grp_list_oa2_AL)/sum(grp_list_da_AL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_BL) == 0):
            Overdue_Disbursed_BL.append('unknown')
        else:
            Overdue_Disbursed_BL.append(
                sum(grp_list_oa2_BL)/sum(grp_list_da_BL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_CC) == 0):
            Overdue_Disbursed_CC.append('unknown')
        else:
            Overdue_Disbursed_CC.append(
                sum(grp_list_oa2_CC)/sum(grp_list_da_CC))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_CD) == 0):
            Overdue_Disbursed_CD.append('unknown')
        else:
            Overdue_Disbursed_CD.append(
                sum(grp_list_oa2_CD)/sum(grp_list_da_CD))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_CV) == 0):
            Overdue_Disbursed_CV.append('unknown')
        else:
            Overdue_Disbursed_CV.append(
                sum(grp_list_oa2_CV)/sum(grp_list_da_CV))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_GL) == 0):
            Overdue_Disbursed_GL.append('unknown')
        else:
            Overdue_Disbursed_GL.append(
                sum(grp_list_oa2_GL)/sum(grp_list_da_GL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_HL) == 0):
            Overdue_Disbursed_HL.append('unknown')
        else:
            Overdue_Disbursed_HL.append(
                sum(grp_list_oa2_HL)/sum(grp_list_da_HL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_LAS) == 0):
            Overdue_Disbursed_LAS.append('unknown')
        else:
            Overdue_Disbursed_LAS.append(
                sum(grp_list_oa2_LAS)/sum(grp_list_da_LAS))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_MFBL) == 0):
            Overdue_Disbursed_MFBL.append('unknown')
        else:
            Overdue_Disbursed_MFBL.append(
                sum(grp_list_oa2_MFBL)/sum(grp_list_da_MFBL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_MFHL) == 0):
            Overdue_Disbursed_MFHL.append('unknown')
        else:
            Overdue_Disbursed_MFHL.append(
                sum(grp_list_oa2_MFHL)/sum(grp_list_da_MFHL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_MFOT) == 0):
            Overdue_Disbursed_MFOT.append('unknown')
        else:
            Overdue_Disbursed_MFOT.append(
                sum(grp_list_oa2_MFOT)/sum(grp_list_da_MFOT))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_OTH) == 0):
            Overdue_Disbursed_OTH.append('unknown')
        else:
            Overdue_Disbursed_OTH.append(
                sum(grp_list_oa2_OTH)/sum(grp_list_da_OTH))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_PL) == 0):
            Overdue_Disbursed_PL.append('unknown')
        else:
            Overdue_Disbursed_PL.append(
                sum(grp_list_oa2_PL)/sum(grp_list_da_PL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_PLBL) == 0):
            Overdue_Disbursed_PLBL.append('unknown')
        else:
            Overdue_Disbursed_PLBL.append(
                sum(grp_list_oa2_PLBL)/sum(grp_list_da_PLBL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_RL) == 0):
            Overdue_Disbursed_RL.append('unknown')
        else:
            Overdue_Disbursed_RL.append(
                sum(grp_list_oa2_RL)/sum(grp_list_da_RL))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_SCC) == 0):
            Overdue_Disbursed_SCC.append('unknown')
        else:
            Overdue_Disbursed_SCC.append(
                sum(grp_list_oa2_SCC)/sum(grp_list_da_SCC))

        if (grp_slice['overdueAmount'][i] == 'unknown') or (grp_slice['sanctionAmount'][i] == 'unknown') or (sum(grp_list_da_SEL) == 0):
            Overdue_Disbursed_SEL.append('unknown')
        else:
            Overdue_Disbursed_SEL.append(
                sum(grp_list_oa2_SEL)/sum(grp_list_da_SEL))

        if (grp_slice['dateClosed_lt_PHED_wo'][i] == 1) or (grp_slice['dateClosed_lt_PHED_wo'][i] == 0):
            dateClosed_lt_PHED_wo_CNT.append(count_dtCl_wo_list[x])
        else:
            dateClosed_lt_PHED_wo_CNT.append('unknown')

        if (grp_slice['dateClosed_lt_PHED_suit'][i] == 1) or (grp_slice['dateClosed_lt_PHED_suit'][i] == 0):
            dateClosed_lt_PHED_suit_CNT.append(count_dtCl_suit_list[x])
        else:
            dateClosed_lt_PHED_suit_CNT.append('unknown')

        if (grp_slice['dateClosed_lt_PHED_PH1M'][i] == 1) or (grp_slice['dateClosed_lt_PHED_PH1M'][i] == 0):
            dateClosed_lt_PHED_PH1M_CNT.append(count_dtCl_ph1m_list[x])
        else:
            dateClosed_lt_PHED_PH1M_CNT.append('unknown')

        if (grp_slice['dateClosed_lt_PHED_restruct'][i] == 1) or (grp_slice['dateClosed_lt_PHED_restruct'][i] == 0):
            dateClosed_lt_PHED_restruct_CNT.append(count_dtCl_res_list[x])
        else:
            dateClosed_lt_PHED_restruct_CNT.append('unknown')

    sec_L_cnt_list = list()
    unsec_L_cnt_list = list()

df['dateClosed_lt_PHED_CNT'] = pd.Series(dateClosed_lt_PHED_CNT).values
df['ignore_case_CNT'] = pd.Series(ignore_case_CNT).values

df['sumCurrentBalance'] = pd.Series(sumCurrentBalance).values
df['sumSanctionAmount'] = pd.Series(sumSanctionAmount).values
df['currentBalance_sanctionedAmount_NCC_L'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L).values
df['sumCreditLimit'] = pd.Series(sumCreditLimit).values

df['mode_util_CC_L'] = pd.Series(mode_util_CC_L).values
df['mean_util_CC_L'] = pd.Series(mean_util_CC_L).values
df['median_util_CC_L'] = pd.Series(median_util_CC_L).values
df['min_util_CC_L'] = pd.Series(min_util_CC_L).values

df['mean_util_highCredit_CC_L'] = pd.Series(mean_util_highCredit_CC_L).values
df['mode_util_highCredit_CC_L'] = pd.Series(mode_util_highCredit_CC_L).values
df['median_util_highCredit_CC_L'] = pd.Series(
    median_util_highCredit_CC_L).values
df['min_util_highCredit_CC_L'] = pd.Series(min_util_highCredit_CC_L).values

df['mean_util_highCredit_CC_A'] = pd.Series(mean_util_highCredit_CC_A).values
df['mode_util_highCredit_CC_A'] = pd.Series(mode_util_highCredit_CC_A).values
df['median_util_highCredit_CC_A'] = pd.Series(
    median_util_highCredit_CC_A).values
df['min_util_highCredit_CC_A'] = pd.Series(min_util_highCredit_CC_A).values

df['Mean_SancAmt'] = pd.Series(Mean_SancAmt).values
df['Mean_SancAmt_L'] = pd.Series(Mean_SancAmt_L).values

df['Median_SancAmt'] = pd.Series(Median_SancAmt).values
df['Median_SancAmt_L'] = pd.Series(Median_SancAmt_L).values

df['Mode_SancAmt'] = pd.Series(Mode_SancAmt).values
df['Mode_SancAmt_L'] = pd.Series(Mode_SancAmt_L).values

df['Secured_CNT'] = pd.Series(Secured_CNT).values
df['Unsecured_CNT'] = pd.Series(Unsecured_CNT).values

df['Loans_Sec_UnsecwoRLCC_L'] = pd.Series(Loans_Sec_UnsecwoRLCC_L).values
df['Per_Sec_UnsecwoRLCC_L'] = pd.Series(Per_Sec_UnsecwoRLCC_L).values

df['Mean_SancAmt_AL'] = pd.Series(Mean_SancAmt_AL).values
df['Mean_SancAmt_BL'] = pd.Series(Mean_SancAmt_BL).values
df['Mean_SancAmt_CD'] = pd.Series(Mean_SancAmt_CD).values
df['Mean_SancAmt_CV'] = pd.Series(Mean_SancAmt_CV).values
df['Mean_SancAmt_GL'] = pd.Series(Mean_SancAmt_GL).values
df['Mean_SancAmt_HL'] = pd.Series(Mean_SancAmt_HL).values
df['Mean_SancAmt_LAS'] = pd.Series(Mean_SancAmt_LAS).values
df['Mean_SancAmt_MFBL'] = pd.Series(Mean_SancAmt_MFBL).values
df['Mean_SancAmt_MFHL'] = pd.Series(Mean_SancAmt_MFHL).values
df['Mean_SancAmt_MFOT'] = pd.Series(Mean_SancAmt_MFOT).values
df['Mean_SancAmt_OTH'] = pd.Series(Mean_SancAmt_OTH).values
df['Mean_SancAmt_PL'] = pd.Series(Mean_SancAmt_PL).values
df['Mean_SancAmt_PLBL'] = pd.Series(Mean_SancAmt_PLBL).values
df['Mean_SancAmt_RL'] = pd.Series(Mean_SancAmt_RL).values
df['Mean_SancAmt_SEL'] = pd.Series(Mean_SancAmt_SEL).values

df['Mean_SancAmt_L_AL'] = pd.Series(Mean_SancAmt_L_AL).values
df['Mean_SancAmt_L_BL'] = pd.Series(Mean_SancAmt_L_BL).values
df['Mean_SancAmt_L_CD'] = pd.Series(Mean_SancAmt_L_CD).values
df['Mean_SancAmt_L_CV'] = pd.Series(Mean_SancAmt_L_CV).values
df['Mean_SancAmt_L_GL'] = pd.Series(Mean_SancAmt_L_GL).values
df['Mean_SancAmt_L_HL'] = pd.Series(Mean_SancAmt_L_HL).values
df['Mean_SancAmt_L_LAS'] = pd.Series(Mean_SancAmt_L_LAS).values
df['Mean_SancAmt_L_MFBL'] = pd.Series(Mean_SancAmt_L_MFBL).values
df['Mean_SancAmt_L_MFHL'] = pd.Series(Mean_SancAmt_L_MFHL).values
df['Mean_SancAmt_L_MFOT'] = pd.Series(Mean_SancAmt_L_MFOT).values
df['Mean_SancAmt_L_OTH'] = pd.Series(Mean_SancAmt_L_OTH).values
df['Mean_SancAmt_L_PL'] = pd.Series(Mean_SancAmt_L_PL).values
df['Mean_SancAmt_L_PLBL'] = pd.Series(Mean_SancAmt_L_PLBL).values
df['Mean_SancAmt_L_RL'] = pd.Series(Mean_SancAmt_L_RL).values
df['Mean_SancAmt_L_SEL'] = pd.Series(Mean_SancAmt_L_SEL).values

df['Med_SancAmt_AL'] = pd.Series(Med_SancAmt_AL).values
df['Med_SancAmt_BL'] = pd.Series(Med_SancAmt_BL).values
df['Med_SancAmt_CD'] = pd.Series(Med_SancAmt_CD).values
df['Med_SancAmt_CV'] = pd.Series(Med_SancAmt_CV).values
df['Med_SancAmt_GL'] = pd.Series(Med_SancAmt_GL).values
df['Med_SancAmt_HL'] = pd.Series(Med_SancAmt_HL).values
df['Med_SancAmt_LAS'] = pd.Series(Med_SancAmt_LAS).values
df['Med_SancAmt_MFBL'] = pd.Series(Med_SancAmt_MFBL).values
df['Med_SancAmt_MFHL'] = pd.Series(Med_SancAmt_MFHL).values
df['Med_SancAmt_MFOT'] = pd.Series(Med_SancAmt_MFOT).values
df['Med_SancAmt_OTH'] = pd.Series(Med_SancAmt_OTH).values
df['Med_SancAmt_PL'] = pd.Series(Med_SancAmt_PL).values
df['Med_SancAmt_PLBL'] = pd.Series(Med_SancAmt_PLBL).values
df['Med_SancAmt_RL'] = pd.Series(Med_SancAmt_RL).values
df['Med_SancAmt_SEL'] = pd.Series(Med_SancAmt_SEL).values

df['Med_SancAmt_L_AL'] = pd.Series(Med_SancAmt_L_AL).values
df['Med_SancAmt_L_BL'] = pd.Series(Med_SancAmt_L_BL).values
df['Med_SancAmt_L_CD'] = pd.Series(Med_SancAmt_L_CD).values
df['Med_SancAmt_L_CV'] = pd.Series(Med_SancAmt_L_CV).values
df['Med_SancAmt_L_GL'] = pd.Series(Med_SancAmt_L_GL).values
df['Med_SancAmt_L_HL'] = pd.Series(Med_SancAmt_L_HL).values
df['Med_SancAmt_L_LAS'] = pd.Series(Med_SancAmt_L_LAS).values
df['Med_SancAmt_L_MFBL'] = pd.Series(Med_SancAmt_L_MFBL).values
df['Med_SancAmt_L_MFHL'] = pd.Series(Med_SancAmt_L_MFHL).values
df['Med_SancAmt_L_MFOT'] = pd.Series(Med_SancAmt_L_MFOT).values
df['Med_SancAmt_L_OTH'] = pd.Series(Med_SancAmt_L_OTH).values
df['Med_SancAmt_L_PL'] = pd.Series(Med_SancAmt_L_PL).values
df['Med_SancAmt_L_PLBL'] = pd.Series(Med_SancAmt_L_PLBL).values
df['Med_SancAmt_L_RL'] = pd.Series(Med_SancAmt_L_RL).values
df['Med_SancAmt_L_SEL'] = pd.Series(Med_SancAmt_L_SEL).values

'''
df['Mode_SancAmt_AL'] = pd.Series(Mode_SancAmt_AL).values
df['Mode_SancAmt_BL'] = pd.Series(Mode_SancAmt_BL).values
df['Mode_SancAmt_CD'] = pd.Series(Mode_SancAmt_CD).values
df['Mode_SancAmt_CV'] = pd.Series(Mode_SancAmt_CV).values
df['Mode_SancAmt_GL'] = pd.Series(Mode_SancAmt_GL).values
df['Mode_SancAmt_HL'] = pd.Series(Mode_SancAmt_HL).values
df['Mode_SancAmt_LAS'] = pd.Series(Mode_SancAmt_LAS).values
df['Mode_SancAmt_MFBL'] = pd.Series(Mode_SancAmt_MFBL).values
df['Mode_SancAmt_MFHL'] = pd.Series(Mode_SancAmt_MFHL).values
df['Mode_SancAmt_MFOT'] = pd.Series(Mode_SancAmt_MFOT).values
df['Mode_SancAmt_OTH'] = pd.Series(Mode_SancAmt_OTH).values
df['Mode_SancAmt_PL'] = pd.Series(Mode_SancAmt_PL).values
df['Mode_SancAmt_PLBL'] = pd.Series(Mode_SancAmt_PLBL).values
df['Mode_SancAmt_RL'] = pd.Series(Mode_SancAmt_RL).values
df['Mode_SancAmt_SEL'] = pd.Series(Mode_SancAmt_SEL).values

df['Mode_SancAmt_L_AL'] = pd.Series(Mode_SancAmt_L_AL).values
df['Mode_SancAmt_L_BL'] = pd.Series(Mode_SancAmt_L_BL).values
df['Mode_SancAmt_L_CD'] = pd.Series(Mode_SancAmt_L_CD).values
df['Mode_SancAmt_L_CV'] = pd.Series(Mode_SancAmt_L_CV).values
df['Mode_SancAmt_L_GL'] = pd.Series(Mode_SancAmt_L_GL).values
df['Mode_SancAmt_L_HL'] = pd.Series(Mode_SancAmt_L_HL).values
df['Mode_SancAmt_L_LAS'] = pd.Series(Mode_SancAmt_L_LAS).values
df['Mode_SancAmt_L_MFBL'] = pd.Series(Mode_SancAmt_L_MFBL).values
df['Mode_SancAmt_L_MFHL'] = pd.Series(Mode_SancAmt_L_MFHL).values
df['Mode_SancAmt_L_MFOT'] = pd.Series(Mode_SancAmt_L_MFOT).values
df['Mode_SancAmt_L_OTH'] = pd.Series(Mode_SancAmt_L_OTH).values
df['Mode_SancAmt_L_PL'] = pd.Series(Mode_SancAmt_L_PL).values
df['Mode_SancAmt_L_PLBL'] = pd.Series(Mode_SancAmt_L_PLBL).values
df['Mode_SancAmt_L_RL'] = pd.Series(Mode_SancAmt_L_RL).values
df['Mode_SancAmt_L_SEL'] = pd.Series(Mode_SancAmt_L_SEL).values'''

df['currentBalance_sanctionedAmount_NCC_L_AL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_AL).values
df['currentBalance_sanctionedAmount_NCC_L_BL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_BL).values
df['currentBalance_sanctionedAmount_NCC_L_CD'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_CD).values
df['currentBalance_sanctionedAmount_NCC_L_CV'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_CV).values
df['currentBalance_sanctionedAmount_NCC_L_GL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_GL).values
df['currentBalance_sanctionedAmount_NCC_L_HL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_HL).values
df['currentBalance_sanctionedAmount_NCC_L_LAS'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_LAS).values
df['currentBalance_sanctionedAmount_NCC_L_MFBL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_MFBL).values
df['currentBalance_sanctionedAmount_NCC_L_MFHL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_MFHL).values
df['currentBalance_sanctionedAmount_NCC_L_MFOT'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_MFOT).values
df['currentBalance_sanctionedAmount_NCC_L_OTH'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_OTH).values
df['currentBalance_sanctionedAmount_NCC_L_PL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_PL).values
df['currentBalance_sanctionedAmount_NCC_L_PLBL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_PLBL).values
df['currentBalance_sanctionedAmount_NCC_L_RL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_RL).values
df['currentBalance_sanctionedAmount_NCC_L_SEL'] = pd.Series(
    currentBalance_sanctionedAmount_NCC_L_SEL).values

df['totAcc'] = pd.Series(totAcc).values
df['sanc_amt_grp'] = pd.Series(sanc_amt_grp).values
df['cnt_grp'] = pd.Series(cnt_grp).values

df['totAcc_L'] = pd.Series(totAcc_L).values
df['sum_L_sanc_amt_grp_L'] = pd.Series(sum_L_sanc_amt_grp_L).values
df['cnt_L_grp_L'] = pd.Series(cnt_L_grp_L).values

df['curr_bal_grp_L'] = pd.Series(curr_bal_grp_L).values

df['writeOff_CNT'] = pd.Series(writeOff_CNT).values
df['restructured_CNT'] = pd.Series(restructured_CNT).values

df['writeOff_CNT_AL'] = pd.Series(writeOff_CNT_AL).values
df['writeOff_CNT_BL'] = pd.Series(writeOff_CNT_BL).values
df['writeOff_CNT_CC'] = pd.Series(writeOff_CNT_CC).values
df['writeOff_CNT_CD'] = pd.Series(writeOff_CNT_CD).values
df['writeOff_CNT_CV'] = pd.Series(writeOff_CNT_CV).values
df['writeOff_CNT_GL'] = pd.Series(writeOff_CNT_GL).values
df['writeOff_CNT_HL'] = pd.Series(writeOff_CNT_HL).values
df['writeOff_CNT_LAS'] = pd.Series(writeOff_CNT_LAS).values
df['writeOff_CNT_MFBL'] = pd.Series(writeOff_CNT_MFBL).values
df['writeOff_CNT_MFHL'] = pd.Series(writeOff_CNT_MFHL).values
df['writeOff_CNT_MFOT'] = pd.Series(writeOff_CNT_MFOT).values
df['writeOff_CNT_OTH'] = pd.Series(writeOff_CNT_OTH).values
df['writeOff_CNT_PL'] = pd.Series(writeOff_CNT_PL).values
df['writeOff_CNT_PLBL'] = pd.Series(writeOff_CNT_PLBL).values
df['writeOff_CNT_RL'] = pd.Series(writeOff_CNT_RL).values
df['writeOff_CNT_SCC'] = pd.Series(writeOff_CNT_SCC).values
df['writeOff_CNT_SEL'] = pd.Series(writeOff_CNT_SEL).values

df['restructured_CNT_AL'] = pd.Series(restructured_CNT_AL).values
df['restructured_CNT_BL'] = pd.Series(restructured_CNT_BL).values
df['restructured_CNT_CC'] = pd.Series(restructured_CNT_CC).values
df['restructured_CNT_CD'] = pd.Series(restructured_CNT_CD).values
df['restructured_CNT_CV'] = pd.Series(restructured_CNT_CV).values
df['restructured_CNT_GL'] = pd.Series(restructured_CNT_GL).values
df['restructured_CNT_HL'] = pd.Series(restructured_CNT_HL).values
df['restructured_CNT_LAS'] = pd.Series(restructured_CNT_LAS).values
df['restructured_CNT_MFBL'] = pd.Series(restructured_CNT_MFBL).values
df['restructured_CNT_MFHL'] = pd.Series(restructured_CNT_MFHL).values
df['restructured_CNT_MFOT'] = pd.Series(restructured_CNT_MFOT).values
df['restructured_CNT_OTH'] = pd.Series(restructured_CNT_OTH).values
df['restructured_CNT_PL'] = pd.Series(restructured_CNT_PL).values
df['restructured_CNT_PLBL'] = pd.Series(restructured_CNT_PLBL).values
df['restructured_CNT_RL'] = pd.Series(restructured_CNT_RL).values
df['restructured_CNT_SCC'] = pd.Series(restructured_CNT_SCC).values
df['restructured_CNT_SEL'] = pd.Series(restructured_CNT_SEL).values

df['writeOff_last3M_CNT'] = pd.Series(writeOff_last3M_CNT).values

df['writeOff_last3M_CNT_AL'] = pd.Series(writeOff_last3M_CNT_AL).values
df['writeOff_last3M_CNT_BL'] = pd.Series(writeOff_last3M_CNT_BL).values
df['writeOff_last3M_CNT_CC'] = pd.Series(writeOff_last3M_CNT_CC).values
df['writeOff_last3M_CNT_CD'] = pd.Series(writeOff_last3M_CNT_CD).values
df['writeOff_last3M_CNT_CV'] = pd.Series(writeOff_last3M_CNT_CV).values
df['writeOff_last3M_CNT_GL'] = pd.Series(writeOff_last3M_CNT_GL).values
df['writeOff_last3M_CNT_HL'] = pd.Series(writeOff_last3M_CNT_HL).values
df['writeOff_last3M_CNT_LAS'] = pd.Series(writeOff_last3M_CNT_LAS).values
df['writeOff_last3M_CNT_MFBL'] = pd.Series(writeOff_last3M_CNT_MFBL).values
df['writeOff_last3M_CNT_MFHL'] = pd.Series(writeOff_last3M_CNT_MFHL).values
df['writeOff_last3M_CNT_MFOT'] = pd.Series(writeOff_last3M_CNT_MFOT).values
df['writeOff_last3M_CNT_OTH'] = pd.Series(writeOff_last3M_CNT_OTH).values
df['writeOff_last3M_CNT_PL'] = pd.Series(writeOff_last3M_CNT_PL).values
df['writeOff_last3M_CNT_PLBL'] = pd.Series(writeOff_last3M_CNT_PLBL).values
df['writeOff_last3M_CNT_RL'] = pd.Series(writeOff_last3M_CNT_RL).values
df['writeOff_last3M_CNT_SCC'] = pd.Series(writeOff_last3M_CNT_SCC).values
df['writeOff_last3M_CNT_SEL'] = pd.Series(writeOff_last3M_CNT_SEL).values

df['writeOff_last6M_CNT'] = pd.Series(writeOff_last6M_CNT).values

df['writeOff_last6M_CNT_AL'] = pd.Series(writeOff_last6M_CNT_AL).values
df['writeOff_last6M_CNT_BL'] = pd.Series(writeOff_last6M_CNT_BL).values
df['writeOff_last6M_CNT_CC'] = pd.Series(writeOff_last6M_CNT_CC).values
df['writeOff_last6M_CNT_CD'] = pd.Series(writeOff_last6M_CNT_CD).values
df['writeOff_last6M_CNT_CV'] = pd.Series(writeOff_last6M_CNT_CV).values
df['writeOff_last6M_CNT_GL'] = pd.Series(writeOff_last6M_CNT_GL).values
df['writeOff_last6M_CNT_HL'] = pd.Series(writeOff_last6M_CNT_HL).values
df['writeOff_last6M_CNT_LAS'] = pd.Series(writeOff_last6M_CNT_LAS).values
df['writeOff_last6M_CNT_MFBL'] = pd.Series(writeOff_last6M_CNT_MFBL).values
df['writeOff_last6M_CNT_MFHL'] = pd.Series(writeOff_last6M_CNT_MFHL).values
df['writeOff_last6M_CNT_MFOT'] = pd.Series(writeOff_last6M_CNT_MFOT).values
df['writeOff_last6M_CNT_OTH'] = pd.Series(writeOff_last6M_CNT_OTH).values
df['writeOff_last6M_CNT_PL'] = pd.Series(writeOff_last6M_CNT_PL).values
df['writeOff_last6M_CNT_PLBL'] = pd.Series(writeOff_last6M_CNT_PLBL).values
df['writeOff_last6M_CNT_RL'] = pd.Series(writeOff_last6M_CNT_RL).values
df['writeOff_last6M_CNT_SCC'] = pd.Series(writeOff_last6M_CNT_SCC).values
df['writeOff_last6M_CNT_SEL'] = pd.Series(writeOff_last6M_CNT_SEL).values

df['writeOff_last9M_CNT'] = pd.Series(writeOff_last9M_CNT).values

df['writeOff_last9M_CNT_AL'] = pd.Series(writeOff_last9M_CNT_AL).values
df['writeOff_last9M_CNT_BL'] = pd.Series(writeOff_last9M_CNT_BL).values
df['writeOff_last9M_CNT_CC'] = pd.Series(writeOff_last9M_CNT_CC).values
df['writeOff_last9M_CNT_CD'] = pd.Series(writeOff_last9M_CNT_CD).values
df['writeOff_last9M_CNT_CV'] = pd.Series(writeOff_last9M_CNT_CV).values
df['writeOff_last9M_CNT_GL'] = pd.Series(writeOff_last9M_CNT_GL).values
df['writeOff_last9M_CNT_HL'] = pd.Series(writeOff_last9M_CNT_HL).values
df['writeOff_last9M_CNT_LAS'] = pd.Series(writeOff_last9M_CNT_LAS).values
df['writeOff_last9M_CNT_MFBL'] = pd.Series(writeOff_last9M_CNT_MFBL).values
df['writeOff_last9M_CNT_MFHL'] = pd.Series(writeOff_last9M_CNT_MFHL).values
df['writeOff_last9M_CNT_MFOT'] = pd.Series(writeOff_last9M_CNT_MFOT).values
df['writeOff_last9M_CNT_OTH'] = pd.Series(writeOff_last9M_CNT_OTH).values
df['writeOff_last9M_CNT_PL'] = pd.Series(writeOff_last9M_CNT_PL).values
df['writeOff_last9M_CNT_PLBL'] = pd.Series(writeOff_last9M_CNT_PLBL).values
df['writeOff_last9M_CNT_RL'] = pd.Series(writeOff_last9M_CNT_RL).values
df['writeOff_last9M_CNT_SCC'] = pd.Series(writeOff_last9M_CNT_SCC).values
df['writeOff_last9M_CNT_SEL'] = pd.Series(writeOff_last9M_CNT_SEL).values

df['writeOff_last1Y_CNT'] = pd.Series(writeOff_last1Y_CNT).values

df['writeOff_last1Y_CNT_AL'] = pd.Series(writeOff_last1Y_CNT_AL).values
df['writeOff_last1Y_CNT_BL'] = pd.Series(writeOff_last1Y_CNT_BL).values
df['writeOff_last1Y_CNT_CC'] = pd.Series(writeOff_last1Y_CNT_CC).values
df['writeOff_last1Y_CNT_CD'] = pd.Series(writeOff_last1Y_CNT_CD).values
df['writeOff_last1Y_CNT_CV'] = pd.Series(writeOff_last1Y_CNT_CV).values
df['writeOff_last1Y_CNT_GL'] = pd.Series(writeOff_last1Y_CNT_GL).values
df['writeOff_last1Y_CNT_HL'] = pd.Series(writeOff_last1Y_CNT_HL).values
df['writeOff_last1Y_CNT_LAS'] = pd.Series(writeOff_last1Y_CNT_LAS).values
df['writeOff_last1Y_CNT_MFBL'] = pd.Series(writeOff_last1Y_CNT_MFBL).values
df['writeOff_last1Y_CNT_MFHL'] = pd.Series(writeOff_last1Y_CNT_MFHL).values
df['writeOff_last1Y_CNT_MFOT'] = pd.Series(writeOff_last1Y_CNT_MFOT).values
df['writeOff_last1Y_CNT_OTH'] = pd.Series(writeOff_last1Y_CNT_OTH).values
df['writeOff_last1Y_CNT_PL'] = pd.Series(writeOff_last1Y_CNT_PL).values
df['writeOff_last1Y_CNT_PLBL'] = pd.Series(writeOff_last1Y_CNT_PLBL).values
df['writeOff_last1Y_CNT_RL'] = pd.Series(writeOff_last1Y_CNT_RL).values
df['writeOff_last1Y_CNT_SCC'] = pd.Series(writeOff_last1Y_CNT_SCC).values
df['writeOff_last1Y_CNT_SEL'] = pd.Series(writeOff_last1Y_CNT_SEL).values

df['writeOff_last2Y_CNT'] = pd.Series(writeOff_last2Y_CNT).values

df['writeOff_last2Y_CNT_AL'] = pd.Series(writeOff_last2Y_CNT_AL).values
df['writeOff_last2Y_CNT_BL'] = pd.Series(writeOff_last2Y_CNT_BL).values
df['writeOff_last2Y_CNT_CC'] = pd.Series(writeOff_last2Y_CNT_CC).values
df['writeOff_last2Y_CNT_CD'] = pd.Series(writeOff_last2Y_CNT_CD).values
df['writeOff_last2Y_CNT_CV'] = pd.Series(writeOff_last2Y_CNT_CV).values
df['writeOff_last2Y_CNT_GL'] = pd.Series(writeOff_last2Y_CNT_GL).values
df['writeOff_last2Y_CNT_HL'] = pd.Series(writeOff_last2Y_CNT_HL).values
df['writeOff_last2Y_CNT_LAS'] = pd.Series(writeOff_last2Y_CNT_LAS).values
df['writeOff_last2Y_CNT_MFBL'] = pd.Series(writeOff_last2Y_CNT_MFBL).values
df['writeOff_last2Y_CNT_MFHL'] = pd.Series(writeOff_last2Y_CNT_MFHL).values
df['writeOff_last2Y_CNT_MFOT'] = pd.Series(writeOff_last2Y_CNT_MFOT).values
df['writeOff_last2Y_CNT_OTH'] = pd.Series(writeOff_last2Y_CNT_OTH).values
df['writeOff_last2Y_CNT_PL'] = pd.Series(writeOff_last2Y_CNT_PL).values
df['writeOff_last2Y_CNT_PLBL'] = pd.Series(writeOff_last2Y_CNT_PLBL).values
df['writeOff_last2Y_CNT_RL'] = pd.Series(writeOff_last2Y_CNT_RL).values
df['writeOff_last2Y_CNT_SCC'] = pd.Series(writeOff_last2Y_CNT_SCC).values
df['writeOff_last2Y_CNT_SEL'] = pd.Series(writeOff_last2Y_CNT_SEL).values

df['writeOff_last3Y_CNT'] = pd.Series(writeOff_last3Y_CNT).values

df['writeOff_last3Y_CNT_AL'] = pd.Series(writeOff_last3Y_CNT_AL).values
df['writeOff_last3Y_CNT_BL'] = pd.Series(writeOff_last3Y_CNT_BL).values
df['writeOff_last3Y_CNT_CC'] = pd.Series(writeOff_last3Y_CNT_CC).values
df['writeOff_last3Y_CNT_CD'] = pd.Series(writeOff_last3Y_CNT_CD).values
df['writeOff_last3Y_CNT_CV'] = pd.Series(writeOff_last3Y_CNT_CV).values
df['writeOff_last3Y_CNT_GL'] = pd.Series(writeOff_last3Y_CNT_GL).values
df['writeOff_last3Y_CNT_HL'] = pd.Series(writeOff_last3Y_CNT_HL).values
df['writeOff_last3Y_CNT_LAS'] = pd.Series(writeOff_last3Y_CNT_LAS).values
df['writeOff_last3Y_CNT_MFBL'] = pd.Series(writeOff_last3Y_CNT_MFBL).values
df['writeOff_last3Y_CNT_MFHL'] = pd.Series(writeOff_last3Y_CNT_MFHL).values
df['writeOff_last3Y_CNT_MFOT'] = pd.Series(writeOff_last3Y_CNT_MFOT).values
df['writeOff_last3Y_CNT_OTH'] = pd.Series(writeOff_last3Y_CNT_OTH).values
df['writeOff_last3Y_CNT_PL'] = pd.Series(writeOff_last3Y_CNT_PL).values
df['writeOff_last3Y_CNT_PLBL'] = pd.Series(writeOff_last3Y_CNT_PLBL).values
df['writeOff_last3Y_CNT_RL'] = pd.Series(writeOff_last3Y_CNT_RL).values
df['writeOff_last3Y_CNT_SCC'] = pd.Series(writeOff_last3Y_CNT_SCC).values
df['writeOff_last3Y_CNT_SEL'] = pd.Series(writeOff_last3Y_CNT_SEL).values

df['writeOff_last1Y_PLT1K_CNT'] = pd.Series(writeOff_last1Y_PLT1K_CNT).values
df['writeOff_last2Y_PLT1K_CNT'] = pd.Series(writeOff_last2Y_PLT1K_CNT).values
df['writeOff_last3Y_PLT1K_CNT'] = pd.Series(writeOff_last3Y_PLT1K_CNT).values

df['opened_last3M_CNT'] = pd.Series(opened_last3M_CNT).values

df['opened_last3M_CNT_AL'] = pd.Series(opened_last3M_CNT_AL).values
df['opened_last3M_CNT_BL'] = pd.Series(opened_last3M_CNT_BL).values
df['opened_last3M_CNT_CC'] = pd.Series(opened_last3M_CNT_CC).values
df['opened_last3M_CNT_CD'] = pd.Series(opened_last3M_CNT_CD).values
df['opened_last3M_CNT_CV'] = pd.Series(opened_last3M_CNT_CV).values
df['opened_last3M_CNT_GL'] = pd.Series(opened_last3M_CNT_GL).values
df['opened_last3M_CNT_HL'] = pd.Series(opened_last3M_CNT_HL).values
df['opened_last3M_CNT_LAS'] = pd.Series(opened_last3M_CNT_LAS).values
df['opened_last3M_CNT_MFBL'] = pd.Series(opened_last3M_CNT_MFBL).values
df['opened_last3M_CNT_MFHL'] = pd.Series(opened_last3M_CNT_MFHL).values
df['opened_last3M_CNT_MFOT'] = pd.Series(opened_last3M_CNT_MFOT).values
df['opened_last3M_CNT_OTH'] = pd.Series(opened_last3M_CNT_OTH).values
df['opened_last3M_CNT_PL'] = pd.Series(opened_last3M_CNT_PL).values
df['opened_last3M_CNT_PLBL'] = pd.Series(opened_last3M_CNT_PLBL).values
df['opened_last3M_CNT_RL'] = pd.Series(opened_last3M_CNT_RL).values
df['opened_last3M_CNT_SCC'] = pd.Series(opened_last3M_CNT_SCC).values
df['opened_last3M_CNT_SEL'] = pd.Series(opened_last3M_CNT_SEL).values

df['opened_last6M_CNT'] = pd.Series(opened_last6M_CNT).values

df['opened_last6M_CNT_AL'] = pd.Series(opened_last6M_CNT_AL).values
df['opened_last6M_CNT_BL'] = pd.Series(opened_last6M_CNT_BL).values
df['opened_last6M_CNT_CC'] = pd.Series(opened_last6M_CNT_CC).values
df['opened_last6M_CNT_CD'] = pd.Series(opened_last6M_CNT_CD).values
df['opened_last6M_CNT_CV'] = pd.Series(opened_last6M_CNT_CV).values
df['opened_last6M_CNT_GL'] = pd.Series(opened_last6M_CNT_GL).values
df['opened_last6M_CNT_HL'] = pd.Series(opened_last6M_CNT_HL).values
df['opened_last6M_CNT_LAS'] = pd.Series(opened_last6M_CNT_LAS).values
df['opened_last6M_CNT_MFBL'] = pd.Series(opened_last6M_CNT_MFBL).values
df['opened_last6M_CNT_MFHL'] = pd.Series(opened_last6M_CNT_MFHL).values
df['opened_last6M_CNT_MFOT'] = pd.Series(opened_last6M_CNT_MFOT).values
df['opened_last6M_CNT_OTH'] = pd.Series(opened_last6M_CNT_OTH).values
df['opened_last6M_CNT_PL'] = pd.Series(opened_last6M_CNT_PL).values
df['opened_last6M_CNT_PLBL'] = pd.Series(opened_last6M_CNT_PLBL).values
df['opened_last6M_CNT_RL'] = pd.Series(opened_last6M_CNT_RL).values
df['opened_last6M_CNT_SCC'] = pd.Series(opened_last6M_CNT_SCC).values
df['opened_last6M_CNT_SEL'] = pd.Series(opened_last6M_CNT_SEL).values

df['opened_last9M_CNT'] = pd.Series(opened_last9M_CNT).values

df['opened_last9M_CNT_AL'] = pd.Series(opened_last9M_CNT_AL).values
df['opened_last9M_CNT_BL'] = pd.Series(opened_last9M_CNT_BL).values
df['opened_last9M_CNT_CC'] = pd.Series(opened_last9M_CNT_CC).values
df['opened_last9M_CNT_CD'] = pd.Series(opened_last9M_CNT_CD).values
df['opened_last9M_CNT_CV'] = pd.Series(opened_last9M_CNT_CV).values
df['opened_last9M_CNT_GL'] = pd.Series(opened_last9M_CNT_GL).values
df['opened_last9M_CNT_HL'] = pd.Series(opened_last9M_CNT_HL).values
df['opened_last9M_CNT_LAS'] = pd.Series(opened_last9M_CNT_LAS).values
df['opened_last9M_CNT_MFBL'] = pd.Series(opened_last9M_CNT_MFBL).values
df['opened_last9M_CNT_MFHL'] = pd.Series(opened_last9M_CNT_MFHL).values
df['opened_last9M_CNT_MFOT'] = pd.Series(opened_last9M_CNT_MFOT).values
df['opened_last9M_CNT_OTH'] = pd.Series(opened_last9M_CNT_OTH).values
df['opened_last9M_CNT_PL'] = pd.Series(opened_last9M_CNT_PL).values
df['opened_last9M_CNT_PLBL'] = pd.Series(opened_last9M_CNT_PLBL).values
df['opened_last9M_CNT_RL'] = pd.Series(opened_last9M_CNT_RL).values
df['opened_last9M_CNT_SCC'] = pd.Series(opened_last9M_CNT_SCC).values
df['opened_last9M_CNT_SEL'] = pd.Series(opened_last9M_CNT_SEL).values

df['opened_last1Y_CNT'] = pd.Series(opened_last1Y_CNT).values

df['opened_last1Y_CNT_AL'] = pd.Series(opened_last1Y_CNT_AL).values
df['opened_last1Y_CNT_BL'] = pd.Series(opened_last1Y_CNT_BL).values
df['opened_last1Y_CNT_CC'] = pd.Series(opened_last1Y_CNT_CC).values
df['opened_last1Y_CNT_CD'] = pd.Series(opened_last1Y_CNT_CD).values
df['opened_last1Y_CNT_CV'] = pd.Series(opened_last1Y_CNT_CV).values
df['opened_last1Y_CNT_GL'] = pd.Series(opened_last1Y_CNT_GL).values
df['opened_last1Y_CNT_HL'] = pd.Series(opened_last1Y_CNT_HL).values
df['opened_last1Y_CNT_LAS'] = pd.Series(opened_last1Y_CNT_LAS).values
df['opened_last1Y_CNT_MFBL'] = pd.Series(opened_last1Y_CNT_MFBL).values
df['opened_last1Y_CNT_MFHL'] = pd.Series(opened_last1Y_CNT_MFHL).values
df['opened_last1Y_CNT_MFOT'] = pd.Series(opened_last1Y_CNT_MFOT).values
df['opened_last1Y_CNT_OTH'] = pd.Series(opened_last1Y_CNT_OTH).values
df['opened_last1Y_CNT_PL'] = pd.Series(opened_last1Y_CNT_PL).values
df['opened_last1Y_CNT_PLBL'] = pd.Series(opened_last1Y_CNT_PLBL).values
df['opened_last1Y_CNT_RL'] = pd.Series(opened_last1Y_CNT_RL).values
df['opened_last1Y_CNT_SCC'] = pd.Series(opened_last1Y_CNT_SCC).values
df['opened_last1Y_CNT_SEL'] = pd.Series(opened_last1Y_CNT_SEL).values

df['opened_last2Y_CNT'] = pd.Series(opened_last2Y_CNT).values

df['opened_last2Y_CNT_AL'] = pd.Series(opened_last2Y_CNT_AL).values
df['opened_last2Y_CNT_BL'] = pd.Series(opened_last2Y_CNT_BL).values
df['opened_last2Y_CNT_CC'] = pd.Series(opened_last2Y_CNT_CC).values
df['opened_last2Y_CNT_CD'] = pd.Series(opened_last2Y_CNT_CD).values
df['opened_last2Y_CNT_CV'] = pd.Series(opened_last2Y_CNT_CV).values
df['opened_last2Y_CNT_GL'] = pd.Series(opened_last2Y_CNT_GL).values
df['opened_last2Y_CNT_HL'] = pd.Series(opened_last2Y_CNT_HL).values
df['opened_last2Y_CNT_LAS'] = pd.Series(opened_last2Y_CNT_LAS).values
df['opened_last2Y_CNT_MFBL'] = pd.Series(opened_last2Y_CNT_MFBL).values
df['opened_last2Y_CNT_MFHL'] = pd.Series(opened_last2Y_CNT_MFHL).values
df['opened_last2Y_CNT_MFOT'] = pd.Series(opened_last2Y_CNT_MFOT).values
df['opened_last2Y_CNT_OTH'] = pd.Series(opened_last2Y_CNT_OTH).values
df['opened_last2Y_CNT_PL'] = pd.Series(opened_last2Y_CNT_PL).values
df['opened_last2Y_CNT_PLBL'] = pd.Series(opened_last2Y_CNT_PLBL).values
df['opened_last2Y_CNT_RL'] = pd.Series(opened_last2Y_CNT_RL).values
df['opened_last2Y_CNT_SCC'] = pd.Series(opened_last2Y_CNT_SCC).values
df['opened_last2Y_CNT_SEL'] = pd.Series(opened_last2Y_CNT_SEL).values

df['opened_last3Y_CNT'] = pd.Series(opened_last3Y_CNT).values

df['opened_last3Y_CNT_AL'] = pd.Series(opened_last3Y_CNT_AL).values
df['opened_last3Y_CNT_BL'] = pd.Series(opened_last3Y_CNT_BL).values
df['opened_last3Y_CNT_CC'] = pd.Series(opened_last3Y_CNT_CC).values
df['opened_last3Y_CNT_CD'] = pd.Series(opened_last3Y_CNT_CD).values
df['opened_last3Y_CNT_CV'] = pd.Series(opened_last3Y_CNT_CV).values
df['opened_last3Y_CNT_GL'] = pd.Series(opened_last3Y_CNT_GL).values
df['opened_last3Y_CNT_HL'] = pd.Series(opened_last3Y_CNT_HL).values
df['opened_last3Y_CNT_LAS'] = pd.Series(opened_last3Y_CNT_LAS).values
df['opened_last3Y_CNT_MFBL'] = pd.Series(opened_last3Y_CNT_MFBL).values
df['opened_last3Y_CNT_MFHL'] = pd.Series(opened_last3Y_CNT_MFHL).values
df['opened_last3Y_CNT_MFOT'] = pd.Series(opened_last3Y_CNT_MFOT).values
df['opened_last3Y_CNT_OTH'] = pd.Series(opened_last3Y_CNT_OTH).values
df['opened_last3Y_CNT_PL'] = pd.Series(opened_last3Y_CNT_PL).values
df['opened_last3Y_CNT_PLBL'] = pd.Series(opened_last3Y_CNT_PLBL).values
df['opened_last3Y_CNT_RL'] = pd.Series(opened_last3Y_CNT_RL).values
df['opened_last3Y_CNT_SCC'] = pd.Series(opened_last3Y_CNT_SCC).values
df['opened_last3Y_CNT_SEL'] = pd.Series(opened_last3Y_CNT_SEL).values

df['overdueAmount_sum_AL'] = pd.Series(overdueAmount_sum_AL).values
df['overdueAmount_sum_BL'] = pd.Series(overdueAmount_sum_BL).values
df['overdueAmount_sum_CC'] = pd.Series(overdueAmount_sum_CC).values
df['overdueAmount_sum_CD'] = pd.Series(overdueAmount_sum_CD).values
df['overdueAmount_sum_CV'] = pd.Series(overdueAmount_sum_CV).values
df['overdueAmount_sum_GL'] = pd.Series(overdueAmount_sum_GL).values
df['overdueAmount_sum_HL'] = pd.Series(overdueAmount_sum_HL).values
df['overdueAmount_sum_LAS'] = pd.Series(overdueAmount_sum_LAS).values
df['overdueAmount_sum_MFBL'] = pd.Series(overdueAmount_sum_MFBL).values
df['overdueAmount_sum_MFHL'] = pd.Series(overdueAmount_sum_MFHL).values
df['overdueAmount_sum_MFOT'] = pd.Series(overdueAmount_sum_MFOT).values
df['overdueAmount_sum_OTH'] = pd.Series(overdueAmount_sum_OTH).values
df['overdueAmount_sum_PL'] = pd.Series(overdueAmount_sum_PL).values
df['overdueAmount_sum_PLBL'] = pd.Series(overdueAmount_sum_PLBL).values
df['overdueAmount_sum_RL'] = pd.Series(overdueAmount_sum_RL).values
df['overdueAmount_sum_SCC'] = pd.Series(overdueAmount_sum_SCC).values
df['overdueAmount_sum_SEL'] = pd.Series(overdueAmount_sum_SEL).values

df['Overdue_Current_AL'] = pd.Series(Overdue_Current_AL).values
df['Overdue_Current_BL'] = pd.Series(Overdue_Current_BL).values
df['Overdue_Current_CC'] = pd.Series(Overdue_Current_CC).values
df['Overdue_Current_CD'] = pd.Series(Overdue_Current_CD).values
df['Overdue_Current_CV'] = pd.Series(Overdue_Current_CV).values
df['Overdue_Current_GL'] = pd.Series(Overdue_Current_GL).values
df['Overdue_Current_HL'] = pd.Series(Overdue_Current_HL).values
df['Overdue_Current_LAS'] = pd.Series(Overdue_Current_LAS).values
df['Overdue_Current_MFBL'] = pd.Series(Overdue_Current_MFBL).values
df['Overdue_Current_MFHL'] = pd.Series(Overdue_Current_MFHL).values
df['Overdue_Current_MFOT'] = pd.Series(Overdue_Current_MFOT).values
df['Overdue_Current_OTH'] = pd.Series(Overdue_Current_OTH).values
df['Overdue_Current_PL'] = pd.Series(Overdue_Current_PL).values
df['Overdue_Current_PLBL'] = pd.Series(Overdue_Current_PLBL).values
df['Overdue_Current_RL'] = pd.Series(Overdue_Current_RL).values
df['Overdue_Current_SCC'] = pd.Series(Overdue_Current_SCC).values
df['Overdue_Current_SEL'] = pd.Series(Overdue_Current_SEL).values

df['Overdue_Disbursed_AL'] = pd.Series(Overdue_Disbursed_AL).values
df['Overdue_Disbursed_BL'] = pd.Series(Overdue_Disbursed_BL).values
df['Overdue_Disbursed_CC'] = pd.Series(Overdue_Disbursed_CC).values
df['Overdue_Disbursed_CD'] = pd.Series(Overdue_Disbursed_CD).values
df['Overdue_Disbursed_CV'] = pd.Series(Overdue_Disbursed_CV).values
df['Overdue_Disbursed_GL'] = pd.Series(Overdue_Disbursed_GL).values
df['Overdue_Disbursed_HL'] = pd.Series(Overdue_Disbursed_HL).values
df['Overdue_Disbursed_LAS'] = pd.Series(Overdue_Disbursed_LAS).values
df['Overdue_Disbursed_MFBL'] = pd.Series(Overdue_Disbursed_MFBL).values
df['Overdue_Disbursed_MFHL'] = pd.Series(Overdue_Disbursed_MFHL).values
df['Overdue_Disbursed_MFOT'] = pd.Series(Overdue_Disbursed_MFOT).values
df['Overdue_Disbursed_OTH'] = pd.Series(Overdue_Disbursed_OTH).values
df['Overdue_Disbursed_PL'] = pd.Series(Overdue_Disbursed_PL).values
df['Overdue_Disbursed_PLBL'] = pd.Series(Overdue_Disbursed_PLBL).values
df['Overdue_Disbursed_RL'] = pd.Series(Overdue_Disbursed_RL).values
df['Overdue_Disbursed_SCC'] = pd.Series(Overdue_Disbursed_SCC).values
df['Overdue_Disbursed_SEL'] = pd.Series(Overdue_Disbursed_SEL).values

df['dateClosed_lt_PHED_wo_CNT'] = pd.Series(dateClosed_lt_PHED_wo_CNT).values
df['dateClosed_lt_PHED_suit_CNT'] = pd.Series(
    dateClosed_lt_PHED_suit_CNT).values
df['dateClosed_lt_PHED_PH1M_CNT'] = pd.Series(
    dateClosed_lt_PHED_PH1M_CNT).values
df['dateClosed_lt_PHED_restruct_CNT'] = pd.Series(
    dateClosed_lt_PHED_restruct_CNT).values

# Second sequential code
df['dateReportedAndCertified'].fillna('unknown', inplace=True)

mo_diff_ld_drc = list()

WtAvg_SancAmt = list()
WtAvg_SancAmt_L = list()
WAvg_Cur_Bal_L = list()

for x in range(0, df.shape[0]):
    if (df['dateReportedAndCertified'][x] == 'unknown'):
        mo_diff_ld_drc.append(-1)
    elif (df['dateClosed'][x] == 'unknown'):
        mo_diff = diff_month(df['loginDate'][x],
                             df['dateReportedAndCertified'][x])
        mo_diff_ld_drc.append(int(mo_diff))
    elif (df['dateClosed'][x] != 'unknown'):
        mo_diff = diff_month(df['loginDate'][x], df['dateClosed'][x])
        mo_diff_ld_drc.append(int(mo_diff))

    if (df['cnt_grp'][x] == 'unknown') or (df['sanc_amt_grp'][x] == 'unknown'):
        WtAvg_SancAmt.append('unknown')
        WtAvg_SancAmt_L.append('unknown')
    else:
        WtAvg_SancAmt.append(
            df['cnt_grp'][x]*(df['sanc_amt_grp'][x]/df['totAcc'][x]))
        WtAvg_SancAmt_L.append(df['cnt_L_grp_L'][x]
                               * (df['sanc_amt_grp_L'][x]/df['totAcc_L'][x]))

    if (df['cnt_L_grp_L'][x] == 'unknown') or (df['curr_bal_grp_L'][x] == 'unknown'):
        WAvg_Cur_Bal_L.append('unknown')
    else:
        WAvg_Cur_Bal_L.append(df['cnt_L_grp_L'][x] *
                              (df['curr_bal_grp_L'][x]/df['totAcc_L'][x]))

df['mo_diff_ld_drc'] = pd.Series(mo_diff_ld_drc).values
df['WtAvg_SancAmt'] = pd.Series(WtAvg_SancAmt).values
df['WtAvg_SancAmt_L'] = pd.Series(WtAvg_SancAmt_L).values
df['WAvg_Cur_Bal_L'] = pd.Series(WAvg_Cur_Bal_L).values

# Third sequential code
util_CC_L = list()
ratio_list_util_cc_l = list()
ratio_util_cc_l = 0

util_highCredit_CC_L = list()
ratio_list_util_hi_cred = list()
ratio_util_hi_cred = 0

util_highCredit_CC_A = list()
ratio_list_util_hi_cr_a = list()
ratio_util_hi_cr_a = 0

Secured_Unsecured_CNT = list()

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    # print(grp_slice)
    grp_slice.reset_index(drop=True, inplace=True)

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            continue
        else:
            ratio_util_cc_l = float(
                grp_slice['sumCurrentBalance'][i])/float(grp_slice['sumCreditLimit'][i])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            continue
        else:
            ratio_util_hi_cred = float(
                grp_slice['sumSanctionAmount'][i])/float(grp_slice['sumCreditLimit'][i])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            continue
        else:
            ratio_util_hi_cr_a = float(
                grp_slice['sumSanctionAmount'][i])/float(grp_slice['sumCreditLimit'][i])

    ratio_list_util_cc_l.append(ratio_util_cc_l)
    ratio_util_cc_l = 0

    ratio_list_util_hi_cred.append(ratio_util_hi_cred)
    ratio_util_hi_cred = 0

    ratio_list_util_hi_cr_a.append(ratio_util_hi_cr_a)
    ratio_util_hi_cr_a = 0

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            util_CC_L.append('unknown')
        else:
            util_CC_L.append(ratio_list_util_cc_l[x])

        if (grp_slice['dateClosed'][i] != 'unknown') or (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            util_highCredit_CC_L.append('unknown')
        else:
            util_highCredit_CC_L.append(ratio_list_util_hi_cred[x])

        if (grp_slice['accountType'][i] != 10) or (grp_slice['sumCreditLimit'][i] == 0):
            util_highCredit_CC_A.append('unknown')
        else:
            util_highCredit_CC_A.append(ratio_list_util_hi_cr_a[x])

        if (df['Secured_CNT'][x] == 'unknown') and (df['Unsecured_CNT'][x] == 'unknown'):
            Secured_Unsecured_CNT.append('unknown')
        elif (df['Secured_CNT'][x] == 'unknown'):
            Secured_Unsecured_CNT.append(df['Unsecured_CNT'][x])
        elif (df['Unsecured_CNT'][x] == 'unknown'):
            Secured_Unsecured_CNT.append(df['Secured_CNT'][x])
        elif (df['Secured_CNT'][x] != 'unknown') and (df['Unsecured_CNT'][x] != 'unknown'):
            Secured_Unsecured_CNT.append(
                df['Secured_CNT'][x] + df['Unsecured_CNT'][x])

df['util_CC_L'] = pd.Series(util_CC_L).values
df['util_highCredit_CC_L'] = pd.Series(util_highCredit_CC_L).values
df['util_highCredit_CC_A'] = pd.Series(util_highCredit_CC_A).values
df['Secured_Unsecured_CNT'] = pd.Series(Secured_Unsecured_CNT).values

# Fourth sequential code
sanc_amt_sec_L_list = list()
sanc_amt_sec_L = list()

sanc_amt_unsec_L_list = list()
sanc_amt_unsec_L = list()

Disb_Sec_UnsecwoRLCC_L = list()

curr_bal_sec_L_list = list()
curr_bal_sec_L = list()

curr_bal_unsec_L_list = list()
curr_bal_unsec_L = list()

Bal_Sec_UnsecwoRLCC_L = list()

grp_df = df.groupby('ID')

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    # print(grp_slice)
    grp_slice.reset_index(drop=True, inplace=True)
    # print(grp_slice.shape[0])

    if grp_slice.shape[0] > 1:
        # print(grp_slice)
        # print('---')
        for i in range(0, grp_slice.shape[0]):
            if grp_slice['accountType'][i] == 'unknown' or grp_slice['sanctionAmount'][i] == 'unknown':
                continue
            elif grp_slice['accountType'][i] in sec_L:
                sanc_amt_sec_L.append(grp_slice['sanctionAmount'][i])
                # print('sec',sanc_amt_sec_L)
            elif grp_slice['accountType'][i] in unsec_L:
                sanc_amt_unsec_L.append(grp_slice['sanctionAmount'][i])
                # print('unsec',sanc_amt_unsec_L)

            if (grp_slice['accountType'][i] == 'unknown') or (grp_slice['currentBalance'][i] == 'unknown') or (grp_slice['currentBalance'][i] < 0):
                continue
            elif grp_slice['accountType'][i] in sec_L:
                curr_bal_sec_L.append(grp_slice['currentBalance'][i])
                # print('sec',curr_bal_sec_L)
            elif grp_slice['accountType'][i] in unsec_L:
                curr_bal_unsec_L.append(grp_slice['currentBalance'][i])

        for i in range(0, grp_slice.shape[0]):
            if sum(sanc_amt_unsec_L) > 0:
                Disb_Sec_UnsecwoRLCC_L.append(
                    sum(sanc_amt_sec_L)/sum(sanc_amt_unsec_L))
                # print('var', Disb_Sec_UnsecwoRLCC_L)
            else:
                Disb_Sec_UnsecwoRLCC_L.append('unknown')
                # print('var', 'unknown')

            if sum(curr_bal_unsec_L) > 0 and (grp_slice['currentBalance'][i] >= 0):
                Bal_Sec_UnsecwoRLCC_L.append(
                    sum(curr_bal_sec_L)/sum(curr_bal_unsec_L))
                # print('var', Bal_Sec_UnsecwoRLCC_L)
            else:
                Bal_Sec_UnsecwoRLCC_L.append('unknown')
                # print('var', 'unknown')

        sanc_amt_sec_L = list()
        sanc_amt_unsec_L = list()

        curr_bal_sec_L = list()
        curr_bal_unsec_L = list()
        # Disb_Sec_UnsecwoRLCC_L = list()

    else:
        Disb_Sec_UnsecwoRLCC_L.append('unknown')
        Bal_Sec_UnsecwoRLCC_L.append('unknown')

df['Disb_Sec_UnsecwoRLCC_L'] = pd.Series(Disb_Sec_UnsecwoRLCC_L).values
df['Bal_Sec_UnsecwoRLCC_L'] = pd.Series(Bal_Sec_UnsecwoRLCC_L).values

# Code for creditLimit_difference
acc_df = df[df['accountType'] == 10]
acc_grp_df = acc_df.groupby('ID')
acc_id_list = list(acc_df['ID'].values)
acc_unq_id_list = get_unique_values(acc_id_list)

creditLimit_difference = list()

for x in range(0, len(acc_unq_id_list)):
    grp_slice = acc_grp_df.get_group(acc_unq_id_list[x])
    grp_slice.reset_index(drop=True, inplace=True)
    if grp_slice.shape[0] > 1:
        for i in range(0, grp_slice.shape[0]):
            if (grp_slice['accountType'][i] == 10):
                if grp_slice['creditLimit'][i] == 'unknown':
                    creditLimit_difference.append('unknown')
                elif (i+1 < grp_slice.shape[0]) and (grp_slice['creditLimit'][i] != 'unknown') and (grp_slice['creditLimit'][i+1] != 'unknown'):
                    creditLimit_difference.append(
                        grp_slice['creditLimit'][i] - grp_slice['creditLimit'][i+1])
                elif (i+1 < grp_slice.shape[0]) and (grp_slice['creditLimit'][i] != 'unknown') and (grp_slice['creditLimit'][i+1] == 'unknown'):
                    creditLimit_difference.append('unknown')
                else:
                    creditLimit_difference.append('unknown')
            else:
                creditLimit_difference.append('unknown')
    else:
        creditLimit_difference.append('unknown')

acc_df['creditLimit_difference'] = pd.Series(creditLimit_difference).values
df = pd.concat([df, acc_df['creditLimit_difference']], axis=1)
df['creditLimit_difference'].fillna('unknown', inplace=True)

# Fifth sequential code
dpd30_1m = list()
dpd60_1m = list()
dpd90_1m = list()

for x in range(0, df.shape[0]):
    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_1m.append('unknown')
        dpd60_1m.append('unknown')
        dpd90_1m.append('unknown')
    elif (hasNumbers(df['payHistComp'][x][0])):
        if (df['mo_diff_ld_drc'][x] == 1) and (int(df['payHistComp'][x][0]) > 0) and (int(df['payHistComp'][x][0]) <= 30):
            dpd30_1m.append(1)
            dpd60_1m.append(0)
            dpd90_1m.append(0)
        elif (df['mo_diff_ld_drc'][x] == 1) and (int(df['payHistComp'][x][0]) > 30) and (int(df['payHistComp'][x][0]) <= 60):
            dpd30_1m.append(0)
            dpd60_1m.append(1)
            dpd90_1m.append(0)
        elif (df['mo_diff_ld_drc'][x] == 1) and (int(df['payHistComp'][x][0]) > 60) and (int(df['payHistComp'][x][0]) <= 90):
            dpd30_1m.append(0)
            dpd60_1m.append(0)
            dpd90_1m.append(1)
        else:
            dpd30_1m.append(0)
            dpd60_1m.append(0)
            dpd90_1m.append(0)
    else:
        dpd30_1m.append(0)
        dpd60_1m.append(0)
        dpd90_1m.append(0)

df['DPD30P1M_flag'] = pd.Series(dpd30_1m).values
df['DPD60P1M_flag'] = pd.Series(dpd60_1m).values
df['DPD90P1M_flag'] = pd.Series(dpd90_1m).values

# Sixth sequential code
DPD30P1M = list()
count_list_30_1m = list()
count_30_1m = 0

DPD60P1M = list()
count_list_60_1m = list()
count_60_1m = 0

DPD90P1M = list()
count_list_90_1m = list()
count_90_1m = 0

DPD30P1M_AL = list()
DPD30P1M_BL = list()
DPD30P1M_CC = list()
DPD30P1M_CD = list()
DPD30P1M_CV = list()
DPD30P1M_GL = list()
DPD30P1M_HL = list()
DPD30P1M_LAS = list()
DPD30P1M_MFBL = list()
DPD30P1M_MFHL = list()
DPD30P1M_MFOT = list()
DPD30P1M_OTH = list()
DPD30P1M_PL = list()
DPD30P1M_PLBL = list()
DPD30P1M_RL = list()
DPD30P1M_SCC = list()
DPD30P1M_SEL = list()

count_30_list_AL = list()
count_30_list_BL = list()
count_30_list_CC = list()
count_30_list_CD = list()
count_30_list_CV = list()
count_30_list_GL = list()
count_30_list_HL = list()
count_30_list_LAS = list()
count_30_list_MFBL = list()
count_30_list_MFHL = list()
count_30_list_MFOT = list()
count_30_list_OTH = list()
count_30_list_PL = list()
count_30_list_PLBL = list()
count_30_list_RL = list()
count_30_list_SCC = list()
count_30_list_SEL = list()

count_30_AL = 0
count_30_BL = 0
count_30_CC = 0
count_30_CD = 0
count_30_CV = 0
count_30_GL = 0
count_30_HL = 0
count_30_LAS = 0
count_30_MFBL = 0
count_30_MFHL = 0
count_30_MFOT = 0
count_30_OTH = 0
count_30_PL = 0
count_30_PLBL = 0
count_30_RL = 0
count_30_SCC = 0
count_30_SEL = 0

DPD60P1M_AL = list()
DPD60P1M_BL = list()
DPD60P1M_CC = list()
DPD60P1M_CD = list()
DPD60P1M_CV = list()
DPD60P1M_GL = list()
DPD60P1M_HL = list()
DPD60P1M_LAS = list()
DPD60P1M_MFBL = list()
DPD60P1M_MFHL = list()
DPD60P1M_MFOT = list()
DPD60P1M_OTH = list()
DPD60P1M_PL = list()
DPD60P1M_PLBL = list()
DPD60P1M_RL = list()
DPD60P1M_SCC = list()
DPD60P1M_SEL = list()

count_60_list_AL = list()
count_60_list_BL = list()
count_60_list_CC = list()
count_60_list_CD = list()
count_60_list_CV = list()
count_60_list_GL = list()
count_60_list_HL = list()
count_60_list_LAS = list()
count_60_list_MFBL = list()
count_60_list_MFHL = list()
count_60_list_MFOT = list()
count_60_list_OTH = list()
count_60_list_PL = list()
count_60_list_PLBL = list()
count_60_list_RL = list()
count_60_list_SCC = list()
count_60_list_SEL = list()

count_60_AL = 0
count_60_BL = 0
count_60_CC = 0
count_60_CD = 0
count_60_CV = 0
count_60_GL = 0
count_60_HL = 0
count_60_LAS = 0
count_60_MFBL = 0
count_60_MFHL = 0
count_60_MFOT = 0
count_60_OTH = 0
count_60_PL = 0
count_60_PLBL = 0
count_60_RL = 0
count_60_SCC = 0
count_60_SEL = 0

DPD90P1M_AL = list()
DPD90P1M_BL = list()
DPD90P1M_CC = list()
DPD90P1M_CD = list()
DPD90P1M_CV = list()
DPD90P1M_GL = list()
DPD90P1M_HL = list()
DPD90P1M_LAS = list()
DPD90P1M_MFBL = list()
DPD90P1M_MFHL = list()
DPD90P1M_MFOT = list()
DPD90P1M_OTH = list()
DPD90P1M_PL = list()
DPD90P1M_PLBL = list()
DPD90P1M_RL = list()
DPD90P1M_SCC = list()
DPD90P1M_SEL = list()

count_90_list_AL = list()
count_90_list_BL = list()
count_90_list_CC = list()
count_90_list_CD = list()
count_90_list_CV = list()
count_90_list_GL = list()
count_90_list_HL = list()
count_90_list_LAS = list()
count_90_list_MFBL = list()
count_90_list_MFHL = list()
count_90_list_MFOT = list()
count_90_list_OTH = list()
count_90_list_PL = list()
count_90_list_PLBL = list()
count_90_list_RL = list()
count_90_list_SCC = list()
count_90_list_SEL = list()

count_90_AL = 0
count_90_BL = 0
count_90_CC = 0
count_90_CD = 0
count_90_CV = 0
count_90_GL = 0
count_90_HL = 0
count_90_LAS = 0
count_90_MFBL = 0
count_90_MFHL = 0
count_90_MFOT = 0
count_90_OTH = 0
count_90_PL = 0
count_90_PLBL = 0
count_90_RL = 0
count_90_SCC = 0
count_90_SEL = 0

grp_df = df.groupby('ID')

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    # print(grp_slice)
    grp_slice.reset_index(drop=True, inplace=True)
    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['DPD30P1M_flag'][i] == 1) or (grp_slice['DPD30P1M_flag'][i] == 0):
            count_30_1m = count_30_1m + grp_slice['DPD30P1M_flag'][i]

        if (grp_slice['DPD60P1M_flag'][i] == 1) or (grp_slice['DPD60P1M_flag'][i] == 0):
            count_60_1m = count_60_1m + grp_slice['DPD60P1M_flag'][i]

        if (grp_slice['DPD90P1M_flag'][i] == 1) or (grp_slice['DPD90P1M_flag'][i] == 0):
            count_90_1m = count_90_1m + grp_slice['DPD90P1M_flag'][i]

        if (grp_slice['accountType'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_AL = count_30_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_BL = count_30_BL + 1
        elif (grp_slice['accountType'][i] == 'CC') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_CC = count_30_CC + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_CD = count_30_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_CV = count_30_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_GL = count_30_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_HL = count_30_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_LAS = count_30_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_MFBL = count_30_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_MFHL = count_30_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_MFOT = count_30_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_OTH = count_30_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_PL = count_30_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_PLBL = count_30_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_RL = count_30_RL + 1
        elif (grp_slice['accountType'][i] == 'SCC') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_SCC = count_30_SCC + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['DPD30P1M_flag'][i] == 1):
            count_30_SEL = count_30_SEL + 1

        if (grp_slice['accountType'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_AL = count_60_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_BL = count_60_BL + 1
        elif (grp_slice['accountType'][i] == 'CC') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_CC = count_60_CC + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_CD = count_60_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_CV = count_60_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_GL = count_60_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_HL = count_60_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_LAS = count_60_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_MFBL = count_60_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_MFHL = count_60_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_MFOT = count_60_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_OTH = count_60_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_PL = count_60_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_PLBL = count_60_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_RL = count_60_RL + 1
        elif (grp_slice['accountType'][i] == 'SCC') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_SCC = count_60_SCC + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['DPD60P1M_flag'][i] == 1):
            count_60_SEL = count_60_SEL + 1

        if (grp_slice['accountType'][i] == 'unknown'):
            continue
        elif (grp_slice['accountType'][i] == 'AL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_AL = count_90_AL + 1
        elif (grp_slice['accountType'][i] == 'BL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_BL = count_90_BL + 1
        elif (grp_slice['accountType'][i] == 'CC') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_CC = count_90_CC + 1
        elif (grp_slice['accountType'][i] == 'CD') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_CD = count_90_CD + 1
        elif (grp_slice['accountType'][i] == 'CV') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_CV = count_90_CV + 1
        elif (grp_slice['accountType'][i] == 'GL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_GL = count_90_GL + 1
        elif (grp_slice['accountType'][i] == 'HL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_HL = count_90_HL + 1
        elif (grp_slice['accountType'][i] == 'LAS') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_LAS = count_90_LAS + 1
        elif (grp_slice['accountType'][i] == 'MFBL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_MFBL = count_90_MFBL + 1
        elif (grp_slice['accountType'][i] == 'MFHL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_MFHL = count_90_MFHL + 1
        elif (grp_slice['accountType'][i] == 'MFOT') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_MFOT = count_90_MFOT + 1
        elif (grp_slice['accountType'][i] == 'OTH') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_OTH = count_90_OTH + 1
        elif (grp_slice['accountType'][i] == 'PL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_PL = count_90_PL + 1
        elif (grp_slice['accountType'][i] == 'PLBL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_PLBL = count_90_PLBL + 1
        elif (grp_slice['accountType'][i] == 'RL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_RL = count_90_RL + 1
        elif (grp_slice['accountType'][i] == 'SCC') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_SCC = count_90_SCC + 1
        elif (grp_slice['accountType'][i] == 'SEL') and (grp_slice['DPD90P1M_flag'][i] == 1):
            count_90_SEL = count_90_SEL + 1

    count_list_30_1m.append(count_30_1m)
    count_30_1m = 0
    count_list_60_1m.append(count_60_1m)
    count_60_1m = 0
    count_list_90_1m.append(count_90_1m)
    count_90_1m = 0

    count_30_list_AL.append(count_30_AL)
    count_30_list_BL.append(count_30_BL)
    count_30_list_CC.append(count_30_CC)
    count_30_list_CD.append(count_30_CD)
    count_30_list_CV.append(count_30_CV)
    count_30_list_GL.append(count_30_GL)
    count_30_list_HL.append(count_30_HL)
    count_30_list_LAS.append(count_30_LAS)
    count_30_list_MFBL.append(count_30_MFBL)
    count_30_list_MFHL.append(count_30_MFHL)
    count_30_list_MFOT.append(count_30_MFOT)
    count_30_list_OTH.append(count_30_OTH)
    count_30_list_PL.append(count_30_PL)
    count_30_list_PLBL.append(count_30_PLBL)
    count_30_list_RL.append(count_30_RL)
    count_30_list_SCC.append(count_30_SCC)
    count_30_list_SEL.append(count_30_SEL)

    count_30_AL = 0
    count_30_BL = 0
    count_30_CC = 0
    count_30_CD = 0
    count_30_CV = 0
    count_30_GL = 0
    count_30_HL = 0
    count_30_LAS = 0
    count_30_MFBL = 0
    count_30_MFHL = 0
    count_30_MFOT = 0
    count_30_OTH = 0
    count_30_PL = 0
    count_30_PLBL = 0
    count_30_RL = 0
    count_30_SCC = 0
    count_30_SEL = 0

    count_60_list_AL.append(count_60_AL)
    count_60_list_BL.append(count_60_BL)
    count_60_list_CC.append(count_60_CC)
    count_60_list_CD.append(count_60_CD)
    count_60_list_CV.append(count_60_CV)
    count_60_list_GL.append(count_60_GL)
    count_60_list_HL.append(count_60_HL)
    count_60_list_LAS.append(count_60_LAS)
    count_60_list_MFBL.append(count_60_MFBL)
    count_60_list_MFHL.append(count_60_MFHL)
    count_60_list_MFOT.append(count_60_MFOT)
    count_60_list_OTH.append(count_60_OTH)
    count_60_list_PL.append(count_60_PL)
    count_60_list_PLBL.append(count_60_PLBL)
    count_60_list_RL.append(count_60_RL)
    count_60_list_SCC.append(count_60_SCC)
    count_60_list_SEL.append(count_60_SEL)

    count_60_AL = 0
    count_60_BL = 0
    count_60_CC = 0
    count_60_CD = 0
    count_60_CV = 0
    count_60_GL = 0
    count_60_HL = 0
    count_60_LAS = 0
    count_60_MFBL = 0
    count_60_MFHL = 0
    count_60_MFOT = 0
    count_60_OTH = 0
    count_60_PL = 0
    count_60_PLBL = 0
    count_60_RL = 0
    count_60_SCC = 0
    count_60_SEL = 0

    count_90_list_AL.append(count_90_AL)
    count_90_list_BL.append(count_90_BL)
    count_90_list_CC.append(count_90_CC)
    count_90_list_CD.append(count_90_CD)
    count_90_list_CV.append(count_90_CV)
    count_90_list_GL.append(count_90_GL)
    count_90_list_HL.append(count_90_HL)
    count_90_list_LAS.append(count_90_LAS)
    count_90_list_MFBL.append(count_90_MFBL)
    count_90_list_MFHL.append(count_90_MFHL)
    count_90_list_MFOT.append(count_90_MFOT)
    count_90_list_OTH.append(count_90_OTH)
    count_90_list_PL.append(count_90_PL)
    count_90_list_PLBL.append(count_90_PLBL)
    count_90_list_RL.append(count_90_RL)
    count_90_list_SCC.append(count_90_SCC)
    count_90_list_SEL.append(count_90_SEL)

    count_90_AL = 0
    count_90_BL = 0
    count_90_CC = 0
    count_90_CD = 0
    count_90_CV = 0
    count_90_GL = 0
    count_90_HL = 0
    count_90_LAS = 0
    count_90_MFBL = 0
    count_90_MFHL = 0
    count_90_MFOT = 0
    count_90_OTH = 0
    count_90_PL = 0
    count_90_PLBL = 0
    count_90_RL = 0
    count_90_SCC = 0
    count_90_SEL = 0

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['DPD30P1M_flag'][i] == 1) or (grp_slice['DPD30P1M_flag'][i] == 0):
            DPD30P1M.append(count_list_30_1m[x])
        else:
            DPD30P1M.append('unknown')

        if (grp_slice['DPD60P1M_flag'][i] == 1) or (grp_slice['DPD60P1M_flag'][i] == 0):
            DPD60P1M.append(count_list_60_1m[x])
        else:
            DPD60P1M.append('unknown')

        if (grp_slice['DPD90P1M_flag'][i] == 1) or (grp_slice['DPD90P1M_flag'][i] == 0):
            DPD90P1M.append(count_list_90_1m[x])
        else:
            DPD90P1M.append('unknown')

        if (grp_slice['accountType'][i] == 'unknown'):
            DPD30P1M_AL.append('unknown')
            DPD30P1M_BL.append('unknown')
            DPD30P1M_CC.append('unknown')
            DPD30P1M_CD.append('unknown')
            DPD30P1M_CV.append('unknown')
            DPD30P1M_GL.append('unknown')
            DPD30P1M_HL.append('unknown')
            DPD30P1M_LAS.append('unknown')
            DPD30P1M_MFBL.append('unknown')
            DPD30P1M_MFHL.append('unknown')
            DPD30P1M_MFOT.append('unknown')
            DPD30P1M_OTH.append('unknown')
            DPD30P1M_PL.append('unknown')
            DPD30P1M_PLBL.append('unknown')
            DPD30P1M_RL.append('unknown')
            DPD30P1M_SCC.append('unknown')
            DPD30P1M_SEL.append('unknown')

            DPD60P1M_AL.append('unknown')
            DPD60P1M_BL.append('unknown')
            DPD60P1M_CC.append('unknown')
            DPD60P1M_CD.append('unknown')
            DPD60P1M_CV.append('unknown')
            DPD60P1M_GL.append('unknown')
            DPD60P1M_HL.append('unknown')
            DPD60P1M_LAS.append('unknown')
            DPD60P1M_MFBL.append('unknown')
            DPD60P1M_MFHL.append('unknown')
            DPD60P1M_MFOT.append('unknown')
            DPD60P1M_OTH.append('unknown')
            DPD60P1M_PL.append('unknown')
            DPD60P1M_PLBL.append('unknown')
            DPD60P1M_RL.append('unknown')
            DPD60P1M_SCC.append('unknown')
            DPD60P1M_SEL.append('unknown')

            DPD90P1M_AL.append('unknown')
            DPD90P1M_BL.append('unknown')
            DPD90P1M_CC.append('unknown')
            DPD90P1M_CD.append('unknown')
            DPD90P1M_CV.append('unknown')
            DPD90P1M_GL.append('unknown')
            DPD90P1M_HL.append('unknown')
            DPD90P1M_LAS.append('unknown')
            DPD90P1M_MFBL.append('unknown')
            DPD90P1M_MFHL.append('unknown')
            DPD90P1M_MFOT.append('unknown')
            DPD90P1M_OTH.append('unknown')
            DPD90P1M_PL.append('unknown')
            DPD90P1M_PLBL.append('unknown')
            DPD90P1M_RL.append('unknown')
            DPD90P1M_SCC.append('unknown')
            DPD90P1M_SEL.append('unknown')

        else:
            DPD30P1M_AL.append(count_30_list_AL[x])
            DPD30P1M_BL.append(count_30_list_BL[x])
            DPD30P1M_CC.append(count_30_list_CC[x])
            DPD30P1M_CD.append(count_30_list_CD[x])
            DPD30P1M_CV.append(count_30_list_CV[x])
            DPD30P1M_GL.append(count_30_list_GL[x])
            DPD30P1M_HL.append(count_30_list_HL[x])
            DPD30P1M_LAS.append(count_30_list_LAS[x])
            DPD30P1M_MFBL.append(count_30_list_MFBL[x])
            DPD30P1M_MFHL.append(count_30_list_MFHL[x])
            DPD30P1M_MFOT.append(count_30_list_MFOT[x])
            DPD30P1M_OTH.append(count_30_list_OTH[x])
            DPD30P1M_PL.append(count_30_list_PL[x])
            DPD30P1M_PLBL.append(count_30_list_PLBL[x])
            DPD30P1M_RL.append(count_30_list_RL[x])
            DPD30P1M_SCC.append(count_30_list_SCC[x])
            DPD30P1M_SEL.append(count_30_list_SEL[x])

            DPD60P1M_AL.append(count_60_list_AL[x])
            DPD60P1M_BL.append(count_60_list_BL[x])
            DPD60P1M_CC.append(count_60_list_CC[x])
            DPD60P1M_CD.append(count_60_list_CD[x])
            DPD60P1M_CV.append(count_60_list_CV[x])
            DPD60P1M_GL.append(count_60_list_GL[x])
            DPD60P1M_HL.append(count_60_list_HL[x])
            DPD60P1M_LAS.append(count_60_list_LAS[x])
            DPD60P1M_MFBL.append(count_60_list_MFBL[x])
            DPD60P1M_MFHL.append(count_60_list_MFHL[x])
            DPD60P1M_MFOT.append(count_60_list_MFOT[x])
            DPD60P1M_OTH.append(count_60_list_OTH[x])
            DPD60P1M_PL.append(count_60_list_PL[x])
            DPD60P1M_PLBL.append(count_60_list_PLBL[x])
            DPD60P1M_RL.append(count_60_list_RL[x])
            DPD60P1M_SCC.append(count_60_list_SCC[x])
            DPD60P1M_SEL.append(count_60_list_SEL[x])

            DPD90P1M_AL.append(count_90_list_AL[x])
            DPD90P1M_BL.append(count_90_list_BL[x])
            DPD90P1M_CC.append(count_90_list_CC[x])
            DPD90P1M_CD.append(count_90_list_CD[x])
            DPD90P1M_CV.append(count_90_list_CV[x])
            DPD90P1M_GL.append(count_90_list_GL[x])
            DPD90P1M_HL.append(count_90_list_HL[x])
            DPD90P1M_LAS.append(count_90_list_LAS[x])
            DPD90P1M_MFBL.append(count_90_list_MFBL[x])
            DPD90P1M_MFHL.append(count_90_list_MFHL[x])
            DPD90P1M_MFOT.append(count_90_list_MFOT[x])
            DPD90P1M_OTH.append(count_90_list_OTH[x])
            DPD90P1M_PL.append(count_90_list_PL[x])
            DPD90P1M_PLBL.append(count_90_list_PLBL[x])
            DPD90P1M_RL.append(count_90_list_RL[x])
            DPD90P1M_SCC.append(count_90_list_SCC[x])
            DPD90P1M_SEL.append(count_90_list_SEL[x])

df['DPD30P1M'] = pd.Series(DPD30P1M).values
df['DPD60P1M'] = pd.Series(DPD60P1M).values
df['DPD90P1M'] = pd.Series(DPD90P1M).values
df['DPD30P1M_AL'] = pd.Series(DPD30P1M_AL).values
df['DPD30P1M_BL'] = pd.Series(DPD30P1M_BL).values
df['DPD30P1M_CC'] = pd.Series(DPD30P1M_CC).values
df['DPD30P1M_CD'] = pd.Series(DPD30P1M_CD).values
df['DPD30P1M_CV'] = pd.Series(DPD30P1M_CV).values
df['DPD30P1M_GL'] = pd.Series(DPD30P1M_GL).values
df['DPD30P1M_HL'] = pd.Series(DPD30P1M_HL).values
df['DPD30P1M_LAS'] = pd.Series(DPD30P1M_LAS).values
df['DPD30P1M_MFBL'] = pd.Series(DPD30P1M_MFBL).values
df['DPD30P1M_MFHL'] = pd.Series(DPD30P1M_MFHL).values
df['DPD30P1M_MFOT'] = pd.Series(DPD30P1M_MFOT).values
df['DPD30P1M_OTH'] = pd.Series(DPD30P1M_OTH).values
df['DPD30P1M_PL'] = pd.Series(DPD30P1M_PL).values
df['DPD30P1M_PLBL'] = pd.Series(DPD30P1M_PLBL).values
df['DPD30P1M_RL'] = pd.Series(DPD30P1M_RL).values
df['DPD30P1M_SCC'] = pd.Series(DPD30P1M_SCC).values
df['DPD30P1M_SEL'] = pd.Series(DPD30P1M_SEL).values
df['DPD60P1M_AL'] = pd.Series(DPD60P1M_AL).values
df['DPD60P1M_BL'] = pd.Series(DPD60P1M_BL).values
df['DPD60P1M_CC'] = pd.Series(DPD60P1M_CC).values
df['DPD60P1M_CD'] = pd.Series(DPD60P1M_CD).values
df['DPD60P1M_CV'] = pd.Series(DPD60P1M_CV).values
df['DPD60P1M_GL'] = pd.Series(DPD60P1M_GL).values
df['DPD60P1M_HL'] = pd.Series(DPD60P1M_HL).values
df['DPD60P1M_LAS'] = pd.Series(DPD60P1M_LAS).values
df['DPD60P1M_MFBL'] = pd.Series(DPD60P1M_MFBL).values
df['DPD60P1M_MFHL'] = pd.Series(DPD60P1M_MFHL).values
df['DPD60P1M_MFOT'] = pd.Series(DPD60P1M_MFOT).values
df['DPD60P1M_OTH'] = pd.Series(DPD60P1M_OTH).values
df['DPD60P1M_PL'] = pd.Series(DPD60P1M_PL).values
df['DPD60P1M_PLBL'] = pd.Series(DPD60P1M_PLBL).values
df['DPD60P1M_RL'] = pd.Series(DPD60P1M_RL).values
df['DPD60P1M_SCC'] = pd.Series(DPD60P1M_SCC).values
df['DPD60P1M_SEL'] = pd.Series(DPD60P1M_SEL).values
df['DPD90P1M_AL'] = pd.Series(DPD90P1M_AL).values
df['DPD90P1M_BL'] = pd.Series(DPD90P1M_BL).values
df['DPD90P1M_CC'] = pd.Series(DPD90P1M_CC).values
df['DPD90P1M_CD'] = pd.Series(DPD90P1M_CD).values
df['DPD90P1M_CV'] = pd.Series(DPD90P1M_CV).values
df['DPD90P1M_GL'] = pd.Series(DPD90P1M_GL).values
df['DPD90P1M_HL'] = pd.Series(DPD90P1M_HL).values
df['DPD90P1M_LAS'] = pd.Series(DPD90P1M_LAS).values
df['DPD90P1M_MFBL'] = pd.Series(DPD90P1M_MFBL).values
df['DPD90P1M_MFHL'] = pd.Series(DPD90P1M_MFHL).values
df['DPD90P1M_MFOT'] = pd.Series(DPD90P1M_MFOT).values
df['DPD90P1M_OTH'] = pd.Series(DPD90P1M_OTH).values
df['DPD90P1M_PL'] = pd.Series(DPD90P1M_PL).values
df['DPD90P1M_PLBL'] = pd.Series(DPD90P1M_PLBL).values
df['DPD90P1M_RL'] = pd.Series(DPD90P1M_RL).values
df['DPD90P1M_SCC'] = pd.Series(DPD90P1M_SCC).values
df['DPD90P1M_SEL'] = pd.Series(DPD90P1M_SEL).values

# Seventh sequential code
intPayHist = list()
intPayHistComp = list()

for x in range(0, df.shape[0]):
    for i in range(0, len(df['payHistComp'][x])):
        if hasNumbers(df['payHistComp'][x][i]):
            a = int(df['payHistComp'][x][i])
            intPayHist.append(a)
        else:
            intPayHist.append(0)

    intPayHistComp.append(intPayHist)
    intPayHist = list()

df['intPayHistComp'] = pd.Series(intPayHistComp).values

# Eight sequential code
dpd30_3m = list()
dpd60_3m = list()
dpd90_3m = list()
matching = list()

dpd30_6m = list()
dpd60_6m = list()
dpd90_6m = list()
matching_6m = list()

dpd30_1y = list()
dpd60_1y = list()
dpd90_1y = list()
matching_1y = list()

dpd30_2y = list()
dpd60_2y = list()
dpd90_2y = list()
matching_2y = list()

dpd30_3y = list()
dpd60_3y = list()
dpd90_3y = list()
matching_3y = list()

std_last1_mon = list()
std_last3_mon_diff = list()
std_last3_mon = list()
std_last6_mon_diff = list()
std_last6_mon = list()
std_last1_yr_diff = list()
std_last1_yr = list()
std_last2_yr_diff = list()
std_last2_yr = list()
std_last3_yr_diff = list()
std_last3_yr = list()
matching_std = list()

sub_last1_mon = list()
sub_last3_mon_diff = list()
sub_last3_mon = list()
sub_last6_mon_diff = list()
sub_last6_mon = list()
sub_last1_yr_diff = list()
sub_last1_yr = list()
sub_last2_yr_diff = list()
sub_last2_yr = list()
sub_last3_yr_diff = list()
sub_last3_yr = list()
matching_sub = list()

dbt_last1_mon = list()
dbt_last3_mon_diff = list()
dbt_last3_mon = list()
dbt_last6_mon_diff = list()
dbt_last6_mon = list()
dbt_last1_yr_diff = list()
dbt_last1_yr = list()
dbt_last2_yr_diff = list()
dbt_last2_yr = list()
dbt_last3_yr_diff = list()
dbt_last3_yr = list()
matching_dbt = list()

los_last1_mon = list()
los_last3_mon_diff = list()
los_last3_mon = list()
los_last6_mon_diff = list()
los_last6_mon = list()
los_last1_yr_diff = list()
los_last1_yr = list()
los_last2_yr_diff = list()
los_last2_yr = list()
los_last3_yr_diff = list()
los_last3_yr = list()
matching_los = list()

xxx_last1_mon = list()
xxx_last3_mon_diff = list()
xxx_last3_mon = list()
xxx_last6_mon_diff = list()
xxx_last6_mon = list()
xxx_last1_yr_diff = list()
xxx_last1_yr = list()
xxx_last2_yr_diff = list()
xxx_last2_yr = list()
xxx_last3_yr_diff = list()
xxx_last3_yr = list()
matching_xxx = list()

sma_last1_mon = list()
sma_last3_mon_diff = list()
sma_last3_mon = list()
sma_last6_mon_diff = list()
sma_last6_mon = list()
sma_last1_yr_diff = list()
sma_last1_yr = list()
sma_last2_yr_diff = list()
sma_last2_yr = list()
sma_last3_yr_diff = list()
sma_last3_yr = list()
matching_sma = list()

DPD1M_flag = list()
DPD3M_flag = list()
DPD6M_flag = list()
DPD1Y_flag = list()

for x in range(0, df.shape[0]):
    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_3m.append('unknown')
        dpd60_3m.append('unknown')
        dpd90_3m.append('unknown')
    elif (df['mo_diff_ld_drc'][x] >= 0) and (df['mo_diff_ld_drc'][x] <= 3):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            a = df['intPayHistComp'][x][i]
            matching.append(a)
        if (sum(matching) > 0) and (sum(matching) <= 30):
            dpd30_3m.append(1)
            dpd60_3m.append(0)
            dpd90_3m.append(0)
        elif (sum(matching) > 30) and (sum(matching) <= 60):
            dpd30_3m.append(0)
            dpd60_3m.append(1)
            dpd90_3m.append(0)
        elif (sum(matching) > 60) and (sum(matching) <= 90):
            dpd30_3m.append(0)
            dpd60_3m.append(0)
            dpd90_3m.append(1)
        else:
            dpd30_3m.append(0)
            dpd60_3m.append(0)
            dpd90_3m.append(0)
    else:
        dpd30_3m.append(0)
        dpd60_3m.append(0)
        dpd90_3m.append(0)

        matching = list()

    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_6m.append('unknown')
        dpd60_6m.append('unknown')
        dpd90_6m.append('unknown')
    elif (df['mo_diff_ld_drc'][x] >= 0) and (df['mo_diff_ld_drc'][x] <= 6):
        if (6-df['mo_diff_ld_drc'][x] <= len(df['intPayHistComp'][x])):
            for i in range(0, 6-df['mo_diff_ld_drc'][x]):
                a = df['intPayHistComp'][x][i]
                matching_6m.append(a)
        else:
            for i in range(0, len(df['intPayHistComp'][x])):
                a = df['intPayHistComp'][x][i]
                matching_6m.append(a)

        if (sum(matching_6m) > 0) and (sum(matching_6m) <= 30):
            dpd30_6m.append(1)
            dpd60_6m.append(0)
            dpd90_6m.append(0)

        elif (sum(matching_6m) > 30) and (sum(matching_6m) <= 60):
            dpd30_6m.append(0)
            dpd60_6m.append(1)
            dpd90_6m.append(0)

        elif (sum(matching_6m) > 60) and (sum(matching_6m) <= 90):
            dpd30_6m.append(0)
            dpd60_6m.append(0)
            dpd90_6m.append(1)

        else:
            dpd30_6m.append(0)
            dpd60_6m.append(0)
            dpd90_6m.append(0)
    else:
        dpd30_6m.append(0)
        dpd60_6m.append(0)
        dpd90_6m.append(0)

        matching_6m = list()

    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_1y.append('unknown')
        dpd60_1y.append('unknown')
        dpd90_1y.append('unknown')
    elif (df['mo_diff_ld_drc'][x] >= 0) and (df['mo_diff_ld_drc'][x] <= 12):
        if (12-df['mo_diff_ld_drc'][x] <= len(df['intPayHistComp'][x])):
            for i in range(0, 12-df['mo_diff_ld_drc'][x]):
                a = df['intPayHistComp'][x][i]
                matching_1y.append(a)
        else:
            for i in range(0, len(df['intPayHistComp'][x])):
                a = df['intPayHistComp'][x][i]
                matching_1y.append(a)

        if (sum(matching_1y) > 0) and (sum(matching_1y) <= 30):
            dpd30_1y.append(1)
            dpd60_1y.append(0)
            dpd90_1y.append(0)

        elif (sum(matching_1y) > 30) and (sum(matching_1y) <= 60):
            dpd30_1y.append(0)
            dpd60_1y.append(1)
            dpd90_1y.append(0)

        elif (sum(matching_1y) > 60) and (sum(matching_1y) <= 90):
            dpd30_1y.append(0)
            dpd60_1y.append(0)
            dpd90_1y.append(1)

        else:
            dpd30_1y.append(0)
            dpd60_1y.append(0)
            dpd90_1y.append(0)
    else:
        dpd30_1y.append(0)
        dpd60_1y.append(0)
        dpd90_1y.append(0)

        matching_1y = list()

    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_2y.append('unknown')
        dpd60_2y.append('unknown')
        dpd90_2y.append('unknown')
    elif (df['mo_diff_ld_drc'][x] >= 0) and (df['mo_diff_ld_drc'][x] <= 24):
        if (24-df['mo_diff_ld_drc'][x] <= len(df['intPayHistComp'][x])):
            for i in range(0, 24-df['mo_diff_ld_drc'][x]):
                a = df['intPayHistComp'][x][i]
                matching_2y.append(a)
        else:
            for i in range(0, len(df['intPayHistComp'][x])):
                a = df['intPayHistComp'][x][i]
                matching_2y.append(a)

        if (sum(matching_2y) > 0) and (sum(matching_2y) <= 30):
            dpd30_2y.append(1)
            dpd60_2y.append(0)
            dpd90_2y.append(0)

        elif (sum(matching_2y) > 30) and (sum(matching_2y) <= 60):
            dpd30_2y.append(0)
            dpd60_2y.append(1)
            dpd90_2y.append(0)

        elif (sum(matching_2y) > 60) and (sum(matching_2y) <= 90):
            dpd30_2y.append(0)
            dpd60_2y.append(0)
            dpd90_2y.append(1)

        else:
            dpd30_2y.append(0)
            dpd60_2y.append(0)
            dpd90_2y.append(0)
    else:
        dpd30_2y.append(0)
        dpd60_2y.append(0)
        dpd90_2y.append(0)

        matching_2y = list()

    if (df['mo_diff_ld_drc'][x] == -1):
        dpd30_3y.append('unknown')
        dpd60_3y.append('unknown')
        dpd90_3y.append('unknown')
    elif (df['mo_diff_ld_drc'][x] >= 0) and (df['mo_diff_ld_drc'][x] <= 36):
        if (36-df['mo_diff_ld_drc'][x] <= len(df['intPayHistComp'][x])):
            for i in range(0, 36-df['mo_diff_ld_drc'][x]):
                a = df['intPayHistComp'][x][i]
                matching_3y.append(a)
        else:
            for i in range(0, len(df['intPayHistComp'][x])):
                a = df['intPayHistComp'][x][i]
                matching_3y.append(a)

        if (sum(matching_3y) > 0) and (sum(matching_3y) <= 30):
            dpd30_3y.append(1)
            dpd60_3y.append(0)
            dpd90_3y.append(0)

        elif (sum(matching_3y) > 30) and (sum(matching_3y) <= 60):
            dpd30_3y.append(0)
            dpd60_3y.append(1)
            dpd90_3y.append(0)

        elif (sum(matching_3y) > 60) and (sum(matching_3y) <= 90):
            dpd30_3y.append(0)
            dpd60_3y.append(0)
            dpd90_3y.append(1)

        else:
            dpd30_3y.append(0)
            dpd60_3y.append(0)
            dpd90_3y.append(0)
    else:
        dpd30_3y.append(0)
        dpd60_3y.append(0)
        dpd90_3y.append(0)

        matching_3y = list()

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'STD'):
        std_last1_mon.append(1)
    else:
        std_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        std_last3_mon_diff.append(1)
    else:
        std_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        std_last6_mon_diff.append(1)
    else:
        std_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        std_last1_yr_diff.append(1)
    else:
        std_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        std_last2_yr_diff.append(1)
    else:
        std_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        std_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        std_last3_yr_diff.append(1)
    else:
        std_last3_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'SUB'):
        sub_last1_mon.append(1)
    else:
        sub_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        sub_last3_mon_diff.append(1)
    else:
        sub_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        sub_last6_mon_diff.append(1)
    else:
        sub_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        sub_last1_yr_diff.append(1)
    else:
        sub_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        sub_last2_yr_diff.append(1)
    else:
        sub_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sub_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        sub_last3_yr_diff.append(1)
    else:
        sub_last3_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'DBT'):
        dbt_last1_mon.append(1)
    else:
        dbt_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        dbt_last3_mon_diff.append(1)
    else:
        dbt_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        dbt_last6_mon_diff.append(1)
    else:
        dbt_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        dbt_last1_yr_diff.append(1)
    else:
        dbt_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        dbt_last2_yr_diff.append(1)
    else:
        dbt_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        dbt_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        dbt_last3_yr_diff.append(1)
    else:
        dbt_last3_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'LOS'):
        los_last1_mon.append(1)
    else:
        los_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        los_last3_mon_diff.append(1)
    else:
        los_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        los_last6_mon_diff.append(1)
    else:
        los_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        los_last1_yr_diff.append(1)
    else:
        los_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        los_last2_yr_diff.append(1)
    else:
        los_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        los_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        los_last3_yr_diff.append(1)
    else:
        los_last3_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'XXX'):
        xxx_last1_mon.append(1)
    else:
        xxx_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        xxx_last3_mon_diff.append(1)
    else:
        xxx_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        xxx_last6_mon_diff.append(1)
    else:
        xxx_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        xxx_last1_yr_diff.append(1)
    else:
        xxx_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        xxx_last2_yr_diff.append(1)
    else:
        xxx_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        xxx_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        xxx_last3_yr_diff.append(1)
    else:
        xxx_last3_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last1_mon.append('unknown')
    elif (df['mo_diff_ld_drc'][x] == 1) and (df['payHistComp'][x][0] == 'SMA'):
        sma_last1_mon.append(1)
    else:
        sma_last1_mon.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last3_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 4):
        sma_last3_mon_diff.append(1)
    else:
        sma_last3_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last6_mon_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 7):
        sma_last6_mon_diff.append(1)
    else:
        sma_last6_mon_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last1_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 13):
        sma_last1_yr_diff.append(1)
    else:
        sma_last1_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last2_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 25):
        sma_last2_yr_diff.append(1)
    else:
        sma_last2_yr_diff.append(0)

    if (df['mo_diff_ld_drc'][x] == -1):
        sma_last3_yr_diff.append('unknown')
    elif (df['mo_diff_ld_drc'][x] > 1) and (df['mo_diff_ld_drc'][x] < 37):
        sma_last3_yr_diff.append(1)
    else:
        sma_last3_yr_diff.append(0)

df['DPD30P3M_flag'] = pd.Series(dpd30_3m).values
df['DPD60P3M_flag'] = pd.Series(dpd60_3m).values
df['DPD90P3M_flag'] = pd.Series(dpd90_3m).values

df['DPD30P6M_flag'] = pd.Series(dpd30_6m).values
df['DPD60P6M_flag'] = pd.Series(dpd60_6m).values
df['DPD90P6M_flag'] = pd.Series(dpd90_6m).values

df['DPD30P1Y_flag'] = pd.Series(dpd30_1y).values
df['DPD60P1Y_flag'] = pd.Series(dpd60_1y).values
df['DPD90P1Y_flag'] = pd.Series(dpd90_1y).values

df['DPD30P2Y_flag'] = pd.Series(dpd30_2y).values
df['DPD60P2Y_flag'] = pd.Series(dpd60_2y).values
df['DPD90P2Y_flag'] = pd.Series(dpd90_2y).values

df['DPD30P3Y_flag'] = pd.Series(dpd30_3y).values
df['DPD60P3Y_flag'] = pd.Series(dpd60_3y).values
df['DPD90P3Y_flag'] = pd.Series(dpd90_3y).values

df['std_last3_mon_diff'] = pd.Series(std_last3_mon_diff).values
df['std_last6_mon_diff'] = pd.Series(std_last6_mon_diff).values
df['std_last1_yr_diff'] = pd.Series(std_last1_yr_diff).values
df['std_last2_yr_diff'] = pd.Series(std_last2_yr_diff).values
df['std_last3_yr_diff'] = pd.Series(std_last3_yr_diff).values

df['sub_last3_mon_diff'] = pd.Series(sub_last3_mon_diff).values
df['sub_last6_mon_diff'] = pd.Series(sub_last6_mon_diff).values
df['sub_last1_yr_diff'] = pd.Series(sub_last1_yr_diff).values
df['sub_last2_yr_diff'] = pd.Series(sub_last2_yr_diff).values
df['sub_last3_yr_diff'] = pd.Series(sub_last3_yr_diff).values

df['dbt_last3_mon_diff'] = pd.Series(dbt_last3_mon_diff).values
df['dbt_last6_mon_diff'] = pd.Series(dbt_last6_mon_diff).values
df['dbt_last1_yr_diff'] = pd.Series(dbt_last1_yr_diff).values
df['dbt_last2_yr_diff'] = pd.Series(dbt_last2_yr_diff).values
df['dbt_last3_yr_diff'] = pd.Series(dbt_last3_yr_diff).values

df['los_last3_mon_diff'] = pd.Series(los_last3_mon_diff).values
df['los_last6_mon_diff'] = pd.Series(los_last6_mon_diff).values
df['los_last1_yr_diff'] = pd.Series(los_last1_yr_diff).values
df['los_last2_yr_diff'] = pd.Series(los_last2_yr_diff).values
df['los_last3_yr_diff'] = pd.Series(los_last3_yr_diff).values

df['xxx_last3_mon_diff'] = pd.Series(xxx_last3_mon_diff).values
df['xxx_last6_mon_diff'] = pd.Series(xxx_last6_mon_diff).values
df['xxx_last1_yr_diff'] = pd.Series(xxx_last1_yr_diff).values
df['xxx_last2_yr_diff'] = pd.Series(xxx_last2_yr_diff).values
df['xxx_last3_yr_diff'] = pd.Series(xxx_last3_yr_diff).values

df['sma_last3_mon_diff'] = pd.Series(sma_last3_mon_diff).values
df['sma_last6_mon_diff'] = pd.Series(sma_last6_mon_diff).values
df['sma_last1_yr_diff'] = pd.Series(sma_last1_yr_diff).values
df['sma_last2_yr_diff'] = pd.Series(sma_last2_yr_diff).values
df['sma_last3_yr_diff'] = pd.Series(sma_last3_yr_diff).values

for x in range(0, df.shape[0]):
    if (df['std_last3_mon_diff'][x] == 'unknown'):
        std_last3_mon.append('unknown')
    elif (df['std_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            matching_std.append(df['payHistComp'][x][i])
        if any('STD' in s for s in matching_std):
            std_last3_mon.append(1)
        else:
            std_last3_mon.append(0)
        matching_std = list()
    else:
        std_last3_mon.append(0)

    if (df['std_last6_mon_diff'][x] == 'unknown'):
        std_last6_mon.append('unknown')
    elif (df['std_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):
            matching_std.append(df['payHistComp'][x][i])
        if any('STD' in s for s in matching_std):
            std_last6_mon.append(1)
        else:
            std_last6_mon.append(0)
        matching_std = list()
    else:
        std_last6_mon.append(0)

    if (df['std_last1_yr_diff'][x] == 'unknown'):
        std_last1_yr.append('unknown')
    elif (df['std_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):
            matching_std.append(df['payHistComp'][x][i])
        if any('STD' in s for s in matching_std):
            std_last1_yr.append(1)
        else:
            std_last1_yr.append(0)
        matching_std = list()
    else:
        std_last1_yr.append(0)

    if (df['std_last2_yr_diff'][x] == 'unknown'):
        std_last2_yr.append('unknown')
    elif (df['std_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):
            matching_std.append(df['payHistComp'][x][i])
        if any('STD' in s for s in matching_std):
            std_last2_yr.append(1)
        else:
            std_last2_yr.append(0)
        matching_std = list()
    else:
        std_last2_yr.append(0)

    if (df['std_last3_yr_diff'][x] == 'unknown'):
        std_last3_yr.append('unknown')
    elif (df['std_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):
            matching_std.append(df['payHistComp'][x][i])
        if any('STD' in s for s in matching_std):
            std_last3_yr.append(1)
        else:
            std_last3_yr.append(0)
        matching_std = list()
    else:
        std_last3_yr.append(0)

    if (df['sub_last3_mon_diff'][x] == 'unknown'):
        sub_last3_mon.append('unknown')
    elif (df['sub_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):

            matching_sub.append(df['payHistComp'][x][i])
        if any('SUB' in s for s in matching_sub):
            sub_last3_mon.append(1)
        else:
            sub_last3_mon.append(0)

        matching_sub = list()
    else:
        sub_last3_mon.append(0)

    if (df['sub_last6_mon_diff'][x] == 'unknown'):
        sub_last6_mon.append('unknown')
    elif (df['sub_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):

            matching_sub.append(df['payHistComp'][x][i])
        if any('SUB' in s for s in matching_sub):
            sub_last6_mon.append(1)
        else:
            sub_last6_mon.append(0)

        matching_sub = list()
    else:
        sub_last6_mon.append(0)

    if (df['sub_last1_yr_diff'][x] == 'unknown'):
        sub_last1_yr.append('unknown')
    elif (df['sub_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):

            matching_sub.append(df['payHistComp'][x][i])
        if any('SUB' in s for s in matching_sub):
            sub_last1_yr.append(1)
        else:
            sub_last1_yr.append(0)

        matching_sub = list()
    else:
        sub_last1_yr.append(0)

    if (df['sub_last2_yr_diff'][x] == 'unknown'):
        sub_last2_yr.append('unknown')
    elif (df['sub_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):

            matching_sub.append(df['payHistComp'][x][i])
        if any('SUB' in s for s in matching_sub):
            sub_last2_yr.append(1)
        else:
            sub_last2_yr.append(0)

        matching_sub = list()
    else:
        sub_last2_yr.append(0)

    if (df['sub_last3_yr_diff'][x] == 'unknown'):
        sub_last3_yr.append('unknown')
    elif (df['sub_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):

            matching_sub.append(df['payHistComp'][x][i])
        if any('SUB' in s for s in matching_sub):
            sub_last3_yr.append(1)
        else:
            sub_last3_yr.append(0)

        matching_sub = list()
    else:
        sub_last3_yr.append(0)

    if (df['dbt_last3_mon_diff'][x] == 'unknown'):
        dbt_last3_mon.append('unknown')
    elif (df['dbt_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            # print(i)
            matching_dbt.append(df['payHistComp'][x][i])
        if any('DBT' in s for s in matching_dbt):
            dbt_last3_mon.append(1)
        else:
            dbt_last3_mon.append(0)
        # print(matching_dbt)
        matching_dbt = list()
    else:
        dbt_last3_mon.append(0)

    if (df['dbt_last6_mon_diff'][x] == 'unknown'):
        dbt_last6_mon.append('unknown')
    elif (df['dbt_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):
            # print(i)
            matching_dbt.append(df['payHistComp'][x][i])
        if any('DBT' in s for s in matching_dbt):
            dbt_last6_mon.append(1)
        else:
            dbt_last6_mon.append(0)
        # print(matching_dbt)
        matching_dbt = list()
    else:
        dbt_last6_mon.append(0)

    if (df['dbt_last1_yr_diff'][x] == 'unknown'):
        dbt_last1_yr.append('unknown')
    elif (df['dbt_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):
            # print(i)
            matching_dbt.append(df['payHistComp'][x][i])
        if any('DBT' in s for s in matching_dbt):
            dbt_last1_yr.append(1)
        else:
            dbt_last1_yr.append(0)
        matching_dbt = list()
    else:
        dbt_last1_yr.append(0)

    if (df['dbt_last2_yr_diff'][x] == 'unknown'):
        dbt_last2_yr.append('unknown')
    elif (df['dbt_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):
            # print(i)
            matching_dbt.append(df['payHistComp'][x][i])
        if any('DBT' in s for s in matching_dbt):
            dbt_last2_yr.append(1)
        else:
            dbt_last2_yr.append(0)
        # print(matching_dbt)
        matching_dbt = list()
    else:
        dbt_last2_yr.append(0)

    if (df['dbt_last3_yr_diff'][x] == 'unknown'):
        dbt_last3_yr.append('unknown')
    elif (df['dbt_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):
            # print(i)
            matching_dbt.append(df['payHistComp'][x][i])
        if any('DBT' in s for s in matching_dbt):
            dbt_last3_yr.append(1)
        else:
            dbt_last3_yr.append(0)
        # print(matching_dbt)
        matching_dbt = list()
    else:
        dbt_last3_yr.append(0)

    if (df['los_last3_mon_diff'][x] == 'unknown'):
        los_last3_mon.append('unknown')
    elif (df['los_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            matching_los.append(df['payHistComp'][x][i])
        if any('LOS' in s for s in matching_los):
            los_last3_mon.append(1)
        else:
            los_last3_mon.append(0)
        matching_los = list()
    else:
        los_last3_mon.append(0)

    if (df['los_last6_mon_diff'][x] == 'unknown'):
        los_last6_mon.append('unknown')
    elif (df['los_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):
            matching_los.append(df['payHistComp'][x][i])
        if any('LOS' in s for s in matching_los):
            los_last6_mon.append(1)
        else:
            los_last6_mon.append(0)
        matching_los = list()
    else:
        los_last6_mon.append(0)

    if (df['los_last1_yr_diff'][x] == 'unknown'):
        los_last1_yr.append('unknown')
    elif (df['los_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):
            matching_los.append(df['payHistComp'][x][i])
        if any('LOS' in s for s in matching_los):
            los_last1_yr.append(1)
        else:
            los_last1_yr.append(0)
        matching_los = list()
    else:
        los_last1_yr.append(0)

    if (df['los_last2_yr_diff'][x] == 'unknown'):
        los_last2_yr.append('unknown')
    elif (df['los_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):
            matching_los.append(df['payHistComp'][x][i])
        if any('LOS' in s for s in matching_los):
            los_last2_yr.append(1)
        else:
            los_last2_yr.append(0)
        matching_los = list()
    else:
        los_last2_yr.append(0)

    if (df['los_last3_yr_diff'][x] == 'unknown'):
        los_last3_yr.append('unknown')
    elif (df['los_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):
            matching_los.append(df['payHistComp'][x][i])
        if any('LOS' in s for s in matching_los):
            los_last3_yr.append(1)
        else:
            los_last3_yr.append(0)
        matching_los = list()
    else:
        los_last3_yr.append(0)

    if (df['xxx_last3_mon_diff'][x] == 'unknown'):
        xxx_last3_mon.append('unknown')
    elif (df['xxx_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            matching_xxx.append(df['payHistComp'][x][i])
        if any('XXX' in s for s in matching_xxx):
            xxx_last3_mon.append(1)
        else:
            xxx_last3_mon.append(0)
        matching_xxx = list()
    else:
        xxx_last3_mon.append(0)

    if (df['xxx_last6_mon_diff'][x] == 'unknown'):
        xxx_last6_mon.append('unknown')
    elif (df['xxx_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):
            matching_xxx.append(df['payHistComp'][x][i])
        if any('XXX' in s for s in matching_xxx):
            xxx_last6_mon.append(1)
        else:
            xxx_last6_mon.append(0)
        matching_xxx = list()
    else:
        xxx_last6_mon.append(0)

    if (df['xxx_last1_yr_diff'][x] == 'unknown'):
        xxx_last1_yr.append('unknown')
    elif (df['xxx_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):
            matching_xxx.append(df['payHistComp'][x][i])
        if any('XXX' in s for s in matching_xxx):
            xxx_last1_yr.append(1)
        else:
            xxx_last1_yr.append(0)
        matching_xxx = list()
    else:
        xxx_last1_yr.append(0)

    if (df['xxx_last2_yr_diff'][x] == 'unknown'):
        xxx_last2_yr.append('unknown')
    elif (df['xxx_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):
            matching_xxx.append(df['payHistComp'][x][i])
        if any('XXX' in s for s in matching_xxx):
            xxx_last2_yr.append(1)
        else:
            xxx_last2_yr.append(0)
        matching_xxx = list()
    else:
        xxx_last2_yr.append(0)

    if (df['xxx_last3_yr_diff'][x] == 'unknown'):
        xxx_last3_yr.append('unknown')
    elif (df['xxx_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):
            matching_xxx.append(df['payHistComp'][x][i])
        if any('XXX' in s for s in matching_xxx):
            xxx_last3_yr.append(1)
        else:
            xxx_last3_yr.append(0)
        matching_xxx = list()
    else:
        xxx_last3_yr.append(0)

    if (df['sma_last3_mon_diff'][x] == 'unknown'):
        sma_last3_mon.append('unknown')
    elif (df['sma_last3_mon_diff'][x] == 1):
        for i in range(0, 3-df['mo_diff_ld_drc'][x]):
            matching_sma.append(df['payHistComp'][x][i])
        if any('SMA' in s for s in matching_sma):
            sma_last3_mon.append(1)
        else:
            sma_last3_mon.append(0)
        matching_sma = list()
    else:
        sma_last3_mon.append(0)

    if (df['sma_last6_mon_diff'][x] == 'unknown'):
        sma_last6_mon.append('unknown')
    elif (df['sma_last6_mon_diff'][x] == 1):
        for i in range(0, 6-df['mo_diff_ld_drc'][x]):
            matching_sma.append(df['payHistComp'][x][i])
        if any('SMA' in s for s in matching_sma):
            sma_last6_mon.append(1)
        else:
            sma_last6_mon.append(0)
        matching_sma = list()
    else:
        sma_last6_mon.append(0)

    if (df['sma_last1_yr_diff'][x] == 'unknown'):
        sma_last1_yr.append('unknown')
    elif (df['sma_last1_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 12):
        for i in range(0, 12-df['mo_diff_ld_drc'][x]):
            matching_sma.append(df['payHistComp'][x][i])
        if any('SMA' in s for s in matching_sma):
            sma_last1_yr.append(1)
        else:
            sma_last1_yr.append(0)
        matching_sma = list()
    else:
        sma_last1_yr.append(0)

    if (df['sma_last2_yr_diff'][x] == 'unknown'):
        sma_last2_yr.append('unknown')
    elif (df['sma_last2_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) >= 24):
        for i in range(0, 24-df['mo_diff_ld_drc'][x]):
            matching_sma.append(df['payHistComp'][x][i])
        if any('SMA' in s for s in matching_sma):
            sma_last2_yr.append(1)
        else:
            sma_last2_yr.append(0)
        matching_sma = list()
    else:
        sma_last2_yr.append(0)

    if (df['sma_last3_yr_diff'][x] == 'unknown'):
        sma_last3_yr.append('unknown')
    elif (df['sma_last3_yr_diff'][x] == 1) and (len(df['payHistComp'][x]) == 36):
        for i in range(0, 36-df['mo_diff_ld_drc'][x]):
            matching_sma.append(df['payHistComp'][x][i])
        if any('SMA' in s for s in matching_sma):
            sma_last3_yr.append(1)
        else:
            sma_last3_yr.append(0)
        matching_sma = list()
    else:
        sma_last3_yr.append(0)

    if (df['DPD30P1M_flag'][x] == 1) or (df['DPD60P1M_flag'][x] == 1) or (df['DPD90P1M_flag'][x] == 1):
        DPD1M_flag.append(1)
    elif (df['DPD30P1M_flag'][x] == 'unknown') or (df['DPD60P1M_flag'][x] == 'unknown') or (df['DPD90P1M_flag'][x] == 'unknown'):
        DPD1M_flag.append('unknown')
    else:
        DPD1M_flag.append(0)

    if (df['DPD30P3M_flag'][x] == 1) or (df['DPD60P3M_flag'][x] == 1) or (df['DPD90P3M_flag'][x] == 1):
        DPD3M_flag.append(1)
    elif (df['DPD30P3M_flag'][x] == 'unknown') or (df['DPD60P3M_flag'][x] == 'unknown') or (df['DPD90P3M_flag'][x] == 'unknown'):
        DPD3M_flag.append('unknown')
    else:
        DPD3M_flag.append(0)

    if (df['DPD30P6M_flag'][x] == 1) or (df['DPD60P6M_flag'][x] == 1) or (df['DPD90P6M_flag'][x] == 1):
        DPD6M_flag.append(1)
    elif (df['DPD30P6M_flag'][x] == 'unknown') or (df['DPD60P6M_flag'][x] == 'unknown') or (df['DPD90P6M_flag'][x] == 'unknown'):
        DPD6M_flag.append('unknown')
    else:
        DPD6M_flag.append(0)

    if (df['DPD30P1Y_flag'][x] == 1) or (df['DPD60P1Y_flag'][x] == 1) or (df['DPD90P1Y_flag'][x] == 1):
        DPD1Y_flag.append(1)
    elif (df['DPD30P1Y_flag'][x] == 'unknown') or (df['DPD60P1Y_flag'][x] == 'unknown') or (df['DPD90P1Y_flag'][x] == 'unknown'):
        DPD1Y_flag.append('unknown')
    else:
        DPD1Y_flag.append(0)

df['STD1M_flag'] = pd.Series(std_last1_mon).values
df['STD3M_flag'] = pd.Series(std_last3_mon).values
df['STD6M_flag'] = pd.Series(std_last6_mon).values
df['STD1Y_flag'] = pd.Series(std_last1_yr).values
df['STD2Y_flag'] = pd.Series(std_last2_yr).values
df['STD3Y_flag'] = pd.Series(std_last3_yr).values

df['SUB1M_flag'] = pd.Series(sub_last1_mon).values
df['SUB3M_flag'] = pd.Series(sub_last3_mon).values
df['SUB6M_flag'] = pd.Series(sub_last6_mon).values
df['SUB1Y_flag'] = pd.Series(sub_last1_yr).values
df['SUB2Y_flag'] = pd.Series(sub_last2_yr).values
df['SUB3Y_flag'] = pd.Series(sub_last3_yr).values

df['DBT1M_flag'] = pd.Series(dbt_last1_mon).values
df['DBT3M_flag'] = pd.Series(dbt_last3_mon).values
df['DBT6M_flag'] = pd.Series(dbt_last6_mon).values
df['DBT1Y_flag'] = pd.Series(dbt_last1_yr).values
df['DBT2Y_flag'] = pd.Series(dbt_last2_yr).values
df['DBT3Y_flag'] = pd.Series(dbt_last3_yr).values

df['LOS1M_flag'] = pd.Series(los_last1_mon).values
df['LOS3M_flag'] = pd.Series(los_last3_mon).values
df['LOS6M_flag'] = pd.Series(los_last6_mon).values
df['LOS1Y_flag'] = pd.Series(los_last1_yr).values
df['LOS2Y_flag'] = pd.Series(los_last2_yr).values
df['LOS3Y_flag'] = pd.Series(los_last3_yr).values

df['XXX1M_flag'] = pd.Series(xxx_last1_mon).values
df['XXX3M_flag'] = pd.Series(xxx_last3_mon).values
df['XXX6M_flag'] = pd.Series(xxx_last6_mon).values
df['XXX1Y_flag'] = pd.Series(xxx_last1_yr).values
df['XXX2Y_flag'] = pd.Series(xxx_last2_yr).values
df['XXX3Y_flag'] = pd.Series(xxx_last3_yr).values

df['SMA1M_flag'] = pd.Series(sma_last1_mon).values
df['SMA3M_flag'] = pd.Series(sma_last3_mon).values
df['SMA6M_flag'] = pd.Series(sma_last6_mon).values
df['SMA1Y_flag'] = pd.Series(sma_last1_yr).values
df['SMA2Y_flag'] = pd.Series(sma_last2_yr).values
df['SMA3Y_flag'] = pd.Series(sma_last3_yr).values

df['DPD1M_flag'] = pd.Series(DPD1M_flag).values
df['DPD3M_flag'] = pd.Series(DPD3M_flag).values
df['DPD6M_flag'] = pd.Series(DPD6M_flag).values
df['DPD1Y_flag'] = pd.Series(DPD1Y_flag).values

# Ninth sequential code
DPD30P3M = list()
count_list_30_3m = list()
count_30_3m = 0

DPD60P3M = list()
count_list_60_3m = list()
count_60_3m = 0

DPD90P3M = list()
count_list_90_3m = list()
count_90_3m = 0

DPD30P6M = list()
count_list_30_6m = list()
count_30_6m = 0

DPD60P6M = list()
count_list_60_6m = list()
count_60_6m = 0

DPD90P6M = list()
count_list_90_6m = list()
count_90_6m = 0

DPD30P1Y = list()
count_list_30_1y = list()
count_30_1y = 0

DPD60P1Y = list()
count_list_60_1y = list()
count_60_1y = 0

DPD90P1Y = list()
count_list_90_1y = list()
count_90_1y = 0

DPD30P2Y = list()
count_list_30_2y = list()
count_30_2y = 0

DPD60P2Y = list()
count_list_60_2y = list()
count_60_2y = 0

DPD90P2Y = list()
count_list_90_2y = list()
count_90_2y = 0

DPD30P3Y = list()
count_list_30_3y = list()
count_30_3y = 0

DPD60P3Y = list()
count_list_60_3y = list()
count_60_3y = 0

DPD90P3Y = list()
count_list_90_3y = list()
count_90_3y = 0

DPD30P3M_AL = list()
DPD30P3M_BL = list()
DPD30P3M_CC = list()
DPD30P3M_CD = list()
DPD30P3M_CV = list()
DPD30P3M_GL = list()
DPD30P3M_HL = list()
DPD30P3M_LAS = list()
DPD30P3M_MFBL = list()
DPD30P3M_MFHL = list()
DPD30P3M_MFOT = list()
DPD30P3M_OTH = list()
DPD30P3M_PL = list()
DPD30P3M_PLBL = list()
DPD30P3M_RL = list()
DPD30P3M_SCC = list()
DPD30P3M_SEL = list()

count_30_3m_list_AL = list()
count_30_3m_list_BL = list()
count_30_3m_list_CC = list()
count_30_3m_list_CD = list()
count_30_3m_list_CV = list()
count_30_3m_list_GL = list()
count_30_3m_list_HL = list()
count_30_3m_list_LAS = list()
count_30_3m_list_MFBL = list()
count_30_3m_list_MFHL = list()
count_30_3m_list_MFOT = list()
count_30_3m_list_OTH = list()
count_30_3m_list_PL = list()
count_30_3m_list_PLBL = list()
count_30_3m_list_RL = list()
count_30_3m_list_SCC = list()
count_30_3m_list_SEL = list()

count_30_3m_AL = 0
count_30_3m_BL = 0
count_30_3m_CC = 0
count_30_3m_CD = 0
count_30_3m_CV = 0
count_30_3m_GL = 0
count_30_3m_HL = 0
count_30_3m_LAS = 0
count_30_3m_MFBL = 0
count_30_3m_MFHL = 0
count_30_3m_MFOT = 0
count_30_3m_OTH = 0
count_30_3m_PL = 0
count_30_3m_PLBL = 0
count_30_3m_RL = 0
count_30_3m_SCC = 0
count_30_3m_SEL = 0

DPD60P3M_AL = list()
DPD60P3M_BL = list()
DPD60P3M_CC = list()
DPD60P3M_CD = list()
DPD60P3M_CV = list()
DPD60P3M_GL = list()
DPD60P3M_HL = list()
DPD60P3M_LAS = list()
DPD60P3M_MFBL = list()
DPD60P3M_MFHL = list()
DPD60P3M_MFOT = list()
DPD60P3M_OTH = list()
DPD60P3M_PL = list()
DPD60P3M_PLBL = list()
DPD60P3M_RL = list()
DPD60P3M_SCC = list()
DPD60P3M_SEL = list()

count_60_3m_list_AL = list()
count_60_3m_list_BL = list()
count_60_3m_list_CC = list()
count_60_3m_list_CD = list()
count_60_3m_list_CV = list()
count_60_3m_list_GL = list()
count_60_3m_list_HL = list()
count_60_3m_list_LAS = list()
count_60_3m_list_MFBL = list()
count_60_3m_list_MFHL = list()
count_60_3m_list_MFOT = list()
count_60_3m_list_OTH = list()
count_60_3m_list_PL = list()
count_60_3m_list_PLBL = list()
count_60_3m_list_RL = list()
count_60_3m_list_SCC = list()
count_60_3m_list_SEL = list()

count_60_3m_AL = 0
count_60_3m_BL = 0
count_60_3m_CC = 0
count_60_3m_CD = 0
count_60_3m_CV = 0
count_60_3m_GL = 0
count_60_3m_HL = 0
count_60_3m_LAS = 0
count_60_3m_MFBL = 0
count_60_3m_MFHL = 0
count_60_3m_MFOT = 0
count_60_3m_OTH = 0
count_60_3m_PL = 0
count_60_3m_PLBL = 0
count_60_3m_RL = 0
count_60_3m_SCC = 0
count_60_3m_SEL = 0

DPD90P3M_AL = list()
DPD90P3M_BL = list()
DPD90P3M_CC = list()
DPD90P3M_CD = list()
DPD90P3M_CV = list()
DPD90P3M_GL = list()
DPD90P3M_HL = list()
DPD90P3M_LAS = list()
DPD90P3M_MFBL = list()
DPD90P3M_MFHL = list()
DPD90P3M_MFOT = list()
DPD90P3M_OTH = list()
DPD90P3M_PL = list()
DPD90P3M_PLBL = list()
DPD90P3M_RL = list()
DPD90P3M_SCC = list()
DPD90P3M_SEL = list()

count_90_3m_list_AL = list()
count_90_3m_list_BL = list()
count_90_3m_list_CC = list()
count_90_3m_list_CD = list()
count_90_3m_list_CV = list()
count_90_3m_list_GL = list()
count_90_3m_list_HL = list()
count_90_3m_list_LAS = list()
count_90_3m_list_MFBL = list()
count_90_3m_list_MFHL = list()
count_90_3m_list_MFOT = list()
count_90_3m_list_OTH = list()
count_90_3m_list_PL = list()
count_90_3m_list_PLBL = list()
count_90_3m_list_RL = list()
count_90_3m_list_SCC = list()
count_90_3m_list_SEL = list()

count_90_3m_AL = 0
count_90_3m_BL = 0
count_90_3m_CC = 0
count_90_3m_CD = 0
count_90_3m_CV = 0
count_90_3m_GL = 0
count_90_3m_HL = 0
count_90_3m_LAS = 0
count_90_3m_MFBL = 0
count_90_3m_MFHL = 0
count_90_3m_MFOT = 0
count_90_3m_OTH = 0
count_90_3m_PL = 0
count_90_3m_PLBL = 0
count_90_3m_RL = 0
count_90_3m_SCC = 0
count_90_3m_SEL = 0

DPD30P6M_AL = list()
DPD30P6M_BL = list()
DPD30P6M_CC = list()
DPD30P6M_CD = list()
DPD30P6M_CV = list()
DPD30P6M_GL = list()
DPD30P6M_HL = list()
DPD30P6M_LAS = list()
DPD30P6M_MFBL = list()
DPD30P6M_MFHL = list()
DPD30P6M_MFOT = list()
DPD30P6M_OTH = list()
DPD30P6M_PL = list()
DPD30P6M_PLBL = list()
DPD30P6M_RL = list()
DPD30P6M_SCC = list()
DPD30P6M_SEL = list()

count_30_6m_list_AL = list()
count_30_6m_list_BL = list()
count_30_6m_list_CC = list()
count_30_6m_list_CD = list()
count_30_6m_list_CV = list()
count_30_6m_list_GL = list()
count_30_6m_list_HL = list()
count_30_6m_list_LAS = list()
count_30_6m_list_MFBL = list()
count_30_6m_list_MFHL = list()
count_30_6m_list_MFOT = list()
count_30_6m_list_OTH = list()
count_30_6m_list_PL = list()
count_30_6m_list_PLBL = list()
count_30_6m_list_RL = list()
count_30_6m_list_SCC = list()
count_30_6m_list_SEL = list()

count_30_6m_AL = 0
count_30_6m_BL = 0
count_30_6m_CC = 0
count_30_6m_CD = 0
count_30_6m_CV = 0
count_30_6m_GL = 0
count_30_6m_HL = 0
count_30_6m_LAS = 0
count_30_6m_MFBL = 0
count_30_6m_MFHL = 0
count_30_6m_MFOT = 0
count_30_6m_OTH = 0
count_30_6m_PL = 0
count_30_6m_PLBL = 0
count_30_6m_RL = 0
count_30_6m_SCC = 0
count_30_6m_SEL = 0

DPD60P6M_AL = list()
DPD60P6M_BL = list()
DPD60P6M_CC = list()
DPD60P6M_CD = list()
DPD60P6M_CV = list()
DPD60P6M_GL = list()
DPD60P6M_HL = list()
DPD60P6M_LAS = list()
DPD60P6M_MFBL = list()
DPD60P6M_MFHL = list()
DPD60P6M_MFOT = list()
DPD60P6M_OTH = list()
DPD60P6M_PL = list()
DPD60P6M_PLBL = list()
DPD60P6M_RL = list()
DPD60P6M_SCC = list()
DPD60P6M_SEL = list()

count_60_6m_list_AL = list()
count_60_6m_list_BL = list()
count_60_6m_list_CC = list()
count_60_6m_list_CD = list()
count_60_6m_list_CV = list()
count_60_6m_list_GL = list()
count_60_6m_list_HL = list()
count_60_6m_list_LAS = list()
count_60_6m_list_MFBL = list()
count_60_6m_list_MFHL = list()
count_60_6m_list_MFOT = list()
count_60_6m_list_OTH = list()
count_60_6m_list_PL = list()
count_60_6m_list_PLBL = list()
count_60_6m_list_RL = list()
count_60_6m_list_SCC = list()
count_60_6m_list_SEL = list()

count_60_6m_AL = 0
count_60_6m_BL = 0
count_60_6m_CC = 0
count_60_6m_CD = 0
count_60_6m_CV = 0
count_60_6m_GL = 0
count_60_6m_HL = 0
count_60_6m_LAS = 0
count_60_6m_MFBL = 0
count_60_6m_MFHL = 0
count_60_6m_MFOT = 0
count_60_6m_OTH = 0
count_60_6m_PL = 0
count_60_6m_PLBL = 0
count_60_6m_RL = 0
count_60_6m_SCC = 0
count_60_6m_SEL = 0

DPD90P6M_AL = list()
DPD90P6M_BL = list()
DPD90P6M_CC = list()
DPD90P6M_CD = list()
DPD90P6M_CV = list()
DPD90P6M_GL = list()
DPD90P6M_HL = list()
DPD90P6M_LAS = list()
DPD90P6M_MFBL = list()
DPD90P6M_MFHL = list()
DPD90P6M_MFOT = list()
DPD90P6M_OTH = list()
DPD90P6M_PL = list()
DPD90P6M_PLBL = list()
DPD90P6M_RL = list()
DPD90P6M_SCC = list()
DPD90P6M_SEL = list()

count_90_6m_list_AL = list()
count_90_6m_list_BL = list()
count_90_6m_list_CC = list()
count_90_6m_list_CD = list()
count_90_6m_list_CV = list()
count_90_6m_list_GL = list()
count_90_6m_list_HL = list()
count_90_6m_list_LAS = list()
count_90_6m_list_MFBL = list()
count_90_6m_list_MFHL = list()
count_90_6m_list_MFOT = list()
count_90_6m_list_OTH = list()
count_90_6m_list_PL = list()
count_90_6m_list_PLBL = list()
count_90_6m_list_RL = list()
count_90_6m_list_SCC = list()
count_90_6m_list_SEL = list()

count_90_6m_AL = 0
count_90_6m_BL = 0
count_90_6m_CC = 0
count_90_6m_CD = 0
count_90_6m_CV = 0
count_90_6m_GL = 0
count_90_6m_HL = 0
count_90_6m_LAS = 0
count_90_6m_MFBL = 0
count_90_6m_MFHL = 0
count_90_6m_MFOT = 0
count_90_6m_OTH = 0
count_90_6m_PL = 0
count_90_6m_PLBL = 0
count_90_6m_RL = 0
count_90_6m_SCC = 0
count_90_6m_SEL = 0

DPD30P1Y_AL = list()
DPD30P1Y_BL = list()
DPD30P1Y_CC = list()
DPD30P1Y_CD = list()
DPD30P1Y_CV = list()
DPD30P1Y_GL = list()
DPD30P1Y_HL = list()
DPD30P1Y_LAS = list()
DPD30P1Y_MFBL = list()
DPD30P1Y_MFHL = list()
DPD30P1Y_MFOT = list()
DPD30P1Y_OTH = list()
DPD30P1Y_PL = list()
DPD30P1Y_PLBL = list()
DPD30P1Y_RL = list()
DPD30P1Y_SCC = list()
DPD30P1Y_SEL = list()

count_30_1y_list_AL = list()
count_30_1y_list_BL = list()
count_30_1y_list_CC = list()
count_30_1y_list_CD = list()
count_30_1y_list_CV = list()
count_30_1y_list_GL = list()
count_30_1y_list_HL = list()
count_30_1y_list_LAS = list()
count_30_1y_list_MFBL = list()
count_30_1y_list_MFHL = list()
count_30_1y_list_MFOT = list()
count_30_1y_list_OTH = list()
count_30_1y_list_PL = list()
count_30_1y_list_PLBL = list()
count_30_1y_list_RL = list()
count_30_1y_list_SCC = list()
count_30_1y_list_SEL = list()

count_30_1y_AL = 0
count_30_1y_BL = 0
count_30_1y_CC = 0
count_30_1y_CD = 0
count_30_1y_CV = 0
count_30_1y_GL = 0
count_30_1y_HL = 0
count_30_1y_LAS = 0
count_30_1y_MFBL = 0
count_30_1y_MFHL = 0
count_30_1y_MFOT = 0
count_30_1y_OTH = 0
count_30_1y_PL = 0
count_30_1y_PLBL = 0
count_30_1y_RL = 0
count_30_1y_SCC = 0
count_30_1y_SEL = 0

DPD60P1Y_AL = list()
DPD60P1Y_BL = list()
DPD60P1Y_CC = list()
DPD60P1Y_CD = list()
DPD60P1Y_CV = list()
DPD60P1Y_GL = list()
DPD60P1Y_HL = list()
DPD60P1Y_LAS = list()
DPD60P1Y_MFBL = list()
DPD60P1Y_MFHL = list()
DPD60P1Y_MFOT = list()
DPD60P1Y_OTH = list()
DPD60P1Y_PL = list()
DPD60P1Y_PLBL = list()
DPD60P1Y_RL = list()
DPD60P1Y_SCC = list()
DPD60P1Y_SEL = list()

count_60_1y_list_AL = list()
count_60_1y_list_BL = list()
count_60_1y_list_CC = list()
count_60_1y_list_CD = list()
count_60_1y_list_CV = list()
count_60_1y_list_GL = list()
count_60_1y_list_HL = list()
count_60_1y_list_LAS = list()
count_60_1y_list_MFBL = list()
count_60_1y_list_MFHL = list()
count_60_1y_list_MFOT = list()
count_60_1y_list_OTH = list()
count_60_1y_list_PL = list()
count_60_1y_list_PLBL = list()
count_60_1y_list_RL = list()
count_60_1y_list_SCC = list()
count_60_1y_list_SEL = list()

count_60_1y_AL = 0
count_60_1y_BL = 0
count_60_1y_CC = 0
count_60_1y_CD = 0
count_60_1y_CV = 0
count_60_1y_GL = 0
count_60_1y_HL = 0
count_60_1y_LAS = 0
count_60_1y_MFBL = 0
count_60_1y_MFHL = 0
count_60_1y_MFOT = 0
count_60_1y_OTH = 0
count_60_1y_PL = 0
count_60_1y_PLBL = 0
count_60_1y_RL = 0
count_60_1y_SCC = 0
count_60_1y_SEL = 0

DPD90P1Y_AL = list()
DPD90P1Y_BL = list()
DPD90P1Y_CC = list()
DPD90P1Y_CD = list()
DPD90P1Y_CV = list()
DPD90P1Y_GL = list()
DPD90P1Y_HL = list()
DPD90P1Y_LAS = list()
DPD90P1Y_MFBL = list()
DPD90P1Y_MFHL = list()
DPD90P1Y_MFOT = list()
DPD90P1Y_OTH = list()
DPD90P1Y_PL = list()
DPD90P1Y_PLBL = list()
DPD90P1Y_RL = list()
DPD90P1Y_SCC = list()
DPD90P1Y_SEL = list()

count_90_1y_list_AL = list()
count_90_1y_list_BL = list()
count_90_1y_list_CC = list()
count_90_1y_list_CD = list()
count_90_1y_list_CV = list()
count_90_1y_list_GL = list()
count_90_1y_list_HL = list()
count_90_1y_list_LAS = list()
count_90_1y_list_MFBL = list()
count_90_1y_list_MFHL = list()
count_90_1y_list_MFOT = list()
count_90_1y_list_OTH = list()
count_90_1y_list_PL = list()
count_90_1y_list_PLBL = list()
count_90_1y_list_RL = list()
count_90_1y_list_SCC = list()
count_90_1y_list_SEL = list()

count_90_1y_AL = 0
count_90_1y_BL = 0
count_90_1y_CC = 0
count_90_1y_CD = 0
count_90_1y_CV = 0
count_90_1y_GL = 0
count_90_1y_HL = 0
count_90_1y_LAS = 0
count_90_1y_MFBL = 0
count_90_1y_MFHL = 0
count_90_1y_MFOT = 0
count_90_1y_OTH = 0
count_90_1y_PL = 0
count_90_1y_PLBL = 0
count_90_1y_RL = 0
count_90_1y_SCC = 0
count_90_1y_SEL = 0

DPD30P2Y_AL = list()
DPD30P2Y_BL = list()
DPD30P2Y_CC = list()
DPD30P2Y_CD = list()
DPD30P2Y_CV = list()
DPD30P2Y_GL = list()
DPD30P2Y_HL = list()
DPD30P2Y_LAS = list()
DPD30P2Y_MFBL = list()
DPD30P2Y_MFHL = list()
DPD30P2Y_MFOT = list()
DPD30P2Y_OTH = list()
DPD30P2Y_PL = list()
DPD30P2Y_PLBL = list()
DPD30P2Y_RL = list()
DPD30P2Y_SCC = list()
DPD30P2Y_SEL = list()

count_30_2y_list_AL = list()
count_30_2y_list_BL = list()
count_30_2y_list_CC = list()
count_30_2y_list_CD = list()
count_30_2y_list_CV = list()
count_30_2y_list_GL = list()
count_30_2y_list_HL = list()
count_30_2y_list_LAS = list()
count_30_2y_list_MFBL = list()
count_30_2y_list_MFHL = list()
count_30_2y_list_MFOT = list()
count_30_2y_list_OTH = list()
count_30_2y_list_PL = list()
count_30_2y_list_PLBL = list()
count_30_2y_list_RL = list()
count_30_2y_list_SCC = list()
count_30_2y_list_SEL = list()

count_30_2y_AL = 0
count_30_2y_BL = 0
count_30_2y_CC = 0
count_30_2y_CD = 0
count_30_2y_CV = 0
count_30_2y_GL = 0
count_30_2y_HL = 0
count_30_2y_LAS = 0
count_30_2y_MFBL = 0
count_30_2y_MFHL = 0
count_30_2y_MFOT = 0
count_30_2y_OTH = 0
count_30_2y_PL = 0
count_30_2y_PLBL = 0
count_30_2y_RL = 0
count_30_2y_SCC = 0
count_30_2y_SEL = 0

DPD60P2Y_AL = list()
DPD60P2Y_BL = list()
DPD60P2Y_CC = list()
DPD60P2Y_CD = list()
DPD60P2Y_CV = list()
DPD60P2Y_GL = list()
DPD60P2Y_HL = list()
DPD60P2Y_LAS = list()
DPD60P2Y_MFBL = list()
DPD60P2Y_MFHL = list()
DPD60P2Y_MFOT = list()
DPD60P2Y_OTH = list()
DPD60P2Y_PL = list()
DPD60P2Y_PLBL = list()
DPD60P2Y_RL = list()
DPD60P2Y_SCC = list()
DPD60P2Y_SEL = list()

count_60_2y_list_AL = list()
count_60_2y_list_BL = list()
count_60_2y_list_CC = list()
count_60_2y_list_CD = list()
count_60_2y_list_CV = list()
count_60_2y_list_GL = list()
count_60_2y_list_HL = list()
count_60_2y_list_LAS = list()
count_60_2y_list_MFBL = list()
count_60_2y_list_MFHL = list()
count_60_2y_list_MFOT = list()
count_60_2y_list_OTH = list()
count_60_2y_list_PL = list()
count_60_2y_list_PLBL = list()
count_60_2y_list_RL = list()
count_60_2y_list_SCC = list()
count_60_2y_list_SEL = list()

count_60_2y_AL = 0
count_60_2y_BL = 0
count_60_2y_CC = 0
count_60_2y_CD = 0
count_60_2y_CV = 0
count_60_2y_GL = 0
count_60_2y_HL = 0
count_60_2y_LAS = 0
count_60_2y_MFBL = 0
count_60_2y_MFHL = 0
count_60_2y_MFOT = 0
count_60_2y_OTH = 0
count_60_2y_PL = 0
count_60_2y_PLBL = 0
count_60_2y_RL = 0
count_60_2y_SCC = 0
count_60_2y_SEL = 0

DPD90P2Y_AL = list()
DPD90P2Y_BL = list()
DPD90P2Y_CC = list()
DPD90P2Y_CD = list()
DPD90P2Y_CV = list()
DPD90P2Y_GL = list()
DPD90P2Y_HL = list()
DPD90P2Y_LAS = list()
DPD90P2Y_MFBL = list()
DPD90P2Y_MFHL = list()
DPD90P2Y_MFOT = list()
DPD90P2Y_OTH = list()
DPD90P2Y_PL = list()
DPD90P2Y_PLBL = list()
DPD90P2Y_RL = list()
DPD90P2Y_SCC = list()
DPD90P2Y_SEL = list()

count_90_2y_list_AL = list()
count_90_2y_list_BL = list()
count_90_2y_list_CC = list()
count_90_2y_list_CD = list()
count_90_2y_list_CV = list()
count_90_2y_list_GL = list()
count_90_2y_list_HL = list()
count_90_2y_list_LAS = list()
count_90_2y_list_MFBL = list()
count_90_2y_list_MFHL = list()
count_90_2y_list_MFOT = list()
count_90_2y_list_OTH = list()
count_90_2y_list_PL = list()
count_90_2y_list_PLBL = list()
count_90_2y_list_RL = list()
count_90_2y_list_SCC = list()
count_90_2y_list_SEL = list()

count_90_2y_AL = 0
count_90_2y_BL = 0
count_90_2y_CC = 0
count_90_2y_CD = 0
count_90_2y_CV = 0
count_90_2y_GL = 0
count_90_2y_HL = 0
count_90_2y_LAS = 0
count_90_2y_MFBL = 0
count_90_2y_MFHL = 0
count_90_2y_MFOT = 0
count_90_2y_OTH = 0
count_90_2y_PL = 0
count_90_2y_PLBL = 0
count_90_2y_RL = 0
count_90_2y_SCC = 0
count_90_2y_SEL = 0

DPD30P3Y_AL = list()
DPD30P3Y_BL = list()
DPD30P3Y_CC = list()
DPD30P3Y_CD = list()
DPD30P3Y_CV = list()
DPD30P3Y_GL = list()
DPD30P3Y_HL = list()
DPD30P3Y_LAS = list()
DPD30P3Y_MFBL = list()
DPD30P3Y_MFHL = list()
DPD30P3Y_MFOT = list()
DPD30P3Y_OTH = list()
DPD30P3Y_PL = list()
DPD30P3Y_PLBL = list()
DPD30P3Y_RL = list()
DPD30P3Y_SCC = list()
DPD30P3Y_SEL = list()

count_30_3y_list_AL = list()
count_30_3y_list_BL = list()
count_30_3y_list_CC = list()
count_30_3y_list_CD = list()
count_30_3y_list_CV = list()
count_30_3y_list_GL = list()
count_30_3y_list_HL = list()
count_30_3y_list_LAS = list()
count_30_3y_list_MFBL = list()
count_30_3y_list_MFHL = list()
count_30_3y_list_MFOT = list()
count_30_3y_list_OTH = list()
count_30_3y_list_PL = list()
count_30_3y_list_PLBL = list()
count_30_3y_list_RL = list()
count_30_3y_list_SCC = list()
count_30_3y_list_SEL = list()

count_30_3y_AL = 0
count_30_3y_BL = 0
count_30_3y_CC = 0
count_30_3y_CD = 0
count_30_3y_CV = 0
count_30_3y_GL = 0
count_30_3y_HL = 0
count_30_3y_LAS = 0
count_30_3y_MFBL = 0
count_30_3y_MFHL = 0
count_30_3y_MFOT = 0
count_30_3y_OTH = 0
count_30_3y_PL = 0
count_30_3y_PLBL = 0
count_30_3y_RL = 0
count_30_3y_SCC = 0
count_30_3y_SEL = 0

DPD60P3Y_AL = list()
DPD60P3Y_BL = list()
DPD60P3Y_CC = list()
DPD60P3Y_CD = list()
DPD60P3Y_CV = list()
DPD60P3Y_GL = list()
DPD60P3Y_HL = list()
DPD60P3Y_LAS = list()
DPD60P3Y_MFBL = list()
DPD60P3Y_MFHL = list()
DPD60P3Y_MFOT = list()
DPD60P3Y_OTH = list()
DPD60P3Y_PL = list()
DPD60P3Y_PLBL = list()
DPD60P3Y_RL = list()
DPD60P3Y_SCC = list()
DPD60P3Y_SEL = list()

count_60_3y_list_AL = list()
count_60_3y_list_BL = list()
count_60_3y_list_CC = list()
count_60_3y_list_CD = list()
count_60_3y_list_CV = list()
count_60_3y_list_GL = list()
count_60_3y_list_HL = list()
count_60_3y_list_LAS = list()
count_60_3y_list_MFBL = list()
count_60_3y_list_MFHL = list()
count_60_3y_list_MFOT = list()
count_60_3y_list_OTH = list()
count_60_3y_list_PL = list()
count_60_3y_list_PLBL = list()
count_60_3y_list_RL = list()
count_60_3y_list_SCC = list()
count_60_3y_list_SEL = list()

count_60_3y_AL = 0
count_60_3y_BL = 0
count_60_3y_CC = 0
count_60_3y_CD = 0
count_60_3y_CV = 0
count_60_3y_GL = 0
count_60_3y_HL = 0
count_60_3y_LAS = 0
count_60_3y_MFBL = 0
count_60_3y_MFHL = 0
count_60_3y_MFOT = 0
count_60_3y_OTH = 0
count_60_3y_PL = 0
count_60_3y_PLBL = 0
count_60_3y_RL = 0
count_60_3y_SCC = 0
count_60_3y_SEL = 0

DPD90P3Y_AL = list()
DPD90P3Y_BL = list()
DPD90P3Y_CC = list()
DPD90P3Y_CD = list()
DPD90P3Y_CV = list()
DPD90P3Y_GL = list()
DPD90P3Y_HL = list()
DPD90P3Y_LAS = list()
DPD90P3Y_MFBL = list()
DPD90P3Y_MFHL = list()
DPD90P3Y_MFOT = list()
DPD90P3Y_OTH = list()
DPD90P3Y_PL = list()
DPD90P3Y_PLBL = list()
DPD90P3Y_RL = list()
DPD90P3Y_SCC = list()
DPD90P3Y_SEL = list()

count_90_3y_list_AL = list()
count_90_3y_list_BL = list()
count_90_3y_list_CC = list()
count_90_3y_list_CD = list()
count_90_3y_list_CV = list()
count_90_3y_list_GL = list()
count_90_3y_list_HL = list()
count_90_3y_list_LAS = list()
count_90_3y_list_MFBL = list()
count_90_3y_list_MFHL = list()
count_90_3y_list_MFOT = list()
count_90_3y_list_OTH = list()
count_90_3y_list_PL = list()
count_90_3y_list_PLBL = list()
count_90_3y_list_RL = list()
count_90_3y_list_SCC = list()
count_90_3y_list_SEL = list()

count_90_3y_AL = 0
count_90_3y_BL = 0
count_90_3y_CC = 0
count_90_3y_CD = 0
count_90_3y_CV = 0
count_90_3y_GL = 0
count_90_3y_HL = 0
count_90_3y_LAS = 0
count_90_3y_MFBL = 0
count_90_3y_MFHL = 0
count_90_3y_MFOT = 0
count_90_3y_OTH = 0
count_90_3y_PL = 0
count_90_3y_PLBL = 0
count_90_3y_RL = 0
count_90_3y_SCC = 0
count_90_3y_SEL = 0

STD1M = list()
count_std__list_1m = list()
count_std__1m = 0

STD3M = list()
count_std__list_3m = list()
count_std__3m = 0

STD6M = list()
count_std__list_6m = list()
count_std__6m = 0

STD1Y = list()
count_std__list_1y = list()
count_std__1y = 0

STD2Y = list()
count_std__list_2y = list()
count_std__2y = 0

STD3Y = list()
count_std__list_3y = list()
count_std__3y = 0

STD1M_AL = list()
STD1M_BL = list()
STD1M_CC = list()
STD1M_CD = list()
STD1M_CV = list()
STD1M_GL = list()
STD1M_HL = list()
STD1M_LAS = list()
STD1M_MFBL = list()
STD1M_MFHL = list()
STD1M_MFOT = list()
STD1M_OTH = list()
STD1M_PL = list()
STD1M_PLBL = list()
STD1M_RL = list()
STD1M_SCC = list()
STD1M_SEL = list()

count_std_1m_list_AL = list()
count_std_1m_list_BL = list()
count_std_1m_list_CC = list()
count_std_1m_list_CD = list()
count_std_1m_list_CV = list()
count_std_1m_list_GL = list()
count_std_1m_list_HL = list()
count_std_1m_list_LAS = list()
count_std_1m_list_MFBL = list()
count_std_1m_list_MFHL = list()
count_std_1m_list_MFOT = list()
count_std_1m_list_OTH = list()
count_std_1m_list_PL = list()
count_std_1m_list_PLBL = list()
count_std_1m_list_RL = list()
count_std_1m_list_SCC = list()
count_std_1m_list_SEL = list()

count_std_1m_AL = 0
count_std_1m_BL = 0
count_std_1m_CC = 0
count_std_1m_CD = 0
count_std_1m_CV = 0
count_std_1m_GL = 0
count_std_1m_HL = 0
count_std_1m_LAS = 0
count_std_1m_MFBL = 0
count_std_1m_MFHL = 0
count_std_1m_MFOT = 0
count_std_1m_OTH = 0
count_std_1m_PL = 0
count_std_1m_PLBL = 0
count_std_1m_RL = 0
count_std_1m_SCC = 0
count_std_1m_SEL = 0

STD3M_AL = list()
STD3M_BL = list()
STD3M_CC = list()
STD3M_CD = list()
STD3M_CV = list()
STD3M_GL = list()
STD3M_HL = list()
STD3M_LAS = list()
STD3M_MFBL = list()
STD3M_MFHL = list()
STD3M_MFOT = list()
STD3M_OTH = list()
STD3M_PL = list()
STD3M_PLBL = list()
STD3M_RL = list()
STD3M_SCC = list()
STD3M_SEL = list()

count_std_3m_list_AL = list()
count_std_3m_list_BL = list()
count_std_3m_list_CC = list()
count_std_3m_list_CD = list()
count_std_3m_list_CV = list()
count_std_3m_list_GL = list()
count_std_3m_list_HL = list()
count_std_3m_list_LAS = list()
count_std_3m_list_MFBL = list()
count_std_3m_list_MFHL = list()
count_std_3m_list_MFOT = list()
count_std_3m_list_OTH = list()
count_std_3m_list_PL = list()
count_std_3m_list_PLBL = list()
count_std_3m_list_RL = list()
count_std_3m_list_SCC = list()
count_std_3m_list_SEL = list()

count_std_3m_AL = 0
count_std_3m_BL = 0
count_std_3m_CC = 0
count_std_3m_CD = 0
count_std_3m_CV = 0
count_std_3m_GL = 0
count_std_3m_HL = 0
count_std_3m_LAS = 0
count_std_3m_MFBL = 0
count_std_3m_MFHL = 0
count_std_3m_MFOT = 0
count_std_3m_OTH = 0
count_std_3m_PL = 0
count_std_3m_PLBL = 0
count_std_3m_RL = 0
count_std_3m_SCC = 0
count_std_3m_SEL = 0

STD6M_AL = list()
STD6M_BL = list()
STD6M_CC = list()
STD6M_CD = list()
STD6M_CV = list()
STD6M_GL = list()
STD6M_HL = list()
STD6M_LAS = list()
STD6M_MFBL = list()
STD6M_MFHL = list()
STD6M_MFOT = list()
STD6M_OTH = list()
STD6M_PL = list()
STD6M_PLBL = list()
STD6M_RL = list()
STD6M_SCC = list()
STD6M_SEL = list()

count_std_6m_list_AL = list()
count_std_6m_list_BL = list()
count_std_6m_list_CC = list()
count_std_6m_list_CD = list()
count_std_6m_list_CV = list()
count_std_6m_list_GL = list()
count_std_6m_list_HL = list()
count_std_6m_list_LAS = list()
count_std_6m_list_MFBL = list()
count_std_6m_list_MFHL = list()
count_std_6m_list_MFOT = list()
count_std_6m_list_OTH = list()
count_std_6m_list_PL = list()
count_std_6m_list_PLBL = list()
count_std_6m_list_RL = list()
count_std_6m_list_SCC = list()
count_std_6m_list_SEL = list()

count_std_6m_AL = 0
count_std_6m_BL = 0
count_std_6m_CC = 0
count_std_6m_CD = 0
count_std_6m_CV = 0
count_std_6m_GL = 0
count_std_6m_HL = 0
count_std_6m_LAS = 0
count_std_6m_MFBL = 0
count_std_6m_MFHL = 0
count_std_6m_MFOT = 0
count_std_6m_OTH = 0
count_std_6m_PL = 0
count_std_6m_PLBL = 0
count_std_6m_RL = 0
count_std_6m_SCC = 0
count_std_6m_SEL = 0

STD1Y_AL = list()
STD1Y_BL = list()
STD1Y_CC = list()
STD1Y_CD = list()
STD1Y_CV = list()
STD1Y_GL = list()
STD1Y_HL = list()
STD1Y_LAS = list()
STD1Y_MFBL = list()
STD1Y_MFHL = list()
STD1Y_MFOT = list()
STD1Y_OTH = list()
STD1Y_PL = list()
STD1Y_PLBL = list()
STD1Y_RL = list()
STD1Y_SCC = list()
STD1Y_SEL = list()

count_std_1y_list_AL = list()
count_std_1y_list_BL = list()
count_std_1y_list_CC = list()
count_std_1y_list_CD = list()
count_std_1y_list_CV = list()
count_std_1y_list_GL = list()
count_std_1y_list_HL = list()
count_std_1y_list_LAS = list()
count_std_1y_list_MFBL = list()
count_std_1y_list_MFHL = list()
count_std_1y_list_MFOT = list()
count_std_1y_list_OTH = list()
count_std_1y_list_PL = list()
count_std_1y_list_PLBL = list()
count_std_1y_list_RL = list()
count_std_1y_list_SCC = list()
count_std_1y_list_SEL = list()

count_std_1y_AL = 0
count_std_1y_BL = 0
count_std_1y_CC = 0
count_std_1y_CD = 0
count_std_1y_CV = 0
count_std_1y_GL = 0
count_std_1y_HL = 0
count_std_1y_LAS = 0
count_std_1y_MFBL = 0
count_std_1y_MFHL = 0
count_std_1y_MFOT = 0
count_std_1y_OTH = 0
count_std_1y_PL = 0
count_std_1y_PLBL = 0
count_std_1y_RL = 0
count_std_1y_SCC = 0
count_std_1y_SEL = 0

STD2Y_AL = list()
STD2Y_BL = list()
STD2Y_CC = list()
STD2Y_CD = list()
STD2Y_CV = list()
STD2Y_GL = list()
STD2Y_HL = list()
STD2Y_LAS = list()
STD2Y_MFBL = list()
STD2Y_MFHL = list()
STD2Y_MFOT = list()
STD2Y_OTH = list()
STD2Y_PL = list()
STD2Y_PLBL = list()
STD2Y_RL = list()
STD2Y_SCC = list()
STD2Y_SEL = list()

count_std_2y_list_AL = list()
count_std_2y_list_BL = list()
count_std_2y_list_CC = list()
count_std_2y_list_CD = list()
count_std_2y_list_CV = list()
count_std_2y_list_GL = list()
count_std_2y_list_HL = list()
count_std_2y_list_LAS = list()
count_std_2y_list_MFBL = list()
count_std_2y_list_MFHL = list()
count_std_2y_list_MFOT = list()
count_std_2y_list_OTH = list()
count_std_2y_list_PL = list()
count_std_2y_list_PLBL = list()
count_std_2y_list_RL = list()
count_std_2y_list_SCC = list()
count_std_2y_list_SEL = list()

count_std_2y_AL = 0
count_std_2y_BL = 0
count_std_2y_CC = 0
count_std_2y_CD = 0
count_std_2y_CV = 0
count_std_2y_GL = 0
count_std_2y_HL = 0
count_std_2y_LAS = 0
count_std_2y_MFBL = 0
count_std_2y_MFHL = 0
count_std_2y_MFOT = 0
count_std_2y_OTH = 0
count_std_2y_PL = 0
count_std_2y_PLBL = 0
count_std_2y_RL = 0
count_std_2y_SCC = 0
count_std_2y_SEL = 0

STD3Y_AL = list()
STD3Y_BL = list()
STD3Y_CC = list()
STD3Y_CD = list()
STD3Y_CV = list()
STD3Y_GL = list()
STD3Y_HL = list()
STD3Y_LAS = list()
STD3Y_MFBL = list()
STD3Y_MFHL = list()
STD3Y_MFOT = list()
STD3Y_OTH = list()
STD3Y_PL = list()
STD3Y_PLBL = list()
STD3Y_RL = list()
STD3Y_SCC = list()
STD3Y_SEL = list()

count_std_3y_list_AL = list()
count_std_3y_list_BL = list()
count_std_3y_list_CC = list()
count_std_3y_list_CD = list()
count_std_3y_list_CV = list()
count_std_3y_list_GL = list()
count_std_3y_list_HL = list()
count_std_3y_list_LAS = list()
count_std_3y_list_MFBL = list()
count_std_3y_list_MFHL = list()
count_std_3y_list_MFOT = list()
count_std_3y_list_OTH = list()
count_std_3y_list_PL = list()
count_std_3y_list_PLBL = list()
count_std_3y_list_RL = list()
count_std_3y_list_SCC = list()
count_std_3y_list_SEL = list()

count_std_3y_AL = 0
count_std_3y_BL = 0
count_std_3y_CC = 0
count_std_3y_CD = 0
count_std_3y_CV = 0
count_std_3y_GL = 0
count_std_3y_HL = 0
count_std_3y_LAS = 0
count_std_3y_MFBL = 0
count_std_3y_MFHL = 0
count_std_3y_MFOT = 0
count_std_3y_OTH = 0
count_std_3y_PL = 0
count_std_3y_PLBL = 0
count_std_3y_RL = 0
count_std_3y_SCC = 0
count_std_3y_SEL = 0

SUB1M = list()
count_sub_list_1m = list()
count_sub_1m = 0

SUB3M = list()
count_sub_list_3m = list()
count_sub_3m = 0

SUB6M = list()
count_sub_list_6m = list()
count_sub_6m = 0

SUB1Y = list()
count_sub_list_1y = list()
count_sub_1y = 0

SUB2Y = list()
count_sub_list_2y = list()
count_sub_2y = 0

SUB3Y = list()
count_sub_list_3y = list()
count_sub_3y = 0

SUB1M_AL = list()
SUB1M_BL = list()
SUB1M_CC = list()
SUB1M_CD = list()
SUB1M_CV = list()
SUB1M_GL = list()
SUB1M_HL = list()
SUB1M_LAS = list()
SUB1M_MFBL = list()
SUB1M_MFHL = list()
SUB1M_MFOT = list()
SUB1M_OTH = list()
SUB1M_PL = list()
SUB1M_PLBL = list()
SUB1M_RL = list()
SUB1M_SCC = list()
SUB1M_SEL = list()

count_sub_1m_list_AL = list()
count_sub_1m_list_BL = list()
count_sub_1m_list_CC = list()
count_sub_1m_list_CD = list()
count_sub_1m_list_CV = list()
count_sub_1m_list_GL = list()
count_sub_1m_list_HL = list()
count_sub_1m_list_LAS = list()
count_sub_1m_list_MFBL = list()
count_sub_1m_list_MFHL = list()
count_sub_1m_list_MFOT = list()
count_sub_1m_list_OTH = list()
count_sub_1m_list_PL = list()
count_sub_1m_list_PLBL = list()
count_sub_1m_list_RL = list()
count_sub_1m_list_SCC = list()
count_sub_1m_list_SEL = list()

count_sub_1m_AL = 0
count_sub_1m_BL = 0
count_sub_1m_CC = 0
count_sub_1m_CD = 0
count_sub_1m_CV = 0
count_sub_1m_GL = 0
count_sub_1m_HL = 0
count_sub_1m_LAS = 0
count_sub_1m_MFBL = 0
count_sub_1m_MFHL = 0
count_sub_1m_MFOT = 0
count_sub_1m_OTH = 0
count_sub_1m_PL = 0
count_sub_1m_PLBL = 0
count_sub_1m_RL = 0
count_sub_1m_SCC = 0
count_sub_1m_SEL = 0

SUB3M_AL = list()
SUB3M_BL = list()
SUB3M_CC = list()
SUB3M_CD = list()
SUB3M_CV = list()
SUB3M_GL = list()
SUB3M_HL = list()
SUB3M_LAS = list()
SUB3M_MFBL = list()
SUB3M_MFHL = list()
SUB3M_MFOT = list()
SUB3M_OTH = list()
SUB3M_PL = list()
SUB3M_PLBL = list()
SUB3M_RL = list()
SUB3M_SCC = list()
SUB3M_SEL = list()

count_sub_3m_list_AL = list()
count_sub_3m_list_BL = list()
count_sub_3m_list_CC = list()
count_sub_3m_list_CD = list()
count_sub_3m_list_CV = list()
count_sub_3m_list_GL = list()
count_sub_3m_list_HL = list()
count_sub_3m_list_LAS = list()
count_sub_3m_list_MFBL = list()
count_sub_3m_list_MFHL = list()
count_sub_3m_list_MFOT = list()
count_sub_3m_list_OTH = list()
count_sub_3m_list_PL = list()
count_sub_3m_list_PLBL = list()
count_sub_3m_list_RL = list()
count_sub_3m_list_SCC = list()
count_sub_3m_list_SEL = list()

count_sub_3m_AL = 0
count_sub_3m_BL = 0
count_sub_3m_CC = 0
count_sub_3m_CD = 0
count_sub_3m_CV = 0
count_sub_3m_GL = 0
count_sub_3m_HL = 0
count_sub_3m_LAS = 0
count_sub_3m_MFBL = 0
count_sub_3m_MFHL = 0
count_sub_3m_MFOT = 0
count_sub_3m_OTH = 0
count_sub_3m_PL = 0
count_sub_3m_PLBL = 0
count_sub_3m_RL = 0
count_sub_3m_SCC = 0
count_sub_3m_SEL = 0

SUB6M_AL = list()
SUB6M_BL = list()
SUB6M_CC = list()
SUB6M_CD = list()
SUB6M_CV = list()
SUB6M_GL = list()
SUB6M_HL = list()
SUB6M_LAS = list()
SUB6M_MFBL = list()
SUB6M_MFHL = list()
SUB6M_MFOT = list()
SUB6M_OTH = list()
SUB6M_PL = list()
SUB6M_PLBL = list()
SUB6M_RL = list()
SUB6M_SCC = list()
SUB6M_SEL = list()

count_sub_6m_list_AL = list()
count_sub_6m_list_BL = list()
count_sub_6m_list_CC = list()
count_sub_6m_list_CD = list()
count_sub_6m_list_CV = list()
count_sub_6m_list_GL = list()
count_sub_6m_list_HL = list()
count_sub_6m_list_LAS = list()
count_sub_6m_list_MFBL = list()
count_sub_6m_list_MFHL = list()
count_sub_6m_list_MFOT = list()
count_sub_6m_list_OTH = list()
count_sub_6m_list_PL = list()
count_sub_6m_list_PLBL = list()
count_sub_6m_list_RL = list()
count_sub_6m_list_SCC = list()
count_sub_6m_list_SEL = list()

count_sub_6m_AL = 0
count_sub_6m_BL = 0
count_sub_6m_CC = 0
count_sub_6m_CD = 0
count_sub_6m_CV = 0
count_sub_6m_GL = 0
count_sub_6m_HL = 0
count_sub_6m_LAS = 0
count_sub_6m_MFBL = 0
count_sub_6m_MFHL = 0
count_sub_6m_MFOT = 0
count_sub_6m_OTH = 0
count_sub_6m_PL = 0
count_sub_6m_PLBL = 0
count_sub_6m_RL = 0
count_sub_6m_SCC = 0
count_sub_6m_SEL = 0

SUB1Y_AL = list()
SUB1Y_BL = list()
SUB1Y_CC = list()
SUB1Y_CD = list()
SUB1Y_CV = list()
SUB1Y_GL = list()
SUB1Y_HL = list()
SUB1Y_LAS = list()
SUB1Y_MFBL = list()
SUB1Y_MFHL = list()
SUB1Y_MFOT = list()
SUB1Y_OTH = list()
SUB1Y_PL = list()
SUB1Y_PLBL = list()
SUB1Y_RL = list()
SUB1Y_SCC = list()
SUB1Y_SEL = list()

count_sub_1y_list_AL = list()
count_sub_1y_list_BL = list()
count_sub_1y_list_CC = list()
count_sub_1y_list_CD = list()
count_sub_1y_list_CV = list()
count_sub_1y_list_GL = list()
count_sub_1y_list_HL = list()
count_sub_1y_list_LAS = list()
count_sub_1y_list_MFBL = list()
count_sub_1y_list_MFHL = list()
count_sub_1y_list_MFOT = list()
count_sub_1y_list_OTH = list()
count_sub_1y_list_PL = list()
count_sub_1y_list_PLBL = list()
count_sub_1y_list_RL = list()
count_sub_1y_list_SCC = list()
count_sub_1y_list_SEL = list()

count_sub_1y_AL = 0
count_sub_1y_BL = 0
count_sub_1y_CC = 0
count_sub_1y_CD = 0
count_sub_1y_CV = 0
count_sub_1y_GL = 0
count_sub_1y_HL = 0
count_sub_1y_LAS = 0
count_sub_1y_MFBL = 0
count_sub_1y_MFHL = 0
count_sub_1y_MFOT = 0
count_sub_1y_OTH = 0
count_sub_1y_PL = 0
count_sub_1y_PLBL = 0
count_sub_1y_RL = 0
count_sub_1y_SCC = 0
count_sub_1y_SEL = 0

SUB2Y_AL = list()
SUB2Y_BL = list()
SUB2Y_CC = list()
SUB2Y_CD = list()
SUB2Y_CV = list()
SUB2Y_GL = list()
SUB2Y_HL = list()
SUB2Y_LAS = list()
SUB2Y_MFBL = list()
SUB2Y_MFHL = list()
SUB2Y_MFOT = list()
SUB2Y_OTH = list()
SUB2Y_PL = list()
SUB2Y_PLBL = list()
SUB2Y_RL = list()
SUB2Y_SCC = list()
SUB2Y_SEL = list()

count_sub_2y_list_AL = list()
count_sub_2y_list_BL = list()
count_sub_2y_list_CC = list()
count_sub_2y_list_CD = list()
count_sub_2y_list_CV = list()
count_sub_2y_list_GL = list()
count_sub_2y_list_HL = list()
count_sub_2y_list_LAS = list()
count_sub_2y_list_MFBL = list()
count_sub_2y_list_MFHL = list()
count_sub_2y_list_MFOT = list()
count_sub_2y_list_OTH = list()
count_sub_2y_list_PL = list()
count_sub_2y_list_PLBL = list()
count_sub_2y_list_RL = list()
count_sub_2y_list_SCC = list()
count_sub_2y_list_SEL = list()

count_sub_2y_AL = 0
count_sub_2y_BL = 0
count_sub_2y_CC = 0
count_sub_2y_CD = 0
count_sub_2y_CV = 0
count_sub_2y_GL = 0
count_sub_2y_HL = 0
count_sub_2y_LAS = 0
count_sub_2y_MFBL = 0
count_sub_2y_MFHL = 0
count_sub_2y_MFOT = 0
count_sub_2y_OTH = 0
count_sub_2y_PL = 0
count_sub_2y_PLBL = 0
count_sub_2y_RL = 0
count_sub_2y_SCC = 0
count_sub_2y_SEL = 0

SUB3Y_AL = list()
SUB3Y_BL = list()
SUB3Y_CC = list()
SUB3Y_CD = list()
SUB3Y_CV = list()
SUB3Y_GL = list()
SUB3Y_HL = list()
SUB3Y_LAS = list()
SUB3Y_MFBL = list()
SUB3Y_MFHL = list()
SUB3Y_MFOT = list()
SUB3Y_OTH = list()
SUB3Y_PL = list()
SUB3Y_PLBL = list()
SUB3Y_RL = list()
SUB3Y_SCC = list()
SUB3Y_SEL = list()

count_sub_3y_list_AL = list()
count_sub_3y_list_BL = list()
count_sub_3y_list_CC = list()
count_sub_3y_list_CD = list()
count_sub_3y_list_CV = list()
count_sub_3y_list_GL = list()
count_sub_3y_list_HL = list()
count_sub_3y_list_LAS = list()
count_sub_3y_list_MFBL = list()
count_sub_3y_list_MFHL = list()
count_sub_3y_list_MFOT = list()
count_sub_3y_list_OTH = list()
count_sub_3y_list_PL = list()
count_sub_3y_list_PLBL = list()
count_sub_3y_list_RL = list()
count_sub_3y_list_SCC = list()
count_sub_3y_list_SEL = list()

count_sub_3y_AL = 0
count_sub_3y_BL = 0
count_sub_3y_CC = 0
count_sub_3y_CD = 0
count_sub_3y_CV = 0
count_sub_3y_GL = 0
count_sub_3y_HL = 0
count_sub_3y_LAS = 0
count_sub_3y_MFBL = 0
count_sub_3y_MFHL = 0
count_sub_3y_MFOT = 0
count_sub_3y_OTH = 0
count_sub_3y_PL = 0
count_sub_3y_PLBL = 0
count_sub_3y_RL = 0
count_sub_3y_SCC = 0
count_sub_3y_SEL = 0

DBT1M = list()
count_dbt_list_1m = list()
count_dbt_1m = 0

DBT3M = list()
count_dbt_list_3m = list()
count_dbt_3m = 0

DBT6M = list()
count_dbt_list_6m = list()
count_dbt_6m = 0

DBT1Y = list()
count_dbt_list_1y = list()
count_dbt_1y = 0

DBT2Y = list()
count_dbt_list_2y = list()
count_dbt_2y = 0

DBT3Y = list()
count_dbt_list_3y = list()
count_dbt_3y = 0

DBT1M_AL = list()
DBT1M_BL = list()
DBT1M_CC = list()
DBT1M_CD = list()
DBT1M_CV = list()
DBT1M_GL = list()
DBT1M_HL = list()
DBT1M_LAS = list()
DBT1M_MFBL = list()
DBT1M_MFHL = list()
DBT1M_MFOT = list()
DBT1M_OTH = list()
DBT1M_PL = list()
DBT1M_PLBL = list()
DBT1M_RL = list()
DBT1M_SCC = list()
DBT1M_SEL = list()

count_dbt_1m_list_AL = list()
count_dbt_1m_list_BL = list()
count_dbt_1m_list_CC = list()
count_dbt_1m_list_CD = list()
count_dbt_1m_list_CV = list()
count_dbt_1m_list_GL = list()
count_dbt_1m_list_HL = list()
count_dbt_1m_list_LAS = list()
count_dbt_1m_list_MFBL = list()
count_dbt_1m_list_MFHL = list()
count_dbt_1m_list_MFOT = list()
count_dbt_1m_list_OTH = list()
count_dbt_1m_list_PL = list()
count_dbt_1m_list_PLBL = list()
count_dbt_1m_list_RL = list()
count_dbt_1m_list_SCC = list()
count_dbt_1m_list_SEL = list()

count_dbt_1m_AL = 0
count_dbt_1m_BL = 0
count_dbt_1m_CC = 0
count_dbt_1m_CD = 0
count_dbt_1m_CV = 0
count_dbt_1m_GL = 0
count_dbt_1m_HL = 0
count_dbt_1m_LAS = 0
count_dbt_1m_MFBL = 0
count_dbt_1m_MFHL = 0
count_dbt_1m_MFOT = 0
count_dbt_1m_OTH = 0
count_dbt_1m_PL = 0
count_dbt_1m_PLBL = 0
count_dbt_1m_RL = 0
count_dbt_1m_SCC = 0
count_dbt_1m_SEL = 0

DBT3M_AL = list()
DBT3M_BL = list()
DBT3M_CC = list()
DBT3M_CD = list()
DBT3M_CV = list()
DBT3M_GL = list()
DBT3M_HL = list()
DBT3M_LAS = list()
DBT3M_MFBL = list()
DBT3M_MFHL = list()
DBT3M_MFOT = list()
DBT3M_OTH = list()
DBT3M_PL = list()
DBT3M_PLBL = list()
DBT3M_RL = list()
DBT3M_SCC = list()
DBT3M_SEL = list()

count_dbt_3m_list_AL = list()
count_dbt_3m_list_BL = list()
count_dbt_3m_list_CC = list()
count_dbt_3m_list_CD = list()
count_dbt_3m_list_CV = list()
count_dbt_3m_list_GL = list()
count_dbt_3m_list_HL = list()
count_dbt_3m_list_LAS = list()
count_dbt_3m_list_MFBL = list()
count_dbt_3m_list_MFHL = list()
count_dbt_3m_list_MFOT = list()
count_dbt_3m_list_OTH = list()
count_dbt_3m_list_PL = list()
count_dbt_3m_list_PLBL = list()
count_dbt_3m_list_RL = list()
count_dbt_3m_list_SCC = list()
count_dbt_3m_list_SEL = list()

count_dbt_3m_AL = 0
count_dbt_3m_BL = 0
count_dbt_3m_CC = 0
count_dbt_3m_CD = 0
count_dbt_3m_CV = 0
count_dbt_3m_GL = 0
count_dbt_3m_HL = 0
count_dbt_3m_LAS = 0
count_dbt_3m_MFBL = 0
count_dbt_3m_MFHL = 0
count_dbt_3m_MFOT = 0
count_dbt_3m_OTH = 0
count_dbt_3m_PL = 0
count_dbt_3m_PLBL = 0
count_dbt_3m_RL = 0
count_dbt_3m_SCC = 0
count_dbt_3m_SEL = 0

DBT6M_AL = list()
DBT6M_BL = list()
DBT6M_CC = list()
DBT6M_CD = list()
DBT6M_CV = list()
DBT6M_GL = list()
DBT6M_HL = list()
DBT6M_LAS = list()
DBT6M_MFBL = list()
DBT6M_MFHL = list()
DBT6M_MFOT = list()
DBT6M_OTH = list()
DBT6M_PL = list()
DBT6M_PLBL = list()
DBT6M_RL = list()
DBT6M_SCC = list()
DBT6M_SEL = list()

count_dbt_6m_list_AL = list()
count_dbt_6m_list_BL = list()
count_dbt_6m_list_CC = list()
count_dbt_6m_list_CD = list()
count_dbt_6m_list_CV = list()
count_dbt_6m_list_GL = list()
count_dbt_6m_list_HL = list()
count_dbt_6m_list_LAS = list()
count_dbt_6m_list_MFBL = list()
count_dbt_6m_list_MFHL = list()
count_dbt_6m_list_MFOT = list()
count_dbt_6m_list_OTH = list()
count_dbt_6m_list_PL = list()
count_dbt_6m_list_PLBL = list()
count_dbt_6m_list_RL = list()
count_dbt_6m_list_SCC = list()
count_dbt_6m_list_SEL = list()

count_dbt_6m_AL = 0
count_dbt_6m_BL = 0
count_dbt_6m_CC = 0
count_dbt_6m_CD = 0
count_dbt_6m_CV = 0
count_dbt_6m_GL = 0
count_dbt_6m_HL = 0
count_dbt_6m_LAS = 0
count_dbt_6m_MFBL = 0
count_dbt_6m_MFHL = 0
count_dbt_6m_MFOT = 0
count_dbt_6m_OTH = 0
count_dbt_6m_PL = 0
count_dbt_6m_PLBL = 0
count_dbt_6m_RL = 0
count_dbt_6m_SCC = 0
count_dbt_6m_SEL = 0

DBT1Y_AL = list()
DBT1Y_BL = list()
DBT1Y_CC = list()
DBT1Y_CD = list()
DBT1Y_CV = list()
DBT1Y_GL = list()
DBT1Y_HL = list()
DBT1Y_LAS = list()
DBT1Y_MFBL = list()
DBT1Y_MFHL = list()
DBT1Y_MFOT = list()
DBT1Y_OTH = list()
DBT1Y_PL = list()
DBT1Y_PLBL = list()
DBT1Y_RL = list()
DBT1Y_SCC = list()
DBT1Y_SEL = list()

count_dbt_1y_list_AL = list()
count_dbt_1y_list_BL = list()
count_dbt_1y_list_CC = list()
count_dbt_1y_list_CD = list()
count_dbt_1y_list_CV = list()
count_dbt_1y_list_GL = list()
count_dbt_1y_list_HL = list()
count_dbt_1y_list_LAS = list()
count_dbt_1y_list_MFBL = list()
count_dbt_1y_list_MFHL = list()
count_dbt_1y_list_MFOT = list()
count_dbt_1y_list_OTH = list()
count_dbt_1y_list_PL = list()
count_dbt_1y_list_PLBL = list()
count_dbt_1y_list_RL = list()
count_dbt_1y_list_SCC = list()
count_dbt_1y_list_SEL = list()

count_dbt_1y_AL = 0
count_dbt_1y_BL = 0
count_dbt_1y_CC = 0
count_dbt_1y_CD = 0
count_dbt_1y_CV = 0
count_dbt_1y_GL = 0
count_dbt_1y_HL = 0
count_dbt_1y_LAS = 0
count_dbt_1y_MFBL = 0
count_dbt_1y_MFHL = 0
count_dbt_1y_MFOT = 0
count_dbt_1y_OTH = 0
count_dbt_1y_PL = 0
count_dbt_1y_PLBL = 0
count_dbt_1y_RL = 0
count_dbt_1y_SCC = 0
count_dbt_1y_SEL = 0

DBT2Y_AL = list()
DBT2Y_BL = list()
DBT2Y_CC = list()
DBT2Y_CD = list()
DBT2Y_CV = list()
DBT2Y_GL = list()
DBT2Y_HL = list()
DBT2Y_LAS = list()
DBT2Y_MFBL = list()
DBT2Y_MFHL = list()
DBT2Y_MFOT = list()
DBT2Y_OTH = list()
DBT2Y_PL = list()
DBT2Y_PLBL = list()
DBT2Y_RL = list()
DBT2Y_SCC = list()
DBT2Y_SEL = list()

count_dbt_2y_list_AL = list()
count_dbt_2y_list_BL = list()
count_dbt_2y_list_CC = list()
count_dbt_2y_list_CD = list()
count_dbt_2y_list_CV = list()
count_dbt_2y_list_GL = list()
count_dbt_2y_list_HL = list()
count_dbt_2y_list_LAS = list()
count_dbt_2y_list_MFBL = list()
count_dbt_2y_list_MFHL = list()
count_dbt_2y_list_MFOT = list()
count_dbt_2y_list_OTH = list()
count_dbt_2y_list_PL = list()
count_dbt_2y_list_PLBL = list()
count_dbt_2y_list_RL = list()
count_dbt_2y_list_SCC = list()
count_dbt_2y_list_SEL = list()

count_dbt_2y_AL = 0
count_dbt_2y_BL = 0
count_dbt_2y_CC = 0
count_dbt_2y_CD = 0
count_dbt_2y_CV = 0
count_dbt_2y_GL = 0
count_dbt_2y_HL = 0
count_dbt_2y_LAS = 0
count_dbt_2y_MFBL = 0
count_dbt_2y_MFHL = 0
count_dbt_2y_MFOT = 0
count_dbt_2y_OTH = 0
count_dbt_2y_PL = 0
count_dbt_2y_PLBL = 0
count_dbt_2y_RL = 0
count_dbt_2y_SCC = 0
count_dbt_2y_SEL = 0

DBT3Y_AL = list()
DBT3Y_BL = list()
DBT3Y_CC = list()
DBT3Y_CD = list()
DBT3Y_CV = list()
DBT3Y_GL = list()
DBT3Y_HL = list()
DBT3Y_LAS = list()
DBT3Y_MFBL = list()
DBT3Y_MFHL = list()
DBT3Y_MFOT = list()
DBT3Y_OTH = list()
DBT3Y_PL = list()
DBT3Y_PLBL = list()
DBT3Y_RL = list()
DBT3Y_SCC = list()
DBT3Y_SEL = list()

count_dbt_3y_list_AL = list()
count_dbt_3y_list_BL = list()
count_dbt_3y_list_CC = list()
count_dbt_3y_list_CD = list()
count_dbt_3y_list_CV = list()
count_dbt_3y_list_GL = list()
count_dbt_3y_list_HL = list()
count_dbt_3y_list_LAS = list()
count_dbt_3y_list_MFBL = list()
count_dbt_3y_list_MFHL = list()
count_dbt_3y_list_MFOT = list()
count_dbt_3y_list_OTH = list()
count_dbt_3y_list_PL = list()
count_dbt_3y_list_PLBL = list()
count_dbt_3y_list_RL = list()
count_dbt_3y_list_SCC = list()
count_dbt_3y_list_SEL = list()

count_dbt_3y_AL = 0
count_dbt_3y_BL = 0
count_dbt_3y_CC = 0
count_dbt_3y_CD = 0
count_dbt_3y_CV = 0
count_dbt_3y_GL = 0
count_dbt_3y_HL = 0
count_dbt_3y_LAS = 0
count_dbt_3y_MFBL = 0
count_dbt_3y_MFHL = 0
count_dbt_3y_MFOT = 0
count_dbt_3y_OTH = 0
count_dbt_3y_PL = 0
count_dbt_3y_PLBL = 0
count_dbt_3y_RL = 0
count_dbt_3y_SCC = 0
count_dbt_3y_SEL = 0

LOS1M = list()
count_los_list_1m = list()
count_los_1m = 0

LOS3M = list()
count_los_list_3m = list()
count_los_3m = 0

LOS6M = list()
count_los_list_6m = list()
count_los_6m = 0

LOS1Y = list()
count_los_list_1y = list()
count_los_1y = 0

LOS2Y = list()
count_los_list_2y = list()
count_los_2y = 0

LOS3Y = list()
count_los_list_3y = list()
count_los_3y = 0

LOS1M_AL = list()
LOS1M_BL = list()
LOS1M_CC = list()
LOS1M_CD = list()
LOS1M_CV = list()
LOS1M_GL = list()
LOS1M_HL = list()
LOS1M_LAS = list()
LOS1M_MFBL = list()
LOS1M_MFHL = list()
LOS1M_MFOT = list()
LOS1M_OTH = list()
LOS1M_PL = list()
LOS1M_PLBL = list()
LOS1M_RL = list()
LOS1M_SCC = list()
LOS1M_SEL = list()

count_los_1m_list_AL = list()
count_los_1m_list_BL = list()
count_los_1m_list_CC = list()
count_los_1m_list_CD = list()
count_los_1m_list_CV = list()
count_los_1m_list_GL = list()
count_los_1m_list_HL = list()
count_los_1m_list_LAS = list()
count_los_1m_list_MFBL = list()
count_los_1m_list_MFHL = list()
count_los_1m_list_MFOT = list()
count_los_1m_list_OTH = list()
count_los_1m_list_PL = list()
count_los_1m_list_PLBL = list()
count_los_1m_list_RL = list()
count_los_1m_list_SCC = list()
count_los_1m_list_SEL = list()

count_los_1m_AL = 0
count_los_1m_BL = 0
count_los_1m_CC = 0
count_los_1m_CD = 0
count_los_1m_CV = 0
count_los_1m_GL = 0
count_los_1m_HL = 0
count_los_1m_LAS = 0
count_los_1m_MFBL = 0
count_los_1m_MFHL = 0
count_los_1m_MFOT = 0
count_los_1m_OTH = 0
count_los_1m_PL = 0
count_los_1m_PLBL = 0
count_los_1m_RL = 0
count_los_1m_SCC = 0
count_los_1m_SEL = 0

LOS3M_AL = list()
LOS3M_BL = list()
LOS3M_CC = list()
LOS3M_CD = list()
LOS3M_CV = list()
LOS3M_GL = list()
LOS3M_HL = list()
LOS3M_LAS = list()
LOS3M_MFBL = list()
LOS3M_MFHL = list()
LOS3M_MFOT = list()
LOS3M_OTH = list()
LOS3M_PL = list()
LOS3M_PLBL = list()
LOS3M_RL = list()
LOS3M_SCC = list()
LOS3M_SEL = list()

count_los_3m_list_AL = list()
count_los_3m_list_BL = list()
count_los_3m_list_CC = list()
count_los_3m_list_CD = list()
count_los_3m_list_CV = list()
count_los_3m_list_GL = list()
count_los_3m_list_HL = list()
count_los_3m_list_LAS = list()
count_los_3m_list_MFBL = list()
count_los_3m_list_MFHL = list()
count_los_3m_list_MFOT = list()
count_los_3m_list_OTH = list()
count_los_3m_list_PL = list()
count_los_3m_list_PLBL = list()
count_los_3m_list_RL = list()
count_los_3m_list_SCC = list()
count_los_3m_list_SEL = list()

count_los_3m_AL = 0
count_los_3m_BL = 0
count_los_3m_CC = 0
count_los_3m_CD = 0
count_los_3m_CV = 0
count_los_3m_GL = 0
count_los_3m_HL = 0
count_los_3m_LAS = 0
count_los_3m_MFBL = 0
count_los_3m_MFHL = 0
count_los_3m_MFOT = 0
count_los_3m_OTH = 0
count_los_3m_PL = 0
count_los_3m_PLBL = 0
count_los_3m_RL = 0
count_los_3m_SCC = 0
count_los_3m_SEL = 0

LOS6M_AL = list()
LOS6M_BL = list()
LOS6M_CC = list()
LOS6M_CD = list()
LOS6M_CV = list()
LOS6M_GL = list()
LOS6M_HL = list()
LOS6M_LAS = list()
LOS6M_MFBL = list()
LOS6M_MFHL = list()
LOS6M_MFOT = list()
LOS6M_OTH = list()
LOS6M_PL = list()
LOS6M_PLBL = list()
LOS6M_RL = list()
LOS6M_SCC = list()
LOS6M_SEL = list()

count_los_6m_list_AL = list()
count_los_6m_list_BL = list()
count_los_6m_list_CC = list()
count_los_6m_list_CD = list()
count_los_6m_list_CV = list()
count_los_6m_list_GL = list()
count_los_6m_list_HL = list()
count_los_6m_list_LAS = list()
count_los_6m_list_MFBL = list()
count_los_6m_list_MFHL = list()
count_los_6m_list_MFOT = list()
count_los_6m_list_OTH = list()
count_los_6m_list_PL = list()
count_los_6m_list_PLBL = list()
count_los_6m_list_RL = list()
count_los_6m_list_SCC = list()
count_los_6m_list_SEL = list()

count_los_6m_AL = 0
count_los_6m_BL = 0
count_los_6m_CC = 0
count_los_6m_CD = 0
count_los_6m_CV = 0
count_los_6m_GL = 0
count_los_6m_HL = 0
count_los_6m_LAS = 0
count_los_6m_MFBL = 0
count_los_6m_MFHL = 0
count_los_6m_MFOT = 0
count_los_6m_OTH = 0
count_los_6m_PL = 0
count_los_6m_PLBL = 0
count_los_6m_RL = 0
count_los_6m_SCC = 0
count_los_6m_SEL = 0

LOS1Y_AL = list()
LOS1Y_BL = list()
LOS1Y_CC = list()
LOS1Y_CD = list()
LOS1Y_CV = list()
LOS1Y_GL = list()
LOS1Y_HL = list()
LOS1Y_LAS = list()
LOS1Y_MFBL = list()
LOS1Y_MFHL = list()
LOS1Y_MFOT = list()
LOS1Y_OTH = list()
LOS1Y_PL = list()
LOS1Y_PLBL = list()
LOS1Y_RL = list()
LOS1Y_SCC = list()
LOS1Y_SEL = list()

count_los_1y_list_AL = list()
count_los_1y_list_BL = list()
count_los_1y_list_CC = list()
count_los_1y_list_CD = list()
count_los_1y_list_CV = list()
count_los_1y_list_GL = list()
count_los_1y_list_HL = list()
count_los_1y_list_LAS = list()
count_los_1y_list_MFBL = list()
count_los_1y_list_MFHL = list()
count_los_1y_list_MFOT = list()
count_los_1y_list_OTH = list()
count_los_1y_list_PL = list()
count_los_1y_list_PLBL = list()
count_los_1y_list_RL = list()
count_los_1y_list_SCC = list()
count_los_1y_list_SEL = list()

count_los_1y_AL = 0
count_los_1y_BL = 0
count_los_1y_CC = 0
count_los_1y_CD = 0
count_los_1y_CV = 0
count_los_1y_GL = 0
count_los_1y_HL = 0
count_los_1y_LAS = 0
count_los_1y_MFBL = 0
count_los_1y_MFHL = 0
count_los_1y_MFOT = 0
count_los_1y_OTH = 0
count_los_1y_PL = 0
count_los_1y_PLBL = 0
count_los_1y_RL = 0
count_los_1y_SCC = 0
count_los_1y_SEL = 0

LOS2Y_AL = list()
LOS2Y_BL = list()
LOS2Y_CC = list()
LOS2Y_CD = list()
LOS2Y_CV = list()
LOS2Y_GL = list()
LOS2Y_HL = list()
LOS2Y_LAS = list()
LOS2Y_MFBL = list()
LOS2Y_MFHL = list()
LOS2Y_MFOT = list()
LOS2Y_OTH = list()
LOS2Y_PL = list()
LOS2Y_PLBL = list()
LOS2Y_RL = list()
LOS2Y_SCC = list()
LOS2Y_SEL = list()

count_los_2y_list_AL = list()
count_los_2y_list_BL = list()
count_los_2y_list_CC = list()
count_los_2y_list_CD = list()
count_los_2y_list_CV = list()
count_los_2y_list_GL = list()
count_los_2y_list_HL = list()
count_los_2y_list_LAS = list()
count_los_2y_list_MFBL = list()
count_los_2y_list_MFHL = list()
count_los_2y_list_MFOT = list()
count_los_2y_list_OTH = list()
count_los_2y_list_PL = list()
count_los_2y_list_PLBL = list()
count_los_2y_list_RL = list()
count_los_2y_list_SCC = list()
count_los_2y_list_SEL = list()

count_los_2y_AL = 0
count_los_2y_BL = 0
count_los_2y_CC = 0
count_los_2y_CD = 0
count_los_2y_CV = 0
count_los_2y_GL = 0
count_los_2y_HL = 0
count_los_2y_LAS = 0
count_los_2y_MFBL = 0
count_los_2y_MFHL = 0
count_los_2y_MFOT = 0
count_los_2y_OTH = 0
count_los_2y_PL = 0
count_los_2y_PLBL = 0
count_los_2y_RL = 0
count_los_2y_SCC = 0
count_los_2y_SEL = 0

LOS3Y_AL = list()
LOS3Y_BL = list()
LOS3Y_CC = list()
LOS3Y_CD = list()
LOS3Y_CV = list()
LOS3Y_GL = list()
LOS3Y_HL = list()
LOS3Y_LAS = list()
LOS3Y_MFBL = list()
LOS3Y_MFHL = list()
LOS3Y_MFOT = list()
LOS3Y_OTH = list()
LOS3Y_PL = list()
LOS3Y_PLBL = list()
LOS3Y_RL = list()
LOS3Y_SCC = list()
LOS3Y_SEL = list()

count_los_3y_list_AL = list()
count_los_3y_list_BL = list()
count_los_3y_list_CC = list()
count_los_3y_list_CD = list()
count_los_3y_list_CV = list()
count_los_3y_list_GL = list()
count_los_3y_list_HL = list()
count_los_3y_list_LAS = list()
count_los_3y_list_MFBL = list()
count_los_3y_list_MFHL = list()
count_los_3y_list_MFOT = list()
count_los_3y_list_OTH = list()
count_los_3y_list_PL = list()
count_los_3y_list_PLBL = list()
count_los_3y_list_RL = list()
count_los_3y_list_SCC = list()
count_los_3y_list_SEL = list()

count_los_3y_AL = 0
count_los_3y_BL = 0
count_los_3y_CC = 0
count_los_3y_CD = 0
count_los_3y_CV = 0
count_los_3y_GL = 0
count_los_3y_HL = 0
count_los_3y_LAS = 0
count_los_3y_MFBL = 0
count_los_3y_MFHL = 0
count_los_3y_MFOT = 0
count_los_3y_OTH = 0
count_los_3y_PL = 0
count_los_3y_PLBL = 0
count_los_3y_RL = 0
count_los_3y_SCC = 0
count_los_3y_SEL = 0

XXX1M = list()
count_xxx_list_1m = list()
count_xxx_1m = 0

XXX3M = list()
count_xxx_list_3m = list()
count_xxx_3m = 0

XXX6M = list()
count_xxx_list_6m = list()
count_xxx_6m = 0

XXX1Y = list()
count_xxx_list_1y = list()
count_xxx_1y = 0

XXX2Y = list()
count_xxx_list_2y = list()
count_xxx_2y = 0

XXX3Y = list()
count_xxx_list_3y = list()
count_xxx_3y = 0

XXX1M_AL = list()
XXX1M_BL = list()
XXX1M_CC = list()
XXX1M_CD = list()
XXX1M_CV = list()
XXX1M_GL = list()
XXX1M_HL = list()
XXX1M_LAS = list()
XXX1M_MFBL = list()
XXX1M_MFHL = list()
XXX1M_MFOT = list()
XXX1M_OTH = list()
XXX1M_PL = list()
XXX1M_PLBL = list()
XXX1M_RL = list()
XXX1M_SCC = list()
XXX1M_SEL = list()

count_xxx_1m_list_AL = list()
count_xxx_1m_list_BL = list()
count_xxx_1m_list_CC = list()
count_xxx_1m_list_CD = list()
count_xxx_1m_list_CV = list()
count_xxx_1m_list_GL = list()
count_xxx_1m_list_HL = list()
count_xxx_1m_list_LAS = list()
count_xxx_1m_list_MFBL = list()
count_xxx_1m_list_MFHL = list()
count_xxx_1m_list_MFOT = list()
count_xxx_1m_list_OTH = list()
count_xxx_1m_list_PL = list()
count_xxx_1m_list_PLBL = list()
count_xxx_1m_list_RL = list()
count_xxx_1m_list_SCC = list()
count_xxx_1m_list_SEL = list()

count_xxx_1m_AL = 0
count_xxx_1m_BL = 0
count_xxx_1m_CC = 0
count_xxx_1m_CD = 0
count_xxx_1m_CV = 0
count_xxx_1m_GL = 0
count_xxx_1m_HL = 0
count_xxx_1m_LAS = 0
count_xxx_1m_MFBL = 0
count_xxx_1m_MFHL = 0
count_xxx_1m_MFOT = 0
count_xxx_1m_OTH = 0
count_xxx_1m_PL = 0
count_xxx_1m_PLBL = 0
count_xxx_1m_RL = 0
count_xxx_1m_SCC = 0
count_xxx_1m_SEL = 0

XXX3M_AL = list()
XXX3M_BL = list()
XXX3M_CC = list()
XXX3M_CD = list()
XXX3M_CV = list()
XXX3M_GL = list()
XXX3M_HL = list()
XXX3M_LAS = list()
XXX3M_MFBL = list()
XXX3M_MFHL = list()
XXX3M_MFOT = list()
XXX3M_OTH = list()
XXX3M_PL = list()
XXX3M_PLBL = list()
XXX3M_RL = list()
XXX3M_SCC = list()
XXX3M_SEL = list()

count_xxx_3m_list_AL = list()
count_xxx_3m_list_BL = list()
count_xxx_3m_list_CC = list()
count_xxx_3m_list_CD = list()
count_xxx_3m_list_CV = list()
count_xxx_3m_list_GL = list()
count_xxx_3m_list_HL = list()
count_xxx_3m_list_LAS = list()
count_xxx_3m_list_MFBL = list()
count_xxx_3m_list_MFHL = list()
count_xxx_3m_list_MFOT = list()
count_xxx_3m_list_OTH = list()
count_xxx_3m_list_PL = list()
count_xxx_3m_list_PLBL = list()
count_xxx_3m_list_RL = list()
count_xxx_3m_list_SCC = list()
count_xxx_3m_list_SEL = list()

count_xxx_3m_AL = 0
count_xxx_3m_BL = 0
count_xxx_3m_CC = 0
count_xxx_3m_CD = 0
count_xxx_3m_CV = 0
count_xxx_3m_GL = 0
count_xxx_3m_HL = 0
count_xxx_3m_LAS = 0
count_xxx_3m_MFBL = 0
count_xxx_3m_MFHL = 0
count_xxx_3m_MFOT = 0
count_xxx_3m_OTH = 0
count_xxx_3m_PL = 0
count_xxx_3m_PLBL = 0
count_xxx_3m_RL = 0
count_xxx_3m_SCC = 0
count_xxx_3m_SEL = 0

XXX6M_AL = list()
XXX6M_BL = list()
XXX6M_CC = list()
XXX6M_CD = list()
XXX6M_CV = list()
XXX6M_GL = list()
XXX6M_HL = list()
XXX6M_LAS = list()
XXX6M_MFBL = list()
XXX6M_MFHL = list()
XXX6M_MFOT = list()
XXX6M_OTH = list()
XXX6M_PL = list()
XXX6M_PLBL = list()
XXX6M_RL = list()
XXX6M_SCC = list()
XXX6M_SEL = list()

count_xxx_6m_list_AL = list()
count_xxx_6m_list_BL = list()
count_xxx_6m_list_CC = list()
count_xxx_6m_list_CD = list()
count_xxx_6m_list_CV = list()
count_xxx_6m_list_GL = list()
count_xxx_6m_list_HL = list()
count_xxx_6m_list_LAS = list()
count_xxx_6m_list_MFBL = list()
count_xxx_6m_list_MFHL = list()
count_xxx_6m_list_MFOT = list()
count_xxx_6m_list_OTH = list()
count_xxx_6m_list_PL = list()
count_xxx_6m_list_PLBL = list()
count_xxx_6m_list_RL = list()
count_xxx_6m_list_SCC = list()
count_xxx_6m_list_SEL = list()

count_xxx_6m_AL = 0
count_xxx_6m_BL = 0
count_xxx_6m_CC = 0
count_xxx_6m_CD = 0
count_xxx_6m_CV = 0
count_xxx_6m_GL = 0
count_xxx_6m_HL = 0
count_xxx_6m_LAS = 0
count_xxx_6m_MFBL = 0
count_xxx_6m_MFHL = 0
count_xxx_6m_MFOT = 0
count_xxx_6m_OTH = 0
count_xxx_6m_PL = 0
count_xxx_6m_PLBL = 0
count_xxx_6m_RL = 0
count_xxx_6m_SCC = 0
count_xxx_6m_SEL = 0

XXX1Y_AL = list()
XXX1Y_BL = list()
XXX1Y_CC = list()
XXX1Y_CD = list()
XXX1Y_CV = list()
XXX1Y_GL = list()
XXX1Y_HL = list()
XXX1Y_LAS = list()
XXX1Y_MFBL = list()
XXX1Y_MFHL = list()
XXX1Y_MFOT = list()
XXX1Y_OTH = list()
XXX1Y_PL = list()
XXX1Y_PLBL = list()
XXX1Y_RL = list()
XXX1Y_SCC = list()
XXX1Y_SEL = list()

count_xxx_1y_list_AL = list()
count_xxx_1y_list_BL = list()
count_xxx_1y_list_CC = list()
count_xxx_1y_list_CD = list()
count_xxx_1y_list_CV = list()
count_xxx_1y_list_GL = list()
count_xxx_1y_list_HL = list()
count_xxx_1y_list_LAS = list()
count_xxx_1y_list_MFBL = list()
count_xxx_1y_list_MFHL = list()
count_xxx_1y_list_MFOT = list()
count_xxx_1y_list_OTH = list()
count_xxx_1y_list_PL = list()
count_xxx_1y_list_PLBL = list()
count_xxx_1y_list_RL = list()
count_xxx_1y_list_SCC = list()
count_xxx_1y_list_SEL = list()

count_xxx_1y_AL = 0
count_xxx_1y_BL = 0
count_xxx_1y_CC = 0
count_xxx_1y_CD = 0
count_xxx_1y_CV = 0
count_xxx_1y_GL = 0
count_xxx_1y_HL = 0
count_xxx_1y_LAS = 0
count_xxx_1y_MFBL = 0
count_xxx_1y_MFHL = 0
count_xxx_1y_MFOT = 0
count_xxx_1y_OTH = 0
count_xxx_1y_PL = 0
count_xxx_1y_PLBL = 0
count_xxx_1y_RL = 0
count_xxx_1y_SCC = 0
count_xxx_1y_SEL = 0

XXX2Y_AL = list()
XXX2Y_BL = list()
XXX2Y_CC = list()
XXX2Y_CD = list()
XXX2Y_CV = list()
XXX2Y_GL = list()
XXX2Y_HL = list()
XXX2Y_LAS = list()
XXX2Y_MFBL = list()
XXX2Y_MFHL = list()
XXX2Y_MFOT = list()
XXX2Y_OTH = list()
XXX2Y_PL = list()
XXX2Y_PLBL = list()
XXX2Y_RL = list()
XXX2Y_SCC = list()
XXX2Y_SEL = list()

count_xxx_2y_list_AL = list()
count_xxx_2y_list_BL = list()
count_xxx_2y_list_CC = list()
count_xxx_2y_list_CD = list()
count_xxx_2y_list_CV = list()
count_xxx_2y_list_GL = list()
count_xxx_2y_list_HL = list()
count_xxx_2y_list_LAS = list()
count_xxx_2y_list_MFBL = list()
count_xxx_2y_list_MFHL = list()
count_xxx_2y_list_MFOT = list()
count_xxx_2y_list_OTH = list()
count_xxx_2y_list_PL = list()
count_xxx_2y_list_PLBL = list()
count_xxx_2y_list_RL = list()
count_xxx_2y_list_SCC = list()
count_xxx_2y_list_SEL = list()

count_xxx_2y_AL = 0
count_xxx_2y_BL = 0
count_xxx_2y_CC = 0
count_xxx_2y_CD = 0
count_xxx_2y_CV = 0
count_xxx_2y_GL = 0
count_xxx_2y_HL = 0
count_xxx_2y_LAS = 0
count_xxx_2y_MFBL = 0
count_xxx_2y_MFHL = 0
count_xxx_2y_MFOT = 0
count_xxx_2y_OTH = 0
count_xxx_2y_PL = 0
count_xxx_2y_PLBL = 0
count_xxx_2y_RL = 0
count_xxx_2y_SCC = 0
count_xxx_2y_SEL = 0

XXX3Y_AL = list()
XXX3Y_BL = list()
XXX3Y_CC = list()
XXX3Y_CD = list()
XXX3Y_CV = list()
XXX3Y_GL = list()
XXX3Y_HL = list()
XXX3Y_LAS = list()
XXX3Y_MFBL = list()
XXX3Y_MFHL = list()
XXX3Y_MFOT = list()
XXX3Y_OTH = list()
XXX3Y_PL = list()
XXX3Y_PLBL = list()
XXX3Y_RL = list()
XXX3Y_SCC = list()
XXX3Y_SEL = list()

count_xxx_3y_list_AL = list()
count_xxx_3y_list_BL = list()
count_xxx_3y_list_CC = list()
count_xxx_3y_list_CD = list()
count_xxx_3y_list_CV = list()
count_xxx_3y_list_GL = list()
count_xxx_3y_list_HL = list()
count_xxx_3y_list_LAS = list()
count_xxx_3y_list_MFBL = list()
count_xxx_3y_list_MFHL = list()
count_xxx_3y_list_MFOT = list()
count_xxx_3y_list_OTH = list()
count_xxx_3y_list_PL = list()
count_xxx_3y_list_PLBL = list()
count_xxx_3y_list_RL = list()
count_xxx_3y_list_SCC = list()
count_xxx_3y_list_SEL = list()

count_xxx_3y_AL = 0
count_xxx_3y_BL = 0
count_xxx_3y_CC = 0
count_xxx_3y_CD = 0
count_xxx_3y_CV = 0
count_xxx_3y_GL = 0
count_xxx_3y_HL = 0
count_xxx_3y_LAS = 0
count_xxx_3y_MFBL = 0
count_xxx_3y_MFHL = 0
count_xxx_3y_MFOT = 0
count_xxx_3y_OTH = 0
count_xxx_3y_PL = 0
count_xxx_3y_PLBL = 0
count_xxx_3y_RL = 0
count_xxx_3y_SCC = 0
count_xxx_3y_SEL = 0

SMA1M = list()
count_sma_list_1m = list()
count_sma_1m = 0

SMA3M = list()
count_sma_list_3m = list()
count_sma_3m = 0

SMA6M = list()
count_sma_list_6m = list()
count_sma_6m = 0

SMA1Y = list()
count_sma_list_1y = list()
count_sma_1y = 0

SMA2Y = list()
count_sma_list_2y = list()
count_sma_2y = 0

SMA3Y = list()
count_sma_list_3y = list()
count_sma_3y = 0

SMA1M_AL = list()
SMA1M_BL = list()
SMA1M_CC = list()
SMA1M_CD = list()
SMA1M_CV = list()
SMA1M_GL = list()
SMA1M_HL = list()
SMA1M_LAS = list()
SMA1M_MFBL = list()
SMA1M_MFHL = list()
SMA1M_MFOT = list()
SMA1M_OTH = list()
SMA1M_PL = list()
SMA1M_PLBL = list()
SMA1M_RL = list()
SMA1M_SCC = list()
SMA1M_SEL = list()

count_sma_1m_list_AL = list()
count_sma_1m_list_BL = list()
count_sma_1m_list_CC = list()
count_sma_1m_list_CD = list()
count_sma_1m_list_CV = list()
count_sma_1m_list_GL = list()
count_sma_1m_list_HL = list()
count_sma_1m_list_LAS = list()
count_sma_1m_list_MFBL = list()
count_sma_1m_list_MFHL = list()
count_sma_1m_list_MFOT = list()
count_sma_1m_list_OTH = list()
count_sma_1m_list_PL = list()
count_sma_1m_list_PLBL = list()
count_sma_1m_list_RL = list()
count_sma_1m_list_SCC = list()
count_sma_1m_list_SEL = list()

count_sma_1m_AL = 0
count_sma_1m_BL = 0
count_sma_1m_CC = 0
count_sma_1m_CD = 0
count_sma_1m_CV = 0
count_sma_1m_GL = 0
count_sma_1m_HL = 0
count_sma_1m_LAS = 0
count_sma_1m_MFBL = 0
count_sma_1m_MFHL = 0
count_sma_1m_MFOT = 0
count_sma_1m_OTH = 0
count_sma_1m_PL = 0
count_sma_1m_PLBL = 0
count_sma_1m_RL = 0
count_sma_1m_SCC = 0
count_sma_1m_SEL = 0

SMA3M_AL = list()
SMA3M_BL = list()
SMA3M_CC = list()
SMA3M_CD = list()
SMA3M_CV = list()
SMA3M_GL = list()
SMA3M_HL = list()
SMA3M_LAS = list()
SMA3M_MFBL = list()
SMA3M_MFHL = list()
SMA3M_MFOT = list()
SMA3M_OTH = list()
SMA3M_PL = list()
SMA3M_PLBL = list()
SMA3M_RL = list()
SMA3M_SCC = list()
SMA3M_SEL = list()

count_sma_3m_list_AL = list()
count_sma_3m_list_BL = list()
count_sma_3m_list_CC = list()
count_sma_3m_list_CD = list()
count_sma_3m_list_CV = list()
count_sma_3m_list_GL = list()
count_sma_3m_list_HL = list()
count_sma_3m_list_LAS = list()
count_sma_3m_list_MFBL = list()
count_sma_3m_list_MFHL = list()
count_sma_3m_list_MFOT = list()
count_sma_3m_list_OTH = list()
count_sma_3m_list_PL = list()
count_sma_3m_list_PLBL = list()
count_sma_3m_list_RL = list()
count_sma_3m_list_SCC = list()
count_sma_3m_list_SEL = list()

count_sma_3m_AL = 0
count_sma_3m_BL = 0
count_sma_3m_CC = 0
count_sma_3m_CD = 0
count_sma_3m_CV = 0
count_sma_3m_GL = 0
count_sma_3m_HL = 0
count_sma_3m_LAS = 0
count_sma_3m_MFBL = 0
count_sma_3m_MFHL = 0
count_sma_3m_MFOT = 0
count_sma_3m_OTH = 0
count_sma_3m_PL = 0
count_sma_3m_PLBL = 0
count_sma_3m_RL = 0
count_sma_3m_SCC = 0
count_sma_3m_SEL = 0

SMA6M_AL = list()
SMA6M_BL = list()
SMA6M_CC = list()
SMA6M_CD = list()
SMA6M_CV = list()
SMA6M_GL = list()
SMA6M_HL = list()
SMA6M_LAS = list()
SMA6M_MFBL = list()
SMA6M_MFHL = list()
SMA6M_MFOT = list()
SMA6M_OTH = list()
SMA6M_PL = list()
SMA6M_PLBL = list()
SMA6M_RL = list()
SMA6M_SCC = list()
SMA6M_SEL = list()

count_sma_6m_list_AL = list()
count_sma_6m_list_BL = list()
count_sma_6m_list_CC = list()
count_sma_6m_list_CD = list()
count_sma_6m_list_CV = list()
count_sma_6m_list_GL = list()
count_sma_6m_list_HL = list()
count_sma_6m_list_LAS = list()
count_sma_6m_list_MFBL = list()
count_sma_6m_list_MFHL = list()
count_sma_6m_list_MFOT = list()
count_sma_6m_list_OTH = list()
count_sma_6m_list_PL = list()
count_sma_6m_list_PLBL = list()
count_sma_6m_list_RL = list()
count_sma_6m_list_SCC = list()
count_sma_6m_list_SEL = list()

count_sma_6m_AL = 0
count_sma_6m_BL = 0
count_sma_6m_CC = 0
count_sma_6m_CD = 0
count_sma_6m_CV = 0
count_sma_6m_GL = 0
count_sma_6m_HL = 0
count_sma_6m_LAS = 0
count_sma_6m_MFBL = 0
count_sma_6m_MFHL = 0
count_sma_6m_MFOT = 0
count_sma_6m_OTH = 0
count_sma_6m_PL = 0
count_sma_6m_PLBL = 0
count_sma_6m_RL = 0
count_sma_6m_SCC = 0
count_sma_6m_SEL = 0

SMA1Y_AL = list()
SMA1Y_BL = list()
SMA1Y_CC = list()
SMA1Y_CD = list()
SMA1Y_CV = list()
SMA1Y_GL = list()
SMA1Y_HL = list()
SMA1Y_LAS = list()
SMA1Y_MFBL = list()
SMA1Y_MFHL = list()
SMA1Y_MFOT = list()
SMA1Y_OTH = list()
SMA1Y_PL = list()
SMA1Y_PLBL = list()
SMA1Y_RL = list()
SMA1Y_SCC = list()
SMA1Y_SEL = list()

count_sma_1y_list_AL = list()
count_sma_1y_list_BL = list()
count_sma_1y_list_CC = list()
count_sma_1y_list_CD = list()
count_sma_1y_list_CV = list()
count_sma_1y_list_GL = list()
count_sma_1y_list_HL = list()
count_sma_1y_list_LAS = list()
count_sma_1y_list_MFBL = list()
count_sma_1y_list_MFHL = list()
count_sma_1y_list_MFOT = list()
count_sma_1y_list_OTH = list()
count_sma_1y_list_PL = list()
count_sma_1y_list_PLBL = list()
count_sma_1y_list_RL = list()
count_sma_1y_list_SCC = list()
count_sma_1y_list_SEL = list()

count_sma_1y_AL = 0
count_sma_1y_BL = 0
count_sma_1y_CC = 0
count_sma_1y_CD = 0
count_sma_1y_CV = 0
count_sma_1y_GL = 0
count_sma_1y_HL = 0
count_sma_1y_LAS = 0
count_sma_1y_MFBL = 0
count_sma_1y_MFHL = 0
count_sma_1y_MFOT = 0
count_sma_1y_OTH = 0
count_sma_1y_PL = 0
count_sma_1y_PLBL = 0
count_sma_1y_RL = 0
count_sma_1y_SCC = 0
count_sma_1y_SEL = 0

SMA2Y_AL = list()
SMA2Y_BL = list()
SMA2Y_CC = list()
SMA2Y_CD = list()
SMA2Y_CV = list()
SMA2Y_GL = list()
SMA2Y_HL = list()
SMA2Y_LAS = list()
SMA2Y_MFBL = list()
SMA2Y_MFHL = list()
SMA2Y_MFOT = list()
SMA2Y_OTH = list()
SMA2Y_PL = list()
SMA2Y_PLBL = list()
SMA2Y_RL = list()
SMA2Y_SCC = list()
SMA2Y_SEL = list()

count_sma_2y_list_AL = list()
count_sma_2y_list_BL = list()
count_sma_2y_list_CC = list()
count_sma_2y_list_CD = list()
count_sma_2y_list_CV = list()
count_sma_2y_list_GL = list()
count_sma_2y_list_HL = list()
count_sma_2y_list_LAS = list()
count_sma_2y_list_MFBL = list()
count_sma_2y_list_MFHL = list()
count_sma_2y_list_MFOT = list()
count_sma_2y_list_OTH = list()
count_sma_2y_list_PL = list()
count_sma_2y_list_PLBL = list()
count_sma_2y_list_RL = list()
count_sma_2y_list_SCC = list()
count_sma_2y_list_SEL = list()

count_sma_2y_AL = 0
count_sma_2y_BL = 0
count_sma_2y_CC = 0
count_sma_2y_CD = 0
count_sma_2y_CV = 0
count_sma_2y_GL = 0
count_sma_2y_HL = 0
count_sma_2y_LAS = 0
count_sma_2y_MFBL = 0
count_sma_2y_MFHL = 0
count_sma_2y_MFOT = 0
count_sma_2y_OTH = 0
count_sma_2y_PL = 0
count_sma_2y_PLBL = 0
count_sma_2y_RL = 0
count_sma_2y_SCC = 0
count_sma_2y_SEL = 0

SMA3Y_AL = list()
SMA3Y_BL = list()
SMA3Y_CC = list()
SMA3Y_CD = list()
SMA3Y_CV = list()
SMA3Y_GL = list()
SMA3Y_HL = list()
SMA3Y_LAS = list()
SMA3Y_MFBL = list()
SMA3Y_MFHL = list()
SMA3Y_MFOT = list()
SMA3Y_OTH = list()
SMA3Y_PL = list()
SMA3Y_PLBL = list()
SMA3Y_RL = list()
SMA3Y_SCC = list()
SMA3Y_SEL = list()

count_sma_3y_list_AL = list()
count_sma_3y_list_BL = list()
count_sma_3y_list_CC = list()
count_sma_3y_list_CD = list()
count_sma_3y_list_CV = list()
count_sma_3y_list_GL = list()
count_sma_3y_list_HL = list()
count_sma_3y_list_LAS = list()
count_sma_3y_list_MFBL = list()
count_sma_3y_list_MFHL = list()
count_sma_3y_list_MFOT = list()
count_sma_3y_list_OTH = list()
count_sma_3y_list_PL = list()
count_sma_3y_list_PLBL = list()
count_sma_3y_list_RL = list()
count_sma_3y_list_SCC = list()
count_sma_3y_list_SEL = list()

count_sma_3y_AL = 0
count_sma_3y_BL = 0
count_sma_3y_CC = 0
count_sma_3y_CD = 0
count_sma_3y_CV = 0
count_sma_3y_GL = 0
count_sma_3y_HL = 0
count_sma_3y_LAS = 0
count_sma_3y_MFBL = 0
count_sma_3y_MFHL = 0
count_sma_3y_MFOT = 0
count_sma_3y_OTH = 0
count_sma_3y_PL = 0
count_sma_3y_PLBL = 0
count_sma_3y_RL = 0
count_sma_3y_SCC = 0
count_sma_3y_SEL = 0

grp_df = df.groupby('ID')

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    grp_slice.reset_index(drop=True, inplace=True)
    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['DPD30P3M_flag'][i] == 1) or (grp_slice['DPD30P3M_flag'][i] == 0):
            count_30_3m = count_30_3m + grp_slice['DPD30P3M_flag'][i]

        if (grp_slice['DPD60P3M_flag'][i] == 1) or (grp_slice['DPD60P3M_flag'][i] == 0):
            count_60_3m = count_60_3m + grp_slice['DPD60P3M_flag'][i]

        if (grp_slice['DPD90P3M_flag'][i] == 1) or (grp_slice['DPD90P3M_flag'][i] == 0):
            count_90_3m = count_90_3m + grp_slice['DPD90P3M_flag'][i]

        if (grp_slice['DPD30P6M_flag'][i] == 1) or (grp_slice['DPD30P6M_flag'][i] == 0):
            count_30_6m = count_30_6m + grp_slice['DPD30P6M_flag'][i]

        if (grp_slice['DPD60P6M_flag'][i] == 1) or (grp_slice['DPD60P6M_flag'][i] == 0):
            count_60_6m = count_60_6m + grp_slice['DPD60P6M_flag'][i]

        if (grp_slice['DPD90P6M_flag'][i] == 1) or (grp_slice['DPD90P6M_flag'][i] == 0):
            count_90_6m = count_90_6m + grp_slice['DPD90P6M_flag'][i]

        if (grp_slice['DPD30P1Y_flag'][i] == 1) or (grp_slice['DPD30P1Y_flag'][i] == 0):
            count_30_1y = count_30_1y + grp_slice['DPD30P1Y_flag'][i]

        if (grp_slice['DPD60P1Y_flag'][i] == 1) or (grp_slice['DPD60P1Y_flag'][i] == 0):
            count_60_1y = count_60_1y + grp_slice['DPD60P1Y_flag'][i]

        if (grp_slice['DPD90P1Y_flag'][i] == 1) or (grp_slice['DPD90P1Y_flag'][i] == 0):
            count_90_1y = count_90_1y + grp_slice['DPD90P1Y_flag'][i]

        if (grp_slice['DPD30P2Y_flag'][i] == 1) or (grp_slice['DPD30P2Y_flag'][i] == 0):
            count_30_2y = count_30_2y + grp_slice['DPD30P2Y_flag'][i]

        if (grp_slice['DPD60P2Y_flag'][i] == 1) or (grp_slice['DPD60P2Y_flag'][i] == 0):
            count_60_2y = count_60_2y + grp_slice['DPD60P2Y_flag'][i]

        if (grp_slice['DPD90P2Y_flag'][i] == 1) or (grp_slice['DPD90P2Y_flag'][i] == 0):
            count_90_2y = count_90_2y + grp_slice['DPD90P2Y_flag'][i]

        if (grp_slice['DPD30P3Y_flag'][i] == 1) or (grp_slice['DPD30P3Y_flag'][i] == 0):
            count_30_3y = count_30_3y + grp_slice['DPD30P3Y_flag'][i]

        if (grp_slice['DPD60P3Y_flag'][i] == 1) or (grp_slice['DPD60P3Y_flag'][i] == 0):
            count_60_3y = count_60_3y + grp_slice['DPD60P3Y_flag'][i]

        if (grp_slice['DPD90P3Y_flag'][i] == 1) or (grp_slice['DPD90P3Y_flag'][i] == 0):
            count_90_3y = count_90_3y + grp_slice['DPD90P3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_AL = count_30_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_BL = count_30_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_CC = count_30_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_CD = count_30_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_CV = count_30_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_GL = count_30_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_HL = count_30_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_LAS = count_30_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_MFBL = count_30_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_MFHL = count_30_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_MFOT = count_30_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_OTH = count_30_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_PL = count_30_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_PLBL = count_30_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_RL = count_30_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_SCC = count_30_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD30P3M_flag'][i] == 1):
            count_30_3m_SEL = count_30_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_AL = count_60_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_BL = count_60_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_CC = count_60_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_CD = count_60_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_CV = count_60_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_GL = count_60_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_HL = count_60_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_LAS = count_60_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_MFBL = count_60_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_MFHL = count_60_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_MFOT = count_60_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_OTH = count_60_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_PL = count_60_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_PLBL = count_60_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_RL = count_60_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_SCC = count_60_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD60P3M_flag'][i] == 1):
            count_60_3m_SEL = count_60_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_AL = count_90_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_BL = count_90_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_CC = count_90_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_CD = count_90_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_CV = count_90_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_GL = count_90_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_HL = count_90_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_LAS = count_90_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_MFBL = count_90_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_MFHL = count_90_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_MFOT = count_90_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_OTH = count_90_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_PL = count_90_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_PLBL = count_90_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_RL = count_90_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_SCC = count_90_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD90P3M_flag'][i] == 1):
            count_90_3m_SEL = count_90_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_AL = count_30_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_BL = count_30_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_CC = count_30_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_CD = count_30_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_CV = count_30_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_GL = count_30_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_HL = count_30_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_LAS = count_30_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_MFBL = count_30_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_MFHL = count_30_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_MFOT = count_30_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_OTH = count_30_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_PL = count_30_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_PLBL = count_30_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_RL = count_30_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_SCC = count_30_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD30P6M_flag'][i] == 1):
            count_30_6m_SEL = count_30_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_AL = count_60_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_BL = count_60_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_CC = count_60_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_CD = count_60_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_CV = count_60_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_GL = count_60_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_HL = count_60_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_LAS = count_60_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_MFBL = count_60_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_MFHL = count_60_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_MFOT = count_60_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_OTH = count_60_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_PL = count_60_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_PLBL = count_60_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_RL = count_60_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_SCC = count_60_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD60P6M_flag'][i] == 1):
            count_60_6m_SEL = count_60_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_AL = count_90_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_BL = count_90_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_CC = count_90_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_CD = count_90_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_CV = count_90_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_GL = count_90_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_HL = count_90_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_LAS = count_90_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_MFBL = count_90_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_MFHL = count_90_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_MFOT = count_90_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_OTH = count_90_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_PL = count_90_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_PLBL = count_90_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_RL = count_90_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_SCC = count_90_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD90P6M_flag'][i] == 1):
            count_90_6m_SEL = count_90_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_AL = count_30_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_BL = count_30_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_CC = count_30_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_CD = count_30_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_CV = count_30_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_GL = count_30_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_HL = count_30_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_LAS = count_30_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_MFBL = count_30_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_MFHL = count_30_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_MFOT = count_30_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_OTH = count_30_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_PL = count_30_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_PLBL = count_30_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_RL = count_30_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_SCC = count_30_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD30P1Y_flag'][i] == 1):
            count_30_1y_SEL = count_30_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_AL = count_60_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_BL = count_60_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_CC = count_60_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_CD = count_60_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_CV = count_60_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_GL = count_60_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_HL = count_60_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_LAS = count_60_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_MFBL = count_60_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_MFHL = count_60_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_MFOT = count_60_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_OTH = count_60_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_PL = count_60_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_PLBL = count_60_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_RL = count_60_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_SCC = count_60_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD60P1Y_flag'][i] == 1):
            count_60_1y_SEL = count_60_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_AL = count_90_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_BL = count_90_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_CC = count_90_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_CD = count_90_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_CV = count_90_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_GL = count_90_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_HL = count_90_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_LAS = count_90_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_MFBL = count_90_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_MFHL = count_90_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_MFOT = count_90_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_OTH = count_90_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_PL = count_90_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_PLBL = count_90_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_RL = count_90_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_SCC = count_90_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD90P1Y_flag'][i] == 1):
            count_90_1y_SEL = count_90_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_AL = count_30_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_BL = count_30_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_CC = count_30_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_CD = count_30_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_CV = count_30_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_GL = count_30_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_HL = count_30_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_LAS = count_30_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_MFBL = count_30_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_MFHL = count_30_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_MFOT = count_30_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_OTH = count_30_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_PL = count_30_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_PLBL = count_30_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_RL = count_30_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_SCC = count_30_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD30P2Y_flag'][i] == 1):
            count_30_2y_SEL = count_30_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_AL = count_60_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_BL = count_60_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_CC = count_60_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_CD = count_60_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_CV = count_60_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_GL = count_60_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_HL = count_60_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_LAS = count_60_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_MFBL = count_60_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_MFHL = count_60_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_MFOT = count_60_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_OTH = count_60_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_PL = count_60_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_PLBL = count_60_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_RL = count_60_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_SCC = count_60_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD60P2Y_flag'][i] == 1):
            count_60_2y_SEL = count_60_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_AL = count_90_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_BL = count_90_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_CC = count_90_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_CD = count_90_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_CV = count_90_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_GL = count_90_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_HL = count_90_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_LAS = count_90_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_MFBL = count_90_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_MFHL = count_90_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_MFOT = count_90_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_OTH = count_90_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_PL = count_90_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_PLBL = count_90_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_RL = count_90_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_SCC = count_90_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD90P2Y_flag'][i] == 1):
            count_90_2y_SEL = count_90_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_AL = count_30_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_BL = count_30_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_CC = count_30_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_CD = count_30_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_CV = count_30_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_GL = count_30_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_HL = count_30_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_LAS = count_30_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_MFBL = count_30_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_MFHL = count_30_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_MFOT = count_30_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_OTH = count_30_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_PL = count_30_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_PLBL = count_30_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_RL = count_30_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_SCC = count_30_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD30P3Y_flag'][i] == 1):
            count_30_3y_SEL = count_30_3y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_AL = count_60_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_BL = count_60_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_CC = count_60_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_CD = count_60_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_CV = count_60_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_GL = count_60_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_HL = count_60_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_LAS = count_60_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_MFBL = count_60_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_MFHL = count_60_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_MFOT = count_60_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_OTH = count_60_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_PL = count_60_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_PLBL = count_60_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_RL = count_60_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_SCC = count_60_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD60P3Y_flag'][i] == 1):
            count_60_3y_SEL = count_60_3y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_AL = count_90_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_BL = count_90_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_CC = count_90_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_CD = count_90_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_CV = count_90_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_GL = count_90_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_HL = count_90_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_LAS = count_90_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_MFBL = count_90_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_MFHL = count_90_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_MFOT = count_90_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_OTH = count_90_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_PL = count_90_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_PLBL = count_90_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_RL = count_90_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_SCC = count_90_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DPD90P3Y_flag'][i] == 1):
            count_90_3y_SEL = count_90_3y_SEL + 1

        if (grp_slice['STD1M_flag'][i] == 1) or (grp_slice['STD1M_flag'][i] == 0):
            count_std__1m = count_std__1m + grp_slice['STD1M_flag'][i]

        if (grp_slice['STD3M_flag'][i] == 1) or (grp_slice['STD3M_flag'][i] == 0):
            count_std__3m = count_std__3m + grp_slice['STD3M_flag'][i]

        if (grp_slice['STD6M_flag'][i] == 1) or (grp_slice['STD6M_flag'][i] == 0):
            count_std__6m = count_std__6m + grp_slice['STD6M_flag'][i]

        if (grp_slice['STD1Y_flag'][i] == 1) or (grp_slice['STD1Y_flag'][i] == 0):
            count_std__1y = count_std__1y + grp_slice['STD1Y_flag'][i]

        if (grp_slice['STD2Y_flag'][i] == 1) or (grp_slice['STD2Y_flag'][i] == 0):
            count_std__2y = count_std__2y + grp_slice['STD2Y_flag'][i]

        if (grp_slice['STD3Y_flag'][i] == 1) or (grp_slice['STD3Y_flag'][i] == 0):
            count_std__3y = count_std__3y + grp_slice['STD3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_AL = count_std_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_BL = count_std_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_CC = count_std_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_CD = count_std_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_CV = count_std_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_GL = count_std_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_HL = count_std_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_LAS = count_std_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_MFBL = count_std_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_MFHL = count_std_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_MFOT = count_std_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_OTH = count_std_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_PL = count_std_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_PLBL = count_std_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_RL = count_std_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_SCC = count_std_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD1M_flag'][i] == 1):
            count_std_1m_SEL = count_std_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_AL = count_std_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_BL = count_std_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_CC = count_std_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_CD = count_std_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_CV = count_std_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_GL = count_std_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_HL = count_std_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_LAS = count_std_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_MFBL = count_std_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_MFHL = count_std_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_MFOT = count_std_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_OTH = count_std_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_PL = count_std_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_PLBL = count_std_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_RL = count_std_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_SCC = count_std_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD3M_flag'][i] == 1):
            count_std_3m_SEL = count_std_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_AL = count_std_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_BL = count_std_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_CC = count_std_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_CD = count_std_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_CV = count_std_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_GL = count_std_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_HL = count_std_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_LAS = count_std_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_MFBL = count_std_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_MFHL = count_std_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_MFOT = count_std_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_OTH = count_std_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_PL = count_std_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_PLBL = count_std_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_RL = count_std_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_SCC = count_std_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD6M_flag'][i] == 1):
            count_std_6m_SEL = count_std_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_AL = count_std_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_BL = count_std_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_CC = count_std_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_CD = count_std_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_CV = count_std_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_GL = count_std_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_HL = count_std_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_LAS = count_std_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_MFBL = count_std_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_MFHL = count_std_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_MFOT = count_std_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_OTH = count_std_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_PL = count_std_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_PLBL = count_std_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_RL = count_std_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_SCC = count_std_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD1Y_flag'][i] == 1):
            count_std_1y_SEL = count_std_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_AL = count_std_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_BL = count_std_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_CC = count_std_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_CD = count_std_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_CV = count_std_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_GL = count_std_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_HL = count_std_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_LAS = count_std_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_MFBL = count_std_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_MFHL = count_std_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_MFOT = count_std_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_OTH = count_std_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_PL = count_std_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_PLBL = count_std_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_RL = count_std_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_SCC = count_std_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD2Y_flag'][i] == 1):
            count_std_2y_SEL = count_std_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_AL = count_std_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_BL = count_std_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_CC = count_std_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_CD = count_std_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_CV = count_std_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_GL = count_std_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_HL = count_std_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_LAS = count_std_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_MFBL = count_std_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_MFHL = count_std_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_MFOT = count_std_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_OTH = count_std_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_PL = count_std_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_PLBL = count_std_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_RL = count_std_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_SCC = count_std_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['STD3Y_flag'][i] == 1):
            count_std_3y_SEL = count_std_3y_SEL + 1

        if (grp_slice['SUB1M_flag'][i] == 1) or (grp_slice['SUB1M_flag'][i] == 0):
            count_sub_1m = count_sub_1m + grp_slice['SUB1M_flag'][i]

        if (grp_slice['SUB3M_flag'][i] == 1) or (grp_slice['SUB3M_flag'][i] == 0):
            count_sub_3m = count_sub_3m + grp_slice['SUB3M_flag'][i]

        if (grp_slice['SUB6M_flag'][i] == 1) or (grp_slice['SUB6M_flag'][i] == 0):
            count_sub_6m = count_sub_6m + grp_slice['SUB6M_flag'][i]

        if (grp_slice['SUB1Y_flag'][i] == 1) or (grp_slice['SUB1Y_flag'][i] == 0):
            count_sub_1y = count_sub_1y + grp_slice['SUB1Y_flag'][i]

        if (grp_slice['SUB2Y_flag'][i] == 1) or (grp_slice['SUB2Y_flag'][i] == 0):
            count_sub_2y = count_sub_2y + grp_slice['SUB2Y_flag'][i]

        if (grp_slice['SUB3Y_flag'][i] == 1) or (grp_slice['SUB3Y_flag'][i] == 0):
            count_sub_3y = count_sub_3y + grp_slice['SUB3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_AL = count_sub_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_BL = count_sub_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_CC = count_sub_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_CD = count_sub_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_CV = count_sub_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_GL = count_sub_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_HL = count_sub_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_LAS = count_sub_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_MFBL = count_sub_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_MFHL = count_sub_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_MFOT = count_sub_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_OTH = count_sub_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_PL = count_sub_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_PLBL = count_sub_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_RL = count_sub_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_SCC = count_sub_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB1M_flag'][i] == 1):
            count_sub_1m_SEL = count_sub_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_AL = count_sub_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_BL = count_sub_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_CC = count_sub_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_CD = count_sub_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_CV = count_sub_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_GL = count_sub_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_HL = count_sub_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_LAS = count_sub_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_MFBL = count_sub_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_MFHL = count_sub_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_MFOT = count_sub_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_OTH = count_sub_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_PL = count_sub_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_PLBL = count_sub_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_RL = count_sub_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_SCC = count_sub_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB3M_flag'][i] == 1):
            count_sub_3m_SEL = count_sub_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_AL = count_sub_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_BL = count_sub_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_CC = count_sub_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_CD = count_sub_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_CV = count_sub_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_GL = count_sub_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_HL = count_sub_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_LAS = count_sub_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_MFBL = count_sub_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_MFHL = count_sub_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_MFOT = count_sub_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_OTH = count_sub_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_PL = count_sub_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_PLBL = count_sub_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_RL = count_sub_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_SCC = count_sub_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB6M_flag'][i] == 1):
            count_sub_6m_SEL = count_sub_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_AL = count_sub_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_BL = count_sub_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_CC = count_sub_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_CD = count_sub_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_CV = count_sub_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_GL = count_sub_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_HL = count_sub_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_LAS = count_sub_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_MFBL = count_sub_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_MFHL = count_sub_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_MFOT = count_sub_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_OTH = count_sub_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_PL = count_sub_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_PLBL = count_sub_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_RL = count_sub_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_SCC = count_sub_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB1Y_flag'][i] == 1):
            count_sub_1y_SEL = count_sub_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_AL = count_sub_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_BL = count_sub_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_CC = count_sub_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_CD = count_sub_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_CV = count_sub_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_GL = count_sub_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_HL = count_sub_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_LAS = count_sub_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_MFBL = count_sub_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_MFHL = count_sub_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_MFOT = count_sub_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_OTH = count_sub_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_PL = count_sub_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_PLBL = count_sub_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_RL = count_sub_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_SCC = count_sub_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB2Y_flag'][i] == 1):
            count_sub_2y_SEL = count_sub_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_AL = count_sub_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_BL = count_sub_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_CC = count_sub_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_CD = count_sub_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_CV = count_sub_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_GL = count_sub_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_HL = count_sub_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_LAS = count_sub_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_MFBL = count_sub_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_MFHL = count_sub_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_MFOT = count_sub_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_OTH = count_sub_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_PL = count_sub_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_PLBL = count_sub_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_RL = count_sub_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_SCC = count_sub_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SUB3Y_flag'][i] == 1):
            count_sub_3y_SEL = count_sub_3y_SEL + 1

        if (grp_slice['DBT1M_flag'][i] == 1) or (grp_slice['DBT1M_flag'][i] == 0):
            count_dbt_1m = count_dbt_1m + grp_slice['DBT1M_flag'][i]

        if (grp_slice['DBT3M_flag'][i] == 1) or (grp_slice['DBT3M_flag'][i] == 0):
            count_dbt_3m = count_dbt_3m + grp_slice['DBT3M_flag'][i]

        if (grp_slice['DBT6M_flag'][i] == 1) or (grp_slice['DBT6M_flag'][i] == 0):
            count_dbt_6m = count_dbt_6m + grp_slice['DBT6M_flag'][i]

        if (grp_slice['DBT1Y_flag'][i] == 1) or (grp_slice['DBT1Y_flag'][i] == 0):
            count_dbt_1y = count_dbt_1y + grp_slice['DBT1Y_flag'][i]

        if (grp_slice['DBT2Y_flag'][i] == 1) or (grp_slice['DBT2Y_flag'][i] == 0):
            count_dbt_2y = count_dbt_2y + grp_slice['DBT2Y_flag'][i]

        if (grp_slice['DBT3Y_flag'][i] == 1) or (grp_slice['DBT3Y_flag'][i] == 0):
            count_dbt_3y = count_dbt_3y + grp_slice['DBT3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_AL = count_dbt_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_BL = count_dbt_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_CC = count_dbt_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_CD = count_dbt_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_CV = count_dbt_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_GL = count_dbt_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_HL = count_dbt_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_LAS = count_dbt_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_MFBL = count_dbt_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_MFHL = count_dbt_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_MFOT = count_dbt_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_OTH = count_dbt_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_PL = count_dbt_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_PLBL = count_dbt_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_RL = count_dbt_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_SCC = count_dbt_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT1M_flag'][i] == 1):
            count_dbt_1m_SEL = count_dbt_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_AL = count_dbt_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_BL = count_dbt_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_CC = count_dbt_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_CD = count_dbt_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_CV = count_dbt_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_GL = count_dbt_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_HL = count_dbt_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_LAS = count_dbt_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_MFBL = count_dbt_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_MFHL = count_dbt_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_MFOT = count_dbt_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_OTH = count_dbt_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_PL = count_dbt_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_PLBL = count_dbt_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_RL = count_dbt_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_SCC = count_dbt_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT3M_flag'][i] == 1):
            count_dbt_3m_SEL = count_dbt_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_AL = count_dbt_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_BL = count_dbt_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_CC = count_dbt_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_CD = count_dbt_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_CV = count_dbt_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_GL = count_dbt_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_HL = count_dbt_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_LAS = count_dbt_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_MFBL = count_dbt_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_MFHL = count_dbt_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_MFOT = count_dbt_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_OTH = count_dbt_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_PL = count_dbt_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_PLBL = count_dbt_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_RL = count_dbt_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_SCC = count_dbt_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT6M_flag'][i] == 1):
            count_dbt_6m_SEL = count_dbt_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_AL = count_dbt_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_BL = count_dbt_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_CC = count_dbt_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_CD = count_dbt_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_CV = count_dbt_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_GL = count_dbt_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_HL = count_dbt_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_LAS = count_dbt_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_MFBL = count_dbt_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_MFHL = count_dbt_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_MFOT = count_dbt_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_OTH = count_dbt_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_PL = count_dbt_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_PLBL = count_dbt_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_RL = count_dbt_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_SCC = count_dbt_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT1Y_flag'][i] == 1):
            count_dbt_1y_SEL = count_dbt_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_AL = count_dbt_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_BL = count_dbt_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_CC = count_dbt_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_CD = count_dbt_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_CV = count_dbt_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_GL = count_dbt_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_HL = count_dbt_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_LAS = count_dbt_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_MFBL = count_dbt_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_MFHL = count_dbt_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_MFOT = count_dbt_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_OTH = count_dbt_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_PL = count_dbt_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_PLBL = count_dbt_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_RL = count_dbt_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_SCC = count_dbt_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT2Y_flag'][i] == 1):
            count_dbt_2y_SEL = count_dbt_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_AL = count_dbt_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_BL = count_dbt_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_CC = count_dbt_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_CD = count_dbt_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_CV = count_dbt_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_GL = count_dbt_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_HL = count_dbt_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_LAS = count_dbt_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_MFBL = count_dbt_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_MFHL = count_dbt_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_MFOT = count_dbt_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_OTH = count_dbt_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_PL = count_dbt_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_PLBL = count_dbt_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_RL = count_dbt_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_SCC = count_dbt_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['DBT3Y_flag'][i] == 1):
            count_dbt_3y_SEL = count_dbt_3y_SEL + 1

        if (grp_slice['LOS1M_flag'][i] == 1) or (grp_slice['LOS1M_flag'][i] == 0):
            count_los_1m = count_los_1m + grp_slice['LOS1M_flag'][i]

        if (grp_slice['LOS3M_flag'][i] == 1) or (grp_slice['LOS3M_flag'][i] == 0):
            count_los_3m = count_los_3m + grp_slice['LOS3M_flag'][i]

        if (grp_slice['LOS6M_flag'][i] == 1) or (grp_slice['LOS6M_flag'][i] == 0):
            count_los_6m = count_los_6m + grp_slice['LOS6M_flag'][i]

        if (grp_slice['LOS1Y_flag'][i] == 1) or (grp_slice['LOS1Y_flag'][i] == 0):
            count_los_1y = count_los_1y + grp_slice['LOS1Y_flag'][i]

        if (grp_slice['LOS2Y_flag'][i] == 1) or (grp_slice['LOS2Y_flag'][i] == 0):
            count_los_2y = count_los_2y + grp_slice['LOS2Y_flag'][i]

        if (grp_slice['LOS3Y_flag'][i] == 1) or (grp_slice['LOS3Y_flag'][i] == 0):
            count_los_3y = count_los_3y + grp_slice['LOS3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_AL = count_los_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_BL = count_los_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_CC = count_los_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_CD = count_los_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_CV = count_los_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_GL = count_los_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_HL = count_los_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_LAS = count_los_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_MFBL = count_los_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_MFHL = count_los_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_MFOT = count_los_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_OTH = count_los_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_PL = count_los_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_PLBL = count_los_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_RL = count_los_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_SCC = count_los_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS1M_flag'][i] == 1):
            count_los_1m_SEL = count_los_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_AL = count_los_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_BL = count_los_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_CC = count_los_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_CD = count_los_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_CV = count_los_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_GL = count_los_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_HL = count_los_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_LAS = count_los_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_MFBL = count_los_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_MFHL = count_los_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_MFOT = count_los_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_OTH = count_los_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_PL = count_los_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_PLBL = count_los_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_RL = count_los_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_SCC = count_los_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS3M_flag'][i] == 1):
            count_los_3m_SEL = count_los_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_AL = count_los_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_BL = count_los_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_CC = count_los_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_CD = count_los_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_CV = count_los_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_GL = count_los_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_HL = count_los_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_LAS = count_los_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_MFBL = count_los_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_MFHL = count_los_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_MFOT = count_los_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_OTH = count_los_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_PL = count_los_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_PLBL = count_los_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_RL = count_los_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_SCC = count_los_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS6M_flag'][i] == 1):
            count_los_6m_SEL = count_los_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_AL = count_los_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_BL = count_los_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_CC = count_los_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_CD = count_los_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_CV = count_los_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_GL = count_los_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_HL = count_los_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_LAS = count_los_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_MFBL = count_los_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_MFHL = count_los_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_MFOT = count_los_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_OTH = count_los_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_PL = count_los_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_PLBL = count_los_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_RL = count_los_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_SCC = count_los_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS1Y_flag'][i] == 1):
            count_los_1y_SEL = count_los_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_AL = count_los_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_BL = count_los_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_CC = count_los_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_CD = count_los_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_CV = count_los_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_GL = count_los_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_HL = count_los_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_LAS = count_los_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_MFBL = count_los_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_MFHL = count_los_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_MFOT = count_los_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_OTH = count_los_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_PL = count_los_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_PLBL = count_los_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_RL = count_los_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_SCC = count_los_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS2Y_flag'][i] == 1):
            count_los_2y_SEL = count_los_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_AL = count_los_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_BL = count_los_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_CC = count_los_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_CD = count_los_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_CV = count_los_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_GL = count_los_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_HL = count_los_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_LAS = count_los_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_MFBL = count_los_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_MFHL = count_los_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_MFOT = count_los_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_OTH = count_los_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_PL = count_los_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_PLBL = count_los_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_RL = count_los_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_SCC = count_los_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['LOS3Y_flag'][i] == 1):
            count_los_3y_SEL = count_los_3y_SEL + 1

        if (grp_slice['XXX1M_flag'][i] == 1) or (grp_slice['XXX1M_flag'][i] == 0):
            count_xxx_1m = count_xxx_1m + grp_slice['XXX1M_flag'][i]

        if (grp_slice['XXX3M_flag'][i] == 1) or (grp_slice['XXX3M_flag'][i] == 0):
            count_xxx_3m = count_xxx_3m + grp_slice['XXX3M_flag'][i]

        if (grp_slice['XXX6M_flag'][i] == 1) or (grp_slice['XXX6M_flag'][i] == 0):
            count_xxx_6m = count_xxx_6m + grp_slice['XXX6M_flag'][i]

        if (grp_slice['XXX1Y_flag'][i] == 1) or (grp_slice['XXX1Y_flag'][i] == 0):
            count_xxx_1y = count_xxx_1y + grp_slice['XXX1Y_flag'][i]

        if (grp_slice['XXX2Y_flag'][i] == 1) or (grp_slice['XXX2Y_flag'][i] == 0):
            count_xxx_2y = count_xxx_2y + grp_slice['XXX2Y_flag'][i]

        if (grp_slice['XXX3Y_flag'][i] == 1) or (grp_slice['XXX3Y_flag'][i] == 0):
            count_xxx_3y = count_xxx_3y + grp_slice['XXX3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_AL = count_xxx_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_BL = count_xxx_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_CC = count_xxx_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_CD = count_xxx_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_CV = count_xxx_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_GL = count_xxx_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_HL = count_xxx_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_LAS = count_xxx_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_MFBL = count_xxx_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_MFHL = count_xxx_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_MFOT = count_xxx_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_OTH = count_xxx_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_PL = count_xxx_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_PLBL = count_xxx_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_RL = count_xxx_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_SCC = count_xxx_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX1M_flag'][i] == 1):
            count_xxx_1m_SEL = count_xxx_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_AL = count_xxx_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_BL = count_xxx_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_CC = count_xxx_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_CD = count_xxx_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_CV = count_xxx_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_GL = count_xxx_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_HL = count_xxx_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_LAS = count_xxx_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_MFBL = count_xxx_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_MFHL = count_xxx_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_MFOT = count_xxx_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_OTH = count_xxx_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_PL = count_xxx_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_PLBL = count_xxx_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_RL = count_xxx_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_SCC = count_xxx_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX3M_flag'][i] == 1):
            count_xxx_3m_SEL = count_xxx_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_AL = count_xxx_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_BL = count_xxx_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_CC = count_xxx_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_CD = count_xxx_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_CV = count_xxx_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_GL = count_xxx_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_HL = count_xxx_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_LAS = count_xxx_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_MFBL = count_xxx_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_MFHL = count_xxx_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_MFOT = count_xxx_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_OTH = count_xxx_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_PL = count_xxx_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_PLBL = count_xxx_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_RL = count_xxx_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_SCC = count_xxx_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX6M_flag'][i] == 1):
            count_xxx_6m_SEL = count_xxx_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_AL = count_xxx_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_BL = count_xxx_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_CC = count_xxx_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_CD = count_xxx_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_CV = count_xxx_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_GL = count_xxx_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_HL = count_xxx_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_LAS = count_xxx_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_MFBL = count_xxx_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_MFHL = count_xxx_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_MFOT = count_xxx_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_OTH = count_xxx_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_PL = count_xxx_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_PLBL = count_xxx_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_RL = count_xxx_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_SCC = count_xxx_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX1Y_flag'][i] == 1):
            count_xxx_1y_SEL = count_xxx_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_AL = count_xxx_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_BL = count_xxx_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_CC = count_xxx_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_CD = count_xxx_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_CV = count_xxx_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_GL = count_xxx_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_HL = count_xxx_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_LAS = count_xxx_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_MFBL = count_xxx_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_MFHL = count_xxx_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_MFOT = count_xxx_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_OTH = count_xxx_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_PL = count_xxx_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_PLBL = count_xxx_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_RL = count_xxx_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_SCC = count_xxx_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX2Y_flag'][i] == 1):
            count_xxx_2y_SEL = count_xxx_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_AL = count_xxx_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_BL = count_xxx_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_CC = count_xxx_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_CD = count_xxx_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_CV = count_xxx_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_GL = count_xxx_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_HL = count_xxx_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_LAS = count_xxx_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_MFBL = count_xxx_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_MFHL = count_xxx_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_MFOT = count_xxx_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_OTH = count_xxx_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_PL = count_xxx_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_PLBL = count_xxx_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_RL = count_xxx_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_SCC = count_xxx_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['XXX3Y_flag'][i] == 1):
            count_xxx_3y_SEL = count_xxx_3y_SEL + 1

        if (grp_slice['SMA1M_flag'][i] == 1) or (grp_slice['SMA1M_flag'][i] == 0):
            count_sma_1m = count_sma_1m + grp_slice['SMA1M_flag'][i]

        if (grp_slice['SMA3M_flag'][i] == 1) or (grp_slice['SMA3M_flag'][i] == 0):
            count_sma_3m = count_sma_3m + grp_slice['SMA3M_flag'][i]

        if (grp_slice['SMA6M_flag'][i] == 1) or (grp_slice['SMA6M_flag'][i] == 0):
            count_sma_6m = count_sma_6m + grp_slice['SMA6M_flag'][i]

        if (grp_slice['SMA1Y_flag'][i] == 1) or (grp_slice['SMA1Y_flag'][i] == 0):
            count_sma_1y = count_sma_1y + grp_slice['SMA1Y_flag'][i]

        if (grp_slice['SMA2Y_flag'][i] == 1) or (grp_slice['SMA2Y_flag'][i] == 0):
            count_sma_2y = count_sma_2y + grp_slice['SMA2Y_flag'][i]

        if (grp_slice['SMA3Y_flag'][i] == 1) or (grp_slice['SMA3Y_flag'][i] == 0):
            count_sma_3y = count_sma_3y + grp_slice['SMA3Y_flag'][i]

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_AL = count_sma_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_BL = count_sma_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_CC = count_sma_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_CD = count_sma_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_CV = count_sma_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_GL = count_sma_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_HL = count_sma_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_LAS = count_sma_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_MFBL = count_sma_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_MFHL = count_sma_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_MFOT = count_sma_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_OTH = count_sma_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_PL = count_sma_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_PLBL = count_sma_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_RL = count_sma_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_SCC = count_sma_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA1M_flag'][i] == 1):
            count_sma_1m_SEL = count_sma_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_AL = count_sma_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_BL = count_sma_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_CC = count_sma_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_CD = count_sma_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_CV = count_sma_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_GL = count_sma_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_HL = count_sma_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_LAS = count_sma_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_MFBL = count_sma_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_MFHL = count_sma_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_MFOT = count_sma_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_OTH = count_sma_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_PL = count_sma_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_PLBL = count_sma_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_RL = count_sma_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_SCC = count_sma_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA3M_flag'][i] == 1):
            count_sma_3m_SEL = count_sma_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_AL = count_sma_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_BL = count_sma_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_CC = count_sma_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_CD = count_sma_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_CV = count_sma_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_GL = count_sma_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_HL = count_sma_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_LAS = count_sma_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_MFBL = count_sma_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_MFHL = count_sma_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_MFOT = count_sma_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_OTH = count_sma_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_PL = count_sma_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_PLBL = count_sma_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_RL = count_sma_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_SCC = count_sma_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA6M_flag'][i] == 1):
            count_sma_6m_SEL = count_sma_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_AL = count_sma_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_BL = count_sma_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_CC = count_sma_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_CD = count_sma_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_CV = count_sma_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_GL = count_sma_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_HL = count_sma_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_LAS = count_sma_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_MFBL = count_sma_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_MFHL = count_sma_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_MFOT = count_sma_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_OTH = count_sma_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_PL = count_sma_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_PLBL = count_sma_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_RL = count_sma_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_SCC = count_sma_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA1Y_flag'][i] == 1):
            count_sma_1y_SEL = count_sma_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_AL = count_sma_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_BL = count_sma_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_CC = count_sma_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_CD = count_sma_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_CV = count_sma_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_GL = count_sma_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_HL = count_sma_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_LAS = count_sma_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_MFBL = count_sma_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_MFHL = count_sma_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_MFOT = count_sma_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_OTH = count_sma_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_PL = count_sma_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_PLBL = count_sma_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_RL = count_sma_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_SCC = count_sma_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA2Y_flag'][i] == 1):
            count_sma_2y_SEL = count_sma_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_AL = count_sma_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_BL = count_sma_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_CC = count_sma_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_CD = count_sma_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_CV = count_sma_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_GL = count_sma_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_HL = count_sma_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_LAS = count_sma_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_MFBL = count_sma_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_MFHL = count_sma_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_MFOT = count_sma_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_OTH = count_sma_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_PL = count_sma_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_PLBL = count_sma_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_RL = count_sma_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_SCC = count_sma_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['SMA3Y_flag'][i] == 1):
            count_sma_3y_SEL = count_sma_3y_SEL + 1

    count_list_30_3m.append(count_30_3m)
    count_30_3m = 0
    count_list_60_3m.append(count_60_3m)
    count_60_3m = 0
    count_list_90_3m.append(count_90_3m)
    count_90_3m = 0

    count_list_30_6m.append(count_30_6m)
    count_30_6m = 0
    count_list_60_6m.append(count_60_6m)
    count_60_6m = 0
    count_list_90_6m.append(count_90_6m)
    count_90_6m = 0

    count_list_30_1y.append(count_30_1y)
    count_30_1y = 0
    count_list_60_1y.append(count_60_1y)
    count_60_1y = 0
    count_list_90_1y.append(count_90_1y)
    count_90_1y = 0

    count_list_30_2y.append(count_30_2y)
    count_30_2y = 0
    count_list_60_2y.append(count_60_2y)
    count_60_2y = 0
    count_list_90_2y.append(count_90_2y)
    count_90_2y = 0

    count_list_30_3y.append(count_30_3y)
    count_30_3y = 0
    count_list_60_3y.append(count_60_3y)
    count_60_3y = 0
    count_list_90_3y.append(count_90_3y)
    count_90_3y = 0

    count_30_3m_list_AL.append(count_30_3m_AL)
    count_30_3m_list_BL.append(count_30_3m_BL)
    count_30_3m_list_CC.append(count_30_3m_CC)
    count_30_3m_list_CD.append(count_30_3m_CD)
    count_30_3m_list_CV.append(count_30_3m_CV)
    count_30_3m_list_GL.append(count_30_3m_GL)
    count_30_3m_list_HL.append(count_30_3m_HL)
    count_30_3m_list_LAS.append(count_30_3m_LAS)
    count_30_3m_list_MFBL.append(count_30_3m_MFBL)
    count_30_3m_list_MFHL.append(count_30_3m_MFHL)
    count_30_3m_list_MFOT.append(count_30_3m_MFOT)
    count_30_3m_list_OTH.append(count_30_3m_OTH)
    count_30_3m_list_PL.append(count_30_3m_PL)
    count_30_3m_list_PLBL.append(count_30_3m_PLBL)
    count_30_3m_list_RL.append(count_30_3m_RL)
    count_30_3m_list_SCC.append(count_30_3m_SCC)
    count_30_3m_list_SEL.append(count_30_3m_SEL)

    count_30_3m_AL = 0
    count_30_3m_BL = 0
    count_30_3m_CC = 0
    count_30_3m_CD = 0
    count_30_3m_CV = 0
    count_30_3m_GL = 0
    count_30_3m_HL = 0
    count_30_3m_LAS = 0
    count_30_3m_MFBL = 0
    count_30_3m_MFHL = 0
    count_30_3m_MFOT = 0
    count_30_3m_OTH = 0
    count_30_3m_PL = 0
    count_30_3m_PLBL = 0
    count_30_3m_RL = 0
    count_30_3m_SCC = 0
    count_30_3m_SEL = 0

    count_60_3m_list_AL.append(count_60_3m_AL)
    count_60_3m_list_BL.append(count_60_3m_BL)
    count_60_3m_list_CC.append(count_60_3m_CC)
    count_60_3m_list_CD.append(count_60_3m_CD)
    count_60_3m_list_CV.append(count_60_3m_CV)
    count_60_3m_list_GL.append(count_60_3m_GL)
    count_60_3m_list_HL.append(count_60_3m_HL)
    count_60_3m_list_LAS.append(count_60_3m_LAS)
    count_60_3m_list_MFBL.append(count_60_3m_MFBL)
    count_60_3m_list_MFHL.append(count_60_3m_MFHL)
    count_60_3m_list_MFOT.append(count_60_3m_MFOT)
    count_60_3m_list_OTH.append(count_60_3m_OTH)
    count_60_3m_list_PL.append(count_60_3m_PL)
    count_60_3m_list_PLBL.append(count_60_3m_PLBL)
    count_60_3m_list_RL.append(count_60_3m_RL)
    count_60_3m_list_SCC.append(count_60_3m_SCC)
    count_60_3m_list_SEL.append(count_60_3m_SEL)

    count_60_3m_AL = 0
    count_60_3m_BL = 0
    count_60_3m_CC = 0
    count_60_3m_CD = 0
    count_60_3m_CV = 0
    count_60_3m_GL = 0
    count_60_3m_HL = 0
    count_60_3m_LAS = 0
    count_60_3m_MFBL = 0
    count_60_3m_MFHL = 0
    count_60_3m_MFOT = 0
    count_60_3m_OTH = 0
    count_60_3m_PL = 0
    count_60_3m_PLBL = 0
    count_60_3m_RL = 0
    count_60_3m_SCC = 0
    count_60_3m_SEL = 0

    count_90_3m_list_AL.append(count_90_3m_AL)
    count_90_3m_list_BL.append(count_90_3m_BL)
    count_90_3m_list_CC.append(count_90_3m_CC)
    count_90_3m_list_CD.append(count_90_3m_CD)
    count_90_3m_list_CV.append(count_90_3m_CV)
    count_90_3m_list_GL.append(count_90_3m_GL)
    count_90_3m_list_HL.append(count_90_3m_HL)
    count_90_3m_list_LAS.append(count_90_3m_LAS)
    count_90_3m_list_MFBL.append(count_90_3m_MFBL)
    count_90_3m_list_MFHL.append(count_90_3m_MFHL)
    count_90_3m_list_MFOT.append(count_90_3m_MFOT)
    count_90_3m_list_OTH.append(count_90_3m_OTH)
    count_90_3m_list_PL.append(count_90_3m_PL)
    count_90_3m_list_PLBL.append(count_90_3m_PLBL)
    count_90_3m_list_RL.append(count_90_3m_RL)
    count_90_3m_list_SCC.append(count_90_3m_SCC)
    count_90_3m_list_SEL.append(count_90_3m_SEL)

    count_90_3m_AL = 0
    count_90_3m_BL = 0
    count_90_3m_CC = 0
    count_90_3m_CD = 0
    count_90_3m_CV = 0
    count_90_3m_GL = 0
    count_90_3m_HL = 0
    count_90_3m_LAS = 0
    count_90_3m_MFBL = 0
    count_90_3m_MFHL = 0
    count_90_3m_MFOT = 0
    count_90_3m_OTH = 0
    count_90_3m_PL = 0
    count_90_3m_PLBL = 0
    count_90_3m_RL = 0
    count_90_3m_SCC = 0
    count_90_3m_SEL = 0

    count_30_6m_list_AL.append(count_30_6m_AL)
    count_30_6m_list_BL.append(count_30_6m_BL)
    count_30_6m_list_CC.append(count_30_6m_CC)
    count_30_6m_list_CD.append(count_30_6m_CD)
    count_30_6m_list_CV.append(count_30_6m_CV)
    count_30_6m_list_GL.append(count_30_6m_GL)
    count_30_6m_list_HL.append(count_30_6m_HL)
    count_30_6m_list_LAS.append(count_30_6m_LAS)
    count_30_6m_list_MFBL.append(count_30_6m_MFBL)
    count_30_6m_list_MFHL.append(count_30_6m_MFHL)
    count_30_6m_list_MFOT.append(count_30_6m_MFOT)
    count_30_6m_list_OTH.append(count_30_6m_OTH)
    count_30_6m_list_PL.append(count_30_6m_PL)
    count_30_6m_list_PLBL.append(count_30_6m_PLBL)
    count_30_6m_list_RL.append(count_30_6m_RL)
    count_30_6m_list_SCC.append(count_30_6m_SCC)
    count_30_6m_list_SEL.append(count_30_6m_SEL)

    count_30_6m_AL = 0
    count_30_6m_BL = 0
    count_30_6m_CC = 0
    count_30_6m_CD = 0
    count_30_6m_CV = 0
    count_30_6m_GL = 0
    count_30_6m_HL = 0
    count_30_6m_LAS = 0
    count_30_6m_MFBL = 0
    count_30_6m_MFHL = 0
    count_30_6m_MFOT = 0
    count_30_6m_OTH = 0
    count_30_6m_PL = 0
    count_30_6m_PLBL = 0
    count_30_6m_RL = 0
    count_30_6m_SCC = 0
    count_30_6m_SEL = 0

    count_60_6m_list_AL.append(count_60_6m_AL)
    count_60_6m_list_BL.append(count_60_6m_BL)
    count_60_6m_list_CC.append(count_60_6m_CC)
    count_60_6m_list_CD.append(count_60_6m_CD)
    count_60_6m_list_CV.append(count_60_6m_CV)
    count_60_6m_list_GL.append(count_60_6m_GL)
    count_60_6m_list_HL.append(count_60_6m_HL)
    count_60_6m_list_LAS.append(count_60_6m_LAS)
    count_60_6m_list_MFBL.append(count_60_6m_MFBL)
    count_60_6m_list_MFHL.append(count_60_6m_MFHL)
    count_60_6m_list_MFOT.append(count_60_6m_MFOT)
    count_60_6m_list_OTH.append(count_60_6m_OTH)
    count_60_6m_list_PL.append(count_60_6m_PL)
    count_60_6m_list_PLBL.append(count_60_6m_PLBL)
    count_60_6m_list_RL.append(count_60_6m_RL)
    count_60_6m_list_SCC.append(count_60_6m_SCC)
    count_60_6m_list_SEL.append(count_60_6m_SEL)

    count_60_6m_AL = 0
    count_60_6m_BL = 0
    count_60_6m_CC = 0
    count_60_6m_CD = 0
    count_60_6m_CV = 0
    count_60_6m_GL = 0
    count_60_6m_HL = 0
    count_60_6m_LAS = 0
    count_60_6m_MFBL = 0
    count_60_6m_MFHL = 0
    count_60_6m_MFOT = 0
    count_60_6m_OTH = 0
    count_60_6m_PL = 0
    count_60_6m_PLBL = 0
    count_60_6m_RL = 0
    count_60_6m_SCC = 0
    count_60_6m_SEL = 0

    count_90_6m_list_AL.append(count_90_6m_AL)
    count_90_6m_list_BL.append(count_90_6m_BL)
    count_90_6m_list_CC.append(count_90_6m_CC)
    count_90_6m_list_CD.append(count_90_6m_CD)
    count_90_6m_list_CV.append(count_90_6m_CV)
    count_90_6m_list_GL.append(count_90_6m_GL)
    count_90_6m_list_HL.append(count_90_6m_HL)
    count_90_6m_list_LAS.append(count_90_6m_LAS)
    count_90_6m_list_MFBL.append(count_90_6m_MFBL)
    count_90_6m_list_MFHL.append(count_90_6m_MFHL)
    count_90_6m_list_MFOT.append(count_90_6m_MFOT)
    count_90_6m_list_OTH.append(count_90_6m_OTH)
    count_90_6m_list_PL.append(count_90_6m_PL)
    count_90_6m_list_PLBL.append(count_90_6m_PLBL)
    count_90_6m_list_RL.append(count_90_6m_RL)
    count_90_6m_list_SCC.append(count_90_6m_SCC)
    count_90_6m_list_SEL.append(count_90_6m_SEL)

    count_90_6m_AL = 0
    count_90_6m_BL = 0
    count_90_6m_CC = 0
    count_90_6m_CD = 0
    count_90_6m_CV = 0
    count_90_6m_GL = 0
    count_90_6m_HL = 0
    count_90_6m_LAS = 0
    count_90_6m_MFBL = 0
    count_90_6m_MFHL = 0
    count_90_6m_MFOT = 0
    count_90_6m_OTH = 0
    count_90_6m_PL = 0
    count_90_6m_PLBL = 0
    count_90_6m_RL = 0
    count_90_6m_SCC = 0
    count_90_6m_SEL = 0

    count_30_1y_list_AL.append(count_30_1y_AL)
    count_30_1y_list_BL.append(count_30_1y_BL)
    count_30_1y_list_CC.append(count_30_1y_CC)
    count_30_1y_list_CD.append(count_30_1y_CD)
    count_30_1y_list_CV.append(count_30_1y_CV)
    count_30_1y_list_GL.append(count_30_1y_GL)
    count_30_1y_list_HL.append(count_30_1y_HL)
    count_30_1y_list_LAS.append(count_30_1y_LAS)
    count_30_1y_list_MFBL.append(count_30_1y_MFBL)
    count_30_1y_list_MFHL.append(count_30_1y_MFHL)
    count_30_1y_list_MFOT.append(count_30_1y_MFOT)
    count_30_1y_list_OTH.append(count_30_1y_OTH)
    count_30_1y_list_PL.append(count_30_1y_PL)
    count_30_1y_list_PLBL.append(count_30_1y_PLBL)
    count_30_1y_list_RL.append(count_30_1y_RL)
    count_30_1y_list_SCC.append(count_30_1y_SCC)
    count_30_1y_list_SEL.append(count_30_1y_SEL)

    count_30_1y_AL = 0
    count_30_1y_BL = 0
    count_30_1y_CC = 0
    count_30_1y_CD = 0
    count_30_1y_CV = 0
    count_30_1y_GL = 0
    count_30_1y_HL = 0
    count_30_1y_LAS = 0
    count_30_1y_MFBL = 0
    count_30_1y_MFHL = 0
    count_30_1y_MFOT = 0
    count_30_1y_OTH = 0
    count_30_1y_PL = 0
    count_30_1y_PLBL = 0
    count_30_1y_RL = 0
    count_30_1y_SCC = 0
    count_30_1y_SEL = 0

    count_60_1y_list_AL.append(count_60_1y_AL)
    count_60_1y_list_BL.append(count_60_1y_BL)
    count_60_1y_list_CC.append(count_60_1y_CC)
    count_60_1y_list_CD.append(count_60_1y_CD)
    count_60_1y_list_CV.append(count_60_1y_CV)
    count_60_1y_list_GL.append(count_60_1y_GL)
    count_60_1y_list_HL.append(count_60_1y_HL)
    count_60_1y_list_LAS.append(count_60_1y_LAS)
    count_60_1y_list_MFBL.append(count_60_1y_MFBL)
    count_60_1y_list_MFHL.append(count_60_1y_MFHL)
    count_60_1y_list_MFOT.append(count_60_1y_MFOT)
    count_60_1y_list_OTH.append(count_60_1y_OTH)
    count_60_1y_list_PL.append(count_60_1y_PL)
    count_60_1y_list_PLBL.append(count_60_1y_PLBL)
    count_60_1y_list_RL.append(count_60_1y_RL)
    count_60_1y_list_SCC.append(count_60_1y_SCC)
    count_60_1y_list_SEL.append(count_60_1y_SEL)

    count_60_1y_AL = 0
    count_60_1y_BL = 0
    count_60_1y_CC = 0
    count_60_1y_CD = 0
    count_60_1y_CV = 0
    count_60_1y_GL = 0
    count_60_1y_HL = 0
    count_60_1y_LAS = 0
    count_60_1y_MFBL = 0
    count_60_1y_MFHL = 0
    count_60_1y_MFOT = 0
    count_60_1y_OTH = 0
    count_60_1y_PL = 0
    count_60_1y_PLBL = 0
    count_60_1y_RL = 0
    count_60_1y_SCC = 0
    count_60_1y_SEL = 0

    count_90_1y_list_AL.append(count_90_1y_AL)
    count_90_1y_list_BL.append(count_90_1y_BL)
    count_90_1y_list_CC.append(count_90_1y_CC)
    count_90_1y_list_CD.append(count_90_1y_CD)
    count_90_1y_list_CV.append(count_90_1y_CV)
    count_90_1y_list_GL.append(count_90_1y_GL)
    count_90_1y_list_HL.append(count_90_1y_HL)
    count_90_1y_list_LAS.append(count_90_1y_LAS)
    count_90_1y_list_MFBL.append(count_90_1y_MFBL)
    count_90_1y_list_MFHL.append(count_90_1y_MFHL)
    count_90_1y_list_MFOT.append(count_90_1y_MFOT)
    count_90_1y_list_OTH.append(count_90_1y_OTH)
    count_90_1y_list_PL.append(count_90_1y_PL)
    count_90_1y_list_PLBL.append(count_90_1y_PLBL)
    count_90_1y_list_RL.append(count_90_1y_RL)
    count_90_1y_list_SCC.append(count_90_1y_SCC)
    count_90_1y_list_SEL.append(count_90_1y_SEL)

    count_90_1y_AL = 0
    count_90_1y_BL = 0
    count_90_1y_CC = 0
    count_90_1y_CD = 0
    count_90_1y_CV = 0
    count_90_1y_GL = 0
    count_90_1y_HL = 0
    count_90_1y_LAS = 0
    count_90_1y_MFBL = 0
    count_90_1y_MFHL = 0
    count_90_1y_MFOT = 0
    count_90_1y_OTH = 0
    count_90_1y_PL = 0
    count_90_1y_PLBL = 0
    count_90_1y_RL = 0
    count_90_1y_SCC = 0
    count_90_1y_SEL = 0

    count_30_2y_list_AL.append(count_30_2y_AL)
    count_30_2y_list_BL.append(count_30_2y_BL)
    count_30_2y_list_CC.append(count_30_2y_CC)
    count_30_2y_list_CD.append(count_30_2y_CD)
    count_30_2y_list_CV.append(count_30_2y_CV)
    count_30_2y_list_GL.append(count_30_2y_GL)
    count_30_2y_list_HL.append(count_30_2y_HL)
    count_30_2y_list_LAS.append(count_30_2y_LAS)
    count_30_2y_list_MFBL.append(count_30_2y_MFBL)
    count_30_2y_list_MFHL.append(count_30_2y_MFHL)
    count_30_2y_list_MFOT.append(count_30_2y_MFOT)
    count_30_2y_list_OTH.append(count_30_2y_OTH)
    count_30_2y_list_PL.append(count_30_2y_PL)
    count_30_2y_list_PLBL.append(count_30_2y_PLBL)
    count_30_2y_list_RL.append(count_30_2y_RL)
    count_30_2y_list_SCC.append(count_30_2y_SCC)
    count_30_2y_list_SEL.append(count_30_2y_SEL)

    count_30_2y_AL = 0
    count_30_2y_BL = 0
    count_30_2y_CC = 0
    count_30_2y_CD = 0
    count_30_2y_CV = 0
    count_30_2y_GL = 0
    count_30_2y_HL = 0
    count_30_2y_LAS = 0
    count_30_2y_MFBL = 0
    count_30_2y_MFHL = 0
    count_30_2y_MFOT = 0
    count_30_2y_OTH = 0
    count_30_2y_PL = 0
    count_30_2y_PLBL = 0
    count_30_2y_RL = 0
    count_30_2y_SCC = 0
    count_30_2y_SEL = 0

    count_60_2y_list_AL.append(count_60_2y_AL)
    count_60_2y_list_BL.append(count_60_2y_BL)
    count_60_2y_list_CC.append(count_60_2y_CC)
    count_60_2y_list_CD.append(count_60_2y_CD)
    count_60_2y_list_CV.append(count_60_2y_CV)
    count_60_2y_list_GL.append(count_60_2y_GL)
    count_60_2y_list_HL.append(count_60_2y_HL)
    count_60_2y_list_LAS.append(count_60_2y_LAS)
    count_60_2y_list_MFBL.append(count_60_2y_MFBL)
    count_60_2y_list_MFHL.append(count_60_2y_MFHL)
    count_60_2y_list_MFOT.append(count_60_2y_MFOT)
    count_60_2y_list_OTH.append(count_60_2y_OTH)
    count_60_2y_list_PL.append(count_60_2y_PL)
    count_60_2y_list_PLBL.append(count_60_2y_PLBL)
    count_60_2y_list_RL.append(count_60_2y_RL)
    count_60_2y_list_SCC.append(count_60_2y_SCC)
    count_60_2y_list_SEL.append(count_60_2y_SEL)

    count_60_2y_AL = 0
    count_60_2y_BL = 0
    count_60_2y_CC = 0
    count_60_2y_CD = 0
    count_60_2y_CV = 0
    count_60_2y_GL = 0
    count_60_2y_HL = 0
    count_60_2y_LAS = 0
    count_60_2y_MFBL = 0
    count_60_2y_MFHL = 0
    count_60_2y_MFOT = 0
    count_60_2y_OTH = 0
    count_60_2y_PL = 0
    count_60_2y_PLBL = 0
    count_60_2y_RL = 0
    count_60_2y_SCC = 0
    count_60_2y_SEL = 0

    count_90_2y_list_AL.append(count_90_2y_AL)
    count_90_2y_list_BL.append(count_90_2y_BL)
    count_90_2y_list_CC.append(count_90_2y_CC)
    count_90_2y_list_CD.append(count_90_2y_CD)
    count_90_2y_list_CV.append(count_90_2y_CV)
    count_90_2y_list_GL.append(count_90_2y_GL)
    count_90_2y_list_HL.append(count_90_2y_HL)
    count_90_2y_list_LAS.append(count_90_2y_LAS)
    count_90_2y_list_MFBL.append(count_90_2y_MFBL)
    count_90_2y_list_MFHL.append(count_90_2y_MFHL)
    count_90_2y_list_MFOT.append(count_90_2y_MFOT)
    count_90_2y_list_OTH.append(count_90_2y_OTH)
    count_90_2y_list_PL.append(count_90_2y_PL)
    count_90_2y_list_PLBL.append(count_90_2y_PLBL)
    count_90_2y_list_RL.append(count_90_2y_RL)
    count_90_2y_list_SCC.append(count_90_2y_SCC)
    count_90_2y_list_SEL.append(count_90_2y_SEL)

    count_90_2y_AL = 0
    count_90_2y_BL = 0
    count_90_2y_CC = 0
    count_90_2y_CD = 0
    count_90_2y_CV = 0
    count_90_2y_GL = 0
    count_90_2y_HL = 0
    count_90_2y_LAS = 0
    count_90_2y_MFBL = 0
    count_90_2y_MFHL = 0
    count_90_2y_MFOT = 0
    count_90_2y_OTH = 0
    count_90_2y_PL = 0
    count_90_2y_PLBL = 0
    count_90_2y_RL = 0
    count_90_2y_SCC = 0
    count_90_2y_SEL = 0

    count_30_3y_list_AL.append(count_30_3y_AL)
    count_30_3y_list_BL.append(count_30_3y_BL)
    count_30_3y_list_CC.append(count_30_3y_CC)
    count_30_3y_list_CD.append(count_30_3y_CD)
    count_30_3y_list_CV.append(count_30_3y_CV)
    count_30_3y_list_GL.append(count_30_3y_GL)
    count_30_3y_list_HL.append(count_30_3y_HL)
    count_30_3y_list_LAS.append(count_30_3y_LAS)
    count_30_3y_list_MFBL.append(count_30_3y_MFBL)
    count_30_3y_list_MFHL.append(count_30_3y_MFHL)
    count_30_3y_list_MFOT.append(count_30_3y_MFOT)
    count_30_3y_list_OTH.append(count_30_3y_OTH)
    count_30_3y_list_PL.append(count_30_3y_PL)
    count_30_3y_list_PLBL.append(count_30_3y_PLBL)
    count_30_3y_list_RL.append(count_30_3y_RL)
    count_30_3y_list_SCC.append(count_30_3y_SCC)
    count_30_3y_list_SEL.append(count_30_3y_SEL)

    count_30_3y_AL = 0
    count_30_3y_BL = 0
    count_30_3y_CC = 0
    count_30_3y_CD = 0
    count_30_3y_CV = 0
    count_30_3y_GL = 0
    count_30_3y_HL = 0
    count_30_3y_LAS = 0
    count_30_3y_MFBL = 0
    count_30_3y_MFHL = 0
    count_30_3y_MFOT = 0
    count_30_3y_OTH = 0
    count_30_3y_PL = 0
    count_30_3y_PLBL = 0
    count_30_3y_RL = 0
    count_30_3y_SCC = 0
    count_30_3y_SEL = 0

    count_60_3y_list_AL.append(count_60_3y_AL)
    count_60_3y_list_BL.append(count_60_3y_BL)
    count_60_3y_list_CC.append(count_60_3y_CC)
    count_60_3y_list_CD.append(count_60_3y_CD)
    count_60_3y_list_CV.append(count_60_3y_CV)
    count_60_3y_list_GL.append(count_60_3y_GL)
    count_60_3y_list_HL.append(count_60_3y_HL)
    count_60_3y_list_LAS.append(count_60_3y_LAS)
    count_60_3y_list_MFBL.append(count_60_3y_MFBL)
    count_60_3y_list_MFHL.append(count_60_3y_MFHL)
    count_60_3y_list_MFOT.append(count_60_3y_MFOT)
    count_60_3y_list_OTH.append(count_60_3y_OTH)
    count_60_3y_list_PL.append(count_60_3y_PL)
    count_60_3y_list_PLBL.append(count_60_3y_PLBL)
    count_60_3y_list_RL.append(count_60_3y_RL)
    count_60_3y_list_SCC.append(count_60_3y_SCC)
    count_60_3y_list_SEL.append(count_60_3y_SEL)

    count_60_3y_AL = 0
    count_60_3y_BL = 0
    count_60_3y_CC = 0
    count_60_3y_CD = 0
    count_60_3y_CV = 0
    count_60_3y_GL = 0
    count_60_3y_HL = 0
    count_60_3y_LAS = 0
    count_60_3y_MFBL = 0
    count_60_3y_MFHL = 0
    count_60_3y_MFOT = 0
    count_60_3y_OTH = 0
    count_60_3y_PL = 0
    count_60_3y_PLBL = 0
    count_60_3y_RL = 0
    count_60_3y_SCC = 0
    count_60_3y_SEL = 0

    count_90_3y_list_AL.append(count_90_3y_AL)
    count_90_3y_list_BL.append(count_90_3y_BL)
    count_90_3y_list_CC.append(count_90_3y_CC)
    count_90_3y_list_CD.append(count_90_3y_CD)
    count_90_3y_list_CV.append(count_90_3y_CV)
    count_90_3y_list_GL.append(count_90_3y_GL)
    count_90_3y_list_HL.append(count_90_3y_HL)
    count_90_3y_list_LAS.append(count_90_3y_LAS)
    count_90_3y_list_MFBL.append(count_90_3y_MFBL)
    count_90_3y_list_MFHL.append(count_90_3y_MFHL)
    count_90_3y_list_MFOT.append(count_90_3y_MFOT)
    count_90_3y_list_OTH.append(count_90_3y_OTH)
    count_90_3y_list_PL.append(count_90_3y_PL)
    count_90_3y_list_PLBL.append(count_90_3y_PLBL)
    count_90_3y_list_RL.append(count_90_3y_RL)
    count_90_3y_list_SCC.append(count_90_3y_SCC)
    count_90_3y_list_SEL.append(count_90_3y_SEL)

    count_90_3y_AL = 0
    count_90_3y_BL = 0
    count_90_3y_CC = 0
    count_90_3y_CD = 0
    count_90_3y_CV = 0
    count_90_3y_GL = 0
    count_90_3y_HL = 0
    count_90_3y_LAS = 0
    count_90_3y_MFBL = 0
    count_90_3y_MFHL = 0
    count_90_3y_MFOT = 0
    count_90_3y_OTH = 0
    count_90_3y_PL = 0
    count_90_3y_PLBL = 0
    count_90_3y_RL = 0
    count_90_3y_SCC = 0
    count_90_3y_SEL = 0

    count_std__list_1m.append(count_std__1m)
    count_std__1m = 0
    count_std__list_3m.append(count_std__3m)
    count_std__3m = 0
    count_std__list_6m.append(count_std__6m)
    count_std__6m = 0
    count_std__list_1y.append(count_std__1y)
    count_std__1y = 0
    count_std__list_2y.append(count_std__2y)
    count_std__2y = 0
    count_std__list_3y.append(count_std__3y)
    count_std__3y = 0

    count_std_1m_list_AL.append(count_std_1m_AL)
    count_std_1m_list_BL.append(count_std_1m_BL)
    count_std_1m_list_CC.append(count_std_1m_CC)
    count_std_1m_list_CD.append(count_std_1m_CD)
    count_std_1m_list_CV.append(count_std_1m_CV)
    count_std_1m_list_GL.append(count_std_1m_GL)
    count_std_1m_list_HL.append(count_std_1m_HL)
    count_std_1m_list_LAS.append(count_std_1m_LAS)
    count_std_1m_list_MFBL.append(count_std_1m_MFBL)
    count_std_1m_list_MFHL.append(count_std_1m_MFHL)
    count_std_1m_list_MFOT.append(count_std_1m_MFOT)
    count_std_1m_list_OTH.append(count_std_1m_OTH)
    count_std_1m_list_PL.append(count_std_1m_PL)
    count_std_1m_list_PLBL.append(count_std_1m_PLBL)
    count_std_1m_list_RL.append(count_std_1m_RL)
    count_std_1m_list_SCC.append(count_std_1m_SCC)
    count_std_1m_list_SEL.append(count_std_1m_SEL)

    count_std_1m_AL = 0
    count_std_1m_BL = 0
    count_std_1m_CC = 0
    count_std_1m_CD = 0
    count_std_1m_CV = 0
    count_std_1m_GL = 0
    count_std_1m_HL = 0
    count_std_1m_LAS = 0
    count_std_1m_MFBL = 0
    count_std_1m_MFHL = 0
    count_std_1m_MFOT = 0
    count_std_1m_OTH = 0
    count_std_1m_PL = 0
    count_std_1m_PLBL = 0
    count_std_1m_RL = 0
    count_std_1m_SCC = 0
    count_std_1m_SEL = 0

    count_std_3m_list_AL.append(count_std_3m_AL)
    count_std_3m_list_BL.append(count_std_3m_BL)
    count_std_3m_list_CC.append(count_std_3m_CC)
    count_std_3m_list_CD.append(count_std_3m_CD)
    count_std_3m_list_CV.append(count_std_3m_CV)
    count_std_3m_list_GL.append(count_std_3m_GL)
    count_std_3m_list_HL.append(count_std_3m_HL)
    count_std_3m_list_LAS.append(count_std_3m_LAS)
    count_std_3m_list_MFBL.append(count_std_3m_MFBL)
    count_std_3m_list_MFHL.append(count_std_3m_MFHL)
    count_std_3m_list_MFOT.append(count_std_3m_MFOT)
    count_std_3m_list_OTH.append(count_std_3m_OTH)
    count_std_3m_list_PL.append(count_std_3m_PL)
    count_std_3m_list_PLBL.append(count_std_3m_PLBL)
    count_std_3m_list_RL.append(count_std_3m_RL)
    count_std_3m_list_SCC.append(count_std_3m_SCC)
    count_std_3m_list_SEL.append(count_std_3m_SEL)

    count_std_3m_AL = 0
    count_std_3m_BL = 0
    count_std_3m_CC = 0
    count_std_3m_CD = 0
    count_std_3m_CV = 0
    count_std_3m_GL = 0
    count_std_3m_HL = 0
    count_std_3m_LAS = 0
    count_std_3m_MFBL = 0
    count_std_3m_MFHL = 0
    count_std_3m_MFOT = 0
    count_std_3m_OTH = 0
    count_std_3m_PL = 0
    count_std_3m_PLBL = 0
    count_std_3m_RL = 0
    count_std_3m_SCC = 0
    count_std_3m_SEL = 0

    count_std_6m_list_AL.append(count_std_6m_AL)
    count_std_6m_list_BL.append(count_std_6m_BL)
    count_std_6m_list_CC.append(count_std_6m_CC)
    count_std_6m_list_CD.append(count_std_6m_CD)
    count_std_6m_list_CV.append(count_std_6m_CV)
    count_std_6m_list_GL.append(count_std_6m_GL)
    count_std_6m_list_HL.append(count_std_6m_HL)
    count_std_6m_list_LAS.append(count_std_6m_LAS)
    count_std_6m_list_MFBL.append(count_std_6m_MFBL)
    count_std_6m_list_MFHL.append(count_std_6m_MFHL)
    count_std_6m_list_MFOT.append(count_std_6m_MFOT)
    count_std_6m_list_OTH.append(count_std_6m_OTH)
    count_std_6m_list_PL.append(count_std_6m_PL)
    count_std_6m_list_PLBL.append(count_std_6m_PLBL)
    count_std_6m_list_RL.append(count_std_6m_RL)
    count_std_6m_list_SCC.append(count_std_6m_SCC)
    count_std_6m_list_SEL.append(count_std_6m_SEL)

    count_std_6m_AL = 0
    count_std_6m_BL = 0
    count_std_6m_CC = 0
    count_std_6m_CD = 0
    count_std_6m_CV = 0
    count_std_6m_GL = 0
    count_std_6m_HL = 0
    count_std_6m_LAS = 0
    count_std_6m_MFBL = 0
    count_std_6m_MFHL = 0
    count_std_6m_MFOT = 0
    count_std_6m_OTH = 0
    count_std_6m_PL = 0
    count_std_6m_PLBL = 0
    count_std_6m_RL = 0
    count_std_6m_SCC = 0
    count_std_6m_SEL = 0

    count_std_1y_list_AL.append(count_std_1y_AL)
    count_std_1y_list_BL.append(count_std_1y_BL)
    count_std_1y_list_CC.append(count_std_1y_CC)
    count_std_1y_list_CD.append(count_std_1y_CD)
    count_std_1y_list_CV.append(count_std_1y_CV)
    count_std_1y_list_GL.append(count_std_1y_GL)
    count_std_1y_list_HL.append(count_std_1y_HL)
    count_std_1y_list_LAS.append(count_std_1y_LAS)
    count_std_1y_list_MFBL.append(count_std_1y_MFBL)
    count_std_1y_list_MFHL.append(count_std_1y_MFHL)
    count_std_1y_list_MFOT.append(count_std_1y_MFOT)
    count_std_1y_list_OTH.append(count_std_1y_OTH)
    count_std_1y_list_PL.append(count_std_1y_PL)
    count_std_1y_list_PLBL.append(count_std_1y_PLBL)
    count_std_1y_list_RL.append(count_std_1y_RL)
    count_std_1y_list_SCC.append(count_std_1y_SCC)
    count_std_1y_list_SEL.append(count_std_1y_SEL)

    count_std_1y_AL = 0
    count_std_1y_BL = 0
    count_std_1y_CC = 0
    count_std_1y_CD = 0
    count_std_1y_CV = 0
    count_std_1y_GL = 0
    count_std_1y_HL = 0
    count_std_1y_LAS = 0
    count_std_1y_MFBL = 0
    count_std_1y_MFHL = 0
    count_std_1y_MFOT = 0
    count_std_1y_OTH = 0
    count_std_1y_PL = 0
    count_std_1y_PLBL = 0
    count_std_1y_RL = 0
    count_std_1y_SCC = 0
    count_std_1y_SEL = 0

    count_std_2y_list_AL.append(count_std_2y_AL)
    count_std_2y_list_BL.append(count_std_2y_BL)
    count_std_2y_list_CC.append(count_std_2y_CC)
    count_std_2y_list_CD.append(count_std_2y_CD)
    count_std_2y_list_CV.append(count_std_2y_CV)
    count_std_2y_list_GL.append(count_std_2y_GL)
    count_std_2y_list_HL.append(count_std_2y_HL)
    count_std_2y_list_LAS.append(count_std_2y_LAS)
    count_std_2y_list_MFBL.append(count_std_2y_MFBL)
    count_std_2y_list_MFHL.append(count_std_2y_MFHL)
    count_std_2y_list_MFOT.append(count_std_2y_MFOT)
    count_std_2y_list_OTH.append(count_std_2y_OTH)
    count_std_2y_list_PL.append(count_std_2y_PL)
    count_std_2y_list_PLBL.append(count_std_2y_PLBL)
    count_std_2y_list_RL.append(count_std_2y_RL)
    count_std_2y_list_SCC.append(count_std_2y_SCC)
    count_std_2y_list_SEL.append(count_std_2y_SEL)

    count_std_2y_AL = 0
    count_std_2y_BL = 0
    count_std_2y_CC = 0
    count_std_2y_CD = 0
    count_std_2y_CV = 0
    count_std_2y_GL = 0
    count_std_2y_HL = 0
    count_std_2y_LAS = 0
    count_std_2y_MFBL = 0
    count_std_2y_MFHL = 0
    count_std_2y_MFOT = 0
    count_std_2y_OTH = 0
    count_std_2y_PL = 0
    count_std_2y_PLBL = 0
    count_std_2y_RL = 0
    count_std_2y_SCC = 0
    count_std_2y_SEL = 0

    count_std_3y_list_AL.append(count_std_3y_AL)
    count_std_3y_list_BL.append(count_std_3y_BL)
    count_std_3y_list_CC.append(count_std_3y_CC)
    count_std_3y_list_CD.append(count_std_3y_CD)
    count_std_3y_list_CV.append(count_std_3y_CV)
    count_std_3y_list_GL.append(count_std_3y_GL)
    count_std_3y_list_HL.append(count_std_3y_HL)
    count_std_3y_list_LAS.append(count_std_3y_LAS)
    count_std_3y_list_MFBL.append(count_std_3y_MFBL)
    count_std_3y_list_MFHL.append(count_std_3y_MFHL)
    count_std_3y_list_MFOT.append(count_std_3y_MFOT)
    count_std_3y_list_OTH.append(count_std_3y_OTH)
    count_std_3y_list_PL.append(count_std_3y_PL)
    count_std_3y_list_PLBL.append(count_std_3y_PLBL)
    count_std_3y_list_RL.append(count_std_3y_RL)
    count_std_3y_list_SCC.append(count_std_3y_SCC)
    count_std_3y_list_SEL.append(count_std_3y_SEL)

    count_std_3y_AL = 0
    count_std_3y_BL = 0
    count_std_3y_CC = 0
    count_std_3y_CD = 0
    count_std_3y_CV = 0
    count_std_3y_GL = 0
    count_std_3y_HL = 0
    count_std_3y_LAS = 0
    count_std_3y_MFBL = 0
    count_std_3y_MFHL = 0
    count_std_3y_MFOT = 0
    count_std_3y_OTH = 0
    count_std_3y_PL = 0
    count_std_3y_PLBL = 0
    count_std_3y_RL = 0
    count_std_3y_SCC = 0
    count_std_3y_SEL = 0

    count_sub_list_1m.append(count_sub_1m)
    count_sub_1m = 0
    count_sub_list_3m.append(count_sub_3m)
    count_sub_3m = 0
    count_sub_list_6m.append(count_sub_6m)
    count_sub_6m = 0
    count_sub_list_1y.append(count_sub_1y)
    count_sub_1y = 0
    count_sub_list_2y.append(count_sub_2y)
    count_sub_2y = 0
    count_sub_list_3y.append(count_sub_3y)
    count_sub_3y = 0

    count_sub_1m_list_AL.append(count_sub_1m_AL)
    count_sub_1m_list_BL.append(count_sub_1m_BL)
    count_sub_1m_list_CC.append(count_sub_1m_CC)
    count_sub_1m_list_CD.append(count_sub_1m_CD)
    count_sub_1m_list_CV.append(count_sub_1m_CV)
    count_sub_1m_list_GL.append(count_sub_1m_GL)
    count_sub_1m_list_HL.append(count_sub_1m_HL)
    count_sub_1m_list_LAS.append(count_sub_1m_LAS)
    count_sub_1m_list_MFBL.append(count_sub_1m_MFBL)
    count_sub_1m_list_MFHL.append(count_sub_1m_MFHL)
    count_sub_1m_list_MFOT.append(count_sub_1m_MFOT)
    count_sub_1m_list_OTH.append(count_sub_1m_OTH)
    count_sub_1m_list_PL.append(count_sub_1m_PL)
    count_sub_1m_list_PLBL.append(count_sub_1m_PLBL)
    count_sub_1m_list_RL.append(count_sub_1m_RL)
    count_sub_1m_list_SCC.append(count_sub_1m_SCC)
    count_sub_1m_list_SEL.append(count_sub_1m_SEL)

    count_sub_1m_AL = 0
    count_sub_1m_BL = 0
    count_sub_1m_CC = 0
    count_sub_1m_CD = 0
    count_sub_1m_CV = 0
    count_sub_1m_GL = 0
    count_sub_1m_HL = 0
    count_sub_1m_LAS = 0
    count_sub_1m_MFBL = 0
    count_sub_1m_MFHL = 0
    count_sub_1m_MFOT = 0
    count_sub_1m_OTH = 0
    count_sub_1m_PL = 0
    count_sub_1m_PLBL = 0
    count_sub_1m_RL = 0
    count_sub_1m_SCC = 0
    count_sub_1m_SEL = 0

    count_sub_3m_list_AL.append(count_sub_3m_AL)
    count_sub_3m_list_BL.append(count_sub_3m_BL)
    count_sub_3m_list_CC.append(count_sub_3m_CC)
    count_sub_3m_list_CD.append(count_sub_3m_CD)
    count_sub_3m_list_CV.append(count_sub_3m_CV)
    count_sub_3m_list_GL.append(count_sub_3m_GL)
    count_sub_3m_list_HL.append(count_sub_3m_HL)
    count_sub_3m_list_LAS.append(count_sub_3m_LAS)
    count_sub_3m_list_MFBL.append(count_sub_3m_MFBL)
    count_sub_3m_list_MFHL.append(count_sub_3m_MFHL)
    count_sub_3m_list_MFOT.append(count_sub_3m_MFOT)
    count_sub_3m_list_OTH.append(count_sub_3m_OTH)
    count_sub_3m_list_PL.append(count_sub_3m_PL)
    count_sub_3m_list_PLBL.append(count_sub_3m_PLBL)
    count_sub_3m_list_RL.append(count_sub_3m_RL)
    count_sub_3m_list_SCC.append(count_sub_3m_SCC)
    count_sub_3m_list_SEL.append(count_sub_3m_SEL)

    count_sub_3m_AL = 0
    count_sub_3m_BL = 0
    count_sub_3m_CC = 0
    count_sub_3m_CD = 0
    count_sub_3m_CV = 0
    count_sub_3m_GL = 0
    count_sub_3m_HL = 0
    count_sub_3m_LAS = 0
    count_sub_3m_MFBL = 0
    count_sub_3m_MFHL = 0
    count_sub_3m_MFOT = 0
    count_sub_3m_OTH = 0
    count_sub_3m_PL = 0
    count_sub_3m_PLBL = 0
    count_sub_3m_RL = 0
    count_sub_3m_SCC = 0
    count_sub_3m_SEL = 0

    count_sub_6m_list_AL.append(count_sub_6m_AL)
    count_sub_6m_list_BL.append(count_sub_6m_BL)
    count_sub_6m_list_CC.append(count_sub_6m_CC)
    count_sub_6m_list_CD.append(count_sub_6m_CD)
    count_sub_6m_list_CV.append(count_sub_6m_CV)
    count_sub_6m_list_GL.append(count_sub_6m_GL)
    count_sub_6m_list_HL.append(count_sub_6m_HL)
    count_sub_6m_list_LAS.append(count_sub_6m_LAS)
    count_sub_6m_list_MFBL.append(count_sub_6m_MFBL)
    count_sub_6m_list_MFHL.append(count_sub_6m_MFHL)
    count_sub_6m_list_MFOT.append(count_sub_6m_MFOT)
    count_sub_6m_list_OTH.append(count_sub_6m_OTH)
    count_sub_6m_list_PL.append(count_sub_6m_PL)
    count_sub_6m_list_PLBL.append(count_sub_6m_PLBL)
    count_sub_6m_list_RL.append(count_sub_6m_RL)
    count_sub_6m_list_SCC.append(count_sub_6m_SCC)
    count_sub_6m_list_SEL.append(count_sub_6m_SEL)

    count_sub_6m_AL = 0
    count_sub_6m_BL = 0
    count_sub_6m_CC = 0
    count_sub_6m_CD = 0
    count_sub_6m_CV = 0
    count_sub_6m_GL = 0
    count_sub_6m_HL = 0
    count_sub_6m_LAS = 0
    count_sub_6m_MFBL = 0
    count_sub_6m_MFHL = 0
    count_sub_6m_MFOT = 0
    count_sub_6m_OTH = 0
    count_sub_6m_PL = 0
    count_sub_6m_PLBL = 0
    count_sub_6m_RL = 0
    count_sub_6m_SCC = 0
    count_sub_6m_SEL = 0

    count_sub_1y_list_AL.append(count_sub_1y_AL)
    count_sub_1y_list_BL.append(count_sub_1y_BL)
    count_sub_1y_list_CC.append(count_sub_1y_CC)
    count_sub_1y_list_CD.append(count_sub_1y_CD)
    count_sub_1y_list_CV.append(count_sub_1y_CV)
    count_sub_1y_list_GL.append(count_sub_1y_GL)
    count_sub_1y_list_HL.append(count_sub_1y_HL)
    count_sub_1y_list_LAS.append(count_sub_1y_LAS)
    count_sub_1y_list_MFBL.append(count_sub_1y_MFBL)
    count_sub_1y_list_MFHL.append(count_sub_1y_MFHL)
    count_sub_1y_list_MFOT.append(count_sub_1y_MFOT)
    count_sub_1y_list_OTH.append(count_sub_1y_OTH)
    count_sub_1y_list_PL.append(count_sub_1y_PL)
    count_sub_1y_list_PLBL.append(count_sub_1y_PLBL)
    count_sub_1y_list_RL.append(count_sub_1y_RL)
    count_sub_1y_list_SCC.append(count_sub_1y_SCC)
    count_sub_1y_list_SEL.append(count_sub_1y_SEL)

    count_sub_1y_AL = 0
    count_sub_1y_BL = 0
    count_sub_1y_CC = 0
    count_sub_1y_CD = 0
    count_sub_1y_CV = 0
    count_sub_1y_GL = 0
    count_sub_1y_HL = 0
    count_sub_1y_LAS = 0
    count_sub_1y_MFBL = 0
    count_sub_1y_MFHL = 0
    count_sub_1y_MFOT = 0
    count_sub_1y_OTH = 0
    count_sub_1y_PL = 0
    count_sub_1y_PLBL = 0
    count_sub_1y_RL = 0
    count_sub_1y_SCC = 0
    count_sub_1y_SEL = 0

    count_sub_2y_list_AL.append(count_sub_2y_AL)
    count_sub_2y_list_BL.append(count_sub_2y_BL)
    count_sub_2y_list_CC.append(count_sub_2y_CC)
    count_sub_2y_list_CD.append(count_sub_2y_CD)
    count_sub_2y_list_CV.append(count_sub_2y_CV)
    count_sub_2y_list_GL.append(count_sub_2y_GL)
    count_sub_2y_list_HL.append(count_sub_2y_HL)
    count_sub_2y_list_LAS.append(count_sub_2y_LAS)
    count_sub_2y_list_MFBL.append(count_sub_2y_MFBL)
    count_sub_2y_list_MFHL.append(count_sub_2y_MFHL)
    count_sub_2y_list_MFOT.append(count_sub_2y_MFOT)
    count_sub_2y_list_OTH.append(count_sub_2y_OTH)
    count_sub_2y_list_PL.append(count_sub_2y_PL)
    count_sub_2y_list_PLBL.append(count_sub_2y_PLBL)
    count_sub_2y_list_RL.append(count_sub_2y_RL)
    count_sub_2y_list_SCC.append(count_sub_2y_SCC)
    count_sub_2y_list_SEL.append(count_sub_2y_SEL)

    count_sub_2y_AL = 0
    count_sub_2y_BL = 0
    count_sub_2y_CC = 0
    count_sub_2y_CD = 0
    count_sub_2y_CV = 0
    count_sub_2y_GL = 0
    count_sub_2y_HL = 0
    count_sub_2y_LAS = 0
    count_sub_2y_MFBL = 0
    count_sub_2y_MFHL = 0
    count_sub_2y_MFOT = 0
    count_sub_2y_OTH = 0
    count_sub_2y_PL = 0
    count_sub_2y_PLBL = 0
    count_sub_2y_RL = 0
    count_sub_2y_SCC = 0
    count_sub_2y_SEL = 0

    count_sub_3y_list_AL.append(count_sub_3y_AL)
    count_sub_3y_list_BL.append(count_sub_3y_BL)
    count_sub_3y_list_CC.append(count_sub_3y_CC)
    count_sub_3y_list_CD.append(count_sub_3y_CD)
    count_sub_3y_list_CV.append(count_sub_3y_CV)
    count_sub_3y_list_GL.append(count_sub_3y_GL)
    count_sub_3y_list_HL.append(count_sub_3y_HL)
    count_sub_3y_list_LAS.append(count_sub_3y_LAS)
    count_sub_3y_list_MFBL.append(count_sub_3y_MFBL)
    count_sub_3y_list_MFHL.append(count_sub_3y_MFHL)
    count_sub_3y_list_MFOT.append(count_sub_3y_MFOT)
    count_sub_3y_list_OTH.append(count_sub_3y_OTH)
    count_sub_3y_list_PL.append(count_sub_3y_PL)
    count_sub_3y_list_PLBL.append(count_sub_3y_PLBL)
    count_sub_3y_list_RL.append(count_sub_3y_RL)
    count_sub_3y_list_SCC.append(count_sub_3y_SCC)
    count_sub_3y_list_SEL.append(count_sub_3y_SEL)

    count_sub_3y_AL = 0
    count_sub_3y_BL = 0
    count_sub_3y_CC = 0
    count_sub_3y_CD = 0
    count_sub_3y_CV = 0
    count_sub_3y_GL = 0
    count_sub_3y_HL = 0
    count_sub_3y_LAS = 0
    count_sub_3y_MFBL = 0
    count_sub_3y_MFHL = 0
    count_sub_3y_MFOT = 0
    count_sub_3y_OTH = 0
    count_sub_3y_PL = 0
    count_sub_3y_PLBL = 0
    count_sub_3y_RL = 0
    count_sub_3y_SCC = 0
    count_sub_3y_SEL = 0

    count_dbt_list_1m.append(count_dbt_1m)
    count_dbt_1m = 0
    count_dbt_list_3m.append(count_dbt_3m)
    count_dbt_3m = 0
    count_dbt_list_6m.append(count_dbt_6m)
    count_dbt_6m = 0
    count_dbt_list_1y.append(count_dbt_1y)
    count_dbt_1y = 0
    count_dbt_list_2y.append(count_dbt_2y)
    count_dbt_2y = 0
    count_dbt_list_3y.append(count_dbt_3y)
    count_dbt_3y = 0

    count_dbt_1m_list_AL.append(count_dbt_1m_AL)
    count_dbt_1m_list_BL.append(count_dbt_1m_BL)
    count_dbt_1m_list_CC.append(count_dbt_1m_CC)
    count_dbt_1m_list_CD.append(count_dbt_1m_CD)
    count_dbt_1m_list_CV.append(count_dbt_1m_CV)
    count_dbt_1m_list_GL.append(count_dbt_1m_GL)
    count_dbt_1m_list_HL.append(count_dbt_1m_HL)
    count_dbt_1m_list_LAS.append(count_dbt_1m_LAS)
    count_dbt_1m_list_MFBL.append(count_dbt_1m_MFBL)
    count_dbt_1m_list_MFHL.append(count_dbt_1m_MFHL)
    count_dbt_1m_list_MFOT.append(count_dbt_1m_MFOT)
    count_dbt_1m_list_OTH.append(count_dbt_1m_OTH)
    count_dbt_1m_list_PL.append(count_dbt_1m_PL)
    count_dbt_1m_list_PLBL.append(count_dbt_1m_PLBL)
    count_dbt_1m_list_RL.append(count_dbt_1m_RL)
    count_dbt_1m_list_SCC.append(count_dbt_1m_SCC)
    count_dbt_1m_list_SEL.append(count_dbt_1m_SEL)

    count_dbt_1m_AL = 0
    count_dbt_1m_BL = 0
    count_dbt_1m_CC = 0
    count_dbt_1m_CD = 0
    count_dbt_1m_CV = 0
    count_dbt_1m_GL = 0
    count_dbt_1m_HL = 0
    count_dbt_1m_LAS = 0
    count_dbt_1m_MFBL = 0
    count_dbt_1m_MFHL = 0
    count_dbt_1m_MFOT = 0
    count_dbt_1m_OTH = 0
    count_dbt_1m_PL = 0
    count_dbt_1m_PLBL = 0
    count_dbt_1m_RL = 0
    count_dbt_1m_SCC = 0
    count_dbt_1m_SEL = 0

    count_dbt_3m_list_AL.append(count_dbt_3m_AL)
    count_dbt_3m_list_BL.append(count_dbt_3m_BL)
    count_dbt_3m_list_CC.append(count_dbt_3m_CC)
    count_dbt_3m_list_CD.append(count_dbt_3m_CD)
    count_dbt_3m_list_CV.append(count_dbt_3m_CV)
    count_dbt_3m_list_GL.append(count_dbt_3m_GL)
    count_dbt_3m_list_HL.append(count_dbt_3m_HL)
    count_dbt_3m_list_LAS.append(count_dbt_3m_LAS)
    count_dbt_3m_list_MFBL.append(count_dbt_3m_MFBL)
    count_dbt_3m_list_MFHL.append(count_dbt_3m_MFHL)
    count_dbt_3m_list_MFOT.append(count_dbt_3m_MFOT)
    count_dbt_3m_list_OTH.append(count_dbt_3m_OTH)
    count_dbt_3m_list_PL.append(count_dbt_3m_PL)
    count_dbt_3m_list_PLBL.append(count_dbt_3m_PLBL)
    count_dbt_3m_list_RL.append(count_dbt_3m_RL)
    count_dbt_3m_list_SCC.append(count_dbt_3m_SCC)
    count_dbt_3m_list_SEL.append(count_dbt_3m_SEL)

    count_dbt_3m_AL = 0
    count_dbt_3m_BL = 0
    count_dbt_3m_CC = 0
    count_dbt_3m_CD = 0
    count_dbt_3m_CV = 0
    count_dbt_3m_GL = 0
    count_dbt_3m_HL = 0
    count_dbt_3m_LAS = 0
    count_dbt_3m_MFBL = 0
    count_dbt_3m_MFHL = 0
    count_dbt_3m_MFOT = 0
    count_dbt_3m_OTH = 0
    count_dbt_3m_PL = 0
    count_dbt_3m_PLBL = 0
    count_dbt_3m_RL = 0
    count_dbt_3m_SCC = 0
    count_dbt_3m_SEL = 0

    count_dbt_6m_list_AL.append(count_dbt_6m_AL)
    count_dbt_6m_list_BL.append(count_dbt_6m_BL)
    count_dbt_6m_list_CC.append(count_dbt_6m_CC)
    count_dbt_6m_list_CD.append(count_dbt_6m_CD)
    count_dbt_6m_list_CV.append(count_dbt_6m_CV)
    count_dbt_6m_list_GL.append(count_dbt_6m_GL)
    count_dbt_6m_list_HL.append(count_dbt_6m_HL)
    count_dbt_6m_list_LAS.append(count_dbt_6m_LAS)
    count_dbt_6m_list_MFBL.append(count_dbt_6m_MFBL)
    count_dbt_6m_list_MFHL.append(count_dbt_6m_MFHL)
    count_dbt_6m_list_MFOT.append(count_dbt_6m_MFOT)
    count_dbt_6m_list_OTH.append(count_dbt_6m_OTH)
    count_dbt_6m_list_PL.append(count_dbt_6m_PL)
    count_dbt_6m_list_PLBL.append(count_dbt_6m_PLBL)
    count_dbt_6m_list_RL.append(count_dbt_6m_RL)
    count_dbt_6m_list_SCC.append(count_dbt_6m_SCC)
    count_dbt_6m_list_SEL.append(count_dbt_6m_SEL)

    count_dbt_6m_AL = 0
    count_dbt_6m_BL = 0
    count_dbt_6m_CC = 0
    count_dbt_6m_CD = 0
    count_dbt_6m_CV = 0
    count_dbt_6m_GL = 0
    count_dbt_6m_HL = 0
    count_dbt_6m_LAS = 0
    count_dbt_6m_MFBL = 0
    count_dbt_6m_MFHL = 0
    count_dbt_6m_MFOT = 0
    count_dbt_6m_OTH = 0
    count_dbt_6m_PL = 0
    count_dbt_6m_PLBL = 0
    count_dbt_6m_RL = 0
    count_dbt_6m_SCC = 0
    count_dbt_6m_SEL = 0

    count_dbt_1y_list_AL.append(count_dbt_1y_AL)
    count_dbt_1y_list_BL.append(count_dbt_1y_BL)
    count_dbt_1y_list_CC.append(count_dbt_1y_CC)
    count_dbt_1y_list_CD.append(count_dbt_1y_CD)
    count_dbt_1y_list_CV.append(count_dbt_1y_CV)
    count_dbt_1y_list_GL.append(count_dbt_1y_GL)
    count_dbt_1y_list_HL.append(count_dbt_1y_HL)
    count_dbt_1y_list_LAS.append(count_dbt_1y_LAS)
    count_dbt_1y_list_MFBL.append(count_dbt_1y_MFBL)
    count_dbt_1y_list_MFHL.append(count_dbt_1y_MFHL)
    count_dbt_1y_list_MFOT.append(count_dbt_1y_MFOT)
    count_dbt_1y_list_OTH.append(count_dbt_1y_OTH)
    count_dbt_1y_list_PL.append(count_dbt_1y_PL)
    count_dbt_1y_list_PLBL.append(count_dbt_1y_PLBL)
    count_dbt_1y_list_RL.append(count_dbt_1y_RL)
    count_dbt_1y_list_SCC.append(count_dbt_1y_SCC)
    count_dbt_1y_list_SEL.append(count_dbt_1y_SEL)

    count_dbt_1y_AL = 0
    count_dbt_1y_BL = 0
    count_dbt_1y_CC = 0
    count_dbt_1y_CD = 0
    count_dbt_1y_CV = 0
    count_dbt_1y_GL = 0
    count_dbt_1y_HL = 0
    count_dbt_1y_LAS = 0
    count_dbt_1y_MFBL = 0
    count_dbt_1y_MFHL = 0
    count_dbt_1y_MFOT = 0
    count_dbt_1y_OTH = 0
    count_dbt_1y_PL = 0
    count_dbt_1y_PLBL = 0
    count_dbt_1y_RL = 0
    count_dbt_1y_SCC = 0
    count_dbt_1y_SEL = 0

    count_dbt_2y_list_AL.append(count_dbt_2y_AL)
    count_dbt_2y_list_BL.append(count_dbt_2y_BL)
    count_dbt_2y_list_CC.append(count_dbt_2y_CC)
    count_dbt_2y_list_CD.append(count_dbt_2y_CD)
    count_dbt_2y_list_CV.append(count_dbt_2y_CV)
    count_dbt_2y_list_GL.append(count_dbt_2y_GL)
    count_dbt_2y_list_HL.append(count_dbt_2y_HL)
    count_dbt_2y_list_LAS.append(count_dbt_2y_LAS)
    count_dbt_2y_list_MFBL.append(count_dbt_2y_MFBL)
    count_dbt_2y_list_MFHL.append(count_dbt_2y_MFHL)
    count_dbt_2y_list_MFOT.append(count_dbt_2y_MFOT)
    count_dbt_2y_list_OTH.append(count_dbt_2y_OTH)
    count_dbt_2y_list_PL.append(count_dbt_2y_PL)
    count_dbt_2y_list_PLBL.append(count_dbt_2y_PLBL)
    count_dbt_2y_list_RL.append(count_dbt_2y_RL)
    count_dbt_2y_list_SCC.append(count_dbt_2y_SCC)
    count_dbt_2y_list_SEL.append(count_dbt_2y_SEL)

    count_dbt_2y_AL = 0
    count_dbt_2y_BL = 0
    count_dbt_2y_CC = 0
    count_dbt_2y_CD = 0
    count_dbt_2y_CV = 0
    count_dbt_2y_GL = 0
    count_dbt_2y_HL = 0
    count_dbt_2y_LAS = 0
    count_dbt_2y_MFBL = 0
    count_dbt_2y_MFHL = 0
    count_dbt_2y_MFOT = 0
    count_dbt_2y_OTH = 0
    count_dbt_2y_PL = 0
    count_dbt_2y_PLBL = 0
    count_dbt_2y_RL = 0
    count_dbt_2y_SCC = 0
    count_dbt_2y_SEL = 0

    count_dbt_3y_list_AL.append(count_dbt_3y_AL)
    count_dbt_3y_list_BL.append(count_dbt_3y_BL)
    count_dbt_3y_list_CC.append(count_dbt_3y_CC)
    count_dbt_3y_list_CD.append(count_dbt_3y_CD)
    count_dbt_3y_list_CV.append(count_dbt_3y_CV)
    count_dbt_3y_list_GL.append(count_dbt_3y_GL)
    count_dbt_3y_list_HL.append(count_dbt_3y_HL)
    count_dbt_3y_list_LAS.append(count_dbt_3y_LAS)
    count_dbt_3y_list_MFBL.append(count_dbt_3y_MFBL)
    count_dbt_3y_list_MFHL.append(count_dbt_3y_MFHL)
    count_dbt_3y_list_MFOT.append(count_dbt_3y_MFOT)
    count_dbt_3y_list_OTH.append(count_dbt_3y_OTH)
    count_dbt_3y_list_PL.append(count_dbt_3y_PL)
    count_dbt_3y_list_PLBL.append(count_dbt_3y_PLBL)
    count_dbt_3y_list_RL.append(count_dbt_3y_RL)
    count_dbt_3y_list_SCC.append(count_dbt_3y_SCC)
    count_dbt_3y_list_SEL.append(count_dbt_3y_SEL)

    count_dbt_3y_AL = 0
    count_dbt_3y_BL = 0
    count_dbt_3y_CC = 0
    count_dbt_3y_CD = 0
    count_dbt_3y_CV = 0
    count_dbt_3y_GL = 0
    count_dbt_3y_HL = 0
    count_dbt_3y_LAS = 0
    count_dbt_3y_MFBL = 0
    count_dbt_3y_MFHL = 0
    count_dbt_3y_MFOT = 0
    count_dbt_3y_OTH = 0
    count_dbt_3y_PL = 0
    count_dbt_3y_PLBL = 0
    count_dbt_3y_RL = 0
    count_dbt_3y_SCC = 0
    count_dbt_3y_SEL = 0

    count_los_list_1m.append(count_los_1m)
    count_los_1m = 0
    count_los_list_3m.append(count_los_3m)
    count_los_3m = 0
    count_los_list_6m.append(count_los_6m)
    count_los_6m = 0
    count_los_list_1y.append(count_los_1y)
    count_los_1y = 0
    count_los_list_2y.append(count_los_2y)
    count_los_2y = 0
    count_los_list_3y.append(count_los_3y)
    count_los_3y = 0

    count_los_1m_list_AL.append(count_los_1m_AL)
    count_los_1m_list_BL.append(count_los_1m_BL)
    count_los_1m_list_CC.append(count_los_1m_CC)
    count_los_1m_list_CD.append(count_los_1m_CD)
    count_los_1m_list_CV.append(count_los_1m_CV)
    count_los_1m_list_GL.append(count_los_1m_GL)
    count_los_1m_list_HL.append(count_los_1m_HL)
    count_los_1m_list_LAS.append(count_los_1m_LAS)
    count_los_1m_list_MFBL.append(count_los_1m_MFBL)
    count_los_1m_list_MFHL.append(count_los_1m_MFHL)
    count_los_1m_list_MFOT.append(count_los_1m_MFOT)
    count_los_1m_list_OTH.append(count_los_1m_OTH)
    count_los_1m_list_PL.append(count_los_1m_PL)
    count_los_1m_list_PLBL.append(count_los_1m_PLBL)
    count_los_1m_list_RL.append(count_los_1m_RL)
    count_los_1m_list_SCC.append(count_los_1m_SCC)
    count_los_1m_list_SEL.append(count_los_1m_SEL)

    count_los_1m_AL = 0
    count_los_1m_BL = 0
    count_los_1m_CC = 0
    count_los_1m_CD = 0
    count_los_1m_CV = 0
    count_los_1m_GL = 0
    count_los_1m_HL = 0
    count_los_1m_LAS = 0
    count_los_1m_MFBL = 0
    count_los_1m_MFHL = 0
    count_los_1m_MFOT = 0
    count_los_1m_OTH = 0
    count_los_1m_PL = 0
    count_los_1m_PLBL = 0
    count_los_1m_RL = 0
    count_los_1m_SCC = 0
    count_los_1m_SEL = 0

    count_los_3m_list_AL.append(count_los_3m_AL)
    count_los_3m_list_BL.append(count_los_3m_BL)
    count_los_3m_list_CC.append(count_los_3m_CC)
    count_los_3m_list_CD.append(count_los_3m_CD)
    count_los_3m_list_CV.append(count_los_3m_CV)
    count_los_3m_list_GL.append(count_los_3m_GL)
    count_los_3m_list_HL.append(count_los_3m_HL)
    count_los_3m_list_LAS.append(count_los_3m_LAS)
    count_los_3m_list_MFBL.append(count_los_3m_MFBL)
    count_los_3m_list_MFHL.append(count_los_3m_MFHL)
    count_los_3m_list_MFOT.append(count_los_3m_MFOT)
    count_los_3m_list_OTH.append(count_los_3m_OTH)
    count_los_3m_list_PL.append(count_los_3m_PL)
    count_los_3m_list_PLBL.append(count_los_3m_PLBL)
    count_los_3m_list_RL.append(count_los_3m_RL)
    count_los_3m_list_SCC.append(count_los_3m_SCC)
    count_los_3m_list_SEL.append(count_los_3m_SEL)

    count_los_3m_AL = 0
    count_los_3m_BL = 0
    count_los_3m_CC = 0
    count_los_3m_CD = 0
    count_los_3m_CV = 0
    count_los_3m_GL = 0
    count_los_3m_HL = 0
    count_los_3m_LAS = 0
    count_los_3m_MFBL = 0
    count_los_3m_MFHL = 0
    count_los_3m_MFOT = 0
    count_los_3m_OTH = 0
    count_los_3m_PL = 0
    count_los_3m_PLBL = 0
    count_los_3m_RL = 0
    count_los_3m_SCC = 0
    count_los_3m_SEL = 0

    count_los_6m_list_AL.append(count_los_6m_AL)
    count_los_6m_list_BL.append(count_los_6m_BL)
    count_los_6m_list_CC.append(count_los_6m_CC)
    count_los_6m_list_CD.append(count_los_6m_CD)
    count_los_6m_list_CV.append(count_los_6m_CV)
    count_los_6m_list_GL.append(count_los_6m_GL)
    count_los_6m_list_HL.append(count_los_6m_HL)
    count_los_6m_list_LAS.append(count_los_6m_LAS)
    count_los_6m_list_MFBL.append(count_los_6m_MFBL)
    count_los_6m_list_MFHL.append(count_los_6m_MFHL)
    count_los_6m_list_MFOT.append(count_los_6m_MFOT)
    count_los_6m_list_OTH.append(count_los_6m_OTH)
    count_los_6m_list_PL.append(count_los_6m_PL)
    count_los_6m_list_PLBL.append(count_los_6m_PLBL)
    count_los_6m_list_RL.append(count_los_6m_RL)
    count_los_6m_list_SCC.append(count_los_6m_SCC)
    count_los_6m_list_SEL.append(count_los_6m_SEL)

    count_los_6m_AL = 0
    count_los_6m_BL = 0
    count_los_6m_CC = 0
    count_los_6m_CD = 0
    count_los_6m_CV = 0
    count_los_6m_GL = 0
    count_los_6m_HL = 0
    count_los_6m_LAS = 0
    count_los_6m_MFBL = 0
    count_los_6m_MFHL = 0
    count_los_6m_MFOT = 0
    count_los_6m_OTH = 0
    count_los_6m_PL = 0
    count_los_6m_PLBL = 0
    count_los_6m_RL = 0
    count_los_6m_SCC = 0
    count_los_6m_SEL = 0

    count_los_1y_list_AL.append(count_los_1y_AL)
    count_los_1y_list_BL.append(count_los_1y_BL)
    count_los_1y_list_CC.append(count_los_1y_CC)
    count_los_1y_list_CD.append(count_los_1y_CD)
    count_los_1y_list_CV.append(count_los_1y_CV)
    count_los_1y_list_GL.append(count_los_1y_GL)
    count_los_1y_list_HL.append(count_los_1y_HL)
    count_los_1y_list_LAS.append(count_los_1y_LAS)
    count_los_1y_list_MFBL.append(count_los_1y_MFBL)
    count_los_1y_list_MFHL.append(count_los_1y_MFHL)
    count_los_1y_list_MFOT.append(count_los_1y_MFOT)
    count_los_1y_list_OTH.append(count_los_1y_OTH)
    count_los_1y_list_PL.append(count_los_1y_PL)
    count_los_1y_list_PLBL.append(count_los_1y_PLBL)
    count_los_1y_list_RL.append(count_los_1y_RL)
    count_los_1y_list_SCC.append(count_los_1y_SCC)
    count_los_1y_list_SEL.append(count_los_1y_SEL)

    count_los_1y_AL = 0
    count_los_1y_BL = 0
    count_los_1y_CC = 0
    count_los_1y_CD = 0
    count_los_1y_CV = 0
    count_los_1y_GL = 0
    count_los_1y_HL = 0
    count_los_1y_LAS = 0
    count_los_1y_MFBL = 0
    count_los_1y_MFHL = 0
    count_los_1y_MFOT = 0
    count_los_1y_OTH = 0
    count_los_1y_PL = 0
    count_los_1y_PLBL = 0
    count_los_1y_RL = 0
    count_los_1y_SCC = 0
    count_los_1y_SEL = 0

    count_los_2y_list_AL.append(count_los_2y_AL)
    count_los_2y_list_BL.append(count_los_2y_BL)
    count_los_2y_list_CC.append(count_los_2y_CC)
    count_los_2y_list_CD.append(count_los_2y_CD)
    count_los_2y_list_CV.append(count_los_2y_CV)
    count_los_2y_list_GL.append(count_los_2y_GL)
    count_los_2y_list_HL.append(count_los_2y_HL)
    count_los_2y_list_LAS.append(count_los_2y_LAS)
    count_los_2y_list_MFBL.append(count_los_2y_MFBL)
    count_los_2y_list_MFHL.append(count_los_2y_MFHL)
    count_los_2y_list_MFOT.append(count_los_2y_MFOT)
    count_los_2y_list_OTH.append(count_los_2y_OTH)
    count_los_2y_list_PL.append(count_los_2y_PL)
    count_los_2y_list_PLBL.append(count_los_2y_PLBL)
    count_los_2y_list_RL.append(count_los_2y_RL)
    count_los_2y_list_SCC.append(count_los_2y_SCC)
    count_los_2y_list_SEL.append(count_los_2y_SEL)

    count_los_2y_AL = 0
    count_los_2y_BL = 0
    count_los_2y_CC = 0
    count_los_2y_CD = 0
    count_los_2y_CV = 0
    count_los_2y_GL = 0
    count_los_2y_HL = 0
    count_los_2y_LAS = 0
    count_los_2y_MFBL = 0
    count_los_2y_MFHL = 0
    count_los_2y_MFOT = 0
    count_los_2y_OTH = 0
    count_los_2y_PL = 0
    count_los_2y_PLBL = 0
    count_los_2y_RL = 0
    count_los_2y_SCC = 0
    count_los_2y_SEL = 0

    count_los_3y_list_AL.append(count_los_3y_AL)
    count_los_3y_list_BL.append(count_los_3y_BL)
    count_los_3y_list_CC.append(count_los_3y_CC)
    count_los_3y_list_CD.append(count_los_3y_CD)
    count_los_3y_list_CV.append(count_los_3y_CV)
    count_los_3y_list_GL.append(count_los_3y_GL)
    count_los_3y_list_HL.append(count_los_3y_HL)
    count_los_3y_list_LAS.append(count_los_3y_LAS)
    count_los_3y_list_MFBL.append(count_los_3y_MFBL)
    count_los_3y_list_MFHL.append(count_los_3y_MFHL)
    count_los_3y_list_MFOT.append(count_los_3y_MFOT)
    count_los_3y_list_OTH.append(count_los_3y_OTH)
    count_los_3y_list_PL.append(count_los_3y_PL)
    count_los_3y_list_PLBL.append(count_los_3y_PLBL)
    count_los_3y_list_RL.append(count_los_3y_RL)
    count_los_3y_list_SCC.append(count_los_3y_SCC)
    count_los_3y_list_SEL.append(count_los_3y_SEL)

    count_los_3y_AL = 0
    count_los_3y_BL = 0
    count_los_3y_CC = 0
    count_los_3y_CD = 0
    count_los_3y_CV = 0
    count_los_3y_GL = 0
    count_los_3y_HL = 0
    count_los_3y_LAS = 0
    count_los_3y_MFBL = 0
    count_los_3y_MFHL = 0
    count_los_3y_MFOT = 0
    count_los_3y_OTH = 0
    count_los_3y_PL = 0
    count_los_3y_PLBL = 0
    count_los_3y_RL = 0
    count_los_3y_SCC = 0
    count_los_3y_SEL = 0

    count_xxx_list_1m.append(count_xxx_1m)
    count_xxx_1m = 0
    count_xxx_list_3m.append(count_xxx_3m)
    count_xxx_3m = 0
    count_xxx_list_6m.append(count_xxx_6m)
    count_xxx_6m = 0
    count_xxx_list_1y.append(count_xxx_1y)
    count_xxx_1y = 0
    count_xxx_list_2y.append(count_xxx_2y)
    count_xxx_2y = 0
    count_xxx_list_3y.append(count_xxx_3y)
    count_xxx_3y = 0

    count_xxx_1m_list_AL.append(count_xxx_1m_AL)
    count_xxx_1m_list_BL.append(count_xxx_1m_BL)
    count_xxx_1m_list_CC.append(count_xxx_1m_CC)
    count_xxx_1m_list_CD.append(count_xxx_1m_CD)
    count_xxx_1m_list_CV.append(count_xxx_1m_CV)
    count_xxx_1m_list_GL.append(count_xxx_1m_GL)
    count_xxx_1m_list_HL.append(count_xxx_1m_HL)
    count_xxx_1m_list_LAS.append(count_xxx_1m_LAS)
    count_xxx_1m_list_MFBL.append(count_xxx_1m_MFBL)
    count_xxx_1m_list_MFHL.append(count_xxx_1m_MFHL)
    count_xxx_1m_list_MFOT.append(count_xxx_1m_MFOT)
    count_xxx_1m_list_OTH.append(count_xxx_1m_OTH)
    count_xxx_1m_list_PL.append(count_xxx_1m_PL)
    count_xxx_1m_list_PLBL.append(count_xxx_1m_PLBL)
    count_xxx_1m_list_RL.append(count_xxx_1m_RL)
    count_xxx_1m_list_SCC.append(count_xxx_1m_SCC)
    count_xxx_1m_list_SEL.append(count_xxx_1m_SEL)

    count_xxx_1m_AL = 0
    count_xxx_1m_BL = 0
    count_xxx_1m_CC = 0
    count_xxx_1m_CD = 0
    count_xxx_1m_CV = 0
    count_xxx_1m_GL = 0
    count_xxx_1m_HL = 0
    count_xxx_1m_LAS = 0
    count_xxx_1m_MFBL = 0
    count_xxx_1m_MFHL = 0
    count_xxx_1m_MFOT = 0
    count_xxx_1m_OTH = 0
    count_xxx_1m_PL = 0
    count_xxx_1m_PLBL = 0
    count_xxx_1m_RL = 0
    count_xxx_1m_SCC = 0
    count_xxx_1m_SEL = 0

    count_xxx_3m_list_AL.append(count_xxx_3m_AL)
    count_xxx_3m_list_BL.append(count_xxx_3m_BL)
    count_xxx_3m_list_CC.append(count_xxx_3m_CC)
    count_xxx_3m_list_CD.append(count_xxx_3m_CD)
    count_xxx_3m_list_CV.append(count_xxx_3m_CV)
    count_xxx_3m_list_GL.append(count_xxx_3m_GL)
    count_xxx_3m_list_HL.append(count_xxx_3m_HL)
    count_xxx_3m_list_LAS.append(count_xxx_3m_LAS)
    count_xxx_3m_list_MFBL.append(count_xxx_3m_MFBL)
    count_xxx_3m_list_MFHL.append(count_xxx_3m_MFHL)
    count_xxx_3m_list_MFOT.append(count_xxx_3m_MFOT)
    count_xxx_3m_list_OTH.append(count_xxx_3m_OTH)
    count_xxx_3m_list_PL.append(count_xxx_3m_PL)
    count_xxx_3m_list_PLBL.append(count_xxx_3m_PLBL)
    count_xxx_3m_list_RL.append(count_xxx_3m_RL)
    count_xxx_3m_list_SCC.append(count_xxx_3m_SCC)
    count_xxx_3m_list_SEL.append(count_xxx_3m_SEL)

    count_xxx_3m_AL = 0
    count_xxx_3m_BL = 0
    count_xxx_3m_CC = 0
    count_xxx_3m_CD = 0
    count_xxx_3m_CV = 0
    count_xxx_3m_GL = 0
    count_xxx_3m_HL = 0
    count_xxx_3m_LAS = 0
    count_xxx_3m_MFBL = 0
    count_xxx_3m_MFHL = 0
    count_xxx_3m_MFOT = 0
    count_xxx_3m_OTH = 0
    count_xxx_3m_PL = 0
    count_xxx_3m_PLBL = 0
    count_xxx_3m_RL = 0
    count_xxx_3m_SCC = 0
    count_xxx_3m_SEL = 0

    count_xxx_6m_list_AL.append(count_xxx_6m_AL)
    count_xxx_6m_list_BL.append(count_xxx_6m_BL)
    count_xxx_6m_list_CC.append(count_xxx_6m_CC)
    count_xxx_6m_list_CD.append(count_xxx_6m_CD)
    count_xxx_6m_list_CV.append(count_xxx_6m_CV)
    count_xxx_6m_list_GL.append(count_xxx_6m_GL)
    count_xxx_6m_list_HL.append(count_xxx_6m_HL)
    count_xxx_6m_list_LAS.append(count_xxx_6m_LAS)
    count_xxx_6m_list_MFBL.append(count_xxx_6m_MFBL)
    count_xxx_6m_list_MFHL.append(count_xxx_6m_MFHL)
    count_xxx_6m_list_MFOT.append(count_xxx_6m_MFOT)
    count_xxx_6m_list_OTH.append(count_xxx_6m_OTH)
    count_xxx_6m_list_PL.append(count_xxx_6m_PL)
    count_xxx_6m_list_PLBL.append(count_xxx_6m_PLBL)
    count_xxx_6m_list_RL.append(count_xxx_6m_RL)
    count_xxx_6m_list_SCC.append(count_xxx_6m_SCC)
    count_xxx_6m_list_SEL.append(count_xxx_6m_SEL)

    count_xxx_6m_AL = 0
    count_xxx_6m_BL = 0
    count_xxx_6m_CC = 0
    count_xxx_6m_CD = 0
    count_xxx_6m_CV = 0
    count_xxx_6m_GL = 0
    count_xxx_6m_HL = 0
    count_xxx_6m_LAS = 0
    count_xxx_6m_MFBL = 0
    count_xxx_6m_MFHL = 0
    count_xxx_6m_MFOT = 0
    count_xxx_6m_OTH = 0
    count_xxx_6m_PL = 0
    count_xxx_6m_PLBL = 0
    count_xxx_6m_RL = 0
    count_xxx_6m_SCC = 0
    count_xxx_6m_SEL = 0

    count_xxx_1y_list_AL.append(count_xxx_1y_AL)
    count_xxx_1y_list_BL.append(count_xxx_1y_BL)
    count_xxx_1y_list_CC.append(count_xxx_1y_CC)
    count_xxx_1y_list_CD.append(count_xxx_1y_CD)
    count_xxx_1y_list_CV.append(count_xxx_1y_CV)
    count_xxx_1y_list_GL.append(count_xxx_1y_GL)
    count_xxx_1y_list_HL.append(count_xxx_1y_HL)
    count_xxx_1y_list_LAS.append(count_xxx_1y_LAS)
    count_xxx_1y_list_MFBL.append(count_xxx_1y_MFBL)
    count_xxx_1y_list_MFHL.append(count_xxx_1y_MFHL)
    count_xxx_1y_list_MFOT.append(count_xxx_1y_MFOT)
    count_xxx_1y_list_OTH.append(count_xxx_1y_OTH)
    count_xxx_1y_list_PL.append(count_xxx_1y_PL)
    count_xxx_1y_list_PLBL.append(count_xxx_1y_PLBL)
    count_xxx_1y_list_RL.append(count_xxx_1y_RL)
    count_xxx_1y_list_SCC.append(count_xxx_1y_SCC)
    count_xxx_1y_list_SEL.append(count_xxx_1y_SEL)

    count_xxx_1y_AL = 0
    count_xxx_1y_BL = 0
    count_xxx_1y_CC = 0
    count_xxx_1y_CD = 0
    count_xxx_1y_CV = 0
    count_xxx_1y_GL = 0
    count_xxx_1y_HL = 0
    count_xxx_1y_LAS = 0
    count_xxx_1y_MFBL = 0
    count_xxx_1y_MFHL = 0
    count_xxx_1y_MFOT = 0
    count_xxx_1y_OTH = 0
    count_xxx_1y_PL = 0
    count_xxx_1y_PLBL = 0
    count_xxx_1y_RL = 0
    count_xxx_1y_SCC = 0
    count_xxx_1y_SEL = 0

    count_xxx_2y_list_AL.append(count_xxx_2y_AL)
    count_xxx_2y_list_BL.append(count_xxx_2y_BL)
    count_xxx_2y_list_CC.append(count_xxx_2y_CC)
    count_xxx_2y_list_CD.append(count_xxx_2y_CD)
    count_xxx_2y_list_CV.append(count_xxx_2y_CV)
    count_xxx_2y_list_GL.append(count_xxx_2y_GL)
    count_xxx_2y_list_HL.append(count_xxx_2y_HL)
    count_xxx_2y_list_LAS.append(count_xxx_2y_LAS)
    count_xxx_2y_list_MFBL.append(count_xxx_2y_MFBL)
    count_xxx_2y_list_MFHL.append(count_xxx_2y_MFHL)
    count_xxx_2y_list_MFOT.append(count_xxx_2y_MFOT)
    count_xxx_2y_list_OTH.append(count_xxx_2y_OTH)
    count_xxx_2y_list_PL.append(count_xxx_2y_PL)
    count_xxx_2y_list_PLBL.append(count_xxx_2y_PLBL)
    count_xxx_2y_list_RL.append(count_xxx_2y_RL)
    count_xxx_2y_list_SCC.append(count_xxx_2y_SCC)
    count_xxx_2y_list_SEL.append(count_xxx_2y_SEL)

    count_xxx_2y_AL = 0
    count_xxx_2y_BL = 0
    count_xxx_2y_CC = 0
    count_xxx_2y_CD = 0
    count_xxx_2y_CV = 0
    count_xxx_2y_GL = 0
    count_xxx_2y_HL = 0
    count_xxx_2y_LAS = 0
    count_xxx_2y_MFBL = 0
    count_xxx_2y_MFHL = 0
    count_xxx_2y_MFOT = 0
    count_xxx_2y_OTH = 0
    count_xxx_2y_PL = 0
    count_xxx_2y_PLBL = 0
    count_xxx_2y_RL = 0
    count_xxx_2y_SCC = 0
    count_xxx_2y_SEL = 0

    count_xxx_3y_list_AL.append(count_xxx_3y_AL)
    count_xxx_3y_list_BL.append(count_xxx_3y_BL)
    count_xxx_3y_list_CC.append(count_xxx_3y_CC)
    count_xxx_3y_list_CD.append(count_xxx_3y_CD)
    count_xxx_3y_list_CV.append(count_xxx_3y_CV)
    count_xxx_3y_list_GL.append(count_xxx_3y_GL)
    count_xxx_3y_list_HL.append(count_xxx_3y_HL)
    count_xxx_3y_list_LAS.append(count_xxx_3y_LAS)
    count_xxx_3y_list_MFBL.append(count_xxx_3y_MFBL)
    count_xxx_3y_list_MFHL.append(count_xxx_3y_MFHL)
    count_xxx_3y_list_MFOT.append(count_xxx_3y_MFOT)
    count_xxx_3y_list_OTH.append(count_xxx_3y_OTH)
    count_xxx_3y_list_PL.append(count_xxx_3y_PL)
    count_xxx_3y_list_PLBL.append(count_xxx_3y_PLBL)
    count_xxx_3y_list_RL.append(count_xxx_3y_RL)
    count_xxx_3y_list_SCC.append(count_xxx_3y_SCC)
    count_xxx_3y_list_SEL.append(count_xxx_3y_SEL)

    count_xxx_3y_AL = 0
    count_xxx_3y_BL = 0
    count_xxx_3y_CC = 0
    count_xxx_3y_CD = 0
    count_xxx_3y_CV = 0
    count_xxx_3y_GL = 0
    count_xxx_3y_HL = 0
    count_xxx_3y_LAS = 0
    count_xxx_3y_MFBL = 0
    count_xxx_3y_MFHL = 0
    count_xxx_3y_MFOT = 0
    count_xxx_3y_OTH = 0
    count_xxx_3y_PL = 0
    count_xxx_3y_PLBL = 0
    count_xxx_3y_RL = 0
    count_xxx_3y_SCC = 0
    count_xxx_3y_SEL = 0

    count_sma_list_1m.append(count_sma_1m)
    count_sma_1m = 0
    count_sma_list_3m.append(count_sma_3m)
    count_sma_3m = 0
    count_sma_list_6m.append(count_sma_6m)
    count_sma_6m = 0
    count_sma_list_1y.append(count_sma_1y)
    count_sma_1y = 0
    count_sma_list_2y.append(count_sma_2y)
    count_sma_2y = 0
    count_sma_list_3y.append(count_sma_3y)
    count_sma_3y = 0

    count_sma_1m_list_AL.append(count_sma_1m_AL)
    count_sma_1m_list_BL.append(count_sma_1m_BL)
    count_sma_1m_list_CC.append(count_sma_1m_CC)
    count_sma_1m_list_CD.append(count_sma_1m_CD)
    count_sma_1m_list_CV.append(count_sma_1m_CV)
    count_sma_1m_list_GL.append(count_sma_1m_GL)
    count_sma_1m_list_HL.append(count_sma_1m_HL)
    count_sma_1m_list_LAS.append(count_sma_1m_LAS)
    count_sma_1m_list_MFBL.append(count_sma_1m_MFBL)
    count_sma_1m_list_MFHL.append(count_sma_1m_MFHL)
    count_sma_1m_list_MFOT.append(count_sma_1m_MFOT)
    count_sma_1m_list_OTH.append(count_sma_1m_OTH)
    count_sma_1m_list_PL.append(count_sma_1m_PL)
    count_sma_1m_list_PLBL.append(count_sma_1m_PLBL)
    count_sma_1m_list_RL.append(count_sma_1m_RL)
    count_sma_1m_list_SCC.append(count_sma_1m_SCC)
    count_sma_1m_list_SEL.append(count_sma_1m_SEL)

    count_sma_1m_AL = 0
    count_sma_1m_BL = 0
    count_sma_1m_CC = 0
    count_sma_1m_CD = 0
    count_sma_1m_CV = 0
    count_sma_1m_GL = 0
    count_sma_1m_HL = 0
    count_sma_1m_LAS = 0
    count_sma_1m_MFBL = 0
    count_sma_1m_MFHL = 0
    count_sma_1m_MFOT = 0
    count_sma_1m_OTH = 0
    count_sma_1m_PL = 0
    count_sma_1m_PLBL = 0
    count_sma_1m_RL = 0
    count_sma_1m_SCC = 0
    count_sma_1m_SEL = 0

    count_sma_3m_list_AL.append(count_sma_3m_AL)
    count_sma_3m_list_BL.append(count_sma_3m_BL)
    count_sma_3m_list_CC.append(count_sma_3m_CC)
    count_sma_3m_list_CD.append(count_sma_3m_CD)
    count_sma_3m_list_CV.append(count_sma_3m_CV)
    count_sma_3m_list_GL.append(count_sma_3m_GL)
    count_sma_3m_list_HL.append(count_sma_3m_HL)
    count_sma_3m_list_LAS.append(count_sma_3m_LAS)
    count_sma_3m_list_MFBL.append(count_sma_3m_MFBL)
    count_sma_3m_list_MFHL.append(count_sma_3m_MFHL)
    count_sma_3m_list_MFOT.append(count_sma_3m_MFOT)
    count_sma_3m_list_OTH.append(count_sma_3m_OTH)
    count_sma_3m_list_PL.append(count_sma_3m_PL)
    count_sma_3m_list_PLBL.append(count_sma_3m_PLBL)
    count_sma_3m_list_RL.append(count_sma_3m_RL)
    count_sma_3m_list_SCC.append(count_sma_3m_SCC)
    count_sma_3m_list_SEL.append(count_sma_3m_SEL)

    count_sma_3m_AL = 0
    count_sma_3m_BL = 0
    count_sma_3m_CC = 0
    count_sma_3m_CD = 0
    count_sma_3m_CV = 0
    count_sma_3m_GL = 0
    count_sma_3m_HL = 0
    count_sma_3m_LAS = 0
    count_sma_3m_MFBL = 0
    count_sma_3m_MFHL = 0
    count_sma_3m_MFOT = 0
    count_sma_3m_OTH = 0
    count_sma_3m_PL = 0
    count_sma_3m_PLBL = 0
    count_sma_3m_RL = 0
    count_sma_3m_SCC = 0
    count_sma_3m_SEL = 0

    count_sma_6m_list_AL.append(count_sma_6m_AL)
    count_sma_6m_list_BL.append(count_sma_6m_BL)
    count_sma_6m_list_CC.append(count_sma_6m_CC)
    count_sma_6m_list_CD.append(count_sma_6m_CD)
    count_sma_6m_list_CV.append(count_sma_6m_CV)
    count_sma_6m_list_GL.append(count_sma_6m_GL)
    count_sma_6m_list_HL.append(count_sma_6m_HL)
    count_sma_6m_list_LAS.append(count_sma_6m_LAS)
    count_sma_6m_list_MFBL.append(count_sma_6m_MFBL)
    count_sma_6m_list_MFHL.append(count_sma_6m_MFHL)
    count_sma_6m_list_MFOT.append(count_sma_6m_MFOT)
    count_sma_6m_list_OTH.append(count_sma_6m_OTH)
    count_sma_6m_list_PL.append(count_sma_6m_PL)
    count_sma_6m_list_PLBL.append(count_sma_6m_PLBL)
    count_sma_6m_list_RL.append(count_sma_6m_RL)
    count_sma_6m_list_SCC.append(count_sma_6m_SCC)
    count_sma_6m_list_SEL.append(count_sma_6m_SEL)

    count_sma_6m_AL = 0
    count_sma_6m_BL = 0
    count_sma_6m_CC = 0
    count_sma_6m_CD = 0
    count_sma_6m_CV = 0
    count_sma_6m_GL = 0
    count_sma_6m_HL = 0
    count_sma_6m_LAS = 0
    count_sma_6m_MFBL = 0
    count_sma_6m_MFHL = 0
    count_sma_6m_MFOT = 0
    count_sma_6m_OTH = 0
    count_sma_6m_PL = 0
    count_sma_6m_PLBL = 0
    count_sma_6m_RL = 0
    count_sma_6m_SCC = 0
    count_sma_6m_SEL = 0

    count_sma_1y_list_AL.append(count_sma_1y_AL)
    count_sma_1y_list_BL.append(count_sma_1y_BL)
    count_sma_1y_list_CC.append(count_sma_1y_CC)
    count_sma_1y_list_CD.append(count_sma_1y_CD)
    count_sma_1y_list_CV.append(count_sma_1y_CV)
    count_sma_1y_list_GL.append(count_sma_1y_GL)
    count_sma_1y_list_HL.append(count_sma_1y_HL)
    count_sma_1y_list_LAS.append(count_sma_1y_LAS)
    count_sma_1y_list_MFBL.append(count_sma_1y_MFBL)
    count_sma_1y_list_MFHL.append(count_sma_1y_MFHL)
    count_sma_1y_list_MFOT.append(count_sma_1y_MFOT)
    count_sma_1y_list_OTH.append(count_sma_1y_OTH)
    count_sma_1y_list_PL.append(count_sma_1y_PL)
    count_sma_1y_list_PLBL.append(count_sma_1y_PLBL)
    count_sma_1y_list_RL.append(count_sma_1y_RL)
    count_sma_1y_list_SCC.append(count_sma_1y_SCC)
    count_sma_1y_list_SEL.append(count_sma_1y_SEL)

    count_sma_1y_AL = 0
    count_sma_1y_BL = 0
    count_sma_1y_CC = 0
    count_sma_1y_CD = 0
    count_sma_1y_CV = 0
    count_sma_1y_GL = 0
    count_sma_1y_HL = 0
    count_sma_1y_LAS = 0
    count_sma_1y_MFBL = 0
    count_sma_1y_MFHL = 0
    count_sma_1y_MFOT = 0
    count_sma_1y_OTH = 0
    count_sma_1y_PL = 0
    count_sma_1y_PLBL = 0
    count_sma_1y_RL = 0
    count_sma_1y_SCC = 0
    count_sma_1y_SEL = 0

    count_sma_2y_list_AL.append(count_sma_2y_AL)
    count_sma_2y_list_BL.append(count_sma_2y_BL)
    count_sma_2y_list_CC.append(count_sma_2y_CC)
    count_sma_2y_list_CD.append(count_sma_2y_CD)
    count_sma_2y_list_CV.append(count_sma_2y_CV)
    count_sma_2y_list_GL.append(count_sma_2y_GL)
    count_sma_2y_list_HL.append(count_sma_2y_HL)
    count_sma_2y_list_LAS.append(count_sma_2y_LAS)
    count_sma_2y_list_MFBL.append(count_sma_2y_MFBL)
    count_sma_2y_list_MFHL.append(count_sma_2y_MFHL)
    count_sma_2y_list_MFOT.append(count_sma_2y_MFOT)
    count_sma_2y_list_OTH.append(count_sma_2y_OTH)
    count_sma_2y_list_PL.append(count_sma_2y_PL)
    count_sma_2y_list_PLBL.append(count_sma_2y_PLBL)
    count_sma_2y_list_RL.append(count_sma_2y_RL)
    count_sma_2y_list_SCC.append(count_sma_2y_SCC)
    count_sma_2y_list_SEL.append(count_sma_2y_SEL)

    count_sma_2y_AL = 0
    count_sma_2y_BL = 0
    count_sma_2y_CC = 0
    count_sma_2y_CD = 0
    count_sma_2y_CV = 0
    count_sma_2y_GL = 0
    count_sma_2y_HL = 0
    count_sma_2y_LAS = 0
    count_sma_2y_MFBL = 0
    count_sma_2y_MFHL = 0
    count_sma_2y_MFOT = 0
    count_sma_2y_OTH = 0
    count_sma_2y_PL = 0
    count_sma_2y_PLBL = 0
    count_sma_2y_RL = 0
    count_sma_2y_SCC = 0
    count_sma_2y_SEL = 0

    count_sma_3y_list_AL.append(count_sma_3y_AL)
    count_sma_3y_list_BL.append(count_sma_3y_BL)
    count_sma_3y_list_CC.append(count_sma_3y_CC)
    count_sma_3y_list_CD.append(count_sma_3y_CD)
    count_sma_3y_list_CV.append(count_sma_3y_CV)
    count_sma_3y_list_GL.append(count_sma_3y_GL)
    count_sma_3y_list_HL.append(count_sma_3y_HL)
    count_sma_3y_list_LAS.append(count_sma_3y_LAS)
    count_sma_3y_list_MFBL.append(count_sma_3y_MFBL)
    count_sma_3y_list_MFHL.append(count_sma_3y_MFHL)
    count_sma_3y_list_MFOT.append(count_sma_3y_MFOT)
    count_sma_3y_list_OTH.append(count_sma_3y_OTH)
    count_sma_3y_list_PL.append(count_sma_3y_PL)
    count_sma_3y_list_PLBL.append(count_sma_3y_PLBL)
    count_sma_3y_list_RL.append(count_sma_3y_RL)
    count_sma_3y_list_SCC.append(count_sma_3y_SCC)
    count_sma_3y_list_SEL.append(count_sma_3y_SEL)

    count_sma_3y_AL = 0
    count_sma_3y_BL = 0
    count_sma_3y_CC = 0
    count_sma_3y_CD = 0
    count_sma_3y_CV = 0
    count_sma_3y_GL = 0
    count_sma_3y_HL = 0
    count_sma_3y_LAS = 0
    count_sma_3y_MFBL = 0
    count_sma_3y_MFHL = 0
    count_sma_3y_MFOT = 0
    count_sma_3y_OTH = 0
    count_sma_3y_PL = 0
    count_sma_3y_PLBL = 0
    count_sma_3y_RL = 0
    count_sma_3y_SCC = 0
    count_sma_3y_SEL = 0

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['DPD30P3M_flag'][i] == 1) or (grp_slice['DPD30P3M_flag'][i] == 0):
            DPD30P3M.append(count_list_30_3m[x])
        else:
            DPD30P3M.append('unknown')

        if (grp_slice['DPD60P3M_flag'][i] == 1) or (grp_slice['DPD60P3M_flag'][i] == 0):
            DPD60P3M.append(count_list_60_3m[x])
        else:
            DPD60P3M.append('unknown')

        if (grp_slice['DPD90P3M_flag'][i] == 1) or (grp_slice['DPD90P3M_flag'][i] == 0):
            DPD90P3M.append(count_list_90_3m[x])
        else:
            DPD90P3M.append('unknown')

        if (grp_slice['DPD30P6M_flag'][i] == 1) or (grp_slice['DPD30P6M_flag'][i] == 0):
            DPD30P6M.append(count_list_30_6m[x])
        else:
            DPD30P6M.append('unknown')

        if (grp_slice['DPD60P6M_flag'][i] == 1) or (grp_slice['DPD60P6M_flag'][i] == 0):
            DPD60P6M.append(count_list_60_6m[x])
        else:
            DPD60P6M.append('unknown')

        if (grp_slice['DPD90P6M_flag'][i] == 1) or (grp_slice['DPD90P6M_flag'][i] == 0):
            DPD90P6M.append(count_list_90_6m[x])
        else:
            DPD90P6M.append('unknown')

        if (grp_slice['DPD30P1Y_flag'][i] == 1) or (grp_slice['DPD30P1Y_flag'][i] == 0):
            DPD30P1Y.append(count_list_30_1y[x])
        else:
            DPD30P1Y.append('unknown')

        if (grp_slice['DPD60P1Y_flag'][i] == 1) or (grp_slice['DPD60P1Y_flag'][i] == 0):
            DPD60P1Y.append(count_list_60_1y[x])
        else:
            DPD60P1Y.append('unknown')

        if (grp_slice['DPD90P1Y_flag'][i] == 1) or (grp_slice['DPD90P1Y_flag'][i] == 0):
            DPD90P1Y.append(count_list_90_1y[x])
        else:
            DPD90P1Y.append('unknown')

        if (grp_slice['DPD30P2Y_flag'][i] == 1) or (grp_slice['DPD30P2Y_flag'][i] == 0):
            DPD30P2Y.append(count_list_30_2y[x])
        else:
            DPD30P2Y.append('unknown')

        if (grp_slice['DPD60P2Y_flag'][i] == 1) or (grp_slice['DPD60P2Y_flag'][i] == 0):
            DPD60P2Y.append(count_list_60_2y[x])
        else:
            DPD60P2Y.append('unknown')

        if (grp_slice['DPD90P2Y_flag'][i] == 1) or (grp_slice['DPD90P2Y_flag'][i] == 0):
            DPD90P2Y.append(count_list_90_2y[x])
        else:
            DPD90P2Y.append('unknown')

        if (grp_slice['DPD30P3Y_flag'][i] == 1) or (grp_slice['DPD30P3Y_flag'][i] == 0):
            DPD30P3Y.append(count_list_30_3y[x])
        else:
            DPD30P3Y.append('unknown')

        if (grp_slice['DPD60P3Y_flag'][i] == 1) or (grp_slice['DPD60P3Y_flag'][i] == 0):
            DPD60P3Y.append(count_list_60_3y[x])
        else:
            DPD60P3Y.append('unknown')

        if (grp_slice['DPD90P3Y_flag'][i] == 1) or (grp_slice['DPD90P3Y_flag'][i] == 0):
            DPD90P3Y.append(count_list_90_3y[x])
        else:
            DPD90P3Y.append('unknown')

        if (grp_slice['STD1M_flag'][i] == 1) or (grp_slice['STD1M_flag'][i] == 0):
            STD1M.append(count_std__list_1m[x])
        else:
            STD1M.append('unknown')

        if (grp_slice['STD3M_flag'][i] == 1) or (grp_slice['STD3M_flag'][i] == 0):
            STD3M.append(count_std__list_3m[x])
        else:
            STD3M.append('unknown')

        if (grp_slice['STD6M_flag'][i] == 1) or (grp_slice['STD6M_flag'][i] == 0):
            STD6M.append(count_std__list_6m[x])
        else:
            STD6M.append('unknown')

        if (grp_slice['STD1Y_flag'][i] == 1) or (grp_slice['STD1Y_flag'][i] == 0):
            STD1Y.append(count_std__list_1y[x])
        else:
            STD1Y.append('unknown')

        if (grp_slice['STD2Y_flag'][i] == 1) or (grp_slice['STD2Y_flag'][i] == 0):
            STD2Y.append(count_std__list_2y[x])
        else:
            STD2Y.append('unknown')

        if (grp_slice['STD3Y_flag'][i] == 1) or (grp_slice['STD3Y_flag'][i] == 0):
            STD3Y.append(count_std__list_3y[x])
        else:
            STD3Y.append('unknown')

        if (grp_slice['SUB1M_flag'][i] == 1) or (grp_slice['SUB1M_flag'][i] == 0):
            SUB1M.append(count_sub_list_1m[x])
        else:
            SUB1M.append('unknown')

        if (grp_slice['SUB3M_flag'][i] == 1) or (grp_slice['SUB3M_flag'][i] == 0):
            SUB3M.append(count_sub_list_3m[x])
        else:
            SUB3M.append('unknown')

        if (grp_slice['SUB6M_flag'][i] == 1) or (grp_slice['SUB6M_flag'][i] == 0):
            SUB6M.append(count_sub_list_6m[x])
        else:
            SUB6M.append('unknown')

        if (grp_slice['SUB1Y_flag'][i] == 1) or (grp_slice['SUB1Y_flag'][i] == 0):
            SUB1Y.append(count_sub_list_1y[x])
        else:
            SUB1Y.append('unknown')

        if (grp_slice['SUB2Y_flag'][i] == 1) or (grp_slice['SUB2Y_flag'][i] == 0):
            SUB2Y.append(count_sub_list_2y[x])
        else:
            SUB2Y.append('unknown')

        if (grp_slice['SUB3Y_flag'][i] == 1) or (grp_slice['SUB3Y_flag'][i] == 0):
            SUB3Y.append(count_sub_list_3y[x])
        else:
            SUB3Y.append('unknown')

        if (grp_slice['DBT1M_flag'][i] == 1) or (grp_slice['DBT1M_flag'][i] == 0):
            DBT1M.append(count_dbt_list_1m[x])
        else:
            DBT1M.append('unknown')

        if (grp_slice['DBT3M_flag'][i] == 1) or (grp_slice['DBT3M_flag'][i] == 0):
            DBT3M.append(count_dbt_list_3m[x])
        else:
            DBT3M.append('unknown')

        if (grp_slice['DBT6M_flag'][i] == 1) or (grp_slice['DBT6M_flag'][i] == 0):
            DBT6M.append(count_dbt_list_6m[x])
        else:
            DBT6M.append('unknown')

        if (grp_slice['DBT1Y_flag'][i] == 1) or (grp_slice['DBT1Y_flag'][i] == 0):
            DBT1Y.append(count_dbt_list_1y[x])
        else:
            DBT1Y.append('unknown')

        if (grp_slice['DBT2Y_flag'][i] == 1) or (grp_slice['DBT2Y_flag'][i] == 0):
            DBT2Y.append(count_dbt_list_2y[x])
        else:
            DBT2Y.append('unknown')

        if (grp_slice['DBT3Y_flag'][i] == 1) or (grp_slice['DBT3Y_flag'][i] == 0):
            DBT3Y.append(count_dbt_list_3y[x])
        else:
            DBT3Y.append('unknown')

        if (grp_slice['LOS1M_flag'][i] == 1) or (grp_slice['LOS1M_flag'][i] == 0):
            LOS1M.append(count_los_list_1m[x])
        else:
            LOS1M.append('unknown')

        if (grp_slice['LOS3M_flag'][i] == 1) or (grp_slice['LOS3M_flag'][i] == 0):
            LOS3M.append(count_los_list_3m[x])
        else:
            LOS3M.append('unknown')

        if (grp_slice['LOS6M_flag'][i] == 1) or (grp_slice['LOS6M_flag'][i] == 0):
            LOS6M.append(count_los_list_6m[x])
        else:
            LOS6M.append('unknown')

        if (grp_slice['LOS1Y_flag'][i] == 1) or (grp_slice['LOS1Y_flag'][i] == 0):
            LOS1Y.append(count_los_list_1y[x])
        else:
            LOS1Y.append('unknown')

        if (grp_slice['LOS2Y_flag'][i] == 1) or (grp_slice['LOS2Y_flag'][i] == 0):
            LOS2Y.append(count_los_list_2y[x])
        else:
            LOS2Y.append('unknown')

        if (grp_slice['LOS3Y_flag'][i] == 1) or (grp_slice['LOS3Y_flag'][i] == 0):
            LOS3Y.append(count_los_list_3y[x])
        else:
            LOS3Y.append('unknown')

        if (grp_slice['XXX1M_flag'][i] == 1) or (grp_slice['XXX1M_flag'][i] == 0):
            XXX1M.append(count_xxx_list_1m[x])
        else:
            XXX1M.append('unknown')

        if (grp_slice['XXX3M_flag'][i] == 1) or (grp_slice['XXX3M_flag'][i] == 0):
            XXX3M.append(count_xxx_list_3m[x])
        else:
            XXX3M.append('unknown')

        if (grp_slice['XXX6M_flag'][i] == 1) or (grp_slice['XXX6M_flag'][i] == 0):
            XXX6M.append(count_xxx_list_6m[x])
        else:
            XXX6M.append('unknown')

        if (grp_slice['XXX1Y_flag'][i] == 1) or (grp_slice['XXX1Y_flag'][i] == 0):
            XXX1Y.append(count_xxx_list_1y[x])
        else:
            XXX1Y.append('unknown')

        if (grp_slice['XXX2Y_flag'][i] == 1) or (grp_slice['XXX2Y_flag'][i] == 0):
            XXX2Y.append(count_xxx_list_2y[x])
        else:
            XXX2Y.append('unknown')

        if (grp_slice['XXX3Y_flag'][i] == 1) or (grp_slice['XXX3Y_flag'][i] == 0):
            XXX3Y.append(count_xxx_list_3y[x])
        else:
            XXX3Y.append('unknown')

        if (grp_slice['SMA1M_flag'][i] == 1) or (grp_slice['SMA1M_flag'][i] == 0):
            SMA1M.append(count_sma_list_1m[x])
        else:
            SMA1M.append('unknown')

        if (grp_slice['SMA3M_flag'][i] == 1) or (grp_slice['SMA3M_flag'][i] == 0):
            SMA3M.append(count_sma_list_3m[x])
        else:
            SMA3M.append('unknown')

        if (grp_slice['SMA6M_flag'][i] == 1) or (grp_slice['SMA6M_flag'][i] == 0):
            SMA6M.append(count_sma_list_6m[x])
        else:
            SMA6M.append('unknown')

        if (grp_slice['SMA1Y_flag'][i] == 1) or (grp_slice['SMA1Y_flag'][i] == 0):
            SMA1Y.append(count_sma_list_1y[x])
        else:
            SMA1Y.append('unknown')

        if (grp_slice['SMA2Y_flag'][i] == 1) or (grp_slice['SMA2Y_flag'][i] == 0):
            SMA2Y.append(count_sma_list_2y[x])
        else:
            SMA2Y.append('unknown')

        if (grp_slice['SMA3Y_flag'][i] == 1) or (grp_slice['SMA3Y_flag'][i] == 0):
            SMA3Y.append(count_sma_list_3y[x])
        else:
            SMA3Y.append('unknown')

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            DPD30P3M_AL.append('unknown')
            DPD30P3M_BL.append('unknown')
            DPD30P3M_CC.append('unknown')
            DPD30P3M_CD.append('unknown')
            DPD30P3M_CV.append('unknown')
            DPD30P3M_GL.append('unknown')
            DPD30P3M_HL.append('unknown')
            DPD30P3M_LAS.append('unknown')
            DPD30P3M_MFBL.append('unknown')
            DPD30P3M_MFHL.append('unknown')
            DPD30P3M_MFOT.append('unknown')
            DPD30P3M_OTH.append('unknown')
            DPD30P3M_PL.append('unknown')
            DPD30P3M_PLBL.append('unknown')
            DPD30P3M_RL.append('unknown')
            DPD30P3M_SCC.append('unknown')
            DPD30P3M_SEL.append('unknown')

            DPD60P3M_AL.append('unknown')
            DPD60P3M_BL.append('unknown')
            DPD60P3M_CC.append('unknown')
            DPD60P3M_CD.append('unknown')
            DPD60P3M_CV.append('unknown')
            DPD60P3M_GL.append('unknown')
            DPD60P3M_HL.append('unknown')
            DPD60P3M_LAS.append('unknown')
            DPD60P3M_MFBL.append('unknown')
            DPD60P3M_MFHL.append('unknown')
            DPD60P3M_MFOT.append('unknown')
            DPD60P3M_OTH.append('unknown')
            DPD60P3M_PL.append('unknown')
            DPD60P3M_PLBL.append('unknown')
            DPD60P3M_RL.append('unknown')
            DPD60P3M_SCC.append('unknown')
            DPD60P3M_SEL.append('unknown')

            DPD90P3M_AL.append('unknown')
            DPD90P3M_BL.append('unknown')
            DPD90P3M_CC.append('unknown')
            DPD90P3M_CD.append('unknown')
            DPD90P3M_CV.append('unknown')
            DPD90P3M_GL.append('unknown')
            DPD90P3M_HL.append('unknown')
            DPD90P3M_LAS.append('unknown')
            DPD90P3M_MFBL.append('unknown')
            DPD90P3M_MFHL.append('unknown')
            DPD90P3M_MFOT.append('unknown')
            DPD90P3M_OTH.append('unknown')
            DPD90P3M_PL.append('unknown')
            DPD90P3M_PLBL.append('unknown')
            DPD90P3M_RL.append('unknown')
            DPD90P3M_SCC.append('unknown')
            DPD90P3M_SEL.append('unknown')

            DPD30P6M_AL.append('unknown')
            DPD30P6M_BL.append('unknown')
            DPD30P6M_CC.append('unknown')
            DPD30P6M_CD.append('unknown')
            DPD30P6M_CV.append('unknown')
            DPD30P6M_GL.append('unknown')
            DPD30P6M_HL.append('unknown')
            DPD30P6M_LAS.append('unknown')
            DPD30P6M_MFBL.append('unknown')
            DPD30P6M_MFHL.append('unknown')
            DPD30P6M_MFOT.append('unknown')
            DPD30P6M_OTH.append('unknown')
            DPD30P6M_PL.append('unknown')
            DPD30P6M_PLBL.append('unknown')
            DPD30P6M_RL.append('unknown')
            DPD30P6M_SCC.append('unknown')
            DPD30P6M_SEL.append('unknown')

            DPD60P6M_AL.append('unknown')
            DPD60P6M_BL.append('unknown')
            DPD60P6M_CC.append('unknown')
            DPD60P6M_CD.append('unknown')
            DPD60P6M_CV.append('unknown')
            DPD60P6M_GL.append('unknown')
            DPD60P6M_HL.append('unknown')
            DPD60P6M_LAS.append('unknown')
            DPD60P6M_MFBL.append('unknown')
            DPD60P6M_MFHL.append('unknown')
            DPD60P6M_MFOT.append('unknown')
            DPD60P6M_OTH.append('unknown')
            DPD60P6M_PL.append('unknown')
            DPD60P6M_PLBL.append('unknown')
            DPD60P6M_RL.append('unknown')
            DPD60P6M_SCC.append('unknown')
            DPD60P6M_SEL.append('unknown')

            DPD90P6M_AL.append('unknown')
            DPD90P6M_BL.append('unknown')
            DPD90P6M_CC.append('unknown')
            DPD90P6M_CD.append('unknown')
            DPD90P6M_CV.append('unknown')
            DPD90P6M_GL.append('unknown')
            DPD90P6M_HL.append('unknown')
            DPD90P6M_LAS.append('unknown')
            DPD90P6M_MFBL.append('unknown')
            DPD90P6M_MFHL.append('unknown')
            DPD90P6M_MFOT.append('unknown')
            DPD90P6M_OTH.append('unknown')
            DPD90P6M_PL.append('unknown')
            DPD90P6M_PLBL.append('unknown')
            DPD90P6M_RL.append('unknown')
            DPD90P6M_SCC.append('unknown')
            DPD90P6M_SEL.append('unknown')

            DPD30P1Y_AL.append('unknown')
            DPD30P1Y_BL.append('unknown')
            DPD30P1Y_CC.append('unknown')
            DPD30P1Y_CD.append('unknown')
            DPD30P1Y_CV.append('unknown')
            DPD30P1Y_GL.append('unknown')
            DPD30P1Y_HL.append('unknown')
            DPD30P1Y_LAS.append('unknown')
            DPD30P1Y_MFBL.append('unknown')
            DPD30P1Y_MFHL.append('unknown')
            DPD30P1Y_MFOT.append('unknown')
            DPD30P1Y_OTH.append('unknown')
            DPD30P1Y_PL.append('unknown')
            DPD30P1Y_PLBL.append('unknown')
            DPD30P1Y_RL.append('unknown')
            DPD30P1Y_SCC.append('unknown')
            DPD30P1Y_SEL.append('unknown')

            DPD60P1Y_AL.append('unknown')
            DPD60P1Y_BL.append('unknown')
            DPD60P1Y_CC.append('unknown')
            DPD60P1Y_CD.append('unknown')
            DPD60P1Y_CV.append('unknown')
            DPD60P1Y_GL.append('unknown')
            DPD60P1Y_HL.append('unknown')
            DPD60P1Y_LAS.append('unknown')
            DPD60P1Y_MFBL.append('unknown')
            DPD60P1Y_MFHL.append('unknown')
            DPD60P1Y_MFOT.append('unknown')
            DPD60P1Y_OTH.append('unknown')
            DPD60P1Y_PL.append('unknown')
            DPD60P1Y_PLBL.append('unknown')
            DPD60P1Y_RL.append('unknown')
            DPD60P1Y_SCC.append('unknown')
            DPD60P1Y_SEL.append('unknown')

            DPD90P1Y_AL.append('unknown')
            DPD90P1Y_BL.append('unknown')
            DPD90P1Y_CC.append('unknown')
            DPD90P1Y_CD.append('unknown')
            DPD90P1Y_CV.append('unknown')
            DPD90P1Y_GL.append('unknown')
            DPD90P1Y_HL.append('unknown')
            DPD90P1Y_LAS.append('unknown')
            DPD90P1Y_MFBL.append('unknown')
            DPD90P1Y_MFHL.append('unknown')
            DPD90P1Y_MFOT.append('unknown')
            DPD90P1Y_OTH.append('unknown')
            DPD90P1Y_PL.append('unknown')
            DPD90P1Y_PLBL.append('unknown')
            DPD90P1Y_RL.append('unknown')
            DPD90P1Y_SCC.append('unknown')
            DPD90P1Y_SEL.append('unknown')

            DPD30P2Y_AL.append('unknown')
            DPD30P2Y_BL.append('unknown')
            DPD30P2Y_CC.append('unknown')
            DPD30P2Y_CD.append('unknown')
            DPD30P2Y_CV.append('unknown')
            DPD30P2Y_GL.append('unknown')
            DPD30P2Y_HL.append('unknown')
            DPD30P2Y_LAS.append('unknown')
            DPD30P2Y_MFBL.append('unknown')
            DPD30P2Y_MFHL.append('unknown')
            DPD30P2Y_MFOT.append('unknown')
            DPD30P2Y_OTH.append('unknown')
            DPD30P2Y_PL.append('unknown')
            DPD30P2Y_PLBL.append('unknown')
            DPD30P2Y_RL.append('unknown')
            DPD30P2Y_SCC.append('unknown')
            DPD30P2Y_SEL.append('unknown')

            DPD60P2Y_AL.append('unknown')
            DPD60P2Y_BL.append('unknown')
            DPD60P2Y_CC.append('unknown')
            DPD60P2Y_CD.append('unknown')
            DPD60P2Y_CV.append('unknown')
            DPD60P2Y_GL.append('unknown')
            DPD60P2Y_HL.append('unknown')
            DPD60P2Y_LAS.append('unknown')
            DPD60P2Y_MFBL.append('unknown')
            DPD60P2Y_MFHL.append('unknown')
            DPD60P2Y_MFOT.append('unknown')
            DPD60P2Y_OTH.append('unknown')
            DPD60P2Y_PL.append('unknown')
            DPD60P2Y_PLBL.append('unknown')
            DPD60P2Y_RL.append('unknown')
            DPD60P2Y_SCC.append('unknown')
            DPD60P2Y_SEL.append('unknown')

            DPD90P2Y_AL.append('unknown')
            DPD90P2Y_BL.append('unknown')
            DPD90P2Y_CC.append('unknown')
            DPD90P2Y_CD.append('unknown')
            DPD90P2Y_CV.append('unknown')
            DPD90P2Y_GL.append('unknown')
            DPD90P2Y_HL.append('unknown')
            DPD90P2Y_LAS.append('unknown')
            DPD90P2Y_MFBL.append('unknown')
            DPD90P2Y_MFHL.append('unknown')
            DPD90P2Y_MFOT.append('unknown')
            DPD90P2Y_OTH.append('unknown')
            DPD90P2Y_PL.append('unknown')
            DPD90P2Y_PLBL.append('unknown')
            DPD90P2Y_RL.append('unknown')
            DPD90P2Y_SCC.append('unknown')
            DPD90P2Y_SEL.append('unknown')

            DPD30P3Y_AL.append('unknown')
            DPD30P3Y_BL.append('unknown')
            DPD30P3Y_CC.append('unknown')
            DPD30P3Y_CD.append('unknown')
            DPD30P3Y_CV.append('unknown')
            DPD30P3Y_GL.append('unknown')
            DPD30P3Y_HL.append('unknown')
            DPD30P3Y_LAS.append('unknown')
            DPD30P3Y_MFBL.append('unknown')
            DPD30P3Y_MFHL.append('unknown')
            DPD30P3Y_MFOT.append('unknown')
            DPD30P3Y_OTH.append('unknown')
            DPD30P3Y_PL.append('unknown')
            DPD30P3Y_PLBL.append('unknown')
            DPD30P3Y_RL.append('unknown')
            DPD30P3Y_SCC.append('unknown')
            DPD30P3Y_SEL.append('unknown')

            DPD60P3Y_AL.append('unknown')
            DPD60P3Y_BL.append('unknown')
            DPD60P3Y_CC.append('unknown')
            DPD60P3Y_CD.append('unknown')
            DPD60P3Y_CV.append('unknown')
            DPD60P3Y_GL.append('unknown')
            DPD60P3Y_HL.append('unknown')
            DPD60P3Y_LAS.append('unknown')
            DPD60P3Y_MFBL.append('unknown')
            DPD60P3Y_MFHL.append('unknown')
            DPD60P3Y_MFOT.append('unknown')
            DPD60P3Y_OTH.append('unknown')
            DPD60P3Y_PL.append('unknown')
            DPD60P3Y_PLBL.append('unknown')
            DPD60P3Y_RL.append('unknown')
            DPD60P3Y_SCC.append('unknown')
            DPD60P3Y_SEL.append('unknown')

            DPD90P3Y_AL.append('unknown')
            DPD90P3Y_BL.append('unknown')
            DPD90P3Y_CC.append('unknown')
            DPD90P3Y_CD.append('unknown')
            DPD90P3Y_CV.append('unknown')
            DPD90P3Y_GL.append('unknown')
            DPD90P3Y_HL.append('unknown')
            DPD90P3Y_LAS.append('unknown')
            DPD90P3Y_MFBL.append('unknown')
            DPD90P3Y_MFHL.append('unknown')
            DPD90P3Y_MFOT.append('unknown')
            DPD90P3Y_OTH.append('unknown')
            DPD90P3Y_PL.append('unknown')
            DPD90P3Y_PLBL.append('unknown')
            DPD90P3Y_RL.append('unknown')
            DPD90P3Y_SCC.append('unknown')
            DPD90P3Y_SEL.append('unknown')

            STD1M_AL.append('unknown')
            STD1M_BL.append('unknown')
            STD1M_CC.append('unknown')
            STD1M_CD.append('unknown')
            STD1M_CV.append('unknown')
            STD1M_GL.append('unknown')
            STD1M_HL.append('unknown')
            STD1M_LAS.append('unknown')
            STD1M_MFBL.append('unknown')
            STD1M_MFHL.append('unknown')
            STD1M_MFOT.append('unknown')
            STD1M_OTH.append('unknown')
            STD1M_PL.append('unknown')
            STD1M_PLBL.append('unknown')
            STD1M_RL.append('unknown')
            STD1M_SCC.append('unknown')
            STD1M_SEL.append('unknown')

            STD3M_AL.append('unknown')
            STD3M_BL.append('unknown')
            STD3M_CC.append('unknown')
            STD3M_CD.append('unknown')
            STD3M_CV.append('unknown')
            STD3M_GL.append('unknown')
            STD3M_HL.append('unknown')
            STD3M_LAS.append('unknown')
            STD3M_MFBL.append('unknown')
            STD3M_MFHL.append('unknown')
            STD3M_MFOT.append('unknown')
            STD3M_OTH.append('unknown')
            STD3M_PL.append('unknown')
            STD3M_PLBL.append('unknown')
            STD3M_RL.append('unknown')
            STD3M_SCC.append('unknown')
            STD3M_SEL.append('unknown')

            STD6M_AL.append('unknown')
            STD6M_BL.append('unknown')
            STD6M_CC.append('unknown')
            STD6M_CD.append('unknown')
            STD6M_CV.append('unknown')
            STD6M_GL.append('unknown')
            STD6M_HL.append('unknown')
            STD6M_LAS.append('unknown')
            STD6M_MFBL.append('unknown')
            STD6M_MFHL.append('unknown')
            STD6M_MFOT.append('unknown')
            STD6M_OTH.append('unknown')
            STD6M_PL.append('unknown')
            STD6M_PLBL.append('unknown')
            STD6M_RL.append('unknown')
            STD6M_SCC.append('unknown')
            STD6M_SEL.append('unknown')

            STD1Y_AL.append('unknown')
            STD1Y_BL.append('unknown')
            STD1Y_CC.append('unknown')
            STD1Y_CD.append('unknown')
            STD1Y_CV.append('unknown')
            STD1Y_GL.append('unknown')
            STD1Y_HL.append('unknown')
            STD1Y_LAS.append('unknown')
            STD1Y_MFBL.append('unknown')
            STD1Y_MFHL.append('unknown')
            STD1Y_MFOT.append('unknown')
            STD1Y_OTH.append('unknown')
            STD1Y_PL.append('unknown')
            STD1Y_PLBL.append('unknown')
            STD1Y_RL.append('unknown')
            STD1Y_SCC.append('unknown')
            STD1Y_SEL.append('unknown')

            STD2Y_AL.append('unknown')
            STD2Y_BL.append('unknown')
            STD2Y_CC.append('unknown')
            STD2Y_CD.append('unknown')
            STD2Y_CV.append('unknown')
            STD2Y_GL.append('unknown')
            STD2Y_HL.append('unknown')
            STD2Y_LAS.append('unknown')
            STD2Y_MFBL.append('unknown')
            STD2Y_MFHL.append('unknown')
            STD2Y_MFOT.append('unknown')
            STD2Y_OTH.append('unknown')
            STD2Y_PL.append('unknown')
            STD2Y_PLBL.append('unknown')
            STD2Y_RL.append('unknown')
            STD2Y_SCC.append('unknown')
            STD2Y_SEL.append('unknown')

            STD3Y_AL.append('unknown')
            STD3Y_BL.append('unknown')
            STD3Y_CC.append('unknown')
            STD3Y_CD.append('unknown')
            STD3Y_CV.append('unknown')
            STD3Y_GL.append('unknown')
            STD3Y_HL.append('unknown')
            STD3Y_LAS.append('unknown')
            STD3Y_MFBL.append('unknown')
            STD3Y_MFHL.append('unknown')
            STD3Y_MFOT.append('unknown')
            STD3Y_OTH.append('unknown')
            STD3Y_PL.append('unknown')
            STD3Y_PLBL.append('unknown')
            STD3Y_RL.append('unknown')
            STD3Y_SCC.append('unknown')
            STD3Y_SEL.append('unknown')

            SUB1M_AL.append('unknown')
            SUB1M_BL.append('unknown')
            SUB1M_CC.append('unknown')
            SUB1M_CD.append('unknown')
            SUB1M_CV.append('unknown')
            SUB1M_GL.append('unknown')
            SUB1M_HL.append('unknown')
            SUB1M_LAS.append('unknown')
            SUB1M_MFBL.append('unknown')
            SUB1M_MFHL.append('unknown')
            SUB1M_MFOT.append('unknown')
            SUB1M_OTH.append('unknown')
            SUB1M_PL.append('unknown')
            SUB1M_PLBL.append('unknown')
            SUB1M_RL.append('unknown')
            SUB1M_SCC.append('unknown')
            SUB1M_SEL.append('unknown')

            SUB3M_AL.append('unknown')
            SUB3M_BL.append('unknown')
            SUB3M_CC.append('unknown')
            SUB3M_CD.append('unknown')
            SUB3M_CV.append('unknown')
            SUB3M_GL.append('unknown')
            SUB3M_HL.append('unknown')
            SUB3M_LAS.append('unknown')
            SUB3M_MFBL.append('unknown')
            SUB3M_MFHL.append('unknown')
            SUB3M_MFOT.append('unknown')
            SUB3M_OTH.append('unknown')
            SUB3M_PL.append('unknown')
            SUB3M_PLBL.append('unknown')
            SUB3M_RL.append('unknown')
            SUB3M_SCC.append('unknown')
            SUB3M_SEL.append('unknown')

            SUB6M_AL.append('unknown')
            SUB6M_BL.append('unknown')
            SUB6M_CC.append('unknown')
            SUB6M_CD.append('unknown')
            SUB6M_CV.append('unknown')
            SUB6M_GL.append('unknown')
            SUB6M_HL.append('unknown')
            SUB6M_LAS.append('unknown')
            SUB6M_MFBL.append('unknown')
            SUB6M_MFHL.append('unknown')
            SUB6M_MFOT.append('unknown')
            SUB6M_OTH.append('unknown')
            SUB6M_PL.append('unknown')
            SUB6M_PLBL.append('unknown')
            SUB6M_RL.append('unknown')
            SUB6M_SCC.append('unknown')
            SUB6M_SEL.append('unknown')

            SUB1Y_AL.append('unknown')
            SUB1Y_BL.append('unknown')
            SUB1Y_CC.append('unknown')
            SUB1Y_CD.append('unknown')
            SUB1Y_CV.append('unknown')
            SUB1Y_GL.append('unknown')
            SUB1Y_HL.append('unknown')
            SUB1Y_LAS.append('unknown')
            SUB1Y_MFBL.append('unknown')
            SUB1Y_MFHL.append('unknown')
            SUB1Y_MFOT.append('unknown')
            SUB1Y_OTH.append('unknown')
            SUB1Y_PL.append('unknown')
            SUB1Y_PLBL.append('unknown')
            SUB1Y_RL.append('unknown')
            SUB1Y_SCC.append('unknown')
            SUB1Y_SEL.append('unknown')

            SUB2Y_AL.append('unknown')
            SUB2Y_BL.append('unknown')
            SUB2Y_CC.append('unknown')
            SUB2Y_CD.append('unknown')
            SUB2Y_CV.append('unknown')
            SUB2Y_GL.append('unknown')
            SUB2Y_HL.append('unknown')
            SUB2Y_LAS.append('unknown')
            SUB2Y_MFBL.append('unknown')
            SUB2Y_MFHL.append('unknown')
            SUB2Y_MFOT.append('unknown')
            SUB2Y_OTH.append('unknown')
            SUB2Y_PL.append('unknown')
            SUB2Y_PLBL.append('unknown')
            SUB2Y_RL.append('unknown')
            SUB2Y_SCC.append('unknown')
            SUB2Y_SEL.append('unknown')

            SUB3Y_AL.append('unknown')
            SUB3Y_BL.append('unknown')
            SUB3Y_CC.append('unknown')
            SUB3Y_CD.append('unknown')
            SUB3Y_CV.append('unknown')
            SUB3Y_GL.append('unknown')
            SUB3Y_HL.append('unknown')
            SUB3Y_LAS.append('unknown')
            SUB3Y_MFBL.append('unknown')
            SUB3Y_MFHL.append('unknown')
            SUB3Y_MFOT.append('unknown')
            SUB3Y_OTH.append('unknown')
            SUB3Y_PL.append('unknown')
            SUB3Y_PLBL.append('unknown')
            SUB3Y_RL.append('unknown')
            SUB3Y_SCC.append('unknown')
            SUB3Y_SEL.append('unknown')

            DBT1M_AL.append('unknown')
            DBT1M_BL.append('unknown')
            DBT1M_CC.append('unknown')
            DBT1M_CD.append('unknown')
            DBT1M_CV.append('unknown')
            DBT1M_GL.append('unknown')
            DBT1M_HL.append('unknown')
            DBT1M_LAS.append('unknown')
            DBT1M_MFBL.append('unknown')
            DBT1M_MFHL.append('unknown')
            DBT1M_MFOT.append('unknown')
            DBT1M_OTH.append('unknown')
            DBT1M_PL.append('unknown')
            DBT1M_PLBL.append('unknown')
            DBT1M_RL.append('unknown')
            DBT1M_SCC.append('unknown')
            DBT1M_SEL.append('unknown')

            DBT3M_AL.append('unknown')
            DBT3M_BL.append('unknown')
            DBT3M_CC.append('unknown')
            DBT3M_CD.append('unknown')
            DBT3M_CV.append('unknown')
            DBT3M_GL.append('unknown')
            DBT3M_HL.append('unknown')
            DBT3M_LAS.append('unknown')
            DBT3M_MFBL.append('unknown')
            DBT3M_MFHL.append('unknown')
            DBT3M_MFOT.append('unknown')
            DBT3M_OTH.append('unknown')
            DBT3M_PL.append('unknown')
            DBT3M_PLBL.append('unknown')
            DBT3M_RL.append('unknown')
            DBT3M_SCC.append('unknown')
            DBT3M_SEL.append('unknown')

            DBT6M_AL.append('unknown')
            DBT6M_BL.append('unknown')
            DBT6M_CC.append('unknown')
            DBT6M_CD.append('unknown')
            DBT6M_CV.append('unknown')
            DBT6M_GL.append('unknown')
            DBT6M_HL.append('unknown')
            DBT6M_LAS.append('unknown')
            DBT6M_MFBL.append('unknown')
            DBT6M_MFHL.append('unknown')
            DBT6M_MFOT.append('unknown')
            DBT6M_OTH.append('unknown')
            DBT6M_PL.append('unknown')
            DBT6M_PLBL.append('unknown')
            DBT6M_RL.append('unknown')
            DBT6M_SCC.append('unknown')
            DBT6M_SEL.append('unknown')

            DBT1Y_AL.append('unknown')
            DBT1Y_BL.append('unknown')
            DBT1Y_CC.append('unknown')
            DBT1Y_CD.append('unknown')
            DBT1Y_CV.append('unknown')
            DBT1Y_GL.append('unknown')
            DBT1Y_HL.append('unknown')
            DBT1Y_LAS.append('unknown')
            DBT1Y_MFBL.append('unknown')
            DBT1Y_MFHL.append('unknown')
            DBT1Y_MFOT.append('unknown')
            DBT1Y_OTH.append('unknown')
            DBT1Y_PL.append('unknown')
            DBT1Y_PLBL.append('unknown')
            DBT1Y_RL.append('unknown')
            DBT1Y_SCC.append('unknown')
            DBT1Y_SEL.append('unknown')

            DBT2Y_AL.append('unknown')
            DBT2Y_BL.append('unknown')
            DBT2Y_CC.append('unknown')
            DBT2Y_CD.append('unknown')
            DBT2Y_CV.append('unknown')
            DBT2Y_GL.append('unknown')
            DBT2Y_HL.append('unknown')
            DBT2Y_LAS.append('unknown')
            DBT2Y_MFBL.append('unknown')
            DBT2Y_MFHL.append('unknown')
            DBT2Y_MFOT.append('unknown')
            DBT2Y_OTH.append('unknown')
            DBT2Y_PL.append('unknown')
            DBT2Y_PLBL.append('unknown')
            DBT2Y_RL.append('unknown')
            DBT2Y_SCC.append('unknown')
            DBT2Y_SEL.append('unknown')

            DBT3Y_AL.append('unknown')
            DBT3Y_BL.append('unknown')
            DBT3Y_CC.append('unknown')
            DBT3Y_CD.append('unknown')
            DBT3Y_CV.append('unknown')
            DBT3Y_GL.append('unknown')
            DBT3Y_HL.append('unknown')
            DBT3Y_LAS.append('unknown')
            DBT3Y_MFBL.append('unknown')
            DBT3Y_MFHL.append('unknown')
            DBT3Y_MFOT.append('unknown')
            DBT3Y_OTH.append('unknown')
            DBT3Y_PL.append('unknown')
            DBT3Y_PLBL.append('unknown')
            DBT3Y_RL.append('unknown')
            DBT3Y_SCC.append('unknown')
            DBT3Y_SEL.append('unknown')

            LOS1M_AL.append('unknown')
            LOS1M_BL.append('unknown')
            LOS1M_CC.append('unknown')
            LOS1M_CD.append('unknown')
            LOS1M_CV.append('unknown')
            LOS1M_GL.append('unknown')
            LOS1M_HL.append('unknown')
            LOS1M_LAS.append('unknown')
            LOS1M_MFBL.append('unknown')
            LOS1M_MFHL.append('unknown')
            LOS1M_MFOT.append('unknown')
            LOS1M_OTH.append('unknown')
            LOS1M_PL.append('unknown')
            LOS1M_PLBL.append('unknown')
            LOS1M_RL.append('unknown')
            LOS1M_SCC.append('unknown')
            LOS1M_SEL.append('unknown')

            LOS3M_AL.append('unknown')
            LOS3M_BL.append('unknown')
            LOS3M_CC.append('unknown')
            LOS3M_CD.append('unknown')
            LOS3M_CV.append('unknown')
            LOS3M_GL.append('unknown')
            LOS3M_HL.append('unknown')
            LOS3M_LAS.append('unknown')
            LOS3M_MFBL.append('unknown')
            LOS3M_MFHL.append('unknown')
            LOS3M_MFOT.append('unknown')
            LOS3M_OTH.append('unknown')
            LOS3M_PL.append('unknown')
            LOS3M_PLBL.append('unknown')
            LOS3M_RL.append('unknown')
            LOS3M_SCC.append('unknown')
            LOS3M_SEL.append('unknown')

            LOS6M_AL.append('unknown')
            LOS6M_BL.append('unknown')
            LOS6M_CC.append('unknown')
            LOS6M_CD.append('unknown')
            LOS6M_CV.append('unknown')
            LOS6M_GL.append('unknown')
            LOS6M_HL.append('unknown')
            LOS6M_LAS.append('unknown')
            LOS6M_MFBL.append('unknown')
            LOS6M_MFHL.append('unknown')
            LOS6M_MFOT.append('unknown')
            LOS6M_OTH.append('unknown')
            LOS6M_PL.append('unknown')
            LOS6M_PLBL.append('unknown')
            LOS6M_RL.append('unknown')
            LOS6M_SCC.append('unknown')
            LOS6M_SEL.append('unknown')

            LOS1Y_AL.append('unknown')
            LOS1Y_BL.append('unknown')
            LOS1Y_CC.append('unknown')
            LOS1Y_CD.append('unknown')
            LOS1Y_CV.append('unknown')
            LOS1Y_GL.append('unknown')
            LOS1Y_HL.append('unknown')
            LOS1Y_LAS.append('unknown')
            LOS1Y_MFBL.append('unknown')
            LOS1Y_MFHL.append('unknown')
            LOS1Y_MFOT.append('unknown')
            LOS1Y_OTH.append('unknown')
            LOS1Y_PL.append('unknown')
            LOS1Y_PLBL.append('unknown')
            LOS1Y_RL.append('unknown')
            LOS1Y_SCC.append('unknown')
            LOS1Y_SEL.append('unknown')

            LOS2Y_AL.append('unknown')
            LOS2Y_BL.append('unknown')
            LOS2Y_CC.append('unknown')
            LOS2Y_CD.append('unknown')
            LOS2Y_CV.append('unknown')
            LOS2Y_GL.append('unknown')
            LOS2Y_HL.append('unknown')
            LOS2Y_LAS.append('unknown')
            LOS2Y_MFBL.append('unknown')
            LOS2Y_MFHL.append('unknown')
            LOS2Y_MFOT.append('unknown')
            LOS2Y_OTH.append('unknown')
            LOS2Y_PL.append('unknown')
            LOS2Y_PLBL.append('unknown')
            LOS2Y_RL.append('unknown')
            LOS2Y_SCC.append('unknown')
            LOS2Y_SEL.append('unknown')

            LOS3Y_AL.append('unknown')
            LOS3Y_BL.append('unknown')
            LOS3Y_CC.append('unknown')
            LOS3Y_CD.append('unknown')
            LOS3Y_CV.append('unknown')
            LOS3Y_GL.append('unknown')
            LOS3Y_HL.append('unknown')
            LOS3Y_LAS.append('unknown')
            LOS3Y_MFBL.append('unknown')
            LOS3Y_MFHL.append('unknown')
            LOS3Y_MFOT.append('unknown')
            LOS3Y_OTH.append('unknown')
            LOS3Y_PL.append('unknown')
            LOS3Y_PLBL.append('unknown')
            LOS3Y_RL.append('unknown')
            LOS3Y_SCC.append('unknown')
            LOS3Y_SEL.append('unknown')

            XXX1M_AL.append('unknown')
            XXX1M_BL.append('unknown')
            XXX1M_CC.append('unknown')
            XXX1M_CD.append('unknown')
            XXX1M_CV.append('unknown')
            XXX1M_GL.append('unknown')
            XXX1M_HL.append('unknown')
            XXX1M_LAS.append('unknown')
            XXX1M_MFBL.append('unknown')
            XXX1M_MFHL.append('unknown')
            XXX1M_MFOT.append('unknown')
            XXX1M_OTH.append('unknown')
            XXX1M_PL.append('unknown')
            XXX1M_PLBL.append('unknown')
            XXX1M_RL.append('unknown')
            XXX1M_SCC.append('unknown')
            XXX1M_SEL.append('unknown')

            XXX3M_AL.append('unknown')
            XXX3M_BL.append('unknown')
            XXX3M_CC.append('unknown')
            XXX3M_CD.append('unknown')
            XXX3M_CV.append('unknown')
            XXX3M_GL.append('unknown')
            XXX3M_HL.append('unknown')
            XXX3M_LAS.append('unknown')
            XXX3M_MFBL.append('unknown')
            XXX3M_MFHL.append('unknown')
            XXX3M_MFOT.append('unknown')
            XXX3M_OTH.append('unknown')
            XXX3M_PL.append('unknown')
            XXX3M_PLBL.append('unknown')
            XXX3M_RL.append('unknown')
            XXX3M_SCC.append('unknown')
            XXX3M_SEL.append('unknown')

            XXX6M_AL.append('unknown')
            XXX6M_BL.append('unknown')
            XXX6M_CC.append('unknown')
            XXX6M_CD.append('unknown')
            XXX6M_CV.append('unknown')
            XXX6M_GL.append('unknown')
            XXX6M_HL.append('unknown')
            XXX6M_LAS.append('unknown')
            XXX6M_MFBL.append('unknown')
            XXX6M_MFHL.append('unknown')
            XXX6M_MFOT.append('unknown')
            XXX6M_OTH.append('unknown')
            XXX6M_PL.append('unknown')
            XXX6M_PLBL.append('unknown')
            XXX6M_RL.append('unknown')
            XXX6M_SCC.append('unknown')
            XXX6M_SEL.append('unknown')

            XXX1Y_AL.append('unknown')
            XXX1Y_BL.append('unknown')
            XXX1Y_CC.append('unknown')
            XXX1Y_CD.append('unknown')
            XXX1Y_CV.append('unknown')
            XXX1Y_GL.append('unknown')
            XXX1Y_HL.append('unknown')
            XXX1Y_LAS.append('unknown')
            XXX1Y_MFBL.append('unknown')
            XXX1Y_MFHL.append('unknown')
            XXX1Y_MFOT.append('unknown')
            XXX1Y_OTH.append('unknown')
            XXX1Y_PL.append('unknown')
            XXX1Y_PLBL.append('unknown')
            XXX1Y_RL.append('unknown')
            XXX1Y_SCC.append('unknown')
            XXX1Y_SEL.append('unknown')

            XXX2Y_AL.append('unknown')
            XXX2Y_BL.append('unknown')
            XXX2Y_CC.append('unknown')
            XXX2Y_CD.append('unknown')
            XXX2Y_CV.append('unknown')
            XXX2Y_GL.append('unknown')
            XXX2Y_HL.append('unknown')
            XXX2Y_LAS.append('unknown')
            XXX2Y_MFBL.append('unknown')
            XXX2Y_MFHL.append('unknown')
            XXX2Y_MFOT.append('unknown')
            XXX2Y_OTH.append('unknown')
            XXX2Y_PL.append('unknown')
            XXX2Y_PLBL.append('unknown')
            XXX2Y_RL.append('unknown')
            XXX2Y_SCC.append('unknown')
            XXX2Y_SEL.append('unknown')

            XXX3Y_AL.append('unknown')
            XXX3Y_BL.append('unknown')
            XXX3Y_CC.append('unknown')
            XXX3Y_CD.append('unknown')
            XXX3Y_CV.append('unknown')
            XXX3Y_GL.append('unknown')
            XXX3Y_HL.append('unknown')
            XXX3Y_LAS.append('unknown')
            XXX3Y_MFBL.append('unknown')
            XXX3Y_MFHL.append('unknown')
            XXX3Y_MFOT.append('unknown')
            XXX3Y_OTH.append('unknown')
            XXX3Y_PL.append('unknown')
            XXX3Y_PLBL.append('unknown')
            XXX3Y_RL.append('unknown')
            XXX3Y_SCC.append('unknown')
            XXX3Y_SEL.append('unknown')

            SMA1M_AL.append('unknown')
            SMA1M_BL.append('unknown')
            SMA1M_CC.append('unknown')
            SMA1M_CD.append('unknown')
            SMA1M_CV.append('unknown')
            SMA1M_GL.append('unknown')
            SMA1M_HL.append('unknown')
            SMA1M_LAS.append('unknown')
            SMA1M_MFBL.append('unknown')
            SMA1M_MFHL.append('unknown')
            SMA1M_MFOT.append('unknown')
            SMA1M_OTH.append('unknown')
            SMA1M_PL.append('unknown')
            SMA1M_PLBL.append('unknown')
            SMA1M_RL.append('unknown')
            SMA1M_SCC.append('unknown')
            SMA1M_SEL.append('unknown')

            SMA3M_AL.append('unknown')
            SMA3M_BL.append('unknown')
            SMA3M_CC.append('unknown')
            SMA3M_CD.append('unknown')
            SMA3M_CV.append('unknown')
            SMA3M_GL.append('unknown')
            SMA3M_HL.append('unknown')
            SMA3M_LAS.append('unknown')
            SMA3M_MFBL.append('unknown')
            SMA3M_MFHL.append('unknown')
            SMA3M_MFOT.append('unknown')
            SMA3M_OTH.append('unknown')
            SMA3M_PL.append('unknown')
            SMA3M_PLBL.append('unknown')
            SMA3M_RL.append('unknown')
            SMA3M_SCC.append('unknown')
            SMA3M_SEL.append('unknown')

            SMA6M_AL.append('unknown')
            SMA6M_BL.append('unknown')
            SMA6M_CC.append('unknown')
            SMA6M_CD.append('unknown')
            SMA6M_CV.append('unknown')
            SMA6M_GL.append('unknown')
            SMA6M_HL.append('unknown')
            SMA6M_LAS.append('unknown')
            SMA6M_MFBL.append('unknown')
            SMA6M_MFHL.append('unknown')
            SMA6M_MFOT.append('unknown')
            SMA6M_OTH.append('unknown')
            SMA6M_PL.append('unknown')
            SMA6M_PLBL.append('unknown')
            SMA6M_RL.append('unknown')
            SMA6M_SCC.append('unknown')
            SMA6M_SEL.append('unknown')

            SMA1Y_AL.append('unknown')
            SMA1Y_BL.append('unknown')
            SMA1Y_CC.append('unknown')
            SMA1Y_CD.append('unknown')
            SMA1Y_CV.append('unknown')
            SMA1Y_GL.append('unknown')
            SMA1Y_HL.append('unknown')
            SMA1Y_LAS.append('unknown')
            SMA1Y_MFBL.append('unknown')
            SMA1Y_MFHL.append('unknown')
            SMA1Y_MFOT.append('unknown')
            SMA1Y_OTH.append('unknown')
            SMA1Y_PL.append('unknown')
            SMA1Y_PLBL.append('unknown')
            SMA1Y_RL.append('unknown')
            SMA1Y_SCC.append('unknown')
            SMA1Y_SEL.append('unknown')

            SMA2Y_AL.append('unknown')
            SMA2Y_BL.append('unknown')
            SMA2Y_CC.append('unknown')
            SMA2Y_CD.append('unknown')
            SMA2Y_CV.append('unknown')
            SMA2Y_GL.append('unknown')
            SMA2Y_HL.append('unknown')
            SMA2Y_LAS.append('unknown')
            SMA2Y_MFBL.append('unknown')
            SMA2Y_MFHL.append('unknown')
            SMA2Y_MFOT.append('unknown')
            SMA2Y_OTH.append('unknown')
            SMA2Y_PL.append('unknown')
            SMA2Y_PLBL.append('unknown')
            SMA2Y_RL.append('unknown')
            SMA2Y_SCC.append('unknown')
            SMA2Y_SEL.append('unknown')

            SMA3Y_AL.append('unknown')
            SMA3Y_BL.append('unknown')
            SMA3Y_CC.append('unknown')
            SMA3Y_CD.append('unknown')
            SMA3Y_CV.append('unknown')
            SMA3Y_GL.append('unknown')
            SMA3Y_HL.append('unknown')
            SMA3Y_LAS.append('unknown')
            SMA3Y_MFBL.append('unknown')
            SMA3Y_MFHL.append('unknown')
            SMA3Y_MFOT.append('unknown')
            SMA3Y_OTH.append('unknown')
            SMA3Y_PL.append('unknown')
            SMA3Y_PLBL.append('unknown')
            SMA3Y_RL.append('unknown')
            SMA3Y_SCC.append('unknown')
            SMA3Y_SEL.append('unknown')

        else:
            DPD30P3M_AL.append(count_30_3m_list_AL[x])
            DPD30P3M_BL.append(count_30_3m_list_BL[x])
            DPD30P3M_CC.append(count_30_3m_list_CC[x])
            DPD30P3M_CD.append(count_30_3m_list_CD[x])
            DPD30P3M_CV.append(count_30_3m_list_CV[x])
            DPD30P3M_GL.append(count_30_3m_list_GL[x])
            DPD30P3M_HL.append(count_30_3m_list_HL[x])
            DPD30P3M_LAS.append(count_30_3m_list_LAS[x])
            DPD30P3M_MFBL.append(count_30_3m_list_MFBL[x])
            DPD30P3M_MFHL.append(count_30_3m_list_MFHL[x])
            DPD30P3M_MFOT.append(count_30_3m_list_MFOT[x])
            DPD30P3M_OTH.append(count_30_3m_list_OTH[x])
            DPD30P3M_PL.append(count_30_3m_list_PL[x])
            DPD30P3M_PLBL.append(count_30_3m_list_PLBL[x])
            DPD30P3M_RL.append(count_30_3m_list_RL[x])
            DPD30P3M_SCC.append(count_30_3m_list_SCC[x])
            DPD30P3M_SEL.append(count_30_3m_list_SEL[x])

            DPD60P3M_AL.append(count_60_3m_list_AL[x])
            DPD60P3M_BL.append(count_60_3m_list_BL[x])
            DPD60P3M_CC.append(count_60_3m_list_CC[x])
            DPD60P3M_CD.append(count_60_3m_list_CD[x])
            DPD60P3M_CV.append(count_60_3m_list_CV[x])
            DPD60P3M_GL.append(count_60_3m_list_GL[x])
            DPD60P3M_HL.append(count_60_3m_list_HL[x])
            DPD60P3M_LAS.append(count_60_3m_list_LAS[x])
            DPD60P3M_MFBL.append(count_60_3m_list_MFBL[x])
            DPD60P3M_MFHL.append(count_60_3m_list_MFHL[x])
            DPD60P3M_MFOT.append(count_60_3m_list_MFOT[x])
            DPD60P3M_OTH.append(count_60_3m_list_OTH[x])
            DPD60P3M_PL.append(count_60_3m_list_PL[x])
            DPD60P3M_PLBL.append(count_60_3m_list_PLBL[x])
            DPD60P3M_RL.append(count_60_3m_list_RL[x])
            DPD60P3M_SCC.append(count_60_3m_list_SCC[x])
            DPD60P3M_SEL.append(count_60_3m_list_SEL[x])

            DPD90P3M_AL.append(count_90_3m_list_AL[x])
            DPD90P3M_BL.append(count_90_3m_list_BL[x])
            DPD90P3M_CC.append(count_90_3m_list_CC[x])
            DPD90P3M_CD.append(count_90_3m_list_CD[x])
            DPD90P3M_CV.append(count_90_3m_list_CV[x])
            DPD90P3M_GL.append(count_90_3m_list_GL[x])
            DPD90P3M_HL.append(count_90_3m_list_HL[x])
            DPD90P3M_LAS.append(count_90_3m_list_LAS[x])
            DPD90P3M_MFBL.append(count_90_3m_list_MFBL[x])
            DPD90P3M_MFHL.append(count_90_3m_list_MFHL[x])
            DPD90P3M_MFOT.append(count_90_3m_list_MFOT[x])
            DPD90P3M_OTH.append(count_90_3m_list_OTH[x])
            DPD90P3M_PL.append(count_90_3m_list_PL[x])
            DPD90P3M_PLBL.append(count_90_3m_list_PLBL[x])
            DPD90P3M_RL.append(count_90_3m_list_RL[x])
            DPD90P3M_SCC.append(count_90_3m_list_SCC[x])
            DPD90P3M_SEL.append(count_90_3m_list_SEL[x])

            DPD30P6M_AL.append(count_30_6m_list_AL[x])
            DPD30P6M_BL.append(count_30_6m_list_BL[x])
            DPD30P6M_CC.append(count_30_6m_list_CC[x])
            DPD30P6M_CD.append(count_30_6m_list_CD[x])
            DPD30P6M_CV.append(count_30_6m_list_CV[x])
            DPD30P6M_GL.append(count_30_6m_list_GL[x])
            DPD30P6M_HL.append(count_30_6m_list_HL[x])
            DPD30P6M_LAS.append(count_30_6m_list_LAS[x])
            DPD30P6M_MFBL.append(count_30_6m_list_MFBL[x])
            DPD30P6M_MFHL.append(count_30_6m_list_MFHL[x])
            DPD30P6M_MFOT.append(count_30_6m_list_MFOT[x])
            DPD30P6M_OTH.append(count_30_6m_list_OTH[x])
            DPD30P6M_PL.append(count_30_6m_list_PL[x])
            DPD30P6M_PLBL.append(count_30_6m_list_PLBL[x])
            DPD30P6M_RL.append(count_30_6m_list_RL[x])
            DPD30P6M_SCC.append(count_30_6m_list_SCC[x])
            DPD30P6M_SEL.append(count_30_6m_list_SEL[x])

            DPD60P6M_AL.append(count_60_6m_list_AL[x])
            DPD60P6M_BL.append(count_60_6m_list_BL[x])
            DPD60P6M_CC.append(count_60_6m_list_CC[x])
            DPD60P6M_CD.append(count_60_6m_list_CD[x])
            DPD60P6M_CV.append(count_60_6m_list_CV[x])
            DPD60P6M_GL.append(count_60_6m_list_GL[x])
            DPD60P6M_HL.append(count_60_6m_list_HL[x])
            DPD60P6M_LAS.append(count_60_6m_list_LAS[x])
            DPD60P6M_MFBL.append(count_60_6m_list_MFBL[x])
            DPD60P6M_MFHL.append(count_60_6m_list_MFHL[x])
            DPD60P6M_MFOT.append(count_60_6m_list_MFOT[x])
            DPD60P6M_OTH.append(count_60_6m_list_OTH[x])
            DPD60P6M_PL.append(count_60_6m_list_PL[x])
            DPD60P6M_PLBL.append(count_60_6m_list_PLBL[x])
            DPD60P6M_RL.append(count_60_6m_list_RL[x])
            DPD60P6M_SCC.append(count_60_6m_list_SCC[x])
            DPD60P6M_SEL.append(count_60_6m_list_SEL[x])

            DPD90P6M_AL.append(count_90_6m_list_AL[x])
            DPD90P6M_BL.append(count_90_6m_list_BL[x])
            DPD90P6M_CC.append(count_90_6m_list_CC[x])
            DPD90P6M_CD.append(count_90_6m_list_CD[x])
            DPD90P6M_CV.append(count_90_6m_list_CV[x])
            DPD90P6M_GL.append(count_90_6m_list_GL[x])
            DPD90P6M_HL.append(count_90_6m_list_HL[x])
            DPD90P6M_LAS.append(count_90_6m_list_LAS[x])
            DPD90P6M_MFBL.append(count_90_6m_list_MFBL[x])
            DPD90P6M_MFHL.append(count_90_6m_list_MFHL[x])
            DPD90P6M_MFOT.append(count_90_6m_list_MFOT[x])
            DPD90P6M_OTH.append(count_90_6m_list_OTH[x])
            DPD90P6M_PL.append(count_90_6m_list_PL[x])
            DPD90P6M_PLBL.append(count_90_6m_list_PLBL[x])
            DPD90P6M_RL.append(count_90_6m_list_RL[x])
            DPD90P6M_SCC.append(count_90_6m_list_SCC[x])
            DPD90P6M_SEL.append(count_90_6m_list_SEL[x])

            DPD30P1Y_AL.append(count_30_1y_list_AL[x])
            DPD30P1Y_BL.append(count_30_1y_list_BL[x])
            DPD30P1Y_CC.append(count_30_1y_list_CC[x])
            DPD30P1Y_CD.append(count_30_1y_list_CD[x])
            DPD30P1Y_CV.append(count_30_1y_list_CV[x])
            DPD30P1Y_GL.append(count_30_1y_list_GL[x])
            DPD30P1Y_HL.append(count_30_1y_list_HL[x])
            DPD30P1Y_LAS.append(count_30_1y_list_LAS[x])
            DPD30P1Y_MFBL.append(count_30_1y_list_MFBL[x])
            DPD30P1Y_MFHL.append(count_30_1y_list_MFHL[x])
            DPD30P1Y_MFOT.append(count_30_1y_list_MFOT[x])
            DPD30P1Y_OTH.append(count_30_1y_list_OTH[x])
            DPD30P1Y_PL.append(count_30_1y_list_PL[x])
            DPD30P1Y_PLBL.append(count_30_1y_list_PLBL[x])
            DPD30P1Y_RL.append(count_30_1y_list_RL[x])
            DPD30P1Y_SCC.append(count_30_1y_list_SCC[x])
            DPD30P1Y_SEL.append(count_30_1y_list_SEL[x])

            DPD60P1Y_AL.append(count_60_1y_list_AL[x])
            DPD60P1Y_BL.append(count_60_1y_list_BL[x])
            DPD60P1Y_CC.append(count_60_1y_list_CC[x])
            DPD60P1Y_CD.append(count_60_1y_list_CD[x])
            DPD60P1Y_CV.append(count_60_1y_list_CV[x])
            DPD60P1Y_GL.append(count_60_1y_list_GL[x])
            DPD60P1Y_HL.append(count_60_1y_list_HL[x])
            DPD60P1Y_LAS.append(count_60_1y_list_LAS[x])
            DPD60P1Y_MFBL.append(count_60_1y_list_MFBL[x])
            DPD60P1Y_MFHL.append(count_60_1y_list_MFHL[x])
            DPD60P1Y_MFOT.append(count_60_1y_list_MFOT[x])
            DPD60P1Y_OTH.append(count_60_1y_list_OTH[x])
            DPD60P1Y_PL.append(count_60_1y_list_PL[x])
            DPD60P1Y_PLBL.append(count_60_1y_list_PLBL[x])
            DPD60P1Y_RL.append(count_60_1y_list_RL[x])
            DPD60P1Y_SCC.append(count_60_1y_list_SCC[x])
            DPD60P1Y_SEL.append(count_60_1y_list_SEL[x])

            DPD90P1Y_AL.append(count_90_1y_list_AL[x])
            DPD90P1Y_BL.append(count_90_1y_list_BL[x])
            DPD90P1Y_CC.append(count_90_1y_list_CC[x])
            DPD90P1Y_CD.append(count_90_1y_list_CD[x])
            DPD90P1Y_CV.append(count_90_1y_list_CV[x])
            DPD90P1Y_GL.append(count_90_1y_list_GL[x])
            DPD90P1Y_HL.append(count_90_1y_list_HL[x])
            DPD90P1Y_LAS.append(count_90_1y_list_LAS[x])
            DPD90P1Y_MFBL.append(count_90_1y_list_MFBL[x])
            DPD90P1Y_MFHL.append(count_90_1y_list_MFHL[x])
            DPD90P1Y_MFOT.append(count_90_1y_list_MFOT[x])
            DPD90P1Y_OTH.append(count_90_1y_list_OTH[x])
            DPD90P1Y_PL.append(count_90_1y_list_PL[x])
            DPD90P1Y_PLBL.append(count_90_1y_list_PLBL[x])
            DPD90P1Y_RL.append(count_90_1y_list_RL[x])
            DPD90P1Y_SCC.append(count_90_1y_list_SCC[x])
            DPD90P1Y_SEL.append(count_90_1y_list_SEL[x])

            DPD30P2Y_AL.append(count_30_2y_list_AL[x])
            DPD30P2Y_BL.append(count_30_2y_list_BL[x])
            DPD30P2Y_CC.append(count_30_2y_list_CC[x])
            DPD30P2Y_CD.append(count_30_2y_list_CD[x])
            DPD30P2Y_CV.append(count_30_2y_list_CV[x])
            DPD30P2Y_GL.append(count_30_2y_list_GL[x])
            DPD30P2Y_HL.append(count_30_2y_list_HL[x])
            DPD30P2Y_LAS.append(count_30_2y_list_LAS[x])
            DPD30P2Y_MFBL.append(count_30_2y_list_MFBL[x])
            DPD30P2Y_MFHL.append(count_30_2y_list_MFHL[x])
            DPD30P2Y_MFOT.append(count_30_2y_list_MFOT[x])
            DPD30P2Y_OTH.append(count_30_2y_list_OTH[x])
            DPD30P2Y_PL.append(count_30_2y_list_PL[x])
            DPD30P2Y_PLBL.append(count_30_2y_list_PLBL[x])
            DPD30P2Y_RL.append(count_30_2y_list_RL[x])
            DPD30P2Y_SCC.append(count_30_2y_list_SCC[x])
            DPD30P2Y_SEL.append(count_30_2y_list_SEL[x])

            DPD60P2Y_AL.append(count_60_2y_list_AL[x])
            DPD60P2Y_BL.append(count_60_2y_list_BL[x])
            DPD60P2Y_CC.append(count_60_2y_list_CC[x])
            DPD60P2Y_CD.append(count_60_2y_list_CD[x])
            DPD60P2Y_CV.append(count_60_2y_list_CV[x])
            DPD60P2Y_GL.append(count_60_2y_list_GL[x])
            DPD60P2Y_HL.append(count_60_2y_list_HL[x])
            DPD60P2Y_LAS.append(count_60_2y_list_LAS[x])
            DPD60P2Y_MFBL.append(count_60_2y_list_MFBL[x])
            DPD60P2Y_MFHL.append(count_60_2y_list_MFHL[x])
            DPD60P2Y_MFOT.append(count_60_2y_list_MFOT[x])
            DPD60P2Y_OTH.append(count_60_2y_list_OTH[x])
            DPD60P2Y_PL.append(count_60_2y_list_PL[x])
            DPD60P2Y_PLBL.append(count_60_2y_list_PLBL[x])
            DPD60P2Y_RL.append(count_60_2y_list_RL[x])
            DPD60P2Y_SCC.append(count_60_2y_list_SCC[x])
            DPD60P2Y_SEL.append(count_60_2y_list_SEL[x])

            DPD90P2Y_AL.append(count_90_2y_list_AL[x])
            DPD90P2Y_BL.append(count_90_2y_list_BL[x])
            DPD90P2Y_CC.append(count_90_2y_list_CC[x])
            DPD90P2Y_CD.append(count_90_2y_list_CD[x])
            DPD90P2Y_CV.append(count_90_2y_list_CV[x])
            DPD90P2Y_GL.append(count_90_2y_list_GL[x])
            DPD90P2Y_HL.append(count_90_2y_list_HL[x])
            DPD90P2Y_LAS.append(count_90_2y_list_LAS[x])
            DPD90P2Y_MFBL.append(count_90_2y_list_MFBL[x])
            DPD90P2Y_MFHL.append(count_90_2y_list_MFHL[x])
            DPD90P2Y_MFOT.append(count_90_2y_list_MFOT[x])
            DPD90P2Y_OTH.append(count_90_2y_list_OTH[x])
            DPD90P2Y_PL.append(count_90_2y_list_PL[x])
            DPD90P2Y_PLBL.append(count_90_2y_list_PLBL[x])
            DPD90P2Y_RL.append(count_90_2y_list_RL[x])
            DPD90P2Y_SCC.append(count_90_2y_list_SCC[x])
            DPD90P2Y_SEL.append(count_90_2y_list_SEL[x])

            DPD30P3Y_AL.append(count_30_3y_list_AL[x])
            DPD30P3Y_BL.append(count_30_3y_list_BL[x])
            DPD30P3Y_CC.append(count_30_3y_list_CC[x])
            DPD30P3Y_CD.append(count_30_3y_list_CD[x])
            DPD30P3Y_CV.append(count_30_3y_list_CV[x])
            DPD30P3Y_GL.append(count_30_3y_list_GL[x])
            DPD30P3Y_HL.append(count_30_3y_list_HL[x])
            DPD30P3Y_LAS.append(count_30_3y_list_LAS[x])
            DPD30P3Y_MFBL.append(count_30_3y_list_MFBL[x])
            DPD30P3Y_MFHL.append(count_30_3y_list_MFHL[x])
            DPD30P3Y_MFOT.append(count_30_3y_list_MFOT[x])
            DPD30P3Y_OTH.append(count_30_3y_list_OTH[x])
            DPD30P3Y_PL.append(count_30_3y_list_PL[x])
            DPD30P3Y_PLBL.append(count_30_3y_list_PLBL[x])
            DPD30P3Y_RL.append(count_30_3y_list_RL[x])
            DPD30P3Y_SCC.append(count_30_3y_list_SCC[x])
            DPD30P3Y_SEL.append(count_30_3y_list_SEL[x])

            DPD60P3Y_AL.append(count_60_3y_list_AL[x])
            DPD60P3Y_BL.append(count_60_3y_list_BL[x])
            DPD60P3Y_CC.append(count_60_3y_list_CC[x])
            DPD60P3Y_CD.append(count_60_3y_list_CD[x])
            DPD60P3Y_CV.append(count_60_3y_list_CV[x])
            DPD60P3Y_GL.append(count_60_3y_list_GL[x])
            DPD60P3Y_HL.append(count_60_3y_list_HL[x])
            DPD60P3Y_LAS.append(count_60_3y_list_LAS[x])
            DPD60P3Y_MFBL.append(count_60_3y_list_MFBL[x])
            DPD60P3Y_MFHL.append(count_60_3y_list_MFHL[x])
            DPD60P3Y_MFOT.append(count_60_3y_list_MFOT[x])
            DPD60P3Y_OTH.append(count_60_3y_list_OTH[x])
            DPD60P3Y_PL.append(count_60_3y_list_PL[x])
            DPD60P3Y_PLBL.append(count_60_3y_list_PLBL[x])
            DPD60P3Y_RL.append(count_60_3y_list_RL[x])
            DPD60P3Y_SCC.append(count_60_3y_list_SCC[x])
            DPD60P3Y_SEL.append(count_60_3y_list_SEL[x])

            DPD90P3Y_AL.append(count_90_3y_list_AL[x])
            DPD90P3Y_BL.append(count_90_3y_list_BL[x])
            DPD90P3Y_CC.append(count_90_3y_list_CC[x])
            DPD90P3Y_CD.append(count_90_3y_list_CD[x])
            DPD90P3Y_CV.append(count_90_3y_list_CV[x])
            DPD90P3Y_GL.append(count_90_3y_list_GL[x])
            DPD90P3Y_HL.append(count_90_3y_list_HL[x])
            DPD90P3Y_LAS.append(count_90_3y_list_LAS[x])
            DPD90P3Y_MFBL.append(count_90_3y_list_MFBL[x])
            DPD90P3Y_MFHL.append(count_90_3y_list_MFHL[x])
            DPD90P3Y_MFOT.append(count_90_3y_list_MFOT[x])
            DPD90P3Y_OTH.append(count_90_3y_list_OTH[x])
            DPD90P3Y_PL.append(count_90_3y_list_PL[x])
            DPD90P3Y_PLBL.append(count_90_3y_list_PLBL[x])
            DPD90P3Y_RL.append(count_90_3y_list_RL[x])
            DPD90P3Y_SCC.append(count_90_3y_list_SCC[x])
            DPD90P3Y_SEL.append(count_90_3y_list_SEL[x])

            STD1M_AL.append(count_std_1m_list_AL[x])
            STD1M_BL.append(count_std_1m_list_BL[x])
            STD1M_CC.append(count_std_1m_list_CC[x])
            STD1M_CD.append(count_std_1m_list_CD[x])
            STD1M_CV.append(count_std_1m_list_CV[x])
            STD1M_GL.append(count_std_1m_list_GL[x])
            STD1M_HL.append(count_std_1m_list_HL[x])
            STD1M_LAS.append(count_std_1m_list_LAS[x])
            STD1M_MFBL.append(count_std_1m_list_MFBL[x])
            STD1M_MFHL.append(count_std_1m_list_MFHL[x])
            STD1M_MFOT.append(count_std_1m_list_MFOT[x])
            STD1M_OTH.append(count_std_1m_list_OTH[x])
            STD1M_PL.append(count_std_1m_list_PL[x])
            STD1M_PLBL.append(count_std_1m_list_PLBL[x])
            STD1M_RL.append(count_std_1m_list_RL[x])
            STD1M_SCC.append(count_std_1m_list_SCC[x])
            STD1M_SEL.append(count_std_1m_list_SEL[x])

            STD3M_AL.append(count_std_3m_list_AL[x])
            STD3M_BL.append(count_std_3m_list_BL[x])
            STD3M_CC.append(count_std_3m_list_CC[x])
            STD3M_CD.append(count_std_3m_list_CD[x])
            STD3M_CV.append(count_std_3m_list_CV[x])
            STD3M_GL.append(count_std_3m_list_GL[x])
            STD3M_HL.append(count_std_3m_list_HL[x])
            STD3M_LAS.append(count_std_3m_list_LAS[x])
            STD3M_MFBL.append(count_std_3m_list_MFBL[x])
            STD3M_MFHL.append(count_std_3m_list_MFHL[x])
            STD3M_MFOT.append(count_std_3m_list_MFOT[x])
            STD3M_OTH.append(count_std_3m_list_OTH[x])
            STD3M_PL.append(count_std_3m_list_PL[x])
            STD3M_PLBL.append(count_std_3m_list_PLBL[x])
            STD3M_RL.append(count_std_3m_list_RL[x])
            STD3M_SCC.append(count_std_3m_list_SCC[x])
            STD3M_SEL.append(count_std_3m_list_SEL[x])

            STD6M_AL.append(count_std_6m_list_AL[x])
            STD6M_BL.append(count_std_6m_list_BL[x])
            STD6M_CC.append(count_std_6m_list_CC[x])
            STD6M_CD.append(count_std_6m_list_CD[x])
            STD6M_CV.append(count_std_6m_list_CV[x])
            STD6M_GL.append(count_std_6m_list_GL[x])
            STD6M_HL.append(count_std_6m_list_HL[x])
            STD6M_LAS.append(count_std_6m_list_LAS[x])
            STD6M_MFBL.append(count_std_6m_list_MFBL[x])
            STD6M_MFHL.append(count_std_6m_list_MFHL[x])
            STD6M_MFOT.append(count_std_6m_list_MFOT[x])
            STD6M_OTH.append(count_std_6m_list_OTH[x])
            STD6M_PL.append(count_std_6m_list_PL[x])
            STD6M_PLBL.append(count_std_6m_list_PLBL[x])
            STD6M_RL.append(count_std_6m_list_RL[x])
            STD6M_SCC.append(count_std_6m_list_SCC[x])
            STD6M_SEL.append(count_std_6m_list_SEL[x])

            STD1Y_AL.append(count_std_1y_list_AL[x])
            STD1Y_BL.append(count_std_1y_list_BL[x])
            STD1Y_CC.append(count_std_1y_list_CC[x])
            STD1Y_CD.append(count_std_1y_list_CD[x])
            STD1Y_CV.append(count_std_1y_list_CV[x])
            STD1Y_GL.append(count_std_1y_list_GL[x])
            STD1Y_HL.append(count_std_1y_list_HL[x])
            STD1Y_LAS.append(count_std_1y_list_LAS[x])
            STD1Y_MFBL.append(count_std_1y_list_MFBL[x])
            STD1Y_MFHL.append(count_std_1y_list_MFHL[x])
            STD1Y_MFOT.append(count_std_1y_list_MFOT[x])
            STD1Y_OTH.append(count_std_1y_list_OTH[x])
            STD1Y_PL.append(count_std_1y_list_PL[x])
            STD1Y_PLBL.append(count_std_1y_list_PLBL[x])
            STD1Y_RL.append(count_std_1y_list_RL[x])
            STD1Y_SCC.append(count_std_1y_list_SCC[x])
            STD1Y_SEL.append(count_std_1y_list_SEL[x])

            STD2Y_AL.append(count_std_2y_list_AL[x])
            STD2Y_BL.append(count_std_2y_list_BL[x])
            STD2Y_CC.append(count_std_2y_list_CC[x])
            STD2Y_CD.append(count_std_2y_list_CD[x])
            STD2Y_CV.append(count_std_2y_list_CV[x])
            STD2Y_GL.append(count_std_2y_list_GL[x])
            STD2Y_HL.append(count_std_2y_list_HL[x])
            STD2Y_LAS.append(count_std_2y_list_LAS[x])
            STD2Y_MFBL.append(count_std_2y_list_MFBL[x])
            STD2Y_MFHL.append(count_std_2y_list_MFHL[x])
            STD2Y_MFOT.append(count_std_2y_list_MFOT[x])
            STD2Y_OTH.append(count_std_2y_list_OTH[x])
            STD2Y_PL.append(count_std_2y_list_PL[x])
            STD2Y_PLBL.append(count_std_2y_list_PLBL[x])
            STD2Y_RL.append(count_std_2y_list_RL[x])
            STD2Y_SCC.append(count_std_2y_list_SCC[x])
            STD2Y_SEL.append(count_std_2y_list_SEL[x])

            STD3Y_AL.append(count_std_3y_list_AL[x])
            STD3Y_BL.append(count_std_3y_list_BL[x])
            STD3Y_CC.append(count_std_3y_list_CC[x])
            STD3Y_CD.append(count_std_3y_list_CD[x])
            STD3Y_CV.append(count_std_3y_list_CV[x])
            STD3Y_GL.append(count_std_3y_list_GL[x])
            STD3Y_HL.append(count_std_3y_list_HL[x])
            STD3Y_LAS.append(count_std_3y_list_LAS[x])
            STD3Y_MFBL.append(count_std_3y_list_MFBL[x])
            STD3Y_MFHL.append(count_std_3y_list_MFHL[x])
            STD3Y_MFOT.append(count_std_3y_list_MFOT[x])
            STD3Y_OTH.append(count_std_3y_list_OTH[x])
            STD3Y_PL.append(count_std_3y_list_PL[x])
            STD3Y_PLBL.append(count_std_3y_list_PLBL[x])
            STD3Y_RL.append(count_std_3y_list_RL[x])
            STD3Y_SCC.append(count_std_3y_list_SCC[x])
            STD3Y_SEL.append(count_std_3y_list_SEL[x])

            SUB1M_AL.append(count_sub_1m_list_AL[x])
            SUB1M_BL.append(count_sub_1m_list_BL[x])
            SUB1M_CC.append(count_sub_1m_list_CC[x])
            SUB1M_CD.append(count_sub_1m_list_CD[x])
            SUB1M_CV.append(count_sub_1m_list_CV[x])
            SUB1M_GL.append(count_sub_1m_list_GL[x])
            SUB1M_HL.append(count_sub_1m_list_HL[x])
            SUB1M_LAS.append(count_sub_1m_list_LAS[x])
            SUB1M_MFBL.append(count_sub_1m_list_MFBL[x])
            SUB1M_MFHL.append(count_sub_1m_list_MFHL[x])
            SUB1M_MFOT.append(count_sub_1m_list_MFOT[x])
            SUB1M_OTH.append(count_sub_1m_list_OTH[x])
            SUB1M_PL.append(count_sub_1m_list_PL[x])
            SUB1M_PLBL.append(count_sub_1m_list_PLBL[x])
            SUB1M_RL.append(count_sub_1m_list_RL[x])
            SUB1M_SCC.append(count_sub_1m_list_SCC[x])
            SUB1M_SEL.append(count_sub_1m_list_SEL[x])

            SUB3M_AL.append(count_sub_3m_list_AL[x])
            SUB3M_BL.append(count_sub_3m_list_BL[x])
            SUB3M_CC.append(count_sub_3m_list_CC[x])
            SUB3M_CD.append(count_sub_3m_list_CD[x])
            SUB3M_CV.append(count_sub_3m_list_CV[x])
            SUB3M_GL.append(count_sub_3m_list_GL[x])
            SUB3M_HL.append(count_sub_3m_list_HL[x])
            SUB3M_LAS.append(count_sub_3m_list_LAS[x])
            SUB3M_MFBL.append(count_sub_3m_list_MFBL[x])
            SUB3M_MFHL.append(count_sub_3m_list_MFHL[x])
            SUB3M_MFOT.append(count_sub_3m_list_MFOT[x])
            SUB3M_OTH.append(count_sub_3m_list_OTH[x])
            SUB3M_PL.append(count_sub_3m_list_PL[x])
            SUB3M_PLBL.append(count_sub_3m_list_PLBL[x])
            SUB3M_RL.append(count_sub_3m_list_RL[x])
            SUB3M_SCC.append(count_sub_3m_list_SCC[x])
            SUB3M_SEL.append(count_sub_3m_list_SEL[x])

            SUB6M_AL.append(count_sub_6m_list_AL[x])
            SUB6M_BL.append(count_sub_6m_list_BL[x])
            SUB6M_CC.append(count_sub_6m_list_CC[x])
            SUB6M_CD.append(count_sub_6m_list_CD[x])
            SUB6M_CV.append(count_sub_6m_list_CV[x])
            SUB6M_GL.append(count_sub_6m_list_GL[x])
            SUB6M_HL.append(count_sub_6m_list_HL[x])
            SUB6M_LAS.append(count_sub_6m_list_LAS[x])
            SUB6M_MFBL.append(count_sub_6m_list_MFBL[x])
            SUB6M_MFHL.append(count_sub_6m_list_MFHL[x])
            SUB6M_MFOT.append(count_sub_6m_list_MFOT[x])
            SUB6M_OTH.append(count_sub_6m_list_OTH[x])
            SUB6M_PL.append(count_sub_6m_list_PL[x])
            SUB6M_PLBL.append(count_sub_6m_list_PLBL[x])
            SUB6M_RL.append(count_sub_6m_list_RL[x])
            SUB6M_SCC.append(count_sub_6m_list_SCC[x])
            SUB6M_SEL.append(count_sub_6m_list_SEL[x])

            SUB1Y_AL.append(count_sub_1y_list_AL[x])
            SUB1Y_BL.append(count_sub_1y_list_BL[x])
            SUB1Y_CC.append(count_sub_1y_list_CC[x])
            SUB1Y_CD.append(count_sub_1y_list_CD[x])
            SUB1Y_CV.append(count_sub_1y_list_CV[x])
            SUB1Y_GL.append(count_sub_1y_list_GL[x])
            SUB1Y_HL.append(count_sub_1y_list_HL[x])
            SUB1Y_LAS.append(count_sub_1y_list_LAS[x])
            SUB1Y_MFBL.append(count_sub_1y_list_MFBL[x])
            SUB1Y_MFHL.append(count_sub_1y_list_MFHL[x])
            SUB1Y_MFOT.append(count_sub_1y_list_MFOT[x])
            SUB1Y_OTH.append(count_sub_1y_list_OTH[x])
            SUB1Y_PL.append(count_sub_1y_list_PL[x])
            SUB1Y_PLBL.append(count_sub_1y_list_PLBL[x])
            SUB1Y_RL.append(count_sub_1y_list_RL[x])
            SUB1Y_SCC.append(count_sub_1y_list_SCC[x])
            SUB1Y_SEL.append(count_sub_1y_list_SEL[x])

            SUB2Y_AL.append(count_sub_2y_list_AL[x])
            SUB2Y_BL.append(count_sub_2y_list_BL[x])
            SUB2Y_CC.append(count_sub_2y_list_CC[x])
            SUB2Y_CD.append(count_sub_2y_list_CD[x])
            SUB2Y_CV.append(count_sub_2y_list_CV[x])
            SUB2Y_GL.append(count_sub_2y_list_GL[x])
            SUB2Y_HL.append(count_sub_2y_list_HL[x])
            SUB2Y_LAS.append(count_sub_2y_list_LAS[x])
            SUB2Y_MFBL.append(count_sub_2y_list_MFBL[x])
            SUB2Y_MFHL.append(count_sub_2y_list_MFHL[x])
            SUB2Y_MFOT.append(count_sub_2y_list_MFOT[x])
            SUB2Y_OTH.append(count_sub_2y_list_OTH[x])
            SUB2Y_PL.append(count_sub_2y_list_PL[x])
            SUB2Y_PLBL.append(count_sub_2y_list_PLBL[x])
            SUB2Y_RL.append(count_sub_2y_list_RL[x])
            SUB2Y_SCC.append(count_sub_2y_list_SCC[x])
            SUB2Y_SEL.append(count_sub_2y_list_SEL[x])

            SUB3Y_AL.append(count_sub_3y_list_AL[x])
            SUB3Y_BL.append(count_sub_3y_list_BL[x])
            SUB3Y_CC.append(count_sub_3y_list_CC[x])
            SUB3Y_CD.append(count_sub_3y_list_CD[x])
            SUB3Y_CV.append(count_sub_3y_list_CV[x])
            SUB3Y_GL.append(count_sub_3y_list_GL[x])
            SUB3Y_HL.append(count_sub_3y_list_HL[x])
            SUB3Y_LAS.append(count_sub_3y_list_LAS[x])
            SUB3Y_MFBL.append(count_sub_3y_list_MFBL[x])
            SUB3Y_MFHL.append(count_sub_3y_list_MFHL[x])
            SUB3Y_MFOT.append(count_sub_3y_list_MFOT[x])
            SUB3Y_OTH.append(count_sub_3y_list_OTH[x])
            SUB3Y_PL.append(count_sub_3y_list_PL[x])
            SUB3Y_PLBL.append(count_sub_3y_list_PLBL[x])
            SUB3Y_RL.append(count_sub_3y_list_RL[x])
            SUB3Y_SCC.append(count_sub_3y_list_SCC[x])
            SUB3Y_SEL.append(count_sub_3y_list_SEL[x])

            DBT1M_AL.append(count_dbt_1m_list_AL[x])
            DBT1M_BL.append(count_dbt_1m_list_BL[x])
            DBT1M_CC.append(count_dbt_1m_list_CC[x])
            DBT1M_CD.append(count_dbt_1m_list_CD[x])
            DBT1M_CV.append(count_dbt_1m_list_CV[x])
            DBT1M_GL.append(count_dbt_1m_list_GL[x])
            DBT1M_HL.append(count_dbt_1m_list_HL[x])
            DBT1M_LAS.append(count_dbt_1m_list_LAS[x])
            DBT1M_MFBL.append(count_dbt_1m_list_MFBL[x])
            DBT1M_MFHL.append(count_dbt_1m_list_MFHL[x])
            DBT1M_MFOT.append(count_dbt_1m_list_MFOT[x])
            DBT1M_OTH.append(count_dbt_1m_list_OTH[x])
            DBT1M_PL.append(count_dbt_1m_list_PL[x])
            DBT1M_PLBL.append(count_dbt_1m_list_PLBL[x])
            DBT1M_RL.append(count_dbt_1m_list_RL[x])
            DBT1M_SCC.append(count_dbt_1m_list_SCC[x])
            DBT1M_SEL.append(count_dbt_1m_list_SEL[x])

            DBT3M_AL.append(count_dbt_3m_list_AL[x])
            DBT3M_BL.append(count_dbt_3m_list_BL[x])
            DBT3M_CC.append(count_dbt_3m_list_CC[x])
            DBT3M_CD.append(count_dbt_3m_list_CD[x])
            DBT3M_CV.append(count_dbt_3m_list_CV[x])
            DBT3M_GL.append(count_dbt_3m_list_GL[x])
            DBT3M_HL.append(count_dbt_3m_list_HL[x])
            DBT3M_LAS.append(count_dbt_3m_list_LAS[x])
            DBT3M_MFBL.append(count_dbt_3m_list_MFBL[x])
            DBT3M_MFHL.append(count_dbt_3m_list_MFHL[x])
            DBT3M_MFOT.append(count_dbt_3m_list_MFOT[x])
            DBT3M_OTH.append(count_dbt_3m_list_OTH[x])
            DBT3M_PL.append(count_dbt_3m_list_PL[x])
            DBT3M_PLBL.append(count_dbt_3m_list_PLBL[x])
            DBT3M_RL.append(count_dbt_3m_list_RL[x])
            DBT3M_SCC.append(count_dbt_3m_list_SCC[x])
            DBT3M_SEL.append(count_dbt_3m_list_SEL[x])

            DBT6M_AL.append(count_dbt_6m_list_AL[x])
            DBT6M_BL.append(count_dbt_6m_list_BL[x])
            DBT6M_CC.append(count_dbt_6m_list_CC[x])
            DBT6M_CD.append(count_dbt_6m_list_CD[x])
            DBT6M_CV.append(count_dbt_6m_list_CV[x])
            DBT6M_GL.append(count_dbt_6m_list_GL[x])
            DBT6M_HL.append(count_dbt_6m_list_HL[x])
            DBT6M_LAS.append(count_dbt_6m_list_LAS[x])
            DBT6M_MFBL.append(count_dbt_6m_list_MFBL[x])
            DBT6M_MFHL.append(count_dbt_6m_list_MFHL[x])
            DBT6M_MFOT.append(count_dbt_6m_list_MFOT[x])
            DBT6M_OTH.append(count_dbt_6m_list_OTH[x])
            DBT6M_PL.append(count_dbt_6m_list_PL[x])
            DBT6M_PLBL.append(count_dbt_6m_list_PLBL[x])
            DBT6M_RL.append(count_dbt_6m_list_RL[x])
            DBT6M_SCC.append(count_dbt_6m_list_SCC[x])
            DBT6M_SEL.append(count_dbt_6m_list_SEL[x])

            DBT1Y_AL.append(count_dbt_1y_list_AL[x])
            DBT1Y_BL.append(count_dbt_1y_list_BL[x])
            DBT1Y_CC.append(count_dbt_1y_list_CC[x])
            DBT1Y_CD.append(count_dbt_1y_list_CD[x])
            DBT1Y_CV.append(count_dbt_1y_list_CV[x])
            DBT1Y_GL.append(count_dbt_1y_list_GL[x])
            DBT1Y_HL.append(count_dbt_1y_list_HL[x])
            DBT1Y_LAS.append(count_dbt_1y_list_LAS[x])
            DBT1Y_MFBL.append(count_dbt_1y_list_MFBL[x])
            DBT1Y_MFHL.append(count_dbt_1y_list_MFHL[x])
            DBT1Y_MFOT.append(count_dbt_1y_list_MFOT[x])
            DBT1Y_OTH.append(count_dbt_1y_list_OTH[x])
            DBT1Y_PL.append(count_dbt_1y_list_PL[x])
            DBT1Y_PLBL.append(count_dbt_1y_list_PLBL[x])
            DBT1Y_RL.append(count_dbt_1y_list_RL[x])
            DBT1Y_SCC.append(count_dbt_1y_list_SCC[x])
            DBT1Y_SEL.append(count_dbt_1y_list_SEL[x])

            DBT2Y_AL.append(count_dbt_2y_list_AL[x])
            DBT2Y_BL.append(count_dbt_2y_list_BL[x])
            DBT2Y_CC.append(count_dbt_2y_list_CC[x])
            DBT2Y_CD.append(count_dbt_2y_list_CD[x])
            DBT2Y_CV.append(count_dbt_2y_list_CV[x])
            DBT2Y_GL.append(count_dbt_2y_list_GL[x])
            DBT2Y_HL.append(count_dbt_2y_list_HL[x])
            DBT2Y_LAS.append(count_dbt_2y_list_LAS[x])
            DBT2Y_MFBL.append(count_dbt_2y_list_MFBL[x])
            DBT2Y_MFHL.append(count_dbt_2y_list_MFHL[x])
            DBT2Y_MFOT.append(count_dbt_2y_list_MFOT[x])
            DBT2Y_OTH.append(count_dbt_2y_list_OTH[x])
            DBT2Y_PL.append(count_dbt_2y_list_PL[x])
            DBT2Y_PLBL.append(count_dbt_2y_list_PLBL[x])
            DBT2Y_RL.append(count_dbt_2y_list_RL[x])
            DBT2Y_SCC.append(count_dbt_2y_list_SCC[x])
            DBT2Y_SEL.append(count_dbt_2y_list_SEL[x])

            DBT3Y_AL.append(count_dbt_3y_list_AL[x])
            DBT3Y_BL.append(count_dbt_3y_list_BL[x])
            DBT3Y_CC.append(count_dbt_3y_list_CC[x])
            DBT3Y_CD.append(count_dbt_3y_list_CD[x])
            DBT3Y_CV.append(count_dbt_3y_list_CV[x])
            DBT3Y_GL.append(count_dbt_3y_list_GL[x])
            DBT3Y_HL.append(count_dbt_3y_list_HL[x])
            DBT3Y_LAS.append(count_dbt_3y_list_LAS[x])
            DBT3Y_MFBL.append(count_dbt_3y_list_MFBL[x])
            DBT3Y_MFHL.append(count_dbt_3y_list_MFHL[x])
            DBT3Y_MFOT.append(count_dbt_3y_list_MFOT[x])
            DBT3Y_OTH.append(count_dbt_3y_list_OTH[x])
            DBT3Y_PL.append(count_dbt_3y_list_PL[x])
            DBT3Y_PLBL.append(count_dbt_3y_list_PLBL[x])
            DBT3Y_RL.append(count_dbt_3y_list_RL[x])
            DBT3Y_SCC.append(count_dbt_3y_list_SCC[x])
            DBT3Y_SEL.append(count_dbt_3y_list_SEL[x])

            LOS1M_AL.append(count_los_1m_list_AL[x])
            LOS1M_BL.append(count_los_1m_list_BL[x])
            LOS1M_CC.append(count_los_1m_list_CC[x])
            LOS1M_CD.append(count_los_1m_list_CD[x])
            LOS1M_CV.append(count_los_1m_list_CV[x])
            LOS1M_GL.append(count_los_1m_list_GL[x])
            LOS1M_HL.append(count_los_1m_list_HL[x])
            LOS1M_LAS.append(count_los_1m_list_LAS[x])
            LOS1M_MFBL.append(count_los_1m_list_MFBL[x])
            LOS1M_MFHL.append(count_los_1m_list_MFHL[x])
            LOS1M_MFOT.append(count_los_1m_list_MFOT[x])
            LOS1M_OTH.append(count_los_1m_list_OTH[x])
            LOS1M_PL.append(count_los_1m_list_PL[x])
            LOS1M_PLBL.append(count_los_1m_list_PLBL[x])
            LOS1M_RL.append(count_los_1m_list_RL[x])
            LOS1M_SCC.append(count_los_1m_list_SCC[x])
            LOS1M_SEL.append(count_los_1m_list_SEL[x])

            LOS3M_AL.append(count_los_3m_list_AL[x])
            LOS3M_BL.append(count_los_3m_list_BL[x])
            LOS3M_CC.append(count_los_3m_list_CC[x])
            LOS3M_CD.append(count_los_3m_list_CD[x])
            LOS3M_CV.append(count_los_3m_list_CV[x])
            LOS3M_GL.append(count_los_3m_list_GL[x])
            LOS3M_HL.append(count_los_3m_list_HL[x])
            LOS3M_LAS.append(count_los_3m_list_LAS[x])
            LOS3M_MFBL.append(count_los_3m_list_MFBL[x])
            LOS3M_MFHL.append(count_los_3m_list_MFHL[x])
            LOS3M_MFOT.append(count_los_3m_list_MFOT[x])
            LOS3M_OTH.append(count_los_3m_list_OTH[x])
            LOS3M_PL.append(count_los_3m_list_PL[x])
            LOS3M_PLBL.append(count_los_3m_list_PLBL[x])
            LOS3M_RL.append(count_los_3m_list_RL[x])
            LOS3M_SCC.append(count_los_3m_list_SCC[x])
            LOS3M_SEL.append(count_los_3m_list_SEL[x])

            LOS6M_AL.append(count_los_6m_list_AL[x])
            LOS6M_BL.append(count_los_6m_list_BL[x])
            LOS6M_CC.append(count_los_6m_list_CC[x])
            LOS6M_CD.append(count_los_6m_list_CD[x])
            LOS6M_CV.append(count_los_6m_list_CV[x])
            LOS6M_GL.append(count_los_6m_list_GL[x])
            LOS6M_HL.append(count_los_6m_list_HL[x])
            LOS6M_LAS.append(count_los_6m_list_LAS[x])
            LOS6M_MFBL.append(count_los_6m_list_MFBL[x])
            LOS6M_MFHL.append(count_los_6m_list_MFHL[x])
            LOS6M_MFOT.append(count_los_6m_list_MFOT[x])
            LOS6M_OTH.append(count_los_6m_list_OTH[x])
            LOS6M_PL.append(count_los_6m_list_PL[x])
            LOS6M_PLBL.append(count_los_6m_list_PLBL[x])
            LOS6M_RL.append(count_los_6m_list_RL[x])
            LOS6M_SCC.append(count_los_6m_list_SCC[x])
            LOS6M_SEL.append(count_los_6m_list_SEL[x])

            LOS1Y_AL.append(count_los_1y_list_AL[x])
            LOS1Y_BL.append(count_los_1y_list_BL[x])
            LOS1Y_CC.append(count_los_1y_list_CC[x])
            LOS1Y_CD.append(count_los_1y_list_CD[x])
            LOS1Y_CV.append(count_los_1y_list_CV[x])
            LOS1Y_GL.append(count_los_1y_list_GL[x])
            LOS1Y_HL.append(count_los_1y_list_HL[x])
            LOS1Y_LAS.append(count_los_1y_list_LAS[x])
            LOS1Y_MFBL.append(count_los_1y_list_MFBL[x])
            LOS1Y_MFHL.append(count_los_1y_list_MFHL[x])
            LOS1Y_MFOT.append(count_los_1y_list_MFOT[x])
            LOS1Y_OTH.append(count_los_1y_list_OTH[x])
            LOS1Y_PL.append(count_los_1y_list_PL[x])
            LOS1Y_PLBL.append(count_los_1y_list_PLBL[x])
            LOS1Y_RL.append(count_los_1y_list_RL[x])
            LOS1Y_SCC.append(count_los_1y_list_SCC[x])
            LOS1Y_SEL.append(count_los_1y_list_SEL[x])

            LOS2Y_AL.append(count_los_2y_list_AL[x])
            LOS2Y_BL.append(count_los_2y_list_BL[x])
            LOS2Y_CC.append(count_los_2y_list_CC[x])
            LOS2Y_CD.append(count_los_2y_list_CD[x])
            LOS2Y_CV.append(count_los_2y_list_CV[x])
            LOS2Y_GL.append(count_los_2y_list_GL[x])
            LOS2Y_HL.append(count_los_2y_list_HL[x])
            LOS2Y_LAS.append(count_los_2y_list_LAS[x])
            LOS2Y_MFBL.append(count_los_2y_list_MFBL[x])
            LOS2Y_MFHL.append(count_los_2y_list_MFHL[x])
            LOS2Y_MFOT.append(count_los_2y_list_MFOT[x])
            LOS2Y_OTH.append(count_los_2y_list_OTH[x])
            LOS2Y_PL.append(count_los_2y_list_PL[x])
            LOS2Y_PLBL.append(count_los_2y_list_PLBL[x])
            LOS2Y_RL.append(count_los_2y_list_RL[x])
            LOS2Y_SCC.append(count_los_2y_list_SCC[x])
            LOS2Y_SEL.append(count_los_2y_list_SEL[x])

            LOS3Y_AL.append(count_los_3y_list_AL[x])
            LOS3Y_BL.append(count_los_3y_list_BL[x])
            LOS3Y_CC.append(count_los_3y_list_CC[x])
            LOS3Y_CD.append(count_los_3y_list_CD[x])
            LOS3Y_CV.append(count_los_3y_list_CV[x])
            LOS3Y_GL.append(count_los_3y_list_GL[x])
            LOS3Y_HL.append(count_los_3y_list_HL[x])
            LOS3Y_LAS.append(count_los_3y_list_LAS[x])
            LOS3Y_MFBL.append(count_los_3y_list_MFBL[x])
            LOS3Y_MFHL.append(count_los_3y_list_MFHL[x])
            LOS3Y_MFOT.append(count_los_3y_list_MFOT[x])
            LOS3Y_OTH.append(count_los_3y_list_OTH[x])
            LOS3Y_PL.append(count_los_3y_list_PL[x])
            LOS3Y_PLBL.append(count_los_3y_list_PLBL[x])
            LOS3Y_RL.append(count_los_3y_list_RL[x])
            LOS3Y_SCC.append(count_los_3y_list_SCC[x])
            LOS3Y_SEL.append(count_los_3y_list_SEL[x])

            XXX1M_AL.append(count_xxx_1m_list_AL[x])
            XXX1M_BL.append(count_xxx_1m_list_BL[x])
            XXX1M_CC.append(count_xxx_1m_list_CC[x])
            XXX1M_CD.append(count_xxx_1m_list_CD[x])
            XXX1M_CV.append(count_xxx_1m_list_CV[x])
            XXX1M_GL.append(count_xxx_1m_list_GL[x])
            XXX1M_HL.append(count_xxx_1m_list_HL[x])
            XXX1M_LAS.append(count_xxx_1m_list_LAS[x])
            XXX1M_MFBL.append(count_xxx_1m_list_MFBL[x])
            XXX1M_MFHL.append(count_xxx_1m_list_MFHL[x])
            XXX1M_MFOT.append(count_xxx_1m_list_MFOT[x])
            XXX1M_OTH.append(count_xxx_1m_list_OTH[x])
            XXX1M_PL.append(count_xxx_1m_list_PL[x])
            XXX1M_PLBL.append(count_xxx_1m_list_PLBL[x])
            XXX1M_RL.append(count_xxx_1m_list_RL[x])
            XXX1M_SCC.append(count_xxx_1m_list_SCC[x])
            XXX1M_SEL.append(count_xxx_1m_list_SEL[x])

            XXX3M_AL.append(count_xxx_3m_list_AL[x])
            XXX3M_BL.append(count_xxx_3m_list_BL[x])
            XXX3M_CC.append(count_xxx_3m_list_CC[x])
            XXX3M_CD.append(count_xxx_3m_list_CD[x])
            XXX3M_CV.append(count_xxx_3m_list_CV[x])
            XXX3M_GL.append(count_xxx_3m_list_GL[x])
            XXX3M_HL.append(count_xxx_3m_list_HL[x])
            XXX3M_LAS.append(count_xxx_3m_list_LAS[x])
            XXX3M_MFBL.append(count_xxx_3m_list_MFBL[x])
            XXX3M_MFHL.append(count_xxx_3m_list_MFHL[x])
            XXX3M_MFOT.append(count_xxx_3m_list_MFOT[x])
            XXX3M_OTH.append(count_xxx_3m_list_OTH[x])
            XXX3M_PL.append(count_xxx_3m_list_PL[x])
            XXX3M_PLBL.append(count_xxx_3m_list_PLBL[x])
            XXX3M_RL.append(count_xxx_3m_list_RL[x])
            XXX3M_SCC.append(count_xxx_3m_list_SCC[x])
            XXX3M_SEL.append(count_xxx_3m_list_SEL[x])

            XXX6M_AL.append(count_xxx_6m_list_AL[x])
            XXX6M_BL.append(count_xxx_6m_list_BL[x])
            XXX6M_CC.append(count_xxx_6m_list_CC[x])
            XXX6M_CD.append(count_xxx_6m_list_CD[x])
            XXX6M_CV.append(count_xxx_6m_list_CV[x])
            XXX6M_GL.append(count_xxx_6m_list_GL[x])
            XXX6M_HL.append(count_xxx_6m_list_HL[x])
            XXX6M_LAS.append(count_xxx_6m_list_LAS[x])
            XXX6M_MFBL.append(count_xxx_6m_list_MFBL[x])
            XXX6M_MFHL.append(count_xxx_6m_list_MFHL[x])
            XXX6M_MFOT.append(count_xxx_6m_list_MFOT[x])
            XXX6M_OTH.append(count_xxx_6m_list_OTH[x])
            XXX6M_PL.append(count_xxx_6m_list_PL[x])
            XXX6M_PLBL.append(count_xxx_6m_list_PLBL[x])
            XXX6M_RL.append(count_xxx_6m_list_RL[x])
            XXX6M_SCC.append(count_xxx_6m_list_SCC[x])
            XXX6M_SEL.append(count_xxx_6m_list_SEL[x])

            XXX1Y_AL.append(count_xxx_1y_list_AL[x])
            XXX1Y_BL.append(count_xxx_1y_list_BL[x])
            XXX1Y_CC.append(count_xxx_1y_list_CC[x])
            XXX1Y_CD.append(count_xxx_1y_list_CD[x])
            XXX1Y_CV.append(count_xxx_1y_list_CV[x])
            XXX1Y_GL.append(count_xxx_1y_list_GL[x])
            XXX1Y_HL.append(count_xxx_1y_list_HL[x])
            XXX1Y_LAS.append(count_xxx_1y_list_LAS[x])
            XXX1Y_MFBL.append(count_xxx_1y_list_MFBL[x])
            XXX1Y_MFHL.append(count_xxx_1y_list_MFHL[x])
            XXX1Y_MFOT.append(count_xxx_1y_list_MFOT[x])
            XXX1Y_OTH.append(count_xxx_1y_list_OTH[x])
            XXX1Y_PL.append(count_xxx_1y_list_PL[x])
            XXX1Y_PLBL.append(count_xxx_1y_list_PLBL[x])
            XXX1Y_RL.append(count_xxx_1y_list_RL[x])
            XXX1Y_SCC.append(count_xxx_1y_list_SCC[x])
            XXX1Y_SEL.append(count_xxx_1y_list_SEL[x])

            XXX2Y_AL.append(count_xxx_2y_list_AL[x])
            XXX2Y_BL.append(count_xxx_2y_list_BL[x])
            XXX2Y_CC.append(count_xxx_2y_list_CC[x])
            XXX2Y_CD.append(count_xxx_2y_list_CD[x])
            XXX2Y_CV.append(count_xxx_2y_list_CV[x])
            XXX2Y_GL.append(count_xxx_2y_list_GL[x])
            XXX2Y_HL.append(count_xxx_2y_list_HL[x])
            XXX2Y_LAS.append(count_xxx_2y_list_LAS[x])
            XXX2Y_MFBL.append(count_xxx_2y_list_MFBL[x])
            XXX2Y_MFHL.append(count_xxx_2y_list_MFHL[x])
            XXX2Y_MFOT.append(count_xxx_2y_list_MFOT[x])
            XXX2Y_OTH.append(count_xxx_2y_list_OTH[x])
            XXX2Y_PL.append(count_xxx_2y_list_PL[x])
            XXX2Y_PLBL.append(count_xxx_2y_list_PLBL[x])
            XXX2Y_RL.append(count_xxx_2y_list_RL[x])
            XXX2Y_SCC.append(count_xxx_2y_list_SCC[x])
            XXX2Y_SEL.append(count_xxx_2y_list_SEL[x])

            XXX3Y_AL.append(count_xxx_3y_list_AL[x])
            XXX3Y_BL.append(count_xxx_3y_list_BL[x])
            XXX3Y_CC.append(count_xxx_3y_list_CC[x])
            XXX3Y_CD.append(count_xxx_3y_list_CD[x])
            XXX3Y_CV.append(count_xxx_3y_list_CV[x])
            XXX3Y_GL.append(count_xxx_3y_list_GL[x])
            XXX3Y_HL.append(count_xxx_3y_list_HL[x])
            XXX3Y_LAS.append(count_xxx_3y_list_LAS[x])
            XXX3Y_MFBL.append(count_xxx_3y_list_MFBL[x])
            XXX3Y_MFHL.append(count_xxx_3y_list_MFHL[x])
            XXX3Y_MFOT.append(count_xxx_3y_list_MFOT[x])
            XXX3Y_OTH.append(count_xxx_3y_list_OTH[x])
            XXX3Y_PL.append(count_xxx_3y_list_PL[x])
            XXX3Y_PLBL.append(count_xxx_3y_list_PLBL[x])
            XXX3Y_RL.append(count_xxx_3y_list_RL[x])
            XXX3Y_SCC.append(count_xxx_3y_list_SCC[x])
            XXX3Y_SEL.append(count_xxx_3y_list_SEL[x])

            SMA1M_AL.append(count_sma_1m_list_AL[x])
            SMA1M_BL.append(count_sma_1m_list_BL[x])
            SMA1M_CC.append(count_sma_1m_list_CC[x])
            SMA1M_CD.append(count_sma_1m_list_CD[x])
            SMA1M_CV.append(count_sma_1m_list_CV[x])
            SMA1M_GL.append(count_sma_1m_list_GL[x])
            SMA1M_HL.append(count_sma_1m_list_HL[x])
            SMA1M_LAS.append(count_sma_1m_list_LAS[x])
            SMA1M_MFBL.append(count_sma_1m_list_MFBL[x])
            SMA1M_MFHL.append(count_sma_1m_list_MFHL[x])
            SMA1M_MFOT.append(count_sma_1m_list_MFOT[x])
            SMA1M_OTH.append(count_sma_1m_list_OTH[x])
            SMA1M_PL.append(count_sma_1m_list_PL[x])
            SMA1M_PLBL.append(count_sma_1m_list_PLBL[x])
            SMA1M_RL.append(count_sma_1m_list_RL[x])
            SMA1M_SCC.append(count_sma_1m_list_SCC[x])
            SMA1M_SEL.append(count_sma_1m_list_SEL[x])

            SMA3M_AL.append(count_sma_3m_list_AL[x])
            SMA3M_BL.append(count_sma_3m_list_BL[x])
            SMA3M_CC.append(count_sma_3m_list_CC[x])
            SMA3M_CD.append(count_sma_3m_list_CD[x])
            SMA3M_CV.append(count_sma_3m_list_CV[x])
            SMA3M_GL.append(count_sma_3m_list_GL[x])
            SMA3M_HL.append(count_sma_3m_list_HL[x])
            SMA3M_LAS.append(count_sma_3m_list_LAS[x])
            SMA3M_MFBL.append(count_sma_3m_list_MFBL[x])
            SMA3M_MFHL.append(count_sma_3m_list_MFHL[x])
            SMA3M_MFOT.append(count_sma_3m_list_MFOT[x])
            SMA3M_OTH.append(count_sma_3m_list_OTH[x])
            SMA3M_PL.append(count_sma_3m_list_PL[x])
            SMA3M_PLBL.append(count_sma_3m_list_PLBL[x])
            SMA3M_RL.append(count_sma_3m_list_RL[x])
            SMA3M_SCC.append(count_sma_3m_list_SCC[x])
            SMA3M_SEL.append(count_sma_3m_list_SEL[x])

            SMA6M_AL.append(count_sma_6m_list_AL[x])
            SMA6M_BL.append(count_sma_6m_list_BL[x])
            SMA6M_CC.append(count_sma_6m_list_CC[x])
            SMA6M_CD.append(count_sma_6m_list_CD[x])
            SMA6M_CV.append(count_sma_6m_list_CV[x])
            SMA6M_GL.append(count_sma_6m_list_GL[x])
            SMA6M_HL.append(count_sma_6m_list_HL[x])
            SMA6M_LAS.append(count_sma_6m_list_LAS[x])
            SMA6M_MFBL.append(count_sma_6m_list_MFBL[x])
            SMA6M_MFHL.append(count_sma_6m_list_MFHL[x])
            SMA6M_MFOT.append(count_sma_6m_list_MFOT[x])
            SMA6M_OTH.append(count_sma_6m_list_OTH[x])
            SMA6M_PL.append(count_sma_6m_list_PL[x])
            SMA6M_PLBL.append(count_sma_6m_list_PLBL[x])
            SMA6M_RL.append(count_sma_6m_list_RL[x])
            SMA6M_SCC.append(count_sma_6m_list_SCC[x])
            SMA6M_SEL.append(count_sma_6m_list_SEL[x])

            SMA1Y_AL.append(count_sma_1y_list_AL[x])
            SMA1Y_BL.append(count_sma_1y_list_BL[x])
            SMA1Y_CC.append(count_sma_1y_list_CC[x])
            SMA1Y_CD.append(count_sma_1y_list_CD[x])
            SMA1Y_CV.append(count_sma_1y_list_CV[x])
            SMA1Y_GL.append(count_sma_1y_list_GL[x])
            SMA1Y_HL.append(count_sma_1y_list_HL[x])
            SMA1Y_LAS.append(count_sma_1y_list_LAS[x])
            SMA1Y_MFBL.append(count_sma_1y_list_MFBL[x])
            SMA1Y_MFHL.append(count_sma_1y_list_MFHL[x])
            SMA1Y_MFOT.append(count_sma_1y_list_MFOT[x])
            SMA1Y_OTH.append(count_sma_1y_list_OTH[x])
            SMA1Y_PL.append(count_sma_1y_list_PL[x])
            SMA1Y_PLBL.append(count_sma_1y_list_PLBL[x])
            SMA1Y_RL.append(count_sma_1y_list_RL[x])
            SMA1Y_SCC.append(count_sma_1y_list_SCC[x])
            SMA1Y_SEL.append(count_sma_1y_list_SEL[x])

            SMA2Y_AL.append(count_sma_2y_list_AL[x])
            SMA2Y_BL.append(count_sma_2y_list_BL[x])
            SMA2Y_CC.append(count_sma_2y_list_CC[x])
            SMA2Y_CD.append(count_sma_2y_list_CD[x])
            SMA2Y_CV.append(count_sma_2y_list_CV[x])
            SMA2Y_GL.append(count_sma_2y_list_GL[x])
            SMA2Y_HL.append(count_sma_2y_list_HL[x])
            SMA2Y_LAS.append(count_sma_2y_list_LAS[x])
            SMA2Y_MFBL.append(count_sma_2y_list_MFBL[x])
            SMA2Y_MFHL.append(count_sma_2y_list_MFHL[x])
            SMA2Y_MFOT.append(count_sma_2y_list_MFOT[x])
            SMA2Y_OTH.append(count_sma_2y_list_OTH[x])
            SMA2Y_PL.append(count_sma_2y_list_PL[x])
            SMA2Y_PLBL.append(count_sma_2y_list_PLBL[x])
            SMA2Y_RL.append(count_sma_2y_list_RL[x])
            SMA2Y_SCC.append(count_sma_2y_list_SCC[x])
            SMA2Y_SEL.append(count_sma_2y_list_SEL[x])

            SMA3Y_AL.append(count_sma_3y_list_AL[x])
            SMA3Y_BL.append(count_sma_3y_list_BL[x])
            SMA3Y_CC.append(count_sma_3y_list_CC[x])
            SMA3Y_CD.append(count_sma_3y_list_CD[x])
            SMA3Y_CV.append(count_sma_3y_list_CV[x])
            SMA3Y_GL.append(count_sma_3y_list_GL[x])
            SMA3Y_HL.append(count_sma_3y_list_HL[x])
            SMA3Y_LAS.append(count_sma_3y_list_LAS[x])
            SMA3Y_MFBL.append(count_sma_3y_list_MFBL[x])
            SMA3Y_MFHL.append(count_sma_3y_list_MFHL[x])
            SMA3Y_MFOT.append(count_sma_3y_list_MFOT[x])
            SMA3Y_OTH.append(count_sma_3y_list_OTH[x])
            SMA3Y_PL.append(count_sma_3y_list_PL[x])
            SMA3Y_PLBL.append(count_sma_3y_list_PLBL[x])
            SMA3Y_RL.append(count_sma_3y_list_RL[x])
            SMA3Y_SCC.append(count_sma_3y_list_SCC[x])
            SMA3Y_SEL.append(count_sma_3y_list_SEL[x])

df['DPD30P3M'] = pd.Series(DPD30P3M).values
df['DPD60P3M'] = pd.Series(DPD60P3M).values
df['DPD90P3M'] = pd.Series(DPD90P3M).values

df['DPD30P3M_AL'] = pd.Series(DPD30P3M_AL).values
df['DPD30P3M_BL'] = pd.Series(DPD30P3M_BL).values
df['DPD30P3M_CC'] = pd.Series(DPD30P3M_CC).values
df['DPD30P3M_CD'] = pd.Series(DPD30P3M_CD).values
df['DPD30P3M_CV'] = pd.Series(DPD30P3M_CV).values
df['DPD30P3M_GL'] = pd.Series(DPD30P3M_GL).values
df['DPD30P3M_HL'] = pd.Series(DPD30P3M_HL).values
df['DPD30P3M_LAS'] = pd.Series(DPD30P3M_LAS).values
df['DPD30P3M_MFBL'] = pd.Series(DPD30P3M_MFBL).values
df['DPD30P3M_MFHL'] = pd.Series(DPD30P3M_MFHL).values
df['DPD30P3M_MFOT'] = pd.Series(DPD30P3M_MFOT).values
df['DPD30P3M_OTH'] = pd.Series(DPD30P3M_OTH).values
df['DPD30P3M_PL'] = pd.Series(DPD30P3M_PL).values
df['DPD30P3M_PLBL'] = pd.Series(DPD30P3M_PLBL).values
df['DPD30P3M_RL'] = pd.Series(DPD30P3M_RL).values
df['DPD30P3M_SCC'] = pd.Series(DPD30P3M_SCC).values
df['DPD30P3M_SEL'] = pd.Series(DPD30P3M_SEL).values

df['DPD60P3M_AL'] = pd.Series(DPD60P3M_AL).values
df['DPD60P3M_BL'] = pd.Series(DPD60P3M_BL).values
df['DPD60P3M_CC'] = pd.Series(DPD60P3M_CC).values
df['DPD60P3M_CD'] = pd.Series(DPD60P3M_CD).values
df['DPD60P3M_CV'] = pd.Series(DPD60P3M_CV).values
df['DPD60P3M_GL'] = pd.Series(DPD60P3M_GL).values
df['DPD60P3M_HL'] = pd.Series(DPD60P3M_HL).values
df['DPD60P3M_LAS'] = pd.Series(DPD60P3M_LAS).values
df['DPD60P3M_MFBL'] = pd.Series(DPD60P3M_MFBL).values
df['DPD60P3M_MFHL'] = pd.Series(DPD60P3M_MFHL).values
df['DPD60P3M_MFOT'] = pd.Series(DPD60P3M_MFOT).values
df['DPD60P3M_OTH'] = pd.Series(DPD60P3M_OTH).values
df['DPD60P3M_PL'] = pd.Series(DPD60P3M_PL).values
df['DPD60P3M_PLBL'] = pd.Series(DPD60P3M_PLBL).values
df['DPD60P3M_RL'] = pd.Series(DPD60P3M_RL).values
df['DPD60P3M_SCC'] = pd.Series(DPD60P3M_SCC).values
df['DPD60P3M_SEL'] = pd.Series(DPD60P3M_SEL).values

df['DPD90P3M_AL'] = pd.Series(DPD90P3M_AL).values
df['DPD90P3M_BL'] = pd.Series(DPD90P3M_BL).values
df['DPD90P3M_CC'] = pd.Series(DPD90P3M_CC).values
df['DPD90P3M_CD'] = pd.Series(DPD90P3M_CD).values
df['DPD90P3M_CV'] = pd.Series(DPD90P3M_CV).values
df['DPD90P3M_GL'] = pd.Series(DPD90P3M_GL).values
df['DPD90P3M_HL'] = pd.Series(DPD90P3M_HL).values
df['DPD90P3M_LAS'] = pd.Series(DPD90P3M_LAS).values
df['DPD90P3M_MFBL'] = pd.Series(DPD90P3M_MFBL).values
df['DPD90P3M_MFHL'] = pd.Series(DPD90P3M_MFHL).values
df['DPD90P3M_MFOT'] = pd.Series(DPD90P3M_MFOT).values
df['DPD90P3M_OTH'] = pd.Series(DPD90P3M_OTH).values
df['DPD90P3M_PL'] = pd.Series(DPD90P3M_PL).values
df['DPD90P3M_PLBL'] = pd.Series(DPD90P3M_PLBL).values
df['DPD90P3M_RL'] = pd.Series(DPD90P3M_RL).values
df['DPD90P3M_SCC'] = pd.Series(DPD90P3M_SCC).values
df['DPD90P3M_SEL'] = pd.Series(DPD90P3M_SEL).values

df['DPD30P6M'] = pd.Series(DPD30P6M).values
df['DPD60P6M'] = pd.Series(DPD60P6M).values
df['DPD90P6M'] = pd.Series(DPD90P6M).values

df['DPD30P6M_AL'] = pd.Series(DPD30P6M_AL).values
df['DPD30P6M_BL'] = pd.Series(DPD30P6M_BL).values
df['DPD30P6M_CC'] = pd.Series(DPD30P6M_CC).values
df['DPD30P6M_CD'] = pd.Series(DPD30P6M_CD).values
df['DPD30P6M_CV'] = pd.Series(DPD30P6M_CV).values
df['DPD30P6M_GL'] = pd.Series(DPD30P6M_GL).values
df['DPD30P6M_HL'] = pd.Series(DPD30P6M_HL).values
df['DPD30P6M_LAS'] = pd.Series(DPD30P6M_LAS).values
df['DPD30P6M_MFBL'] = pd.Series(DPD30P6M_MFBL).values
df['DPD30P6M_MFHL'] = pd.Series(DPD30P6M_MFHL).values
df['DPD30P6M_MFOT'] = pd.Series(DPD30P6M_MFOT).values
df['DPD30P6M_OTH'] = pd.Series(DPD30P6M_OTH).values
df['DPD30P6M_PL'] = pd.Series(DPD30P6M_PL).values
df['DPD30P6M_PLBL'] = pd.Series(DPD30P6M_PLBL).values
df['DPD30P6M_RL'] = pd.Series(DPD30P6M_RL).values
df['DPD30P6M_SCC'] = pd.Series(DPD30P6M_SCC).values
df['DPD30P6M_SEL'] = pd.Series(DPD30P6M_SEL).values

df['DPD60P6M_AL'] = pd.Series(DPD60P6M_AL).values
df['DPD60P6M_BL'] = pd.Series(DPD60P6M_BL).values
df['DPD60P6M_CC'] = pd.Series(DPD60P6M_CC).values
df['DPD60P6M_CD'] = pd.Series(DPD60P6M_CD).values
df['DPD60P6M_CV'] = pd.Series(DPD60P6M_CV).values
df['DPD60P6M_GL'] = pd.Series(DPD60P6M_GL).values
df['DPD60P6M_HL'] = pd.Series(DPD60P6M_HL).values
df['DPD60P6M_LAS'] = pd.Series(DPD60P6M_LAS).values
df['DPD60P6M_MFBL'] = pd.Series(DPD60P6M_MFBL).values
df['DPD60P6M_MFHL'] = pd.Series(DPD60P6M_MFHL).values
df['DPD60P6M_MFOT'] = pd.Series(DPD60P6M_MFOT).values
df['DPD60P6M_OTH'] = pd.Series(DPD60P6M_OTH).values
df['DPD60P6M_PL'] = pd.Series(DPD60P6M_PL).values
df['DPD60P6M_PLBL'] = pd.Series(DPD60P6M_PLBL).values
df['DPD60P6M_RL'] = pd.Series(DPD60P6M_RL).values
df['DPD60P6M_SCC'] = pd.Series(DPD60P6M_SCC).values
df['DPD60P6M_SEL'] = pd.Series(DPD60P6M_SEL).values

df['DPD90P6M_AL'] = pd.Series(DPD90P6M_AL).values
df['DPD90P6M_BL'] = pd.Series(DPD90P6M_BL).values
df['DPD90P6M_CC'] = pd.Series(DPD90P6M_CC).values
df['DPD90P6M_CD'] = pd.Series(DPD90P6M_CD).values
df['DPD90P6M_CV'] = pd.Series(DPD90P6M_CV).values
df['DPD90P6M_GL'] = pd.Series(DPD90P6M_GL).values
df['DPD90P6M_HL'] = pd.Series(DPD90P6M_HL).values
df['DPD90P6M_LAS'] = pd.Series(DPD90P6M_LAS).values
df['DPD90P6M_MFBL'] = pd.Series(DPD90P6M_MFBL).values
df['DPD90P6M_MFHL'] = pd.Series(DPD90P6M_MFHL).values
df['DPD90P6M_MFOT'] = pd.Series(DPD90P6M_MFOT).values
df['DPD90P6M_OTH'] = pd.Series(DPD90P6M_OTH).values
df['DPD90P6M_PL'] = pd.Series(DPD90P6M_PL).values
df['DPD90P6M_PLBL'] = pd.Series(DPD90P6M_PLBL).values
df['DPD90P6M_RL'] = pd.Series(DPD90P6M_RL).values
df['DPD90P6M_SCC'] = pd.Series(DPD90P6M_SCC).values
df['DPD90P6M_SEL'] = pd.Series(DPD90P6M_SEL).values

df['DPD30P1Y'] = pd.Series(DPD30P1Y).values
df['DPD60P1Y'] = pd.Series(DPD60P1Y).values
df['DPD90P1Y'] = pd.Series(DPD90P1Y).values

df['DPD30P1Y_AL'] = pd.Series(DPD30P1Y_AL).values
df['DPD30P1Y_BL'] = pd.Series(DPD30P1Y_BL).values
df['DPD30P1Y_CC'] = pd.Series(DPD30P1Y_CC).values
df['DPD30P1Y_CD'] = pd.Series(DPD30P1Y_CD).values
df['DPD30P1Y_CV'] = pd.Series(DPD30P1Y_CV).values
df['DPD30P1Y_GL'] = pd.Series(DPD30P1Y_GL).values
df['DPD30P1Y_HL'] = pd.Series(DPD30P1Y_HL).values
df['DPD30P1Y_LAS'] = pd.Series(DPD30P1Y_LAS).values
df['DPD30P1Y_MFBL'] = pd.Series(DPD30P1Y_MFBL).values
df['DPD30P1Y_MFHL'] = pd.Series(DPD30P1Y_MFHL).values
df['DPD30P1Y_MFOT'] = pd.Series(DPD30P1Y_MFOT).values
df['DPD30P1Y_OTH'] = pd.Series(DPD30P1Y_OTH).values
df['DPD30P1Y_PL'] = pd.Series(DPD30P1Y_PL).values
df['DPD30P1Y_PLBL'] = pd.Series(DPD30P1Y_PLBL).values
df['DPD30P1Y_RL'] = pd.Series(DPD30P1Y_RL).values
df['DPD30P1Y_SCC'] = pd.Series(DPD30P1Y_SCC).values
df['DPD30P1Y_SEL'] = pd.Series(DPD30P1Y_SEL).values

df['DPD60P1Y_AL'] = pd.Series(DPD60P1Y_AL).values
df['DPD60P1Y_BL'] = pd.Series(DPD60P1Y_BL).values
df['DPD60P1Y_CC'] = pd.Series(DPD60P1Y_CC).values
df['DPD60P1Y_CD'] = pd.Series(DPD60P1Y_CD).values
df['DPD60P1Y_CV'] = pd.Series(DPD60P1Y_CV).values
df['DPD60P1Y_GL'] = pd.Series(DPD60P1Y_GL).values
df['DPD60P1Y_HL'] = pd.Series(DPD60P1Y_HL).values
df['DPD60P1Y_LAS'] = pd.Series(DPD60P1Y_LAS).values
df['DPD60P1Y_MFBL'] = pd.Series(DPD60P1Y_MFBL).values
df['DPD60P1Y_MFHL'] = pd.Series(DPD60P1Y_MFHL).values
df['DPD60P1Y_MFOT'] = pd.Series(DPD60P1Y_MFOT).values
df['DPD60P1Y_OTH'] = pd.Series(DPD60P1Y_OTH).values
df['DPD60P1Y_PL'] = pd.Series(DPD60P1Y_PL).values
df['DPD60P1Y_PLBL'] = pd.Series(DPD60P1Y_PLBL).values
df['DPD60P1Y_RL'] = pd.Series(DPD60P1Y_RL).values
df['DPD60P1Y_SCC'] = pd.Series(DPD60P1Y_SCC).values
df['DPD60P1Y_SEL'] = pd.Series(DPD60P1Y_SEL).values

df['DPD90P1Y_AL'] = pd.Series(DPD90P1Y_AL).values
df['DPD90P1Y_BL'] = pd.Series(DPD90P1Y_BL).values
df['DPD90P1Y_CC'] = pd.Series(DPD90P1Y_CC).values
df['DPD90P1Y_CD'] = pd.Series(DPD90P1Y_CD).values
df['DPD90P1Y_CV'] = pd.Series(DPD90P1Y_CV).values
df['DPD90P1Y_GL'] = pd.Series(DPD90P1Y_GL).values
df['DPD90P1Y_HL'] = pd.Series(DPD90P1Y_HL).values
df['DPD90P1Y_LAS'] = pd.Series(DPD90P1Y_LAS).values
df['DPD90P1Y_MFBL'] = pd.Series(DPD90P1Y_MFBL).values
df['DPD90P1Y_MFHL'] = pd.Series(DPD90P1Y_MFHL).values
df['DPD90P1Y_MFOT'] = pd.Series(DPD90P1Y_MFOT).values
df['DPD90P1Y_OTH'] = pd.Series(DPD90P1Y_OTH).values
df['DPD90P1Y_PL'] = pd.Series(DPD90P1Y_PL).values
df['DPD90P1Y_PLBL'] = pd.Series(DPD90P1Y_PLBL).values
df['DPD90P1Y_RL'] = pd.Series(DPD90P1Y_RL).values
df['DPD90P1Y_SCC'] = pd.Series(DPD90P1Y_SCC).values
df['DPD90P1Y_SEL'] = pd.Series(DPD90P1Y_SEL).values

df['DPD30P2Y'] = pd.Series(DPD30P2Y).values
df['DPD60P2Y'] = pd.Series(DPD60P2Y).values
df['DPD90P2Y'] = pd.Series(DPD90P2Y).values

df['DPD30P2Y_AL'] = pd.Series(DPD30P2Y_AL).values
df['DPD30P2Y_BL'] = pd.Series(DPD30P2Y_BL).values
df['DPD30P2Y_CC'] = pd.Series(DPD30P2Y_CC).values
df['DPD30P2Y_CD'] = pd.Series(DPD30P2Y_CD).values
df['DPD30P2Y_CV'] = pd.Series(DPD30P2Y_CV).values
df['DPD30P2Y_GL'] = pd.Series(DPD30P2Y_GL).values
df['DPD30P2Y_HL'] = pd.Series(DPD30P2Y_HL).values
df['DPD30P2Y_LAS'] = pd.Series(DPD30P2Y_LAS).values
df['DPD30P2Y_MFBL'] = pd.Series(DPD30P2Y_MFBL).values
df['DPD30P2Y_MFHL'] = pd.Series(DPD30P2Y_MFHL).values
df['DPD30P2Y_MFOT'] = pd.Series(DPD30P2Y_MFOT).values
df['DPD30P2Y_OTH'] = pd.Series(DPD30P2Y_OTH).values
df['DPD30P2Y_PL'] = pd.Series(DPD30P2Y_PL).values
df['DPD30P2Y_PLBL'] = pd.Series(DPD30P2Y_PLBL).values
df['DPD30P2Y_RL'] = pd.Series(DPD30P2Y_RL).values
df['DPD30P2Y_SCC'] = pd.Series(DPD30P2Y_SCC).values
df['DPD30P2Y_SEL'] = pd.Series(DPD30P2Y_SEL).values

df['DPD60P2Y_AL'] = pd.Series(DPD60P2Y_AL).values
df['DPD60P2Y_BL'] = pd.Series(DPD60P2Y_BL).values
df['DPD60P2Y_CC'] = pd.Series(DPD60P2Y_CC).values
df['DPD60P2Y_CD'] = pd.Series(DPD60P2Y_CD).values
df['DPD60P2Y_CV'] = pd.Series(DPD60P2Y_CV).values
df['DPD60P2Y_GL'] = pd.Series(DPD60P2Y_GL).values
df['DPD60P2Y_HL'] = pd.Series(DPD60P2Y_HL).values
df['DPD60P2Y_LAS'] = pd.Series(DPD60P2Y_LAS).values
df['DPD60P2Y_MFBL'] = pd.Series(DPD60P2Y_MFBL).values
df['DPD60P2Y_MFHL'] = pd.Series(DPD60P2Y_MFHL).values
df['DPD60P2Y_MFOT'] = pd.Series(DPD60P2Y_MFOT).values
df['DPD60P2Y_OTH'] = pd.Series(DPD60P2Y_OTH).values
df['DPD60P2Y_PL'] = pd.Series(DPD60P2Y_PL).values
df['DPD60P2Y_PLBL'] = pd.Series(DPD60P2Y_PLBL).values
df['DPD60P2Y_RL'] = pd.Series(DPD60P2Y_RL).values
df['DPD60P2Y_SCC'] = pd.Series(DPD60P2Y_SCC).values
df['DPD60P2Y_SEL'] = pd.Series(DPD60P2Y_SEL).values

df['DPD90P2Y_AL'] = pd.Series(DPD90P2Y_AL).values
df['DPD90P2Y_BL'] = pd.Series(DPD90P2Y_BL).values
df['DPD90P2Y_CC'] = pd.Series(DPD90P2Y_CC).values
df['DPD90P2Y_CD'] = pd.Series(DPD90P2Y_CD).values
df['DPD90P2Y_CV'] = pd.Series(DPD90P2Y_CV).values
df['DPD90P2Y_GL'] = pd.Series(DPD90P2Y_GL).values
df['DPD90P2Y_HL'] = pd.Series(DPD90P2Y_HL).values
df['DPD90P2Y_LAS'] = pd.Series(DPD90P2Y_LAS).values
df['DPD90P2Y_MFBL'] = pd.Series(DPD90P2Y_MFBL).values
df['DPD90P2Y_MFHL'] = pd.Series(DPD90P2Y_MFHL).values
df['DPD90P2Y_MFOT'] = pd.Series(DPD90P2Y_MFOT).values
df['DPD90P2Y_OTH'] = pd.Series(DPD90P2Y_OTH).values
df['DPD90P2Y_PL'] = pd.Series(DPD90P2Y_PL).values
df['DPD90P2Y_PLBL'] = pd.Series(DPD90P2Y_PLBL).values
df['DPD90P2Y_RL'] = pd.Series(DPD90P2Y_RL).values
df['DPD90P2Y_SCC'] = pd.Series(DPD90P2Y_SCC).values
df['DPD90P2Y_SEL'] = pd.Series(DPD90P2Y_SEL).values

df['DPD30P3Y'] = pd.Series(DPD30P3Y).values
df['DPD60P3Y'] = pd.Series(DPD60P3Y).values
df['DPD90P3Y'] = pd.Series(DPD90P3Y).values

df['DPD30P3Y_AL'] = pd.Series(DPD30P3Y_AL).values
df['DPD30P3Y_BL'] = pd.Series(DPD30P3Y_BL).values
df['DPD30P3Y_CC'] = pd.Series(DPD30P3Y_CC).values
df['DPD30P3Y_CD'] = pd.Series(DPD30P3Y_CD).values
df['DPD30P3Y_CV'] = pd.Series(DPD30P3Y_CV).values
df['DPD30P3Y_GL'] = pd.Series(DPD30P3Y_GL).values
df['DPD30P3Y_HL'] = pd.Series(DPD30P3Y_HL).values
df['DPD30P3Y_LAS'] = pd.Series(DPD30P3Y_LAS).values
df['DPD30P3Y_MFBL'] = pd.Series(DPD30P3Y_MFBL).values
df['DPD30P3Y_MFHL'] = pd.Series(DPD30P3Y_MFHL).values
df['DPD30P3Y_MFOT'] = pd.Series(DPD30P3Y_MFOT).values
df['DPD30P3Y_OTH'] = pd.Series(DPD30P3Y_OTH).values
df['DPD30P3Y_PL'] = pd.Series(DPD30P3Y_PL).values
df['DPD30P3Y_PLBL'] = pd.Series(DPD30P3Y_PLBL).values
df['DPD30P3Y_RL'] = pd.Series(DPD30P3Y_RL).values
df['DPD30P3Y_SCC'] = pd.Series(DPD30P3Y_SCC).values
df['DPD30P3Y_SEL'] = pd.Series(DPD30P3Y_SEL).values

df['DPD60P3Y_AL'] = pd.Series(DPD60P3Y_AL).values
df['DPD60P3Y_BL'] = pd.Series(DPD60P3Y_BL).values
df['DPD60P3Y_CC'] = pd.Series(DPD60P3Y_CC).values
df['DPD60P3Y_CD'] = pd.Series(DPD60P3Y_CD).values
df['DPD60P3Y_CV'] = pd.Series(DPD60P3Y_CV).values
df['DPD60P3Y_GL'] = pd.Series(DPD60P3Y_GL).values
df['DPD60P3Y_HL'] = pd.Series(DPD60P3Y_HL).values
df['DPD60P3Y_LAS'] = pd.Series(DPD60P3Y_LAS).values
df['DPD60P3Y_MFBL'] = pd.Series(DPD60P3Y_MFBL).values
df['DPD60P3Y_MFHL'] = pd.Series(DPD60P3Y_MFHL).values
df['DPD60P3Y_MFOT'] = pd.Series(DPD60P3Y_MFOT).values
df['DPD60P3Y_OTH'] = pd.Series(DPD60P3Y_OTH).values
df['DPD60P3Y_PL'] = pd.Series(DPD60P3Y_PL).values
df['DPD60P3Y_PLBL'] = pd.Series(DPD60P3Y_PLBL).values
df['DPD60P3Y_RL'] = pd.Series(DPD60P3Y_RL).values
df['DPD60P3Y_SCC'] = pd.Series(DPD60P3Y_SCC).values
df['DPD60P3Y_SEL'] = pd.Series(DPD60P3Y_SEL).values

df['DPD90P3Y_AL'] = pd.Series(DPD90P3Y_AL).values
df['DPD90P3Y_BL'] = pd.Series(DPD90P3Y_BL).values
df['DPD90P3Y_CC'] = pd.Series(DPD90P3Y_CC).values
df['DPD90P3Y_CD'] = pd.Series(DPD90P3Y_CD).values
df['DPD90P3Y_CV'] = pd.Series(DPD90P3Y_CV).values
df['DPD90P3Y_GL'] = pd.Series(DPD90P3Y_GL).values
df['DPD90P3Y_HL'] = pd.Series(DPD90P3Y_HL).values
df['DPD90P3Y_LAS'] = pd.Series(DPD90P3Y_LAS).values
df['DPD90P3Y_MFBL'] = pd.Series(DPD90P3Y_MFBL).values
df['DPD90P3Y_MFHL'] = pd.Series(DPD90P3Y_MFHL).values
df['DPD90P3Y_MFOT'] = pd.Series(DPD90P3Y_MFOT).values
df['DPD90P3Y_OTH'] = pd.Series(DPD90P3Y_OTH).values
df['DPD90P3Y_PL'] = pd.Series(DPD90P3Y_PL).values
df['DPD90P3Y_PLBL'] = pd.Series(DPD90P3Y_PLBL).values
df['DPD90P3Y_RL'] = pd.Series(DPD90P3Y_RL).values
df['DPD90P3Y_SCC'] = pd.Series(DPD90P3Y_SCC).values
df['DPD90P3Y_SEL'] = pd.Series(DPD90P3Y_SEL).values

df['STD1M'] = pd.Series(STD1M).values
df['STD3M'] = pd.Series(STD3M).values
df['STD6M'] = pd.Series(STD6M).values
df['STD1Y'] = pd.Series(STD1Y).values
df['STD2Y'] = pd.Series(STD2Y).values
df['STD3Y'] = pd.Series(STD3Y).values

df['STD1M_AL'] = pd.Series(STD1M_AL).values
df['STD1M_BL'] = pd.Series(STD1M_BL).values
df['STD1M_CC'] = pd.Series(STD1M_CC).values
df['STD1M_CD'] = pd.Series(STD1M_CD).values
df['STD1M_CV'] = pd.Series(STD1M_CV).values
df['STD1M_GL'] = pd.Series(STD1M_GL).values
df['STD1M_HL'] = pd.Series(STD1M_HL).values
df['STD1M_LAS'] = pd.Series(STD1M_LAS).values
df['STD1M_MFBL'] = pd.Series(STD1M_MFBL).values
df['STD1M_MFHL'] = pd.Series(STD1M_MFHL).values
df['STD1M_MFOT'] = pd.Series(STD1M_MFOT).values
df['STD1M_OTH'] = pd.Series(STD1M_OTH).values
df['STD1M_PL'] = pd.Series(STD1M_PL).values
df['STD1M_PLBL'] = pd.Series(STD1M_PLBL).values
df['STD1M_RL'] = pd.Series(STD1M_RL).values
df['STD1M_SCC'] = pd.Series(STD1M_SCC).values
df['STD1M_SEL'] = pd.Series(STD1M_SEL).values

df['STD3M_AL'] = pd.Series(STD3M_AL).values
df['STD3M_BL'] = pd.Series(STD3M_BL).values
df['STD3M_CC'] = pd.Series(STD3M_CC).values
df['STD3M_CD'] = pd.Series(STD3M_CD).values
df['STD3M_CV'] = pd.Series(STD3M_CV).values
df['STD3M_GL'] = pd.Series(STD3M_GL).values
df['STD3M_HL'] = pd.Series(STD3M_HL).values
df['STD3M_LAS'] = pd.Series(STD3M_LAS).values
df['STD3M_MFBL'] = pd.Series(STD3M_MFBL).values
df['STD3M_MFHL'] = pd.Series(STD3M_MFHL).values
df['STD3M_MFOT'] = pd.Series(STD3M_MFOT).values
df['STD3M_OTH'] = pd.Series(STD3M_OTH).values
df['STD3M_PL'] = pd.Series(STD3M_PL).values
df['STD3M_PLBL'] = pd.Series(STD3M_PLBL).values
df['STD3M_RL'] = pd.Series(STD3M_RL).values
df['STD3M_SCC'] = pd.Series(STD3M_SCC).values
df['STD3M_SEL'] = pd.Series(STD3M_SEL).values

df['STD6M_AL'] = pd.Series(STD6M_AL).values
df['STD6M_BL'] = pd.Series(STD6M_BL).values
df['STD6M_CC'] = pd.Series(STD6M_CC).values
df['STD6M_CD'] = pd.Series(STD6M_CD).values
df['STD6M_CV'] = pd.Series(STD6M_CV).values
df['STD6M_GL'] = pd.Series(STD6M_GL).values
df['STD6M_HL'] = pd.Series(STD6M_HL).values
df['STD6M_LAS'] = pd.Series(STD6M_LAS).values
df['STD6M_MFBL'] = pd.Series(STD6M_MFBL).values
df['STD6M_MFHL'] = pd.Series(STD6M_MFHL).values
df['STD6M_MFOT'] = pd.Series(STD6M_MFOT).values
df['STD6M_OTH'] = pd.Series(STD6M_OTH).values
df['STD6M_PL'] = pd.Series(STD6M_PL).values
df['STD6M_PLBL'] = pd.Series(STD6M_PLBL).values
df['STD6M_RL'] = pd.Series(STD6M_RL).values
df['STD6M_SCC'] = pd.Series(STD6M_SCC).values
df['STD6M_SEL'] = pd.Series(STD6M_SEL).values

df['STD1Y_AL'] = pd.Series(STD1Y_AL).values
df['STD1Y_BL'] = pd.Series(STD1Y_BL).values
df['STD1Y_CC'] = pd.Series(STD1Y_CC).values
df['STD1Y_CD'] = pd.Series(STD1Y_CD).values
df['STD1Y_CV'] = pd.Series(STD1Y_CV).values
df['STD1Y_GL'] = pd.Series(STD1Y_GL).values
df['STD1Y_HL'] = pd.Series(STD1Y_HL).values
df['STD1Y_LAS'] = pd.Series(STD1Y_LAS).values
df['STD1Y_MFBL'] = pd.Series(STD1Y_MFBL).values
df['STD1Y_MFHL'] = pd.Series(STD1Y_MFHL).values
df['STD1Y_MFOT'] = pd.Series(STD1Y_MFOT).values
df['STD1Y_OTH'] = pd.Series(STD1Y_OTH).values
df['STD1Y_PL'] = pd.Series(STD1Y_PL).values
df['STD1Y_PLBL'] = pd.Series(STD1Y_PLBL).values
df['STD1Y_RL'] = pd.Series(STD1Y_RL).values
df['STD1Y_SCC'] = pd.Series(STD1Y_SCC).values
df['STD1Y_SEL'] = pd.Series(STD1Y_SEL).values

df['STD2Y_AL'] = pd.Series(STD2Y_AL).values
df['STD2Y_BL'] = pd.Series(STD2Y_BL).values
df['STD2Y_CC'] = pd.Series(STD2Y_CC).values
df['STD2Y_CD'] = pd.Series(STD2Y_CD).values
df['STD2Y_CV'] = pd.Series(STD2Y_CV).values
df['STD2Y_GL'] = pd.Series(STD2Y_GL).values
df['STD2Y_HL'] = pd.Series(STD2Y_HL).values
df['STD2Y_LAS'] = pd.Series(STD2Y_LAS).values
df['STD2Y_MFBL'] = pd.Series(STD2Y_MFBL).values
df['STD2Y_MFHL'] = pd.Series(STD2Y_MFHL).values
df['STD2Y_MFOT'] = pd.Series(STD2Y_MFOT).values
df['STD2Y_OTH'] = pd.Series(STD2Y_OTH).values
df['STD2Y_PL'] = pd.Series(STD2Y_PL).values
df['STD2Y_PLBL'] = pd.Series(STD2Y_PLBL).values
df['STD2Y_RL'] = pd.Series(STD2Y_RL).values
df['STD2Y_SCC'] = pd.Series(STD2Y_SCC).values
df['STD2Y_SEL'] = pd.Series(STD2Y_SEL).values

df['STD3Y_AL'] = pd.Series(STD3Y_AL).values
df['STD3Y_BL'] = pd.Series(STD3Y_BL).values
df['STD3Y_CC'] = pd.Series(STD3Y_CC).values
df['STD3Y_CD'] = pd.Series(STD3Y_CD).values
df['STD3Y_CV'] = pd.Series(STD3Y_CV).values
df['STD3Y_GL'] = pd.Series(STD3Y_GL).values
df['STD3Y_HL'] = pd.Series(STD3Y_HL).values
df['STD3Y_LAS'] = pd.Series(STD3Y_LAS).values
df['STD3Y_MFBL'] = pd.Series(STD3Y_MFBL).values
df['STD3Y_MFHL'] = pd.Series(STD3Y_MFHL).values
df['STD3Y_MFOT'] = pd.Series(STD3Y_MFOT).values
df['STD3Y_OTH'] = pd.Series(STD3Y_OTH).values
df['STD3Y_PL'] = pd.Series(STD3Y_PL).values
df['STD3Y_PLBL'] = pd.Series(STD3Y_PLBL).values
df['STD3Y_RL'] = pd.Series(STD3Y_RL).values
df['STD3Y_SCC'] = pd.Series(STD3Y_SCC).values
df['STD3Y_SEL'] = pd.Series(STD3Y_SEL).values

df['SUB1M'] = pd.Series(SUB1M).values
df['SUB3M'] = pd.Series(SUB3M).values
df['SUB6M'] = pd.Series(SUB6M).values
df['SUB1Y'] = pd.Series(SUB1Y).values
df['SUB2Y'] = pd.Series(SUB2Y).values
df['SUB3Y'] = pd.Series(SUB3Y).values

df['SUB1M_AL'] = pd.Series(SUB1M_AL).values
df['SUB1M_BL'] = pd.Series(SUB1M_BL).values
df['SUB1M_CC'] = pd.Series(SUB1M_CC).values
df['SUB1M_CD'] = pd.Series(SUB1M_CD).values
df['SUB1M_CV'] = pd.Series(SUB1M_CV).values
df['SUB1M_GL'] = pd.Series(SUB1M_GL).values
df['SUB1M_HL'] = pd.Series(SUB1M_HL).values
df['SUB1M_LAS'] = pd.Series(SUB1M_LAS).values
df['SUB1M_MFBL'] = pd.Series(SUB1M_MFBL).values
df['SUB1M_MFHL'] = pd.Series(SUB1M_MFHL).values
df['SUB1M_MFOT'] = pd.Series(SUB1M_MFOT).values
df['SUB1M_OTH'] = pd.Series(SUB1M_OTH).values
df['SUB1M_PL'] = pd.Series(SUB1M_PL).values
df['SUB1M_PLBL'] = pd.Series(SUB1M_PLBL).values
df['SUB1M_RL'] = pd.Series(SUB1M_RL).values
df['SUB1M_SCC'] = pd.Series(SUB1M_SCC).values
df['SUB1M_SEL'] = pd.Series(SUB1M_SEL).values

df['SUB3M_AL'] = pd.Series(SUB3M_AL).values
df['SUB3M_BL'] = pd.Series(SUB3M_BL).values
df['SUB3M_CC'] = pd.Series(SUB3M_CC).values
df['SUB3M_CD'] = pd.Series(SUB3M_CD).values
df['SUB3M_CV'] = pd.Series(SUB3M_CV).values
df['SUB3M_GL'] = pd.Series(SUB3M_GL).values
df['SUB3M_HL'] = pd.Series(SUB3M_HL).values
df['SUB3M_LAS'] = pd.Series(SUB3M_LAS).values
df['SUB3M_MFBL'] = pd.Series(SUB3M_MFBL).values
df['SUB3M_MFHL'] = pd.Series(SUB3M_MFHL).values
df['SUB3M_MFOT'] = pd.Series(SUB3M_MFOT).values
df['SUB3M_OTH'] = pd.Series(SUB3M_OTH).values
df['SUB3M_PL'] = pd.Series(SUB3M_PL).values
df['SUB3M_PLBL'] = pd.Series(SUB3M_PLBL).values
df['SUB3M_RL'] = pd.Series(SUB3M_RL).values
df['SUB3M_SCC'] = pd.Series(SUB3M_SCC).values
df['SUB3M_SEL'] = pd.Series(SUB3M_SEL).values

df['SUB6M_AL'] = pd.Series(SUB6M_AL).values
df['SUB6M_BL'] = pd.Series(SUB6M_BL).values
df['SUB6M_CC'] = pd.Series(SUB6M_CC).values
df['SUB6M_CD'] = pd.Series(SUB6M_CD).values
df['SUB6M_CV'] = pd.Series(SUB6M_CV).values
df['SUB6M_GL'] = pd.Series(SUB6M_GL).values
df['SUB6M_HL'] = pd.Series(SUB6M_HL).values
df['SUB6M_LAS'] = pd.Series(SUB6M_LAS).values
df['SUB6M_MFBL'] = pd.Series(SUB6M_MFBL).values
df['SUB6M_MFHL'] = pd.Series(SUB6M_MFHL).values
df['SUB6M_MFOT'] = pd.Series(SUB6M_MFOT).values
df['SUB6M_OTH'] = pd.Series(SUB6M_OTH).values
df['SUB6M_PL'] = pd.Series(SUB6M_PL).values
df['SUB6M_PLBL'] = pd.Series(SUB6M_PLBL).values
df['SUB6M_RL'] = pd.Series(SUB6M_RL).values
df['SUB6M_SCC'] = pd.Series(SUB6M_SCC).values
df['SUB6M_SEL'] = pd.Series(SUB6M_SEL).values

df['SUB1Y_AL'] = pd.Series(SUB1Y_AL).values
df['SUB1Y_BL'] = pd.Series(SUB1Y_BL).values
df['SUB1Y_CC'] = pd.Series(SUB1Y_CC).values
df['SUB1Y_CD'] = pd.Series(SUB1Y_CD).values
df['SUB1Y_CV'] = pd.Series(SUB1Y_CV).values
df['SUB1Y_GL'] = pd.Series(SUB1Y_GL).values
df['SUB1Y_HL'] = pd.Series(SUB1Y_HL).values
df['SUB1Y_LAS'] = pd.Series(SUB1Y_LAS).values
df['SUB1Y_MFBL'] = pd.Series(SUB1Y_MFBL).values
df['SUB1Y_MFHL'] = pd.Series(SUB1Y_MFHL).values
df['SUB1Y_MFOT'] = pd.Series(SUB1Y_MFOT).values
df['SUB1Y_OTH'] = pd.Series(SUB1Y_OTH).values
df['SUB1Y_PL'] = pd.Series(SUB1Y_PL).values
df['SUB1Y_PLBL'] = pd.Series(SUB1Y_PLBL).values
df['SUB1Y_RL'] = pd.Series(SUB1Y_RL).values
df['SUB1Y_SCC'] = pd.Series(SUB1Y_SCC).values
df['SUB1Y_SEL'] = pd.Series(SUB1Y_SEL).values

df['SUB2Y_AL'] = pd.Series(SUB2Y_AL).values
df['SUB2Y_BL'] = pd.Series(SUB2Y_BL).values
df['SUB2Y_CC'] = pd.Series(SUB2Y_CC).values
df['SUB2Y_CD'] = pd.Series(SUB2Y_CD).values
df['SUB2Y_CV'] = pd.Series(SUB2Y_CV).values
df['SUB2Y_GL'] = pd.Series(SUB2Y_GL).values
df['SUB2Y_HL'] = pd.Series(SUB2Y_HL).values
df['SUB2Y_LAS'] = pd.Series(SUB2Y_LAS).values
df['SUB2Y_MFBL'] = pd.Series(SUB2Y_MFBL).values
df['SUB2Y_MFHL'] = pd.Series(SUB2Y_MFHL).values
df['SUB2Y_MFOT'] = pd.Series(SUB2Y_MFOT).values
df['SUB2Y_OTH'] = pd.Series(SUB2Y_OTH).values
df['SUB2Y_PL'] = pd.Series(SUB2Y_PL).values
df['SUB2Y_PLBL'] = pd.Series(SUB2Y_PLBL).values
df['SUB2Y_RL'] = pd.Series(SUB2Y_RL).values
df['SUB2Y_SCC'] = pd.Series(SUB2Y_SCC).values
df['SUB2Y_SEL'] = pd.Series(SUB2Y_SEL).values

df['SUB3Y_AL'] = pd.Series(SUB3Y_AL).values
df['SUB3Y_BL'] = pd.Series(SUB3Y_BL).values
df['SUB3Y_CC'] = pd.Series(SUB3Y_CC).values
df['SUB3Y_CD'] = pd.Series(SUB3Y_CD).values
df['SUB3Y_CV'] = pd.Series(SUB3Y_CV).values
df['SUB3Y_GL'] = pd.Series(SUB3Y_GL).values
df['SUB3Y_HL'] = pd.Series(SUB3Y_HL).values
df['SUB3Y_LAS'] = pd.Series(SUB3Y_LAS).values
df['SUB3Y_MFBL'] = pd.Series(SUB3Y_MFBL).values
df['SUB3Y_MFHL'] = pd.Series(SUB3Y_MFHL).values
df['SUB3Y_MFOT'] = pd.Series(SUB3Y_MFOT).values
df['SUB3Y_OTH'] = pd.Series(SUB3Y_OTH).values
df['SUB3Y_PL'] = pd.Series(SUB3Y_PL).values
df['SUB3Y_PLBL'] = pd.Series(SUB3Y_PLBL).values
df['SUB3Y_RL'] = pd.Series(SUB3Y_RL).values
df['SUB3Y_SCC'] = pd.Series(SUB3Y_SCC).values
df['SUB3Y_SEL'] = pd.Series(SUB3Y_SEL).values

df['DBT1M'] = pd.Series(DBT1M).values
df['DBT3M'] = pd.Series(DBT3M).values
df['DBT6M'] = pd.Series(DBT6M).values
df['DBT1Y'] = pd.Series(DBT1Y).values
df['DBT2Y'] = pd.Series(DBT2Y).values
df['DBT3Y'] = pd.Series(DBT3Y).values

df['DBT1M_AL'] = pd.Series(DBT1M_AL).values
df['DBT1M_BL'] = pd.Series(DBT1M_BL).values
df['DBT1M_CC'] = pd.Series(DBT1M_CC).values
df['DBT1M_CD'] = pd.Series(DBT1M_CD).values
df['DBT1M_CV'] = pd.Series(DBT1M_CV).values
df['DBT1M_GL'] = pd.Series(DBT1M_GL).values
df['DBT1M_HL'] = pd.Series(DBT1M_HL).values
df['DBT1M_LAS'] = pd.Series(DBT1M_LAS).values
df['DBT1M_MFBL'] = pd.Series(DBT1M_MFBL).values
df['DBT1M_MFHL'] = pd.Series(DBT1M_MFHL).values
df['DBT1M_MFOT'] = pd.Series(DBT1M_MFOT).values
df['DBT1M_OTH'] = pd.Series(DBT1M_OTH).values
df['DBT1M_PL'] = pd.Series(DBT1M_PL).values
df['DBT1M_PLBL'] = pd.Series(DBT1M_PLBL).values
df['DBT1M_RL'] = pd.Series(DBT1M_RL).values
df['DBT1M_SCC'] = pd.Series(DBT1M_SCC).values
df['DBT1M_SEL'] = pd.Series(DBT1M_SEL).values

df['DBT3M_AL'] = pd.Series(DBT3M_AL).values
df['DBT3M_BL'] = pd.Series(DBT3M_BL).values
df['DBT3M_CC'] = pd.Series(DBT3M_CC).values
df['DBT3M_CD'] = pd.Series(DBT3M_CD).values
df['DBT3M_CV'] = pd.Series(DBT3M_CV).values
df['DBT3M_GL'] = pd.Series(DBT3M_GL).values
df['DBT3M_HL'] = pd.Series(DBT3M_HL).values
df['DBT3M_LAS'] = pd.Series(DBT3M_LAS).values
df['DBT3M_MFBL'] = pd.Series(DBT3M_MFBL).values
df['DBT3M_MFHL'] = pd.Series(DBT3M_MFHL).values
df['DBT3M_MFOT'] = pd.Series(DBT3M_MFOT).values
df['DBT3M_OTH'] = pd.Series(DBT3M_OTH).values
df['DBT3M_PL'] = pd.Series(DBT3M_PL).values
df['DBT3M_PLBL'] = pd.Series(DBT3M_PLBL).values
df['DBT3M_RL'] = pd.Series(DBT3M_RL).values
df['DBT3M_SCC'] = pd.Series(DBT3M_SCC).values
df['DBT3M_SEL'] = pd.Series(DBT3M_SEL).values

df['DBT6M_AL'] = pd.Series(DBT6M_AL).values
df['DBT6M_BL'] = pd.Series(DBT6M_BL).values
df['DBT6M_CC'] = pd.Series(DBT6M_CC).values
df['DBT6M_CD'] = pd.Series(DBT6M_CD).values
df['DBT6M_CV'] = pd.Series(DBT6M_CV).values
df['DBT6M_GL'] = pd.Series(DBT6M_GL).values
df['DBT6M_HL'] = pd.Series(DBT6M_HL).values
df['DBT6M_LAS'] = pd.Series(DBT6M_LAS).values
df['DBT6M_MFBL'] = pd.Series(DBT6M_MFBL).values
df['DBT6M_MFHL'] = pd.Series(DBT6M_MFHL).values
df['DBT6M_MFOT'] = pd.Series(DBT6M_MFOT).values
df['DBT6M_OTH'] = pd.Series(DBT6M_OTH).values
df['DBT6M_PL'] = pd.Series(DBT6M_PL).values
df['DBT6M_PLBL'] = pd.Series(DBT6M_PLBL).values
df['DBT6M_RL'] = pd.Series(DBT6M_RL).values
df['DBT6M_SCC'] = pd.Series(DBT6M_SCC).values
df['DBT6M_SEL'] = pd.Series(DBT6M_SEL).values

df['DBT1Y_AL'] = pd.Series(DBT1Y_AL).values
df['DBT1Y_BL'] = pd.Series(DBT1Y_BL).values
df['DBT1Y_CC'] = pd.Series(DBT1Y_CC).values
df['DBT1Y_CD'] = pd.Series(DBT1Y_CD).values
df['DBT1Y_CV'] = pd.Series(DBT1Y_CV).values
df['DBT1Y_GL'] = pd.Series(DBT1Y_GL).values
df['DBT1Y_HL'] = pd.Series(DBT1Y_HL).values
df['DBT1Y_LAS'] = pd.Series(DBT1Y_LAS).values
df['DBT1Y_MFBL'] = pd.Series(DBT1Y_MFBL).values
df['DBT1Y_MFHL'] = pd.Series(DBT1Y_MFHL).values
df['DBT1Y_MFOT'] = pd.Series(DBT1Y_MFOT).values
df['DBT1Y_OTH'] = pd.Series(DBT1Y_OTH).values
df['DBT1Y_PL'] = pd.Series(DBT1Y_PL).values
df['DBT1Y_PLBL'] = pd.Series(DBT1Y_PLBL).values
df['DBT1Y_RL'] = pd.Series(DBT1Y_RL).values
df['DBT1Y_SCC'] = pd.Series(DBT1Y_SCC).values
df['DBT1Y_SEL'] = pd.Series(DBT1Y_SEL).values

df['DBT2Y_AL'] = pd.Series(DBT2Y_AL).values
df['DBT2Y_BL'] = pd.Series(DBT2Y_BL).values
df['DBT2Y_CC'] = pd.Series(DBT2Y_CC).values
df['DBT2Y_CD'] = pd.Series(DBT2Y_CD).values
df['DBT2Y_CV'] = pd.Series(DBT2Y_CV).values
df['DBT2Y_GL'] = pd.Series(DBT2Y_GL).values
df['DBT2Y_HL'] = pd.Series(DBT2Y_HL).values
df['DBT2Y_LAS'] = pd.Series(DBT2Y_LAS).values
df['DBT2Y_MFBL'] = pd.Series(DBT2Y_MFBL).values
df['DBT2Y_MFHL'] = pd.Series(DBT2Y_MFHL).values
df['DBT2Y_MFOT'] = pd.Series(DBT2Y_MFOT).values
df['DBT2Y_OTH'] = pd.Series(DBT2Y_OTH).values
df['DBT2Y_PL'] = pd.Series(DBT2Y_PL).values
df['DBT2Y_PLBL'] = pd.Series(DBT2Y_PLBL).values
df['DBT2Y_RL'] = pd.Series(DBT2Y_RL).values
df['DBT2Y_SCC'] = pd.Series(DBT2Y_SCC).values
df['DBT2Y_SEL'] = pd.Series(DBT2Y_SEL).values

df['DBT3Y_AL'] = pd.Series(DBT3Y_AL).values
df['DBT3Y_BL'] = pd.Series(DBT3Y_BL).values
df['DBT3Y_CC'] = pd.Series(DBT3Y_CC).values
df['DBT3Y_CD'] = pd.Series(DBT3Y_CD).values
df['DBT3Y_CV'] = pd.Series(DBT3Y_CV).values
df['DBT3Y_GL'] = pd.Series(DBT3Y_GL).values
df['DBT3Y_HL'] = pd.Series(DBT3Y_HL).values
df['DBT3Y_LAS'] = pd.Series(DBT3Y_LAS).values
df['DBT3Y_MFBL'] = pd.Series(DBT3Y_MFBL).values
df['DBT3Y_MFHL'] = pd.Series(DBT3Y_MFHL).values
df['DBT3Y_MFOT'] = pd.Series(DBT3Y_MFOT).values
df['DBT3Y_OTH'] = pd.Series(DBT3Y_OTH).values
df['DBT3Y_PL'] = pd.Series(DBT3Y_PL).values
df['DBT3Y_PLBL'] = pd.Series(DBT3Y_PLBL).values
df['DBT3Y_RL'] = pd.Series(DBT3Y_RL).values
df['DBT3Y_SCC'] = pd.Series(DBT3Y_SCC).values
df['DBT3Y_SEL'] = pd.Series(DBT3Y_SEL).values

df['LOS1M'] = pd.Series(LOS1M).values
df['LOS3M'] = pd.Series(LOS3M).values
df['LOS6M'] = pd.Series(LOS6M).values
df['LOS1Y'] = pd.Series(LOS1Y).values
df['LOS2Y'] = pd.Series(LOS2Y).values
df['LOS3Y'] = pd.Series(LOS3Y).values

df['LOS1M_AL'] = pd.Series(LOS1M_AL).values
df['LOS1M_BL'] = pd.Series(LOS1M_BL).values
df['LOS1M_CC'] = pd.Series(LOS1M_CC).values
df['LOS1M_CD'] = pd.Series(LOS1M_CD).values
df['LOS1M_CV'] = pd.Series(LOS1M_CV).values
df['LOS1M_GL'] = pd.Series(LOS1M_GL).values
df['LOS1M_HL'] = pd.Series(LOS1M_HL).values
df['LOS1M_LAS'] = pd.Series(LOS1M_LAS).values
df['LOS1M_MFBL'] = pd.Series(LOS1M_MFBL).values
df['LOS1M_MFHL'] = pd.Series(LOS1M_MFHL).values
df['LOS1M_MFOT'] = pd.Series(LOS1M_MFOT).values
df['LOS1M_OTH'] = pd.Series(LOS1M_OTH).values
df['LOS1M_PL'] = pd.Series(LOS1M_PL).values
df['LOS1M_PLBL'] = pd.Series(LOS1M_PLBL).values
df['LOS1M_RL'] = pd.Series(LOS1M_RL).values
df['LOS1M_SCC'] = pd.Series(LOS1M_SCC).values
df['LOS1M_SEL'] = pd.Series(LOS1M_SEL).values

df['LOS3M_AL'] = pd.Series(LOS3M_AL).values
df['LOS3M_BL'] = pd.Series(LOS3M_BL).values
df['LOS3M_CC'] = pd.Series(LOS3M_CC).values
df['LOS3M_CD'] = pd.Series(LOS3M_CD).values
df['LOS3M_CV'] = pd.Series(LOS3M_CV).values
df['LOS3M_GL'] = pd.Series(LOS3M_GL).values
df['LOS3M_HL'] = pd.Series(LOS3M_HL).values
df['LOS3M_LAS'] = pd.Series(LOS3M_LAS).values
df['LOS3M_MFBL'] = pd.Series(LOS3M_MFBL).values
df['LOS3M_MFHL'] = pd.Series(LOS3M_MFHL).values
df['LOS3M_MFOT'] = pd.Series(LOS3M_MFOT).values
df['LOS3M_OTH'] = pd.Series(LOS3M_OTH).values
df['LOS3M_PL'] = pd.Series(LOS3M_PL).values
df['LOS3M_PLBL'] = pd.Series(LOS3M_PLBL).values
df['LOS3M_RL'] = pd.Series(LOS3M_RL).values
df['LOS3M_SCC'] = pd.Series(LOS3M_SCC).values
df['LOS3M_SEL'] = pd.Series(LOS3M_SEL).values

df['LOS6M_AL'] = pd.Series(LOS6M_AL).values
df['LOS6M_BL'] = pd.Series(LOS6M_BL).values
df['LOS6M_CC'] = pd.Series(LOS6M_CC).values
df['LOS6M_CD'] = pd.Series(LOS6M_CD).values
df['LOS6M_CV'] = pd.Series(LOS6M_CV).values
df['LOS6M_GL'] = pd.Series(LOS6M_GL).values
df['LOS6M_HL'] = pd.Series(LOS6M_HL).values
df['LOS6M_LAS'] = pd.Series(LOS6M_LAS).values
df['LOS6M_MFBL'] = pd.Series(LOS6M_MFBL).values
df['LOS6M_MFHL'] = pd.Series(LOS6M_MFHL).values
df['LOS6M_MFOT'] = pd.Series(LOS6M_MFOT).values
df['LOS6M_OTH'] = pd.Series(LOS6M_OTH).values
df['LOS6M_PL'] = pd.Series(LOS6M_PL).values
df['LOS6M_PLBL'] = pd.Series(LOS6M_PLBL).values
df['LOS6M_RL'] = pd.Series(LOS6M_RL).values
df['LOS6M_SCC'] = pd.Series(LOS6M_SCC).values
df['LOS6M_SEL'] = pd.Series(LOS6M_SEL).values

df['LOS1Y_AL'] = pd.Series(LOS1Y_AL).values
df['LOS1Y_BL'] = pd.Series(LOS1Y_BL).values
df['LOS1Y_CC'] = pd.Series(LOS1Y_CC).values
df['LOS1Y_CD'] = pd.Series(LOS1Y_CD).values
df['LOS1Y_CV'] = pd.Series(LOS1Y_CV).values
df['LOS1Y_GL'] = pd.Series(LOS1Y_GL).values
df['LOS1Y_HL'] = pd.Series(LOS1Y_HL).values
df['LOS1Y_LAS'] = pd.Series(LOS1Y_LAS).values
df['LOS1Y_MFBL'] = pd.Series(LOS1Y_MFBL).values
df['LOS1Y_MFHL'] = pd.Series(LOS1Y_MFHL).values
df['LOS1Y_MFOT'] = pd.Series(LOS1Y_MFOT).values
df['LOS1Y_OTH'] = pd.Series(LOS1Y_OTH).values
df['LOS1Y_PL'] = pd.Series(LOS1Y_PL).values
df['LOS1Y_PLBL'] = pd.Series(LOS1Y_PLBL).values
df['LOS1Y_RL'] = pd.Series(LOS1Y_RL).values
df['LOS1Y_SCC'] = pd.Series(LOS1Y_SCC).values
df['LOS1Y_SEL'] = pd.Series(LOS1Y_SEL).values

df['LOS2Y_AL'] = pd.Series(LOS2Y_AL).values
df['LOS2Y_BL'] = pd.Series(LOS2Y_BL).values
df['LOS2Y_CC'] = pd.Series(LOS2Y_CC).values
df['LOS2Y_CD'] = pd.Series(LOS2Y_CD).values
df['LOS2Y_CV'] = pd.Series(LOS2Y_CV).values
df['LOS2Y_GL'] = pd.Series(LOS2Y_GL).values
df['LOS2Y_HL'] = pd.Series(LOS2Y_HL).values
df['LOS2Y_LAS'] = pd.Series(LOS2Y_LAS).values
df['LOS2Y_MFBL'] = pd.Series(LOS2Y_MFBL).values
df['LOS2Y_MFHL'] = pd.Series(LOS2Y_MFHL).values
df['LOS2Y_MFOT'] = pd.Series(LOS2Y_MFOT).values
df['LOS2Y_OTH'] = pd.Series(LOS2Y_OTH).values
df['LOS2Y_PL'] = pd.Series(LOS2Y_PL).values
df['LOS2Y_PLBL'] = pd.Series(LOS2Y_PLBL).values
df['LOS2Y_RL'] = pd.Series(LOS2Y_RL).values
df['LOS2Y_SCC'] = pd.Series(LOS2Y_SCC).values
df['LOS2Y_SEL'] = pd.Series(LOS2Y_SEL).values

df['LOS3Y_AL'] = pd.Series(LOS3Y_AL).values
df['LOS3Y_BL'] = pd.Series(LOS3Y_BL).values
df['LOS3Y_CC'] = pd.Series(LOS3Y_CC).values
df['LOS3Y_CD'] = pd.Series(LOS3Y_CD).values
df['LOS3Y_CV'] = pd.Series(LOS3Y_CV).values
df['LOS3Y_GL'] = pd.Series(LOS3Y_GL).values
df['LOS3Y_HL'] = pd.Series(LOS3Y_HL).values
df['LOS3Y_LAS'] = pd.Series(LOS3Y_LAS).values
df['LOS3Y_MFBL'] = pd.Series(LOS3Y_MFBL).values
df['LOS3Y_MFHL'] = pd.Series(LOS3Y_MFHL).values
df['LOS3Y_MFOT'] = pd.Series(LOS3Y_MFOT).values
df['LOS3Y_OTH'] = pd.Series(LOS3Y_OTH).values
df['LOS3Y_PL'] = pd.Series(LOS3Y_PL).values
df['LOS3Y_PLBL'] = pd.Series(LOS3Y_PLBL).values
df['LOS3Y_RL'] = pd.Series(LOS3Y_RL).values
df['LOS3Y_SCC'] = pd.Series(LOS3Y_SCC).values
df['LOS3Y_SEL'] = pd.Series(LOS3Y_SEL).values

df['XXX1M'] = pd.Series(XXX1M).values
df['XXX3M'] = pd.Series(XXX3M).values
df['XXX6M'] = pd.Series(XXX6M).values
df['XXX1Y'] = pd.Series(XXX1Y).values
df['XXX2Y'] = pd.Series(XXX2Y).values
df['XXX3Y'] = pd.Series(XXX3Y).values

df['XXX1M_AL'] = pd.Series(XXX1M_AL).values
df['XXX1M_BL'] = pd.Series(XXX1M_BL).values
df['XXX1M_CC'] = pd.Series(XXX1M_CC).values
df['XXX1M_CD'] = pd.Series(XXX1M_CD).values
df['XXX1M_CV'] = pd.Series(XXX1M_CV).values
df['XXX1M_GL'] = pd.Series(XXX1M_GL).values
df['XXX1M_HL'] = pd.Series(XXX1M_HL).values
df['XXX1M_LAS'] = pd.Series(XXX1M_LAS).values
df['XXX1M_MFBL'] = pd.Series(XXX1M_MFBL).values
df['XXX1M_MFHL'] = pd.Series(XXX1M_MFHL).values
df['XXX1M_MFOT'] = pd.Series(XXX1M_MFOT).values
df['XXX1M_OTH'] = pd.Series(XXX1M_OTH).values
df['XXX1M_PL'] = pd.Series(XXX1M_PL).values
df['XXX1M_PLBL'] = pd.Series(XXX1M_PLBL).values
df['XXX1M_RL'] = pd.Series(XXX1M_RL).values
df['XXX1M_SCC'] = pd.Series(XXX1M_SCC).values
df['XXX1M_SEL'] = pd.Series(XXX1M_SEL).values

df['XXX3M_AL'] = pd.Series(XXX3M_AL).values
df['XXX3M_BL'] = pd.Series(XXX3M_BL).values
df['XXX3M_CC'] = pd.Series(XXX3M_CC).values
df['XXX3M_CD'] = pd.Series(XXX3M_CD).values
df['XXX3M_CV'] = pd.Series(XXX3M_CV).values
df['XXX3M_GL'] = pd.Series(XXX3M_GL).values
df['XXX3M_HL'] = pd.Series(XXX3M_HL).values
df['XXX3M_LAS'] = pd.Series(XXX3M_LAS).values
df['XXX3M_MFBL'] = pd.Series(XXX3M_MFBL).values
df['XXX3M_MFHL'] = pd.Series(XXX3M_MFHL).values
df['XXX3M_MFOT'] = pd.Series(XXX3M_MFOT).values
df['XXX3M_OTH'] = pd.Series(XXX3M_OTH).values
df['XXX3M_PL'] = pd.Series(XXX3M_PL).values
df['XXX3M_PLBL'] = pd.Series(XXX3M_PLBL).values
df['XXX3M_RL'] = pd.Series(XXX3M_RL).values
df['XXX3M_SCC'] = pd.Series(XXX3M_SCC).values
df['XXX3M_SEL'] = pd.Series(XXX3M_SEL).values

df['XXX6M_AL'] = pd.Series(XXX6M_AL).values
df['XXX6M_BL'] = pd.Series(XXX6M_BL).values
df['XXX6M_CC'] = pd.Series(XXX6M_CC).values
df['XXX6M_CD'] = pd.Series(XXX6M_CD).values
df['XXX6M_CV'] = pd.Series(XXX6M_CV).values
df['XXX6M_GL'] = pd.Series(XXX6M_GL).values
df['XXX6M_HL'] = pd.Series(XXX6M_HL).values
df['XXX6M_LAS'] = pd.Series(XXX6M_LAS).values
df['XXX6M_MFBL'] = pd.Series(XXX6M_MFBL).values
df['XXX6M_MFHL'] = pd.Series(XXX6M_MFHL).values
df['XXX6M_MFOT'] = pd.Series(XXX6M_MFOT).values
df['XXX6M_OTH'] = pd.Series(XXX6M_OTH).values
df['XXX6M_PL'] = pd.Series(XXX6M_PL).values
df['XXX6M_PLBL'] = pd.Series(XXX6M_PLBL).values
df['XXX6M_RL'] = pd.Series(XXX6M_RL).values
df['XXX6M_SCC'] = pd.Series(XXX6M_SCC).values
df['XXX6M_SEL'] = pd.Series(XXX6M_SEL).values

df['XXX1Y_AL'] = pd.Series(XXX1Y_AL).values
df['XXX1Y_BL'] = pd.Series(XXX1Y_BL).values
df['XXX1Y_CC'] = pd.Series(XXX1Y_CC).values
df['XXX1Y_CD'] = pd.Series(XXX1Y_CD).values
df['XXX1Y_CV'] = pd.Series(XXX1Y_CV).values
df['XXX1Y_GL'] = pd.Series(XXX1Y_GL).values
df['XXX1Y_HL'] = pd.Series(XXX1Y_HL).values
df['XXX1Y_LAS'] = pd.Series(XXX1Y_LAS).values
df['XXX1Y_MFBL'] = pd.Series(XXX1Y_MFBL).values
df['XXX1Y_MFHL'] = pd.Series(XXX1Y_MFHL).values
df['XXX1Y_MFOT'] = pd.Series(XXX1Y_MFOT).values
df['XXX1Y_OTH'] = pd.Series(XXX1Y_OTH).values
df['XXX1Y_PL'] = pd.Series(XXX1Y_PL).values
df['XXX1Y_PLBL'] = pd.Series(XXX1Y_PLBL).values
df['XXX1Y_RL'] = pd.Series(XXX1Y_RL).values
df['XXX1Y_SCC'] = pd.Series(XXX1Y_SCC).values
df['XXX1Y_SEL'] = pd.Series(XXX1Y_SEL).values

df['XXX2Y_AL'] = pd.Series(XXX2Y_AL).values
df['XXX2Y_BL'] = pd.Series(XXX2Y_BL).values
df['XXX2Y_CC'] = pd.Series(XXX2Y_CC).values
df['XXX2Y_CD'] = pd.Series(XXX2Y_CD).values
df['XXX2Y_CV'] = pd.Series(XXX2Y_CV).values
df['XXX2Y_GL'] = pd.Series(XXX2Y_GL).values
df['XXX2Y_HL'] = pd.Series(XXX2Y_HL).values
df['XXX2Y_LAS'] = pd.Series(XXX2Y_LAS).values
df['XXX2Y_MFBL'] = pd.Series(XXX2Y_MFBL).values
df['XXX2Y_MFHL'] = pd.Series(XXX2Y_MFHL).values
df['XXX2Y_MFOT'] = pd.Series(XXX2Y_MFOT).values
df['XXX2Y_OTH'] = pd.Series(XXX2Y_OTH).values
df['XXX2Y_PL'] = pd.Series(XXX2Y_PL).values
df['XXX2Y_PLBL'] = pd.Series(XXX2Y_PLBL).values
df['XXX2Y_RL'] = pd.Series(XXX2Y_RL).values
df['XXX2Y_SCC'] = pd.Series(XXX2Y_SCC).values
df['XXX2Y_SEL'] = pd.Series(XXX2Y_SEL).values

df['XXX3Y_AL'] = pd.Series(XXX3Y_AL).values
df['XXX3Y_BL'] = pd.Series(XXX3Y_BL).values
df['XXX3Y_CC'] = pd.Series(XXX3Y_CC).values
df['XXX3Y_CD'] = pd.Series(XXX3Y_CD).values
df['XXX3Y_CV'] = pd.Series(XXX3Y_CV).values
df['XXX3Y_GL'] = pd.Series(XXX3Y_GL).values
df['XXX3Y_HL'] = pd.Series(XXX3Y_HL).values
df['XXX3Y_LAS'] = pd.Series(XXX3Y_LAS).values
df['XXX3Y_MFBL'] = pd.Series(XXX3Y_MFBL).values
df['XXX3Y_MFHL'] = pd.Series(XXX3Y_MFHL).values
df['XXX3Y_MFOT'] = pd.Series(XXX3Y_MFOT).values
df['XXX3Y_OTH'] = pd.Series(XXX3Y_OTH).values
df['XXX3Y_PL'] = pd.Series(XXX3Y_PL).values
df['XXX3Y_PLBL'] = pd.Series(XXX3Y_PLBL).values
df['XXX3Y_RL'] = pd.Series(XXX3Y_RL).values
df['XXX3Y_SCC'] = pd.Series(XXX3Y_SCC).values
df['XXX3Y_SEL'] = pd.Series(XXX3Y_SEL).values

df['SMA1M'] = pd.Series(SMA1M).values
df['SMA3M'] = pd.Series(SMA3M).values
df['SMA6M'] = pd.Series(SMA6M).values
df['SMA1Y'] = pd.Series(SMA1Y).values
df['SMA2Y'] = pd.Series(SMA2Y).values
df['SMA3Y'] = pd.Series(SMA3Y).values

df['SMA1M_AL'] = pd.Series(SMA1M_AL).values
df['SMA1M_BL'] = pd.Series(SMA1M_BL).values
df['SMA1M_CC'] = pd.Series(SMA1M_CC).values
df['SMA1M_CD'] = pd.Series(SMA1M_CD).values
df['SMA1M_CV'] = pd.Series(SMA1M_CV).values
df['SMA1M_GL'] = pd.Series(SMA1M_GL).values
df['SMA1M_HL'] = pd.Series(SMA1M_HL).values
df['SMA1M_LAS'] = pd.Series(SMA1M_LAS).values
df['SMA1M_MFBL'] = pd.Series(SMA1M_MFBL).values
df['SMA1M_MFHL'] = pd.Series(SMA1M_MFHL).values
df['SMA1M_MFOT'] = pd.Series(SMA1M_MFOT).values
df['SMA1M_OTH'] = pd.Series(SMA1M_OTH).values
df['SMA1M_PL'] = pd.Series(SMA1M_PL).values
df['SMA1M_PLBL'] = pd.Series(SMA1M_PLBL).values
df['SMA1M_RL'] = pd.Series(SMA1M_RL).values
df['SMA1M_SCC'] = pd.Series(SMA1M_SCC).values
df['SMA1M_SEL'] = pd.Series(SMA1M_SEL).values

df['SMA3M_AL'] = pd.Series(SMA3M_AL).values
df['SMA3M_BL'] = pd.Series(SMA3M_BL).values
df['SMA3M_CC'] = pd.Series(SMA3M_CC).values
df['SMA3M_CD'] = pd.Series(SMA3M_CD).values
df['SMA3M_CV'] = pd.Series(SMA3M_CV).values
df['SMA3M_GL'] = pd.Series(SMA3M_GL).values
df['SMA3M_HL'] = pd.Series(SMA3M_HL).values
df['SMA3M_LAS'] = pd.Series(SMA3M_LAS).values
df['SMA3M_MFBL'] = pd.Series(SMA3M_MFBL).values
df['SMA3M_MFHL'] = pd.Series(SMA3M_MFHL).values
df['SMA3M_MFOT'] = pd.Series(SMA3M_MFOT).values
df['SMA3M_OTH'] = pd.Series(SMA3M_OTH).values
df['SMA3M_PL'] = pd.Series(SMA3M_PL).values
df['SMA3M_PLBL'] = pd.Series(SMA3M_PLBL).values
df['SMA3M_RL'] = pd.Series(SMA3M_RL).values
df['SMA3M_SCC'] = pd.Series(SMA3M_SCC).values
df['SMA3M_SEL'] = pd.Series(SMA3M_SEL).values

df['SMA6M_AL'] = pd.Series(SMA6M_AL).values
df['SMA6M_BL'] = pd.Series(SMA6M_BL).values
df['SMA6M_CC'] = pd.Series(SMA6M_CC).values
df['SMA6M_CD'] = pd.Series(SMA6M_CD).values
df['SMA6M_CV'] = pd.Series(SMA6M_CV).values
df['SMA6M_GL'] = pd.Series(SMA6M_GL).values
df['SMA6M_HL'] = pd.Series(SMA6M_HL).values
df['SMA6M_LAS'] = pd.Series(SMA6M_LAS).values
df['SMA6M_MFBL'] = pd.Series(SMA6M_MFBL).values
df['SMA6M_MFHL'] = pd.Series(SMA6M_MFHL).values
df['SMA6M_MFOT'] = pd.Series(SMA6M_MFOT).values
df['SMA6M_OTH'] = pd.Series(SMA6M_OTH).values
df['SMA6M_PL'] = pd.Series(SMA6M_PL).values
df['SMA6M_PLBL'] = pd.Series(SMA6M_PLBL).values
df['SMA6M_RL'] = pd.Series(SMA6M_RL).values
df['SMA6M_SCC'] = pd.Series(SMA6M_SCC).values
df['SMA6M_SEL'] = pd.Series(SMA6M_SEL).values

df['SMA1Y_AL'] = pd.Series(SMA1Y_AL).values
df['SMA1Y_BL'] = pd.Series(SMA1Y_BL).values
df['SMA1Y_CC'] = pd.Series(SMA1Y_CC).values
df['SMA1Y_CD'] = pd.Series(SMA1Y_CD).values
df['SMA1Y_CV'] = pd.Series(SMA1Y_CV).values
df['SMA1Y_GL'] = pd.Series(SMA1Y_GL).values
df['SMA1Y_HL'] = pd.Series(SMA1Y_HL).values
df['SMA1Y_LAS'] = pd.Series(SMA1Y_LAS).values
df['SMA1Y_MFBL'] = pd.Series(SMA1Y_MFBL).values
df['SMA1Y_MFHL'] = pd.Series(SMA1Y_MFHL).values
df['SMA1Y_MFOT'] = pd.Series(SMA1Y_MFOT).values
df['SMA1Y_OTH'] = pd.Series(SMA1Y_OTH).values
df['SMA1Y_PL'] = pd.Series(SMA1Y_PL).values
df['SMA1Y_PLBL'] = pd.Series(SMA1Y_PLBL).values
df['SMA1Y_RL'] = pd.Series(SMA1Y_RL).values
df['SMA1Y_SCC'] = pd.Series(SMA1Y_SCC).values
df['SMA1Y_SEL'] = pd.Series(SMA1Y_SEL).values

df['SMA2Y_AL'] = pd.Series(SMA2Y_AL).values
df['SMA2Y_BL'] = pd.Series(SMA2Y_BL).values
df['SMA2Y_CC'] = pd.Series(SMA2Y_CC).values
df['SMA2Y_CD'] = pd.Series(SMA2Y_CD).values
df['SMA2Y_CV'] = pd.Series(SMA2Y_CV).values
df['SMA2Y_GL'] = pd.Series(SMA2Y_GL).values
df['SMA2Y_HL'] = pd.Series(SMA2Y_HL).values
df['SMA2Y_LAS'] = pd.Series(SMA2Y_LAS).values
df['SMA2Y_MFBL'] = pd.Series(SMA2Y_MFBL).values
df['SMA2Y_MFHL'] = pd.Series(SMA2Y_MFHL).values
df['SMA2Y_MFOT'] = pd.Series(SMA2Y_MFOT).values
df['SMA2Y_OTH'] = pd.Series(SMA2Y_OTH).values
df['SMA2Y_PL'] = pd.Series(SMA2Y_PL).values
df['SMA2Y_PLBL'] = pd.Series(SMA2Y_PLBL).values
df['SMA2Y_RL'] = pd.Series(SMA2Y_RL).values
df['SMA2Y_SCC'] = pd.Series(SMA2Y_SCC).values
df['SMA2Y_SEL'] = pd.Series(SMA2Y_SEL).values

df['SMA3Y_AL'] = pd.Series(SMA3Y_AL).values
df['SMA3Y_BL'] = pd.Series(SMA3Y_BL).values
df['SMA3Y_CC'] = pd.Series(SMA3Y_CC).values
df['SMA3Y_CD'] = pd.Series(SMA3Y_CD).values
df['SMA3Y_CV'] = pd.Series(SMA3Y_CV).values
df['SMA3Y_GL'] = pd.Series(SMA3Y_GL).values
df['SMA3Y_HL'] = pd.Series(SMA3Y_HL).values
df['SMA3Y_LAS'] = pd.Series(SMA3Y_LAS).values
df['SMA3Y_MFBL'] = pd.Series(SMA3Y_MFBL).values
df['SMA3Y_MFHL'] = pd.Series(SMA3Y_MFHL).values
df['SMA3Y_MFOT'] = pd.Series(SMA3Y_MFOT).values
df['SMA3Y_OTH'] = pd.Series(SMA3Y_OTH).values
df['SMA3Y_PL'] = pd.Series(SMA3Y_PL).values
df['SMA3Y_PLBL'] = pd.Series(SMA3Y_PLBL).values
df['SMA3Y_RL'] = pd.Series(SMA3Y_RL).values
df['SMA3Y_SCC'] = pd.Series(SMA3Y_SCC).values
df['SMA3Y_SEL'] = pd.Series(SMA3Y_SEL).values

# Tenth sequential code

Ever_DPD1M_flag = list()
Ever_DPD3M_flag = list()
Ever_DPD6M_flag = list()
Ever_DPD1Y_flag = list()
Ever_DPD2Y_flag = list()
Ever_DPD3Y_flag = list()

Ever_DPD_Sec_L_1mnth_flag = list()
Ever_DPD_Sec_L_3mnth_flag = list()
Ever_DPD_Sec_L_6mnth_flag = list()
Ever_DPD_Sec_L_1yr_flag = list()

Ever_DPD_UnsecwoRLCC_L_1mnth_flag = list()
Ever_DPD_UnsecwoRLCC_L_3mnth_flag = list()
Ever_DPD_UnsecwoRLCC_L_6mnth_flag = list()
Ever_DPD_UnsecwoRLCC_L_1yr_flag = list()

accountTypeSec = [1, 2, 3, 4, 7, 11, 13, 15, 16, 17,
                  31, 32, 33, 34, 42, 43, 44, 50, 54, 58, 59, 0, 98]

accountTypeUnsec = [5, 6, 8, 9, 10, 12, 14, 35, 36,
                    37, 38, 39, 40, 41, 51, 52, 53, 55, 56, 57, 61, 99]

for x in range(0, df.shape[0]):
    if (df['DPD30P1M_flag'][x] == 'unknown') and (df['DPD60P1M_flag'][x] == 'unknown') and (df['DPD90P1M_flag'][x] == 'unknown') and (df['SMA1M_flag'][x] == 'unknown') and (df['SUB1M_flag'][x] == 'unknown') and (df['DBT1M_flag'][x] == 'unknown') and (df['LOS1M_flag'][x] == 'unknown'):
        Ever_DPD1M_flag.append('unknown')
    elif (df['DPD30P1M_flag'][x] == 1) or (df['DPD60P1M_flag'][x] == 1) or (df['DPD90P1M_flag'][x] == 1) or (df['SMA1M_flag'][x] == 1) or (df['SUB1M_flag'][x] == 1) or (df['DBT1M_flag'][x] == 1) or (df['LOS1M_flag'][x] == 1):
        Ever_DPD1M_flag.append(1)
    else:
        Ever_DPD1M_flag.append(0)

    if (df['DPD30P3M_flag'][x] == 'unknown') and (df['DPD60P3M_flag'][x] == 'unknown') and (df['DPD90P3M_flag'][x] == 'unknown') and (df['SMA3M_flag'][x] == 'unknown') and (df['SUB3M_flag'][x] == 'unknown') and (df['DBT3M_flag'][x] == 'unknown') and (df['LOS3M_flag'][x] == 'unknown'):
        Ever_DPD3M_flag.append('unknown')
    elif (df['DPD30P3M_flag'][x] == 1) or (df['DPD60P3M_flag'][x] == 1) or (df['DPD90P3M_flag'][x] == 1) or (df['SMA3M_flag'][x] == 1) or (df['SUB3M_flag'][x] == 1) or (df['DBT3M_flag'][x] == 1) or (df['LOS3M_flag'][x] == 1):
        Ever_DPD3M_flag.append(1)
    else:
        Ever_DPD3M_flag.append(0)

    if (df['DPD30P6M_flag'][x] == 'unknown') and (df['DPD60P6M_flag'][x] == 'unknown') and (df['DPD90P6M_flag'][x] == 'unknown') and (df['SMA6M_flag'][x] == 'unknown') and (df['SUB6M_flag'][x] == 'unknown') and (df['DBT6M_flag'][x] == 'unknown') and (df['LOS6M_flag'][x] == 'unknown'):
        Ever_DPD6M_flag.append('unknown')
    elif (df['DPD30P6M_flag'][x] == 1) or (df['DPD60P6M_flag'][x] == 1) or (df['DPD90P6M_flag'][x] == 1) or (df['SMA6M_flag'][x] == 1) or (df['SUB6M_flag'][x] == 1) or (df['DBT6M_flag'][x] == 1) or (df['LOS6M_flag'][x] == 1):
        Ever_DPD6M_flag.append(1)
    else:
        Ever_DPD6M_flag.append(0)

    if (df['DPD30P1Y_flag'][x] == 'unknown') and (df['DPD60P1Y_flag'][x] == 'unknown') and (df['DPD90P1Y_flag'][x] == 'unknown') and (df['SMA1Y_flag'][x] == 'unknown') and (df['SUB1Y_flag'][x] == 'unknown') and (df['DBT1Y_flag'][x] == 'unknown') and (df['LOS1Y_flag'][x] == 'unknown'):
        Ever_DPD1Y_flag.append('unknown')
    elif (df['DPD30P1Y_flag'][x] == 1) or (df['DPD60P1Y_flag'][x] == 1) or (df['DPD90P1Y_flag'][x] == 1) or (df['SMA1Y_flag'][x] == 1) or (df['SUB1Y_flag'][x] == 1) or (df['DBT1Y_flag'][x] == 1) or (df['LOS1Y_flag'][x] == 1):
        Ever_DPD1Y_flag.append(1)
    else:
        Ever_DPD1Y_flag.append(0)

    if (df['DPD30P2Y_flag'][x] == 'unknown') and (df['DPD60P2Y_flag'][x] == 'unknown') and (df['DPD90P2Y_flag'][x] == 'unknown') and (df['SMA2Y_flag'][x] == 'unknown') and (df['SUB2Y_flag'][x] == 'unknown') and (df['DBT2Y_flag'][x] == 'unknown') and (df['LOS2Y_flag'][x] == 'unknown'):
        Ever_DPD2Y_flag.append('unknown')
    elif (df['DPD30P2Y_flag'][x] == 1) or (df['DPD60P2Y_flag'][x] == 1) or (df['DPD90P2Y_flag'][x] == 1) or (df['SMA2Y_flag'][x] == 1) or (df['SUB2Y_flag'][x] == 1) or (df['DBT2Y_flag'][x] == 1) or (df['LOS2Y_flag'][x] == 1):
        Ever_DPD2Y_flag.append(1)
    else:
        Ever_DPD2Y_flag.append(0)

    if (df['DPD30P3Y_flag'][x] == 'unknown') and (df['DPD60P3Y_flag'][x] == 'unknown') and (df['DPD90P3Y_flag'][x] == 'unknown') and (df['SMA3Y_flag'][x] == 'unknown') and (df['SUB3Y_flag'][x] == 'unknown') and (df['DBT3Y_flag'][x] == 'unknown') and (df['LOS3Y_flag'][x] == 'unknown'):
        Ever_DPD3Y_flag.append('unknown')
    elif (df['DPD30P3Y_flag'][x] == 1) or (df['DPD60P3Y_flag'][x] == 1) or (df['DPD90P3Y_flag'][x] == 1) or (df['SMA3Y_flag'][x] == 1) or (df['SUB3Y_flag'][x] == 1) or (df['DBT3Y_flag'][x] == 1) or (df['LOS3Y_flag'][x] == 1):
        Ever_DPD3Y_flag.append(1)
    else:
        Ever_DPD3Y_flag.append(0)

    if (df['accountType'][x] in accountTypeSec) and (df['DPD1M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_Sec_L_1mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD1M_flag'][x] == 'unknown'):
        Ever_DPD_Sec_L_1mnth_flag.append('unknown')
    else:
        Ever_DPD_Sec_L_1mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeSec) and (df['DPD3M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_Sec_L_3mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD3M_flag'][x] == 'unknown'):
        Ever_DPD_Sec_L_3mnth_flag.append('unknown')
    else:
        Ever_DPD_Sec_L_3mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeSec) and (df['DPD6M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_Sec_L_6mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD6M_flag'][x] == 'unknown'):
        Ever_DPD_Sec_L_6mnth_flag.append('unknown')
    else:
        Ever_DPD_Sec_L_6mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeSec) and (df['DPD1Y_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_Sec_L_1yr_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD1Y_flag'][x] == 'unknown'):
        Ever_DPD_Sec_L_1yr_flag.append('unknown')
    else:
        Ever_DPD_Sec_L_1yr_flag.append(0)

    if (df['accountType'][x] in accountTypeUnsec) and (df['DPD1M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_1mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD1M_flag'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_1mnth_flag.append('unknown')
    else:
        Ever_DPD_UnsecwoRLCC_L_1mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeUnsec) and (df['DPD3M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_3mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD3M_flag'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_3mnth_flag.append('unknown')
    else:
        Ever_DPD_UnsecwoRLCC_L_3mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeUnsec) and (df['DPD6M_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_6mnth_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD6M_flag'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_6mnth_flag.append('unknown')
    else:
        Ever_DPD_UnsecwoRLCC_L_6mnth_flag.append(0)

    if (df['accountType'][x] in accountTypeUnsec) and (df['DPD1Y_flag'][x] == 1) and (df['dateClosed'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_1yr_flag.append(1)
    elif (df['accountType'][x] == 'unknown') and (df['DPD1Y_flag'][x] == 'unknown'):
        Ever_DPD_UnsecwoRLCC_L_1yr_flag.append('unknown')
    else:
        Ever_DPD_UnsecwoRLCC_L_1yr_flag.append(0)

df['Ever_DPD1M_flag'] = pd.Series(Ever_DPD1M_flag).values
df['Ever_DPD3M_flag'] = pd.Series(Ever_DPD3M_flag).values
df['Ever_DPD6M_flag'] = pd.Series(Ever_DPD6M_flag).values
df['Ever_DPD1Y_flag'] = pd.Series(Ever_DPD1Y_flag).values
df['Ever_DPD2Y_flag'] = pd.Series(Ever_DPD2Y_flag).values
df['Ever_DPD3Y_flag'] = pd.Series(Ever_DPD3Y_flag).values

df['Ever_DPD_Sec_L_1mnth_flag'] = pd.Series(Ever_DPD_Sec_L_1mnth_flag).values
df['Ever_DPD_Sec_L_3mnth_flag'] = pd.Series(Ever_DPD_Sec_L_3mnth_flag).values
df['Ever_DPD_Sec_L_6mnth_flag'] = pd.Series(Ever_DPD_Sec_L_6mnth_flag).values
df['Ever_DPD_Sec_L_1yr_flag'] = pd.Series(Ever_DPD_Sec_L_1yr_flag).values

df['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_1mnth_flag).values
df['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_3mnth_flag).values
df['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_6mnth_flag).values
df['Ever_DPD_UnsecwoRLCC_L_1yr_flag'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_1yr_flag).values

# Eleventh sequential code

Ever_DPD1M_AL = list()
Ever_DPD1M_BL = list()
Ever_DPD1M_CC = list()
Ever_DPD1M_CD = list()
Ever_DPD1M_CV = list()
Ever_DPD1M_GL = list()
Ever_DPD1M_HL = list()
Ever_DPD1M_LAS = list()
Ever_DPD1M_MFBL = list()
Ever_DPD1M_MFHL = list()
Ever_DPD1M_MFOT = list()
Ever_DPD1M_OTH = list()
Ever_DPD1M_PL = list()
Ever_DPD1M_PLBL = list()
Ever_DPD1M_RL = list()
Ever_DPD1M_SCC = list()
Ever_DPD1M_SEL = list()

count_ever_1m_list_AL = list()
count_ever_1m_list_BL = list()
count_ever_1m_list_CC = list()
count_ever_1m_list_CD = list()
count_ever_1m_list_CV = list()
count_ever_1m_list_GL = list()
count_ever_1m_list_HL = list()
count_ever_1m_list_LAS = list()
count_ever_1m_list_MFBL = list()
count_ever_1m_list_MFHL = list()
count_ever_1m_list_MFOT = list()
count_ever_1m_list_OTH = list()
count_ever_1m_list_PL = list()
count_ever_1m_list_PLBL = list()
count_ever_1m_list_RL = list()
count_ever_1m_list_SCC = list()
count_ever_1m_list_SEL = list()

count_ever_1m_AL = 0
count_ever_1m_BL = 0
count_ever_1m_CC = 0
count_ever_1m_CD = 0
count_ever_1m_CV = 0
count_ever_1m_GL = 0
count_ever_1m_HL = 0
count_ever_1m_LAS = 0
count_ever_1m_MFBL = 0
count_ever_1m_MFHL = 0
count_ever_1m_MFOT = 0
count_ever_1m_OTH = 0
count_ever_1m_PL = 0
count_ever_1m_PLBL = 0
count_ever_1m_RL = 0
count_ever_1m_SCC = 0
count_ever_1m_SEL = 0

Ever_DPD3M_AL = list()
Ever_DPD3M_BL = list()
Ever_DPD3M_CC = list()
Ever_DPD3M_CD = list()
Ever_DPD3M_CV = list()
Ever_DPD3M_GL = list()
Ever_DPD3M_HL = list()
Ever_DPD3M_LAS = list()
Ever_DPD3M_MFBL = list()
Ever_DPD3M_MFHL = list()
Ever_DPD3M_MFOT = list()
Ever_DPD3M_OTH = list()
Ever_DPD3M_PL = list()
Ever_DPD3M_PLBL = list()
Ever_DPD3M_RL = list()
Ever_DPD3M_SCC = list()
Ever_DPD3M_SEL = list()

count_ever_3m_list_AL = list()
count_ever_3m_list_BL = list()
count_ever_3m_list_CC = list()
count_ever_3m_list_CD = list()
count_ever_3m_list_CV = list()
count_ever_3m_list_GL = list()
count_ever_3m_list_HL = list()
count_ever_3m_list_LAS = list()
count_ever_3m_list_MFBL = list()
count_ever_3m_list_MFHL = list()
count_ever_3m_list_MFOT = list()
count_ever_3m_list_OTH = list()
count_ever_3m_list_PL = list()
count_ever_3m_list_PLBL = list()
count_ever_3m_list_RL = list()
count_ever_3m_list_SCC = list()
count_ever_3m_list_SEL = list()

count_ever_3m_AL = 0
count_ever_3m_BL = 0
count_ever_3m_CC = 0
count_ever_3m_CD = 0
count_ever_3m_CV = 0
count_ever_3m_GL = 0
count_ever_3m_HL = 0
count_ever_3m_LAS = 0
count_ever_3m_MFBL = 0
count_ever_3m_MFHL = 0
count_ever_3m_MFOT = 0
count_ever_3m_OTH = 0
count_ever_3m_PL = 0
count_ever_3m_PLBL = 0
count_ever_3m_RL = 0
count_ever_3m_SCC = 0
count_ever_3m_SEL = 0

Ever_DPD6M_AL = list()
Ever_DPD6M_BL = list()
Ever_DPD6M_CC = list()
Ever_DPD6M_CD = list()
Ever_DPD6M_CV = list()
Ever_DPD6M_GL = list()
Ever_DPD6M_HL = list()
Ever_DPD6M_LAS = list()
Ever_DPD6M_MFBL = list()
Ever_DPD6M_MFHL = list()
Ever_DPD6M_MFOT = list()
Ever_DPD6M_OTH = list()
Ever_DPD6M_PL = list()
Ever_DPD6M_PLBL = list()
Ever_DPD6M_RL = list()
Ever_DPD6M_SCC = list()
Ever_DPD6M_SEL = list()

count_ever_6m_list_AL = list()
count_ever_6m_list_BL = list()
count_ever_6m_list_CC = list()
count_ever_6m_list_CD = list()
count_ever_6m_list_CV = list()
count_ever_6m_list_GL = list()
count_ever_6m_list_HL = list()
count_ever_6m_list_LAS = list()
count_ever_6m_list_MFBL = list()
count_ever_6m_list_MFHL = list()
count_ever_6m_list_MFOT = list()
count_ever_6m_list_OTH = list()
count_ever_6m_list_PL = list()
count_ever_6m_list_PLBL = list()
count_ever_6m_list_RL = list()
count_ever_6m_list_SCC = list()
count_ever_6m_list_SEL = list()

count_ever_6m_AL = 0
count_ever_6m_BL = 0
count_ever_6m_CC = 0
count_ever_6m_CD = 0
count_ever_6m_CV = 0
count_ever_6m_GL = 0
count_ever_6m_HL = 0
count_ever_6m_LAS = 0
count_ever_6m_MFBL = 0
count_ever_6m_MFHL = 0
count_ever_6m_MFOT = 0
count_ever_6m_OTH = 0
count_ever_6m_PL = 0
count_ever_6m_PLBL = 0
count_ever_6m_RL = 0
count_ever_6m_SCC = 0
count_ever_6m_SEL = 0

Ever_DPD1Y_AL = list()
Ever_DPD1Y_BL = list()
Ever_DPD1Y_CC = list()
Ever_DPD1Y_CD = list()
Ever_DPD1Y_CV = list()
Ever_DPD1Y_GL = list()
Ever_DPD1Y_HL = list()
Ever_DPD1Y_LAS = list()
Ever_DPD1Y_MFBL = list()
Ever_DPD1Y_MFHL = list()
Ever_DPD1Y_MFOT = list()
Ever_DPD1Y_OTH = list()
Ever_DPD1Y_PL = list()
Ever_DPD1Y_PLBL = list()
Ever_DPD1Y_RL = list()
Ever_DPD1Y_SCC = list()
Ever_DPD1Y_SEL = list()

count_ever_1y_list_AL = list()
count_ever_1y_list_BL = list()
count_ever_1y_list_CC = list()
count_ever_1y_list_CD = list()
count_ever_1y_list_CV = list()
count_ever_1y_list_GL = list()
count_ever_1y_list_HL = list()
count_ever_1y_list_LAS = list()
count_ever_1y_list_MFBL = list()
count_ever_1y_list_MFHL = list()
count_ever_1y_list_MFOT = list()
count_ever_1y_list_OTH = list()
count_ever_1y_list_PL = list()
count_ever_1y_list_PLBL = list()
count_ever_1y_list_RL = list()
count_ever_1y_list_SCC = list()
count_ever_1y_list_SEL = list()

count_ever_1y_AL = 0
count_ever_1y_BL = 0
count_ever_1y_CC = 0
count_ever_1y_CD = 0
count_ever_1y_CV = 0
count_ever_1y_GL = 0
count_ever_1y_HL = 0
count_ever_1y_LAS = 0
count_ever_1y_MFBL = 0
count_ever_1y_MFHL = 0
count_ever_1y_MFOT = 0
count_ever_1y_OTH = 0
count_ever_1y_PL = 0
count_ever_1y_PLBL = 0
count_ever_1y_RL = 0
count_ever_1y_SCC = 0
count_ever_1y_SEL = 0

Ever_DPD2Y_AL = list()
Ever_DPD2Y_BL = list()
Ever_DPD2Y_CC = list()
Ever_DPD2Y_CD = list()
Ever_DPD2Y_CV = list()
Ever_DPD2Y_GL = list()
Ever_DPD2Y_HL = list()
Ever_DPD2Y_LAS = list()
Ever_DPD2Y_MFBL = list()
Ever_DPD2Y_MFHL = list()
Ever_DPD2Y_MFOT = list()
Ever_DPD2Y_OTH = list()
Ever_DPD2Y_PL = list()
Ever_DPD2Y_PLBL = list()
Ever_DPD2Y_RL = list()
Ever_DPD2Y_SCC = list()
Ever_DPD2Y_SEL = list()

count_ever_2y_list_AL = list()
count_ever_2y_list_BL = list()
count_ever_2y_list_CC = list()
count_ever_2y_list_CD = list()
count_ever_2y_list_CV = list()
count_ever_2y_list_GL = list()
count_ever_2y_list_HL = list()
count_ever_2y_list_LAS = list()
count_ever_2y_list_MFBL = list()
count_ever_2y_list_MFHL = list()
count_ever_2y_list_MFOT = list()
count_ever_2y_list_OTH = list()
count_ever_2y_list_PL = list()
count_ever_2y_list_PLBL = list()
count_ever_2y_list_RL = list()
count_ever_2y_list_SCC = list()
count_ever_2y_list_SEL = list()

count_ever_2y_AL = 0
count_ever_2y_BL = 0
count_ever_2y_CC = 0
count_ever_2y_CD = 0
count_ever_2y_CV = 0
count_ever_2y_GL = 0
count_ever_2y_HL = 0
count_ever_2y_LAS = 0
count_ever_2y_MFBL = 0
count_ever_2y_MFHL = 0
count_ever_2y_MFOT = 0
count_ever_2y_OTH = 0
count_ever_2y_PL = 0
count_ever_2y_PLBL = 0
count_ever_2y_RL = 0
count_ever_2y_SCC = 0
count_ever_2y_SEL = 0

Ever_DPD3Y_AL = list()
Ever_DPD3Y_BL = list()
Ever_DPD3Y_CC = list()
Ever_DPD3Y_CD = list()
Ever_DPD3Y_CV = list()
Ever_DPD3Y_GL = list()
Ever_DPD3Y_HL = list()
Ever_DPD3Y_LAS = list()
Ever_DPD3Y_MFBL = list()
Ever_DPD3Y_MFHL = list()
Ever_DPD3Y_MFOT = list()
Ever_DPD3Y_OTH = list()
Ever_DPD3Y_PL = list()
Ever_DPD3Y_PLBL = list()
Ever_DPD3Y_RL = list()
Ever_DPD3Y_SCC = list()
Ever_DPD3Y_SEL = list()

count_ever_3y_list_AL = list()
count_ever_3y_list_BL = list()
count_ever_3y_list_CC = list()
count_ever_3y_list_CD = list()
count_ever_3y_list_CV = list()
count_ever_3y_list_GL = list()
count_ever_3y_list_HL = list()
count_ever_3y_list_LAS = list()
count_ever_3y_list_MFBL = list()
count_ever_3y_list_MFHL = list()
count_ever_3y_list_MFOT = list()
count_ever_3y_list_OTH = list()
count_ever_3y_list_PL = list()
count_ever_3y_list_PLBL = list()
count_ever_3y_list_RL = list()
count_ever_3y_list_SCC = list()
count_ever_3y_list_SEL = list()

count_ever_3y_AL = 0
count_ever_3y_BL = 0
count_ever_3y_CC = 0
count_ever_3y_CD = 0
count_ever_3y_CV = 0
count_ever_3y_GL = 0
count_ever_3y_HL = 0
count_ever_3y_LAS = 0
count_ever_3y_MFBL = 0
count_ever_3y_MFHL = 0
count_ever_3y_MFOT = 0
count_ever_3y_OTH = 0
count_ever_3y_PL = 0
count_ever_3y_PLBL = 0
count_ever_3y_RL = 0
count_ever_3y_SCC = 0
count_ever_3y_SEL = 0

Ever_DPD_Sec_L_1mnth = list()
count_dpd_ever_list_1m = list()
count_dpd_ever_1m = 0

Ever_DPD_Sec_L_3mnth = list()
count_dpd_ever_list_3m = list()
count_dpd_ever_3m = 0

Ever_DPD_Sec_L_6mnth = list()
count_dpd_ever_list_6m = list()
count_dpd_ever_6m = 0

Ever_DPD_Sec_L_1yr = list()
count_dpd_ever_list_1y = list()
count_dpd_ever_1y = 0

Ever_DPD_UnsecwoRLCC_L_1mnth = list()
count_dpd_ever_unsec_list_1m = list()
count_dpd_ever_unsec_1m = 0

Ever_DPD_UnsecwoRLCC_L_3mnth = list()
count_dpd_ever_unsec_list_3m = list()
count_dpd_ever_unsec_3m = 0

Ever_DPD_UnsecwoRLCC_L_6mnth = list()
count_dpd_ever_unsec_list_6m = list()
count_dpd_ever_unsec_6m = 0

Ever_DPD_UnsecwoRLCC_L_1yr = list()
count_dpd_ever_unsec_list_1y = list()
count_dpd_ever_unsec_1y = 0

grp_df = df.groupby('ID')

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    grp_slice.reset_index(drop=True, inplace=True)
    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_AL = count_ever_1m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_BL = count_ever_1m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_CC = count_ever_1m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_CD = count_ever_1m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_CV = count_ever_1m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_GL = count_ever_1m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_HL = count_ever_1m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_LAS = count_ever_1m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_MFBL = count_ever_1m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_MFHL = count_ever_1m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_MFOT = count_ever_1m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_OTH = count_ever_1m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_PL = count_ever_1m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_PLBL = count_ever_1m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_RL = count_ever_1m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_SCC = count_ever_1m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD1M_flag'][i] == 1):
            count_ever_1m_SEL = count_ever_1m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_AL = count_ever_3m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_BL = count_ever_3m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_CC = count_ever_3m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_CD = count_ever_3m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_CV = count_ever_3m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_GL = count_ever_3m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_HL = count_ever_3m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_LAS = count_ever_3m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_MFBL = count_ever_3m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_MFHL = count_ever_3m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_MFOT = count_ever_3m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_OTH = count_ever_3m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_PL = count_ever_3m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_PLBL = count_ever_3m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_RL = count_ever_3m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_SCC = count_ever_3m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD3M_flag'][i] == 1):
            count_ever_3m_SEL = count_ever_3m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_AL = count_ever_6m_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_BL = count_ever_6m_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_CC = count_ever_6m_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_CD = count_ever_6m_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_CV = count_ever_6m_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_GL = count_ever_6m_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_HL = count_ever_6m_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_LAS = count_ever_6m_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_MFBL = count_ever_6m_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_MFHL = count_ever_6m_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_MFOT = count_ever_6m_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_OTH = count_ever_6m_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_PL = count_ever_6m_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_PLBL = count_ever_6m_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_RL = count_ever_6m_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_SCC = count_ever_6m_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD6M_flag'][i] == 1):
            count_ever_6m_SEL = count_ever_6m_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_AL = count_ever_1y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_BL = count_ever_1y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_CC = count_ever_1y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_CD = count_ever_1y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_CV = count_ever_1y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_GL = count_ever_1y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_HL = count_ever_1y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_LAS = count_ever_1y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_MFBL = count_ever_1y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_MFHL = count_ever_1y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_MFOT = count_ever_1y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_OTH = count_ever_1y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_PL = count_ever_1y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_PLBL = count_ever_1y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_RL = count_ever_1y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_SCC = count_ever_1y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD1Y_flag'][i] == 1):
            count_ever_1y_SEL = count_ever_1y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_AL = count_ever_2y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_BL = count_ever_2y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_CC = count_ever_2y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_CD = count_ever_2y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_CV = count_ever_2y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_GL = count_ever_2y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_HL = count_ever_2y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_LAS = count_ever_2y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_MFBL = count_ever_2y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_MFHL = count_ever_2y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_MFOT = count_ever_2y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_OTH = count_ever_2y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_PL = count_ever_2y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_PLBL = count_ever_2y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_RL = count_ever_2y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_SCC = count_ever_2y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD2Y_flag'][i] == 1):
            count_ever_2y_SEL = count_ever_2y_SEL + 1

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            continue
        elif (grp_slice['dictAccountType'][i] == 'AL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_AL = count_ever_3y_AL + 1
        elif (grp_slice['dictAccountType'][i] == 'BL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_BL = count_ever_3y_BL + 1
        elif (grp_slice['dictAccountType'][i] == 'CC') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_CC = count_ever_3y_CC + 1
        elif (grp_slice['dictAccountType'][i] == 'CD') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_CD = count_ever_3y_CD + 1
        elif (grp_slice['dictAccountType'][i] == 'CV') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_CV = count_ever_3y_CV + 1
        elif (grp_slice['dictAccountType'][i] == 'GL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_GL = count_ever_3y_GL + 1
        elif (grp_slice['dictAccountType'][i] == 'HL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_HL = count_ever_3y_HL + 1
        elif (grp_slice['dictAccountType'][i] == 'LAS') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_LAS = count_ever_3y_LAS + 1
        elif (grp_slice['dictAccountType'][i] == 'MFBL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_MFBL = count_ever_3y_MFBL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFHL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_MFHL = count_ever_3y_MFHL + 1
        elif (grp_slice['dictAccountType'][i] == 'MFOT') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_MFOT = count_ever_3y_MFOT + 1
        elif (grp_slice['dictAccountType'][i] == 'OTH') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_OTH = count_ever_3y_OTH + 1
        elif (grp_slice['dictAccountType'][i] == 'PL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_PL = count_ever_3y_PL + 1
        elif (grp_slice['dictAccountType'][i] == 'PLBL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_PLBL = count_ever_3y_PLBL + 1
        elif (grp_slice['dictAccountType'][i] == 'RL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_RL = count_ever_3y_RL + 1
        elif (grp_slice['dictAccountType'][i] == 'SCC') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_SCC = count_ever_3y_SCC + 1
        elif (grp_slice['dictAccountType'][i] == 'SEL') and (grp_slice['Ever_DPD3Y_flag'][i] == 1):
            count_ever_3y_SEL = count_ever_3y_SEL + 1

        if (grp_slice['Ever_DPD_Sec_L_1mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_1mnth_flag'][i] == 0):
            count_dpd_ever_1m = count_dpd_ever_1m + \
                grp_slice['Ever_DPD_Sec_L_1mnth_flag'][i]

        if (grp_slice['Ever_DPD_Sec_L_3mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_3mnth_flag'][i] == 0):
            count_dpd_ever_3m = count_dpd_ever_3m + \
                grp_slice['Ever_DPD_Sec_L_3mnth_flag'][i]

        if (grp_slice['Ever_DPD_Sec_L_6mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_6mnth_flag'][i] == 0):
            count_dpd_ever_6m = count_dpd_ever_6m + \
                grp_slice['Ever_DPD_Sec_L_6mnth_flag'][i]

        if (grp_slice['Ever_DPD_Sec_L_1yr_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_1yr_flag'][i] == 0):
            count_dpd_ever_1y = count_dpd_ever_1y + \
                grp_slice['Ever_DPD_Sec_L_1yr_flag'][i]

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'][i] == 0):
            count_dpd_ever_unsec_1m = count_dpd_ever_unsec_1m + \
                grp_slice['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'][i]

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'][i] == 0):
            count_dpd_ever_unsec_3m = count_dpd_ever_unsec_3m + \
                grp_slice['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'][i]

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'][i] == 0):
            count_dpd_ever_unsec_6m = count_dpd_ever_unsec_6m + \
                grp_slice['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'][i]

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_1yr_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_1yr_flag'][i] == 0):
            count_dpd_ever_unsec_1y = count_dpd_ever_unsec_1y + \
                grp_slice['Ever_DPD_UnsecwoRLCC_L_1yr_flag'][i]

    count_ever_1m_list_AL.append(count_ever_1m_AL)
    count_ever_1m_list_BL.append(count_ever_1m_BL)
    count_ever_1m_list_CC.append(count_ever_1m_CC)
    count_ever_1m_list_CD.append(count_ever_1m_CD)
    count_ever_1m_list_CV.append(count_ever_1m_CV)
    count_ever_1m_list_GL.append(count_ever_1m_GL)
    count_ever_1m_list_HL.append(count_ever_1m_HL)
    count_ever_1m_list_LAS.append(count_ever_1m_LAS)
    count_ever_1m_list_MFBL.append(count_ever_1m_MFBL)
    count_ever_1m_list_MFHL.append(count_ever_1m_MFHL)
    count_ever_1m_list_MFOT.append(count_ever_1m_MFOT)
    count_ever_1m_list_OTH.append(count_ever_1m_OTH)
    count_ever_1m_list_PL.append(count_ever_1m_PL)
    count_ever_1m_list_PLBL.append(count_ever_1m_PLBL)
    count_ever_1m_list_RL.append(count_ever_1m_RL)
    count_ever_1m_list_SCC.append(count_ever_1m_SCC)
    count_ever_1m_list_SEL.append(count_ever_1m_SEL)

    count_ever_1m_AL = 0
    count_ever_1m_BL = 0
    count_ever_1m_CC = 0
    count_ever_1m_CD = 0
    count_ever_1m_CV = 0
    count_ever_1m_GL = 0
    count_ever_1m_HL = 0
    count_ever_1m_LAS = 0
    count_ever_1m_MFBL = 0
    count_ever_1m_MFHL = 0
    count_ever_1m_MFOT = 0
    count_ever_1m_OTH = 0
    count_ever_1m_PL = 0
    count_ever_1m_PLBL = 0
    count_ever_1m_RL = 0
    count_ever_1m_SCC = 0
    count_ever_1m_SEL = 0

    count_ever_3m_list_AL.append(count_ever_3m_AL)
    count_ever_3m_list_BL.append(count_ever_3m_BL)
    count_ever_3m_list_CC.append(count_ever_3m_CC)
    count_ever_3m_list_CD.append(count_ever_3m_CD)
    count_ever_3m_list_CV.append(count_ever_3m_CV)
    count_ever_3m_list_GL.append(count_ever_3m_GL)
    count_ever_3m_list_HL.append(count_ever_3m_HL)
    count_ever_3m_list_LAS.append(count_ever_3m_LAS)
    count_ever_3m_list_MFBL.append(count_ever_3m_MFBL)
    count_ever_3m_list_MFHL.append(count_ever_3m_MFHL)
    count_ever_3m_list_MFOT.append(count_ever_3m_MFOT)
    count_ever_3m_list_OTH.append(count_ever_3m_OTH)
    count_ever_3m_list_PL.append(count_ever_3m_PL)
    count_ever_3m_list_PLBL.append(count_ever_3m_PLBL)
    count_ever_3m_list_RL.append(count_ever_3m_RL)
    count_ever_3m_list_SCC.append(count_ever_3m_SCC)
    count_ever_3m_list_SEL.append(count_ever_3m_SEL)

    count_ever_3m_AL = 0
    count_ever_3m_BL = 0
    count_ever_3m_CC = 0
    count_ever_3m_CD = 0
    count_ever_3m_CV = 0
    count_ever_3m_GL = 0
    count_ever_3m_HL = 0
    count_ever_3m_LAS = 0
    count_ever_3m_MFBL = 0
    count_ever_3m_MFHL = 0
    count_ever_3m_MFOT = 0
    count_ever_3m_OTH = 0
    count_ever_3m_PL = 0
    count_ever_3m_PLBL = 0
    count_ever_3m_RL = 0
    count_ever_3m_SCC = 0
    count_ever_3m_SEL = 0

    count_ever_6m_list_AL.append(count_ever_6m_AL)
    count_ever_6m_list_BL.append(count_ever_6m_BL)
    count_ever_6m_list_CC.append(count_ever_6m_CC)
    count_ever_6m_list_CD.append(count_ever_6m_CD)
    count_ever_6m_list_CV.append(count_ever_6m_CV)
    count_ever_6m_list_GL.append(count_ever_6m_GL)
    count_ever_6m_list_HL.append(count_ever_6m_HL)
    count_ever_6m_list_LAS.append(count_ever_6m_LAS)
    count_ever_6m_list_MFBL.append(count_ever_6m_MFBL)
    count_ever_6m_list_MFHL.append(count_ever_6m_MFHL)
    count_ever_6m_list_MFOT.append(count_ever_6m_MFOT)
    count_ever_6m_list_OTH.append(count_ever_6m_OTH)
    count_ever_6m_list_PL.append(count_ever_6m_PL)
    count_ever_6m_list_PLBL.append(count_ever_6m_PLBL)
    count_ever_6m_list_RL.append(count_ever_6m_RL)
    count_ever_6m_list_SCC.append(count_ever_6m_SCC)
    count_ever_6m_list_SEL.append(count_ever_6m_SEL)

    count_ever_6m_AL = 0
    count_ever_6m_BL = 0
    count_ever_6m_CC = 0
    count_ever_6m_CD = 0
    count_ever_6m_CV = 0
    count_ever_6m_GL = 0
    count_ever_6m_HL = 0
    count_ever_6m_LAS = 0
    count_ever_6m_MFBL = 0
    count_ever_6m_MFHL = 0
    count_ever_6m_MFOT = 0
    count_ever_6m_OTH = 0
    count_ever_6m_PL = 0
    count_ever_6m_PLBL = 0
    count_ever_6m_RL = 0
    count_ever_6m_SCC = 0
    count_ever_6m_SEL = 0

    count_ever_1y_list_AL.append(count_ever_1y_AL)
    count_ever_1y_list_BL.append(count_ever_1y_BL)
    count_ever_1y_list_CC.append(count_ever_1y_CC)
    count_ever_1y_list_CD.append(count_ever_1y_CD)
    count_ever_1y_list_CV.append(count_ever_1y_CV)
    count_ever_1y_list_GL.append(count_ever_1y_GL)
    count_ever_1y_list_HL.append(count_ever_1y_HL)
    count_ever_1y_list_LAS.append(count_ever_1y_LAS)
    count_ever_1y_list_MFBL.append(count_ever_1y_MFBL)
    count_ever_1y_list_MFHL.append(count_ever_1y_MFHL)
    count_ever_1y_list_MFOT.append(count_ever_1y_MFOT)
    count_ever_1y_list_OTH.append(count_ever_1y_OTH)
    count_ever_1y_list_PL.append(count_ever_1y_PL)
    count_ever_1y_list_PLBL.append(count_ever_1y_PLBL)
    count_ever_1y_list_RL.append(count_ever_1y_RL)
    count_ever_1y_list_SCC.append(count_ever_1y_SCC)
    count_ever_1y_list_SEL.append(count_ever_1y_SEL)

    count_ever_1y_AL = 0
    count_ever_1y_BL = 0
    count_ever_1y_CC = 0
    count_ever_1y_CD = 0
    count_ever_1y_CV = 0
    count_ever_1y_GL = 0
    count_ever_1y_HL = 0
    count_ever_1y_LAS = 0
    count_ever_1y_MFBL = 0
    count_ever_1y_MFHL = 0
    count_ever_1y_MFOT = 0
    count_ever_1y_OTH = 0
    count_ever_1y_PL = 0
    count_ever_1y_PLBL = 0
    count_ever_1y_RL = 0
    count_ever_1y_SCC = 0
    count_ever_1y_SEL = 0

    count_ever_2y_list_AL.append(count_ever_2y_AL)
    count_ever_2y_list_BL.append(count_ever_2y_BL)
    count_ever_2y_list_CC.append(count_ever_2y_CC)
    count_ever_2y_list_CD.append(count_ever_2y_CD)
    count_ever_2y_list_CV.append(count_ever_2y_CV)
    count_ever_2y_list_GL.append(count_ever_2y_GL)
    count_ever_2y_list_HL.append(count_ever_2y_HL)
    count_ever_2y_list_LAS.append(count_ever_2y_LAS)
    count_ever_2y_list_MFBL.append(count_ever_2y_MFBL)
    count_ever_2y_list_MFHL.append(count_ever_2y_MFHL)
    count_ever_2y_list_MFOT.append(count_ever_2y_MFOT)
    count_ever_2y_list_OTH.append(count_ever_2y_OTH)
    count_ever_2y_list_PL.append(count_ever_2y_PL)
    count_ever_2y_list_PLBL.append(count_ever_2y_PLBL)
    count_ever_2y_list_RL.append(count_ever_2y_RL)
    count_ever_2y_list_SCC.append(count_ever_2y_SCC)
    count_ever_2y_list_SEL.append(count_ever_2y_SEL)

    count_ever_2y_AL = 0
    count_ever_2y_BL = 0
    count_ever_2y_CC = 0
    count_ever_2y_CD = 0
    count_ever_2y_CV = 0
    count_ever_2y_GL = 0
    count_ever_2y_HL = 0
    count_ever_2y_LAS = 0
    count_ever_2y_MFBL = 0
    count_ever_2y_MFHL = 0
    count_ever_2y_MFOT = 0
    count_ever_2y_OTH = 0
    count_ever_2y_PL = 0
    count_ever_2y_PLBL = 0
    count_ever_2y_RL = 0
    count_ever_2y_SCC = 0
    count_ever_2y_SEL = 0

    count_ever_3y_list_AL.append(count_ever_3y_AL)
    count_ever_3y_list_BL.append(count_ever_3y_BL)
    count_ever_3y_list_CC.append(count_ever_3y_CC)
    count_ever_3y_list_CD.append(count_ever_3y_CD)
    count_ever_3y_list_CV.append(count_ever_3y_CV)
    count_ever_3y_list_GL.append(count_ever_3y_GL)
    count_ever_3y_list_HL.append(count_ever_3y_HL)
    count_ever_3y_list_LAS.append(count_ever_3y_LAS)
    count_ever_3y_list_MFBL.append(count_ever_3y_MFBL)
    count_ever_3y_list_MFHL.append(count_ever_3y_MFHL)
    count_ever_3y_list_MFOT.append(count_ever_3y_MFOT)
    count_ever_3y_list_OTH.append(count_ever_3y_OTH)
    count_ever_3y_list_PL.append(count_ever_3y_PL)
    count_ever_3y_list_PLBL.append(count_ever_3y_PLBL)
    count_ever_3y_list_RL.append(count_ever_3y_RL)
    count_ever_3y_list_SCC.append(count_ever_3y_SCC)
    count_ever_3y_list_SEL.append(count_ever_3y_SEL)

    count_ever_3y_AL = 0
    count_ever_3y_BL = 0
    count_ever_3y_CC = 0
    count_ever_3y_CD = 0
    count_ever_3y_CV = 0
    count_ever_3y_GL = 0
    count_ever_3y_HL = 0
    count_ever_3y_LAS = 0
    count_ever_3y_MFBL = 0
    count_ever_3y_MFHL = 0
    count_ever_3y_MFOT = 0
    count_ever_3y_OTH = 0
    count_ever_3y_PL = 0
    count_ever_3y_PLBL = 0
    count_ever_3y_RL = 0
    count_ever_3y_SCC = 0
    count_ever_3y_SEL = 0

    count_dpd_ever_list_1m.append(count_dpd_ever_1m)
    count_dpd_ever_1m = 0
    count_dpd_ever_list_3m.append(count_dpd_ever_3m)
    count_dpd_ever_3m = 0
    count_dpd_ever_list_6m.append(count_dpd_ever_6m)
    count_dpd_ever_6m = 0
    count_dpd_ever_list_1y.append(count_dpd_ever_1y)
    count_dpd_ever_1y = 0

    count_dpd_ever_unsec_list_1m.append(count_dpd_ever_unsec_1m)
    count_dpd_ever_unsec_1m = 0
    count_dpd_ever_unsec_list_3m.append(count_dpd_ever_unsec_3m)
    count_dpd_ever_unsec_3m = 0
    count_dpd_ever_unsec_list_6m.append(count_dpd_ever_unsec_6m)
    count_dpd_ever_unsec_6m = 0
    count_dpd_ever_unsec_list_1y.append(count_dpd_ever_unsec_1y)
    count_dpd_ever_unsec_1y = 0

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['Ever_DPD_Sec_L_1mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_1mnth_flag'][i] == 0):
            Ever_DPD_Sec_L_1mnth.append(count_dpd_ever_list_1m[x])
        else:
            Ever_DPD_Sec_L_1mnth.append('unknown')

        if (grp_slice['Ever_DPD_Sec_L_3mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_3mnth_flag'][i] == 0):
            Ever_DPD_Sec_L_3mnth.append(count_dpd_ever_list_3m[x])
        else:
            Ever_DPD_Sec_L_3mnth.append('unknown')

        if (grp_slice['Ever_DPD_Sec_L_6mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_6mnth_flag'][i] == 0):
            Ever_DPD_Sec_L_6mnth.append(count_dpd_ever_list_6m[x])
        else:
            Ever_DPD_Sec_L_6mnth.append('unknown')

        if (grp_slice['Ever_DPD_Sec_L_1yr_flag'][i] == 1) or (grp_slice['Ever_DPD_Sec_L_1yr_flag'][i] == 0):
            Ever_DPD_Sec_L_1yr.append(count_dpd_ever_list_6m[x])
        else:
            Ever_DPD_Sec_L_1yr.append('unknown')

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_1mnth_flag'][i] == 0):
            Ever_DPD_UnsecwoRLCC_L_1mnth.append(
                count_dpd_ever_unsec_list_1m[x])
        else:
            Ever_DPD_UnsecwoRLCC_L_1mnth.append('unknown')

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_3mnth_flag'][i] == 0):
            Ever_DPD_UnsecwoRLCC_L_3mnth.append(
                count_dpd_ever_unsec_list_3m[x])
        else:
            Ever_DPD_UnsecwoRLCC_L_3mnth.append('unknown')

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_6mnth_flag'][i] == 0):
            Ever_DPD_UnsecwoRLCC_L_6mnth.append(
                count_dpd_ever_unsec_list_6m[x])
        else:
            Ever_DPD_UnsecwoRLCC_L_6mnth.append('unknown')

        if (grp_slice['Ever_DPD_UnsecwoRLCC_L_1yr_flag'][i] == 1) or (grp_slice['Ever_DPD_UnsecwoRLCC_L_1yr_flag'][i] == 0):
            Ever_DPD_UnsecwoRLCC_L_1yr.append(count_dpd_ever_unsec_list_6m[x])
        else:
            Ever_DPD_UnsecwoRLCC_L_1yr.append('unknown')

        if (grp_slice['dictAccountType'][i] == 'unknown'):
            Ever_DPD1M_AL.append('unknown')
            Ever_DPD1M_BL.append('unknown')
            Ever_DPD1M_CC.append('unknown')
            Ever_DPD1M_CD.append('unknown')
            Ever_DPD1M_CV.append('unknown')
            Ever_DPD1M_GL.append('unknown')
            Ever_DPD1M_HL.append('unknown')
            Ever_DPD1M_LAS.append('unknown')
            Ever_DPD1M_MFBL.append('unknown')
            Ever_DPD1M_MFHL.append('unknown')
            Ever_DPD1M_MFOT.append('unknown')
            Ever_DPD1M_OTH.append('unknown')
            Ever_DPD1M_PL.append('unknown')
            Ever_DPD1M_PLBL.append('unknown')
            Ever_DPD1M_RL.append('unknown')
            Ever_DPD1M_SCC.append('unknown')
            Ever_DPD1M_SEL.append('unknown')

            Ever_DPD3M_AL.append('unknown')
            Ever_DPD3M_BL.append('unknown')
            Ever_DPD3M_CC.append('unknown')
            Ever_DPD3M_CD.append('unknown')
            Ever_DPD3M_CV.append('unknown')
            Ever_DPD3M_GL.append('unknown')
            Ever_DPD3M_HL.append('unknown')
            Ever_DPD3M_LAS.append('unknown')
            Ever_DPD3M_MFBL.append('unknown')
            Ever_DPD3M_MFHL.append('unknown')
            Ever_DPD3M_MFOT.append('unknown')
            Ever_DPD3M_OTH.append('unknown')
            Ever_DPD3M_PL.append('unknown')
            Ever_DPD3M_PLBL.append('unknown')
            Ever_DPD3M_RL.append('unknown')
            Ever_DPD3M_SCC.append('unknown')
            Ever_DPD3M_SEL.append('unknown')

            Ever_DPD6M_AL.append('unknown')
            Ever_DPD6M_BL.append('unknown')
            Ever_DPD6M_CC.append('unknown')
            Ever_DPD6M_CD.append('unknown')
            Ever_DPD6M_CV.append('unknown')
            Ever_DPD6M_GL.append('unknown')
            Ever_DPD6M_HL.append('unknown')
            Ever_DPD6M_LAS.append('unknown')
            Ever_DPD6M_MFBL.append('unknown')
            Ever_DPD6M_MFHL.append('unknown')
            Ever_DPD6M_MFOT.append('unknown')
            Ever_DPD6M_OTH.append('unknown')
            Ever_DPD6M_PL.append('unknown')
            Ever_DPD6M_PLBL.append('unknown')
            Ever_DPD6M_RL.append('unknown')
            Ever_DPD6M_SCC.append('unknown')
            Ever_DPD6M_SEL.append('unknown')

            Ever_DPD1Y_AL.append('unknown')
            Ever_DPD1Y_BL.append('unknown')
            Ever_DPD1Y_CC.append('unknown')
            Ever_DPD1Y_CD.append('unknown')
            Ever_DPD1Y_CV.append('unknown')
            Ever_DPD1Y_GL.append('unknown')
            Ever_DPD1Y_HL.append('unknown')
            Ever_DPD1Y_LAS.append('unknown')
            Ever_DPD1Y_MFBL.append('unknown')
            Ever_DPD1Y_MFHL.append('unknown')
            Ever_DPD1Y_MFOT.append('unknown')
            Ever_DPD1Y_OTH.append('unknown')
            Ever_DPD1Y_PL.append('unknown')
            Ever_DPD1Y_PLBL.append('unknown')
            Ever_DPD1Y_RL.append('unknown')
            Ever_DPD1Y_SCC.append('unknown')
            Ever_DPD1Y_SEL.append('unknown')

            Ever_DPD2Y_AL.append('unknown')
            Ever_DPD2Y_BL.append('unknown')
            Ever_DPD2Y_CC.append('unknown')
            Ever_DPD2Y_CD.append('unknown')
            Ever_DPD2Y_CV.append('unknown')
            Ever_DPD2Y_GL.append('unknown')
            Ever_DPD2Y_HL.append('unknown')
            Ever_DPD2Y_LAS.append('unknown')
            Ever_DPD2Y_MFBL.append('unknown')
            Ever_DPD2Y_MFHL.append('unknown')
            Ever_DPD2Y_MFOT.append('unknown')
            Ever_DPD2Y_OTH.append('unknown')
            Ever_DPD2Y_PL.append('unknown')
            Ever_DPD2Y_PLBL.append('unknown')
            Ever_DPD2Y_RL.append('unknown')
            Ever_DPD2Y_SCC.append('unknown')
            Ever_DPD2Y_SEL.append('unknown')

            Ever_DPD3Y_AL.append('unknown')
            Ever_DPD3Y_BL.append('unknown')
            Ever_DPD3Y_CC.append('unknown')
            Ever_DPD3Y_CD.append('unknown')
            Ever_DPD3Y_CV.append('unknown')
            Ever_DPD3Y_GL.append('unknown')
            Ever_DPD3Y_HL.append('unknown')
            Ever_DPD3Y_LAS.append('unknown')
            Ever_DPD3Y_MFBL.append('unknown')
            Ever_DPD3Y_MFHL.append('unknown')
            Ever_DPD3Y_MFOT.append('unknown')
            Ever_DPD3Y_OTH.append('unknown')
            Ever_DPD3Y_PL.append('unknown')
            Ever_DPD3Y_PLBL.append('unknown')
            Ever_DPD3Y_RL.append('unknown')
            Ever_DPD3Y_SCC.append('unknown')
            Ever_DPD3Y_SEL.append('unknown')

        else:
            Ever_DPD1M_AL.append(count_ever_1m_list_AL[x])
            Ever_DPD1M_BL.append(count_ever_1m_list_BL[x])
            Ever_DPD1M_CC.append(count_ever_1m_list_CC[x])
            Ever_DPD1M_CD.append(count_ever_1m_list_CD[x])
            Ever_DPD1M_CV.append(count_ever_1m_list_CV[x])
            Ever_DPD1M_GL.append(count_ever_1m_list_GL[x])
            Ever_DPD1M_HL.append(count_ever_1m_list_HL[x])
            Ever_DPD1M_LAS.append(count_ever_1m_list_LAS[x])
            Ever_DPD1M_MFBL.append(count_ever_1m_list_MFBL[x])
            Ever_DPD1M_MFHL.append(count_ever_1m_list_MFHL[x])
            Ever_DPD1M_MFOT.append(count_ever_1m_list_MFOT[x])
            Ever_DPD1M_OTH.append(count_ever_1m_list_OTH[x])
            Ever_DPD1M_PL.append(count_ever_1m_list_PL[x])
            Ever_DPD1M_PLBL.append(count_ever_1m_list_PLBL[x])
            Ever_DPD1M_RL.append(count_ever_1m_list_RL[x])
            Ever_DPD1M_SCC.append(count_ever_1m_list_SCC[x])
            Ever_DPD1M_SEL.append(count_ever_1m_list_SEL[x])

            Ever_DPD3M_AL.append(count_ever_3m_list_AL[x])
            Ever_DPD3M_BL.append(count_ever_3m_list_BL[x])
            Ever_DPD3M_CC.append(count_ever_3m_list_CC[x])
            Ever_DPD3M_CD.append(count_ever_3m_list_CD[x])
            Ever_DPD3M_CV.append(count_ever_3m_list_CV[x])
            Ever_DPD3M_GL.append(count_ever_3m_list_GL[x])
            Ever_DPD3M_HL.append(count_ever_3m_list_HL[x])
            Ever_DPD3M_LAS.append(count_ever_3m_list_LAS[x])
            Ever_DPD3M_MFBL.append(count_ever_3m_list_MFBL[x])
            Ever_DPD3M_MFHL.append(count_ever_3m_list_MFHL[x])
            Ever_DPD3M_MFOT.append(count_ever_3m_list_MFOT[x])
            Ever_DPD3M_OTH.append(count_ever_3m_list_OTH[x])
            Ever_DPD3M_PL.append(count_ever_3m_list_PL[x])
            Ever_DPD3M_PLBL.append(count_ever_3m_list_PLBL[x])
            Ever_DPD3M_RL.append(count_ever_3m_list_RL[x])
            Ever_DPD3M_SCC.append(count_ever_3m_list_SCC[x])
            Ever_DPD3M_SEL.append(count_ever_3m_list_SEL[x])

            Ever_DPD6M_AL.append(count_ever_6m_list_AL[x])
            Ever_DPD6M_BL.append(count_ever_6m_list_BL[x])
            Ever_DPD6M_CC.append(count_ever_6m_list_CC[x])
            Ever_DPD6M_CD.append(count_ever_6m_list_CD[x])
            Ever_DPD6M_CV.append(count_ever_6m_list_CV[x])
            Ever_DPD6M_GL.append(count_ever_6m_list_GL[x])
            Ever_DPD6M_HL.append(count_ever_6m_list_HL[x])
            Ever_DPD6M_LAS.append(count_ever_6m_list_LAS[x])
            Ever_DPD6M_MFBL.append(count_ever_6m_list_MFBL[x])
            Ever_DPD6M_MFHL.append(count_ever_6m_list_MFHL[x])
            Ever_DPD6M_MFOT.append(count_ever_6m_list_MFOT[x])
            Ever_DPD6M_OTH.append(count_ever_6m_list_OTH[x])
            Ever_DPD6M_PL.append(count_ever_6m_list_PL[x])
            Ever_DPD6M_PLBL.append(count_ever_6m_list_PLBL[x])
            Ever_DPD6M_RL.append(count_ever_6m_list_RL[x])
            Ever_DPD6M_SCC.append(count_ever_6m_list_SCC[x])
            Ever_DPD6M_SEL.append(count_ever_6m_list_SEL[x])

            Ever_DPD1Y_AL.append(count_ever_1y_list_AL[x])
            Ever_DPD1Y_BL.append(count_ever_1y_list_BL[x])
            Ever_DPD1Y_CC.append(count_ever_1y_list_CC[x])
            Ever_DPD1Y_CD.append(count_ever_1y_list_CD[x])
            Ever_DPD1Y_CV.append(count_ever_1y_list_CV[x])
            Ever_DPD1Y_GL.append(count_ever_1y_list_GL[x])
            Ever_DPD1Y_HL.append(count_ever_1y_list_HL[x])
            Ever_DPD1Y_LAS.append(count_ever_1y_list_LAS[x])
            Ever_DPD1Y_MFBL.append(count_ever_1y_list_MFBL[x])
            Ever_DPD1Y_MFHL.append(count_ever_1y_list_MFHL[x])
            Ever_DPD1Y_MFOT.append(count_ever_1y_list_MFOT[x])
            Ever_DPD1Y_OTH.append(count_ever_1y_list_OTH[x])
            Ever_DPD1Y_PL.append(count_ever_1y_list_PL[x])
            Ever_DPD1Y_PLBL.append(count_ever_1y_list_PLBL[x])
            Ever_DPD1Y_RL.append(count_ever_1y_list_RL[x])
            Ever_DPD1Y_SCC.append(count_ever_1y_list_SCC[x])
            Ever_DPD1Y_SEL.append(count_ever_1y_list_SEL[x])

            Ever_DPD2Y_AL.append(count_ever_2y_list_AL[x])
            Ever_DPD2Y_BL.append(count_ever_2y_list_BL[x])
            Ever_DPD2Y_CC.append(count_ever_2y_list_CC[x])
            Ever_DPD2Y_CD.append(count_ever_2y_list_CD[x])
            Ever_DPD2Y_CV.append(count_ever_2y_list_CV[x])
            Ever_DPD2Y_GL.append(count_ever_2y_list_GL[x])
            Ever_DPD2Y_HL.append(count_ever_2y_list_HL[x])
            Ever_DPD2Y_LAS.append(count_ever_2y_list_LAS[x])
            Ever_DPD2Y_MFBL.append(count_ever_2y_list_MFBL[x])
            Ever_DPD2Y_MFHL.append(count_ever_2y_list_MFHL[x])
            Ever_DPD2Y_MFOT.append(count_ever_2y_list_MFOT[x])
            Ever_DPD2Y_OTH.append(count_ever_2y_list_OTH[x])
            Ever_DPD2Y_PL.append(count_ever_2y_list_PL[x])
            Ever_DPD2Y_PLBL.append(count_ever_2y_list_PLBL[x])
            Ever_DPD2Y_RL.append(count_ever_2y_list_RL[x])
            Ever_DPD2Y_SCC.append(count_ever_2y_list_SCC[x])
            Ever_DPD2Y_SEL.append(count_ever_2y_list_SEL[x])

            Ever_DPD3Y_AL.append(count_ever_3y_list_AL[x])
            Ever_DPD3Y_BL.append(count_ever_3y_list_BL[x])
            Ever_DPD3Y_CC.append(count_ever_3y_list_CC[x])
            Ever_DPD3Y_CD.append(count_ever_3y_list_CD[x])
            Ever_DPD3Y_CV.append(count_ever_3y_list_CV[x])
            Ever_DPD3Y_GL.append(count_ever_3y_list_GL[x])
            Ever_DPD3Y_HL.append(count_ever_3y_list_HL[x])
            Ever_DPD3Y_LAS.append(count_ever_3y_list_LAS[x])
            Ever_DPD3Y_MFBL.append(count_ever_3y_list_MFBL[x])
            Ever_DPD3Y_MFHL.append(count_ever_3y_list_MFHL[x])
            Ever_DPD3Y_MFOT.append(count_ever_3y_list_MFOT[x])
            Ever_DPD3Y_OTH.append(count_ever_3y_list_OTH[x])
            Ever_DPD3Y_PL.append(count_ever_3y_list_PL[x])
            Ever_DPD3Y_PLBL.append(count_ever_3y_list_PLBL[x])
            Ever_DPD3Y_RL.append(count_ever_3y_list_RL[x])
            Ever_DPD3Y_SCC.append(count_ever_3y_list_SCC[x])
            Ever_DPD3Y_SEL.append(count_ever_3y_list_SEL[x])

df['Ever_DPD1M_AL'] = pd.Series(Ever_DPD1M_AL).values
df['Ever_DPD1M_BL'] = pd.Series(Ever_DPD1M_BL).values
df['Ever_DPD1M_CC'] = pd.Series(Ever_DPD1M_CC).values
df['Ever_DPD1M_CD'] = pd.Series(Ever_DPD1M_CD).values
df['Ever_DPD1M_CV'] = pd.Series(Ever_DPD1M_CV).values
df['Ever_DPD1M_GL'] = pd.Series(Ever_DPD1M_GL).values
df['Ever_DPD1M_HL'] = pd.Series(Ever_DPD1M_HL).values
df['Ever_DPD1M_LAS'] = pd.Series(Ever_DPD1M_LAS).values
df['Ever_DPD1M_MFBL'] = pd.Series(Ever_DPD1M_MFBL).values
df['Ever_DPD1M_MFHL'] = pd.Series(Ever_DPD1M_MFHL).values
df['Ever_DPD1M_MFOT'] = pd.Series(Ever_DPD1M_MFOT).values
df['Ever_DPD1M_OTH'] = pd.Series(Ever_DPD1M_OTH).values
df['Ever_DPD1M_PL'] = pd.Series(Ever_DPD1M_PL).values
df['Ever_DPD1M_PLBL'] = pd.Series(Ever_DPD1M_PLBL).values
df['Ever_DPD1M_RL'] = pd.Series(Ever_DPD1M_RL).values
df['Ever_DPD1M_SCC'] = pd.Series(Ever_DPD1M_SCC).values
df['Ever_DPD1M_SEL'] = pd.Series(Ever_DPD1M_SEL).values

df['Ever_DPD3M_AL'] = pd.Series(Ever_DPD3M_AL).values
df['Ever_DPD3M_BL'] = pd.Series(Ever_DPD3M_BL).values
df['Ever_DPD3M_CC'] = pd.Series(Ever_DPD3M_CC).values
df['Ever_DPD3M_CD'] = pd.Series(Ever_DPD3M_CD).values
df['Ever_DPD3M_CV'] = pd.Series(Ever_DPD3M_CV).values
df['Ever_DPD3M_GL'] = pd.Series(Ever_DPD3M_GL).values
df['Ever_DPD3M_HL'] = pd.Series(Ever_DPD3M_HL).values
df['Ever_DPD3M_LAS'] = pd.Series(Ever_DPD3M_LAS).values
df['Ever_DPD3M_MFBL'] = pd.Series(Ever_DPD3M_MFBL).values
df['Ever_DPD3M_MFHL'] = pd.Series(Ever_DPD3M_MFHL).values
df['Ever_DPD3M_MFOT'] = pd.Series(Ever_DPD3M_MFOT).values
df['Ever_DPD3M_OTH'] = pd.Series(Ever_DPD3M_OTH).values
df['Ever_DPD3M_PL'] = pd.Series(Ever_DPD3M_PL).values
df['Ever_DPD3M_PLBL'] = pd.Series(Ever_DPD3M_PLBL).values
df['Ever_DPD3M_RL'] = pd.Series(Ever_DPD3M_RL).values
df['Ever_DPD3M_SCC'] = pd.Series(Ever_DPD3M_SCC).values
df['Ever_DPD3M_SEL'] = pd.Series(Ever_DPD3M_SEL).values

df['Ever_DPD6M_AL'] = pd.Series(Ever_DPD6M_AL).values
df['Ever_DPD6M_BL'] = pd.Series(Ever_DPD6M_BL).values
df['Ever_DPD6M_CC'] = pd.Series(Ever_DPD6M_CC).values
df['Ever_DPD6M_CD'] = pd.Series(Ever_DPD6M_CD).values
df['Ever_DPD6M_CV'] = pd.Series(Ever_DPD6M_CV).values
df['Ever_DPD6M_GL'] = pd.Series(Ever_DPD6M_GL).values
df['Ever_DPD6M_HL'] = pd.Series(Ever_DPD6M_HL).values
df['Ever_DPD6M_LAS'] = pd.Series(Ever_DPD6M_LAS).values
df['Ever_DPD6M_MFBL'] = pd.Series(Ever_DPD6M_MFBL).values
df['Ever_DPD6M_MFHL'] = pd.Series(Ever_DPD6M_MFHL).values
df['Ever_DPD6M_MFOT'] = pd.Series(Ever_DPD6M_MFOT).values
df['Ever_DPD6M_OTH'] = pd.Series(Ever_DPD6M_OTH).values
df['Ever_DPD6M_PL'] = pd.Series(Ever_DPD6M_PL).values
df['Ever_DPD6M_PLBL'] = pd.Series(Ever_DPD6M_PLBL).values
df['Ever_DPD6M_RL'] = pd.Series(Ever_DPD6M_RL).values
df['Ever_DPD6M_SCC'] = pd.Series(Ever_DPD6M_SCC).values
df['Ever_DPD6M_SEL'] = pd.Series(Ever_DPD6M_SEL).values

df['Ever_DPD1Y_AL'] = pd.Series(Ever_DPD1Y_AL).values
df['Ever_DPD1Y_BL'] = pd.Series(Ever_DPD1Y_BL).values
df['Ever_DPD1Y_CC'] = pd.Series(Ever_DPD1Y_CC).values
df['Ever_DPD1Y_CD'] = pd.Series(Ever_DPD1Y_CD).values
df['Ever_DPD1Y_CV'] = pd.Series(Ever_DPD1Y_CV).values
df['Ever_DPD1Y_GL'] = pd.Series(Ever_DPD1Y_GL).values
df['Ever_DPD1Y_HL'] = pd.Series(Ever_DPD1Y_HL).values
df['Ever_DPD1Y_LAS'] = pd.Series(Ever_DPD1Y_LAS).values
df['Ever_DPD1Y_MFBL'] = pd.Series(Ever_DPD1Y_MFBL).values
df['Ever_DPD1Y_MFHL'] = pd.Series(Ever_DPD1Y_MFHL).values
df['Ever_DPD1Y_MFOT'] = pd.Series(Ever_DPD1Y_MFOT).values
df['Ever_DPD1Y_OTH'] = pd.Series(Ever_DPD1Y_OTH).values
df['Ever_DPD1Y_PL'] = pd.Series(Ever_DPD1Y_PL).values
df['Ever_DPD1Y_PLBL'] = pd.Series(Ever_DPD1Y_PLBL).values
df['Ever_DPD1Y_RL'] = pd.Series(Ever_DPD1Y_RL).values
df['Ever_DPD1Y_SCC'] = pd.Series(Ever_DPD1Y_SCC).values
df['Ever_DPD1Y_SEL'] = pd.Series(Ever_DPD1Y_SEL).values

df['Ever_DPD2Y_AL'] = pd.Series(Ever_DPD2Y_AL).values
df['Ever_DPD2Y_BL'] = pd.Series(Ever_DPD2Y_BL).values
df['Ever_DPD2Y_CC'] = pd.Series(Ever_DPD2Y_CC).values
df['Ever_DPD2Y_CD'] = pd.Series(Ever_DPD2Y_CD).values
df['Ever_DPD2Y_CV'] = pd.Series(Ever_DPD2Y_CV).values
df['Ever_DPD2Y_GL'] = pd.Series(Ever_DPD2Y_GL).values
df['Ever_DPD2Y_HL'] = pd.Series(Ever_DPD2Y_HL).values
df['Ever_DPD2Y_LAS'] = pd.Series(Ever_DPD2Y_LAS).values
df['Ever_DPD2Y_MFBL'] = pd.Series(Ever_DPD2Y_MFBL).values
df['Ever_DPD2Y_MFHL'] = pd.Series(Ever_DPD2Y_MFHL).values
df['Ever_DPD2Y_MFOT'] = pd.Series(Ever_DPD2Y_MFOT).values
df['Ever_DPD2Y_OTH'] = pd.Series(Ever_DPD2Y_OTH).values
df['Ever_DPD2Y_PL'] = pd.Series(Ever_DPD2Y_PL).values
df['Ever_DPD2Y_PLBL'] = pd.Series(Ever_DPD2Y_PLBL).values
df['Ever_DPD2Y_RL'] = pd.Series(Ever_DPD2Y_RL).values
df['Ever_DPD2Y_SCC'] = pd.Series(Ever_DPD2Y_SCC).values
df['Ever_DPD2Y_SEL'] = pd.Series(Ever_DPD2Y_SEL).values

df['Ever_DPD3Y_AL'] = pd.Series(Ever_DPD3Y_AL).values
df['Ever_DPD3Y_BL'] = pd.Series(Ever_DPD3Y_BL).values
df['Ever_DPD3Y_CC'] = pd.Series(Ever_DPD3Y_CC).values
df['Ever_DPD3Y_CD'] = pd.Series(Ever_DPD3Y_CD).values
df['Ever_DPD3Y_CV'] = pd.Series(Ever_DPD3Y_CV).values
df['Ever_DPD3Y_GL'] = pd.Series(Ever_DPD3Y_GL).values
df['Ever_DPD3Y_HL'] = pd.Series(Ever_DPD3Y_HL).values
df['Ever_DPD3Y_LAS'] = pd.Series(Ever_DPD3Y_LAS).values
df['Ever_DPD3Y_MFBL'] = pd.Series(Ever_DPD3Y_MFBL).values
df['Ever_DPD3Y_MFHL'] = pd.Series(Ever_DPD3Y_MFHL).values
df['Ever_DPD3Y_MFOT'] = pd.Series(Ever_DPD3Y_MFOT).values
df['Ever_DPD3Y_OTH'] = pd.Series(Ever_DPD3Y_OTH).values
df['Ever_DPD3Y_PL'] = pd.Series(Ever_DPD3Y_PL).values
df['Ever_DPD3Y_PLBL'] = pd.Series(Ever_DPD3Y_PLBL).values
df['Ever_DPD3Y_RL'] = pd.Series(Ever_DPD3Y_RL).values
df['Ever_DPD3Y_SCC'] = pd.Series(Ever_DPD3Y_SCC).values
df['Ever_DPD3Y_SEL'] = pd.Series(Ever_DPD3Y_SEL).values

df['Ever_DPD_Sec_L_1mnth'] = pd.Series(Ever_DPD_Sec_L_1mnth).values
df['Ever_DPD_Sec_L_3mnth'] = pd.Series(Ever_DPD_Sec_L_3mnth).values
df['Ever_DPD_Sec_L_6mnth'] = pd.Series(Ever_DPD_Sec_L_6mnth).values
df['Ever_DPD_Sec_L_1yr'] = pd.Series(Ever_DPD_Sec_L_1yr).values

df['Ever_DPD_UnsecwoRLCC_L_1mnth'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_1mnth).values
df['Ever_DPD_UnsecwoRLCC_L_3mnth'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_3mnth).values
df['Ever_DPD_UnsecwoRLCC_L_6mnth'] = pd.Series(
    Ever_DPD_UnsecwoRLCC_L_6mnth).values
df['Ever_DPD_UnsecwoRLCC_L_1yr'] = pd.Series(Ever_DPD_UnsecwoRLCC_L_1yr).values

# Time ends
print("%s seconds" % (time.time() - start_time_ut))
