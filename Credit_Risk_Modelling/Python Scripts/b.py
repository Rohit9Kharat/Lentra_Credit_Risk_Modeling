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

grp_df = df.groupby('ID')

for x in range(0, len(unq_id_list)):
    grp_slice = grp_df.get_group(unq_id_list[x])
    # print(grp_slice)
    grp_slice.reset_index(drop=True, inplace=True)
    for i in range(0, grp_slice.shape[0]):
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

    for i in range(0, grp_slice.shape[0]):
        if (grp_slice['dictAccountType'][i] == 'unknown') or (grp_slice['writeOff'][i] == 'unknown'):
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
