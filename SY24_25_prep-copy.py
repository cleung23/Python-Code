import numpy as np
import os
import pandas as pd
from pandas import read_csv
from pandas.core.common import flatten
import datetime as dt
from datetime import timedelta
import calendar
import csv

StartDate = pd.to_datetime("1st of July, 2021")
EndDate = pd.to_datetime(dt.date.today()) + pd.DateOffset(months=1)
SYBeginDate = pd.to_datetime("30th of June, 2024")


def first_day_of_month(start, end):
    dates = pd.date_range(StartDate, EndDate, freq='1M') - pd.offsets.MonthBegin(1)  # Create a list of first days of the month
    return dates.to_frame(index=False, name='FirstDate') #returns a dataframe with first day as column



def last_day_of_month(table):
    table['MonthEndDate'] = table['FirstDate'].apply(lambda x: ((x.replace(day=28) + timedelta(days=4)) - timedelta(days=(x.replace(day=28) + timedelta(days=4)).day)))
    #table = table.drop(['FirstDate'], axis=1)
    return table

def get_school_year(DateTable_All):
    DateTable_All['MonthEndDate'] = pd.to_datetime(DateTable_All["MonthEndDate"]).dt.strftime('%m/%d/%y')
    DateTable_All['MonthNum'] = pd.DatetimeIndex(DateTable_All['MonthEndDate']).month
    DateTable_All['Year'] = pd.DatetimeIndex(DateTable_All['MonthEndDate']).year
    SY = []
    for i, row in DateTable_All.iterrows():
        yr = DateTable_All.iat[i, 3]
        m = DateTable_All.iat[i, 2]
        if m < 7:
            sy = yr - 1
        else:
            sy = yr
        SY.append(sy)
    DateTable_All['School_Year'] = SY
    return DateTable_All

def get_datetable_ready(DateTable_AllCol):
    DateTable_AllCol['Month_Name'] = DateTable_AllCol['MonthNum'].apply(lambda x:calendar.month_abbr[x])
    conv = {1:'Q3', 2:'Q3', 3:'Q3', 4:'Q4', 5:'Q4', 6:'Q4', 7:'Q1', 8:'Q1', 9:'Q1', 10:'Q2', 11:'Q2', 12:'Q2'}
    DateTable_AllCol['Quarter'] = DateTable_AllCol.MonthNum.map(conv)
    DateTable_AllCol['Order'] = DateTable_AllCol['MonthNum'].apply(lambda x:x - 6 if x >= 7 else x + 6)
    DateTable_AllCol['Year_Q'] = DateTable_AllCol['School_Year'].astype(str) + DateTable_AllCol['Quarter']
    Today = pd.to_datetime(dt.date.today())
    DateTable_AllCol['FirstDate'] = pd.to_datetime(DateTable_AllCol["FirstDate"])
    DateTable_AllRow = DateTable_AllCol[['MonthEndDate', 'Month_Name', 'Quarter', 'Year_Q', 'School_Year', 'Order']]
    DateTable_Current = DateTable_AllRow.loc[(DateTable_AllCol['FirstDate'] > SYBeginDate)]
    DateTable_Current = DateTable_Current[['MonthEndDate']]
    DateTable_AllRow.to_csv(
        "/Users/hleung/OneDrive - Children's Home Society of Florida/Dashboard2024/DateTable_AllRow.csv",
        index=False)

    return DateTable_Current

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def get_column_num(SYBeginDate):
    #Identify month end columns from Weekly Tracker
    cols_7 = [10]
    cols_8 = [16]
    cols_9 = [23]
    cols_10 = [31]
    cols_11 = [37]
    cols_12 = [44]
    cols_1 = [52]
    cols_2 = [58]
    cols_3 = [65]
    cols_4 = [73]
    cols_5 = [79]
    cols_6 = [86]
    all_months = cols_7 + cols_8 + cols_9 + cols_10 + cols_11 + cols_12 + cols_1 + cols_2 + cols_3 + cols_4 + cols_5 + cols_6
    Today = pd.to_datetime(dt.date.today())
    a = diff_month(Today, SYBeginDate)

    return all_months[:a]


def get_current_data(DateTable):
    directory = r"/Users/....."
    All = pd.DataFrame()
    Target_all = pd.DataFrame()
    School_Pop = pd.DataFrame()
    Pop = []
    Name = []

    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath, engine='openpyxl')
            filename, ext = filepath.rsplit('.', maxsplit=1)
            name = filename.split('/')[-1]
            pop = df.iat[5, 3]
            MonthEndDate = DateTable['MonthEndDate'].tolist()

            enrich_undup = []
            enrich_s = []
            enrich_hr = []
            tut_undup = []
            tut_s = []
            tut_hr = []
            one_event = []
            ongo_event = []
            vol_undup = []
            vol_hr = []
            men_undup = []
            men_hr = []
            br_s = []
            bs_undups = []
            bs_alls = []
            br_f = []
            bs_undupf = []
            bs_allf = []
            dr_s = []
            ds_undups = []
            ds_alls = []
            dr_f = []
            ds_undupf = []
            ds_allf = []
            vr_s = []
            vs_undups = []
            vs_alls = []
            vr_f = []
            vs_undupf = []
            vs_allf = []
            pr_s = []
            ps_undups = []
            ps_alls = []
            pr_f = []
            ps_undupf = []
            ps_allf = []
            rc_s = []
            rc_f = []

            for x in DateTable['ColNo']:
                eu = df.iat[8, x]
                enrich_undup.append(eu)
                es = df.iat[9, x]
                enrich_s.append(es)
                eh = df.iat[10, x]
                enrich_hr.append(eh)
                tu = df.iat[12, x]
                tut_undup.append(tu)
                ts = df.iat[13, x]
                tut_s.append(ts)
                th = df.iat[14, x]
                tut_hr.append(th)
                oe = df.iat[18, x]
                one_event.append(oe)
                ongoe = df.iat[19, x]
                ongo_event.append(ongoe)
                vu = df.iat[21, x]
                vol_undup.append(vu)
                vh = df.iat[22, x]
                vol_hr.append(vh)
                mu = df.iat[23, x]
                men_undup.append(mu)
                mh = df.iat[24, x]
                men_hr.append(mh)
                brs = df.iat[28, x]
                br_s.append(brs)
                bsu = df.iat[32, x]
                bs_undups.append(bsu)
                bsa = df.iat[33, x]
                bs_alls.append(bsa)
                brf = df.iat[35, x]
                br_f.append(brf)
                bsuf = df.iat[39, x]
                bs_undupf.append(bsuf)
                bsf = df.iat[40, x]
                bs_allf.append(bsf)
                drs = df.iat[43, x]
                dr_s.append(drs)
                dsu = df.iat[47, x]
                ds_undups.append(dsu)
                dsa = df.iat[48, x]
                ds_alls.append(dsa)
                drf = df.iat[50, x]
                dr_f.append(drf)
                dsuf = df.iat[54, x]
                ds_undupf.append(dsuf)
                dsf = df.iat[55, x]
                ds_allf.append(dsf)
                vrs = df.iat[58, x]
                vr_s.append(vrs)
                vsu = df.iat[62, x]
                vs_undups.append(vsu)
                vsa = df.iat[63, x]
                vs_alls.append(vsa)
                vrf = df.iat[65, x]
                vr_f.append(vrf)
                vsuf = df.iat[69, x]
                vs_undupf.append(vsuf)
                vsf = df.iat[70, x]
                vs_allf.append(vsf)
                prs = df.iat[73, x]
                pr_s.append(prs)
                psu = df.iat[77, x]
                ps_undups.append(psu)
                psa = df.iat[78, x]
                ps_alls.append(psa)
                prf = df.iat[80, x]
                pr_f.append(prf)
                psuf = df.iat[84, x]
                ps_undupf.append(psuf)
                psf = df.iat[85, x]
                ps_allf.append(psf)
                rcs = df.iat[88, x]
                rc_s.append(rcs)
                rcf = df.iat[96, x]
                rc_f.append(rcf)

            Enrich_U = pd.DataFrame(np.column_stack([MonthEndDate, enrich_undup]), columns=['MonthEndDate', 'Num'])
            Enrich_U['Desc'] = 'Enrich_Undup_S'
            Enrich_S = pd.DataFrame(np.column_stack([MonthEndDate, enrich_s]), columns=['MonthEndDate', 'Num'])
            Enrich_S['Desc'] = 'Enrich_S'
            Enrich_Hr = pd.DataFrame(np.column_stack([MonthEndDate, enrich_hr]), columns=['MonthEndDate', 'Hr'])
            Enrich_Hr['Desc'] = 'Enrich_Hr'
            Tut_U = pd.DataFrame(np.column_stack([MonthEndDate, tut_undup]), columns=['MonthEndDate', 'Num'])
            Tut_U['Desc'] = 'Tut_Undup_S'
            Tut_S = pd.DataFrame(np.column_stack([MonthEndDate, tut_s]), columns=['MonthEndDate', 'Num'])
            Tut_S['Desc'] = 'Tut_S'
            Tut_Hr = pd.DataFrame(np.column_stack([MonthEndDate, tut_hr]), columns=['MonthEndDate', 'Hr'])
            Tut_Hr['Desc'] = 'Tut_Hr'

            One_Event = pd.DataFrame(np.column_stack([MonthEndDate, one_event]), columns=['MonthEndDate', 'Event'])
            One_Event['Desc'] = 'OneTime_Event'
            On_Event = pd.DataFrame(np.column_stack([MonthEndDate, ongo_event]), columns=['MonthEndDate', 'Event'])
            On_Event['Desc'] = 'OnGoing_Event'
            Vol_U = pd.DataFrame(np.column_stack([MonthEndDate, vol_undup]), columns=['MonthEndDate', 'Num'])
            Vol_U['Desc'] = 'Vol_Undup'
            Vol_Hr = pd.DataFrame(np.column_stack([MonthEndDate, vol_hr]), columns=['MonthEndDate', 'Hr'])
            Vol_Hr['Desc'] = 'Vol_Hr'
            Men_U = pd.DataFrame(np.column_stack([MonthEndDate, men_undup]), columns=['MonthEndDate', 'Num'])
            Men_U['Desc'] = 'Mentor_Undup'
            Men_Hr = pd.DataFrame(np.column_stack([MonthEndDate, men_hr]), columns=['MonthEndDate', 'Hr'])
            Men_Hr['Desc'] = 'Mentor_Hr'

            Br_S = pd.DataFrame(np.column_stack([MonthEndDate, br_s]), columns=['MonthEndDate', 'Num'])
            Br_S['Desc'] = 'Beh_Ref_S'
            Bs_US = pd.DataFrame(np.column_stack([MonthEndDate, bs_undups]), columns=['MonthEndDate', 'Num'])
            Bs_US['Desc'] = 'Beh_Ser_Undup_S'
            Bs_Alls = pd.DataFrame(np.column_stack([MonthEndDate, bs_alls]), columns=['MonthEndDate', 'Num'])
            Bs_Alls['Desc'] = 'Beh_Ser_All_S'
            Br_Allf = pd.DataFrame(np.column_stack([MonthEndDate, br_f]), columns=['MonthEndDate', 'Num'])
            Br_Allf['Desc'] = 'Beh_Ref_All_F'
            Bs_Uf = pd.DataFrame(np.column_stack([MonthEndDate, bs_undupf]), columns=['MonthEndDate', 'Num'])
            Bs_Uf['Desc'] = 'Beh_Ser_Undup_F'
            Bs_Allf = pd.DataFrame(np.column_stack([MonthEndDate, bs_allf]), columns=['MonthEndDate', 'Num'])
            Bs_Allf['Desc'] = 'Beh_Ser_All_F'

            Dr_S = pd.DataFrame(np.column_stack([MonthEndDate, dr_s]), columns=['MonthEndDate', 'Num'])
            Dr_S['Desc'] = 'Dental_Ref_S'
            Ds_US = pd.DataFrame(np.column_stack([MonthEndDate, ds_undups]), columns=['MonthEndDate', 'Num'])
            Ds_US['Desc'] = 'Dental_Ser_Undup_S'
            Ds_Alls = pd.DataFrame(np.column_stack([MonthEndDate, ds_alls]), columns=['MonthEndDate', 'Num'])
            Ds_Alls['Desc'] = 'Dental_Ser_All_S'
            Dr_Allf = pd.DataFrame(np.column_stack([MonthEndDate, dr_f]), columns=['MonthEndDate', 'Num'])
            Dr_Allf['Desc'] = 'Dental_Ref_All_F'
            Ds_Uf = pd.DataFrame(np.column_stack([MonthEndDate, ds_undupf]), columns=['MonthEndDate', 'Num'])
            Ds_Uf['Desc'] = 'Dental_Ser_Undup_F'
            Ds_Allf = pd.DataFrame(np.column_stack([MonthEndDate, ds_allf]), columns=['MonthEndDate', 'Num'])
            Ds_Allf['Desc'] = 'Dental_Ser_All_F'

            Vr_S = pd.DataFrame(np.column_stack([MonthEndDate, vr_s]), columns=['MonthEndDate', 'Num'])
            Vr_S['Desc'] = 'Vision_Ref_S'
            Vs_US = pd.DataFrame(np.column_stack([MonthEndDate, vs_undups]), columns=['MonthEndDate', 'Num'])
            Vs_US['Desc'] = 'Vision_Ser_Undup_S'
            Vs_Alls = pd.DataFrame(np.column_stack([MonthEndDate, vs_alls]), columns=['MonthEndDate', 'Num'])
            Vs_Alls['Desc'] = 'Vision_Ser_All_S'
            Vr_Allf = pd.DataFrame(np.column_stack([MonthEndDate, vr_f]), columns=['MonthEndDate', 'Num'])
            Vr_Allf['Desc'] = 'Vision_Ref_All_F'
            Vs_Uf = pd.DataFrame(np.column_stack([MonthEndDate, vs_undupf]), columns=['MonthEndDate', 'Num'])
            Vs_Uf['Desc'] = 'Vision_Ser_Undup_F'
            Vs_Allf = pd.DataFrame(np.column_stack([MonthEndDate, vs_allf]), columns=['MonthEndDate', 'Num'])
            Vs_Allf['Desc'] = 'Vision_Ser_All_F'

            Pr_S = pd.DataFrame(np.column_stack([MonthEndDate, pr_s]), columns=['MonthEndDate', 'Num'])
            Pr_S['Desc'] = 'PC_Ref_S'
            Ps_US = pd.DataFrame(np.column_stack([MonthEndDate, ps_undups]), columns=['MonthEndDate', 'Num'])
            Ps_US['Desc'] = 'PC_Ser_Undup_S'
            Ps_Alls = pd.DataFrame(np.column_stack([MonthEndDate, ps_alls]), columns=['MonthEndDate', 'Num'])
            Ps_Alls['Desc'] = 'PC_Ser_All_S'
            Pr_Allf = pd.DataFrame(np.column_stack([MonthEndDate, pr_f]), columns=['MonthEndDate', 'Num'])
            Pr_Allf['Desc'] = 'PC_Ref_All_F'
            Ps_Uf = pd.DataFrame(np.column_stack([MonthEndDate, ps_undupf]), columns=['MonthEndDate', 'Num'])
            Ps_Uf['Desc'] = 'PC_Ser_Undup_F'
            Ps_Allf = pd.DataFrame(np.column_stack([MonthEndDate, ps_allf]), columns=['MonthEndDate', 'Num'])
            Ps_Allf['Desc'] = 'PC_Ser_All_F'

            RC_S = pd.DataFrame(np.column_stack([MonthEndDate, rc_s]), columns=['MonthEndDate', 'Num'])
            RC_S['Desc'] = 'RC_S'
            RC_F = pd.DataFrame(np.column_stack([MonthEndDate, rc_f]), columns=['MonthEndDate', 'Num'])
            RC_F['Desc'] = 'RC_F'

            df1 = pd.concat([Enrich_S, Enrich_U, Enrich_Hr, Tut_S, Tut_U, Tut_Hr, One_Event, On_Event,
                                     Vol_U, Vol_Hr, Men_U, Men_Hr, Bs_Alls, Bs_US, Br_S, Br_Allf, Bs_Allf, Bs_Uf,
                                     Ds_Alls, Dr_Allf,
                                     Dr_S, Ds_Allf, Ds_Uf, Ds_US, Vs_Alls, Vs_Uf, Vr_Allf, Vr_S, Vs_Allf, Vs_US,
                                     Ps_Alls,
                                     Pr_Allf, Ps_Uf, Ps_Allf,
                                     Ps_US, Pr_S, RC_S, RC_F], axis=0)

            df1 = df1.replace(np.nan, 0)
            df1 = df1.replace('\xa0', 0)
            df1 = df1.replace('nan', 0)
            df1 = df1.replace('0.0', 0)
            df1['Num'] = df1['Num'].astype(float)
            df1['School'] = name

            All = pd.concat([All, df1], axis=0)

            Target = []
            RowNum = [8, 10, 12, 14, 21, 22, 23, 24, 32, 33, 47, 48, 62, 63, 77, 78]

            for i in RowNum:
                t = df.iat[i, 2]
                Target.append(t)

            Desc = ['Enrich_Undup_S', 'Enrich_Hr', 'Tut_Undup_S', 'Tut_Hr', 'Vol_Undup', 'Vol_Hr', 'Mentor_Undup',
                    'Mentor_Hr',
                    'Beh_Ser_Undup_S', 'Beh_Ser_All_S', 'Dental_Ser_Undup_S', 'Dental_Ser_All_S',
                    'Vision_Ser_Undup_S', 'Vision_Ser_All_S', 'PC_Ser_Undup_S', 'PC_Ser_All_S']

            Target_df = pd.DataFrame(np.column_stack([Desc, Target]), columns=['Desc', 'Target'])
            Target_df['School'] = name
            Target_all = pd.concat([Target_all, Target_df], axis=0)

        # Extracting Population
        Pop.append(pop)
        Name.append(name)
    All['MonthEndDate'] = pd.to_datetime(All['MonthEndDate'])

    return All, Target_all, Pop, Name

def get_past_data():
    School_Pop_Hist = read_csv("/Users....v", header=0)
    Event_agg_all = read_csv("/Users/.....", header=0)
    Hour_agg_all = read_csv("/Users/.....", header=0)
    Number_agg_all = read_csv("/Users/.....", header=0)
    Expand_avg_all = read_csv("/Users/.....", header=0)

    return School_Pop_Hist, Event_agg_all, Hour_agg_all, Number_agg_all, Expand_avg_all

def get_avg_attendance(All):
    labels = ['Enrich_S', 'Tut_S']
    Expand_avg = pd.DataFrame()

    for x in labels:
        EnrichCount = pd.DataFrame()
        df = pd.DataFrame()
        EnrichCount = All[(All['Desc'] == x) & (All['Num'] > 0)]
        EnrichCount = EnrichCount.groupby(['School', 'MonthEndDate'])[["Num"]].agg('mean')
        EnrichCount = EnrichCount.reset_index()

        Steps = All['MonthEndDate'].nunique()
        school_name = []
        school = All.School.unique()
        for i in range(All['School'].nunique()):
            s = np.repeat(school[i], Steps)
            school_name.append(s)
            school_name = list(flatten(school_name))

        MonthEndDate = All.MonthEndDate.unique()
        month = np.repeat(MonthEndDate[None, :], All['School'].nunique(), axis=0).reshape(len(school_name))
        month = list(flatten(month))
        month = pd.to_datetime(month)
        month = month.strftime("%Y-%m-%d").tolist()

        df = pd.DataFrame(np.column_stack([school_name, month]),
                          columns=['School', 'MonthEndDate'])
        df['MonthEndDate'] = pd.to_datetime(month)
        df = pd.merge(df, EnrichCount, left_on=['School', 'MonthEndDate'], right_on=['School', 'MonthEndDate'],
                      how='left')
        df['Desc'] = x
        Expand_avg = pd.concat([Expand_avg, df], axis=0)

    Expand_avg = Expand_avg.replace(np.nan, 0)
    Expand_avg = Expand_avg[['School', 'Desc', 'MonthEndDate', 'Num']]

    return Expand_avg


def combine_new_and_old_data(All, Event_agg_all, Hour_agg_all, Number_agg_all, Expand_avg_all, Expand_avg):
    #Combine 2 years data
    Event = All[(All['Desc'] == 'OnGoing_Event')|(All['Desc'] == 'OneTime_Event')]
    Event_agg = Event.groupby(['School', 'Desc', 'MonthEndDate'])['Event'].aggregate('sum')
    Event_agg = Event_agg.reset_index()
    Event_agg_all = pd.concat([Event_agg, Event_agg_all], axis=0)
    Event_agg_all['MonthEndDate'] = pd.to_datetime(Event_agg_all['MonthEndDate'])
    Event_agg_all = Event_agg_all.sort_values(by = ['School', 'Desc', 'MonthEndDate'], axis=0, ignore_index=True, key=None)

    Hours = All[(All['Desc'] == 'Enrich_Hr')|(All['Desc'] == 'Tut_Hr')|(All['Desc'] == 'Vol_Hr')|(All['Desc'] == 'Mentor_Hr')]
    Hours_agg = Hours.groupby(['School', 'Desc', 'MonthEndDate'])['Hr'].aggregate('sum')
    Hours_agg = Hours_agg.reset_index()
    Hours_agg_all = pd.concat([Hours_agg, Hour_agg_all], axis=0)
    Hours_agg_all['MonthEndDate'] = pd.to_datetime(Hours_agg_all['MonthEndDate'])
    Hours_agg_all = Hours_agg_all.sort_values(by = ['School', 'Desc', 'MonthEndDate'], axis=0, ignore_index=True, key=None)

    desclist = ['Enrich_S', 'Enrich_Undup_S', 'Tut_S', 'Tut_Undup_S', 'Vol_Undup',
                'Mentor_Undup', 'Beh_Ser_All_S', 'Beh_Ser_Undup_S', 'Beh_Ref_S', 'Beh_Ref_All_F', 'Beh_Ser_All_F',
                'Beh_Ser_Undup_F', 'Dental_Ser_All_S', 'Dental_Ser_Undup_S', 'Dental_Ref_S', 'Dental_Ref_All_F',
                'Dental_Ser_All_F', 'Dental_Ser_Undup_F', 'Vision_Ser_All_S', 'Vision_Ser_Undup_S', 'Vision_Ref_S', 'Vision_Ref_All_F',
                'Vision_Ser_All_F', 'Vision_Ser_Undup_F', 'PC_Ser_All_S', 'PC_Ser_Undup_S', 'PC_Ref_S', 'PC_Ref_All_F',
                'PC_Ser_All_F', 'PC_Ser_Undup_F']

    Number = All[All['Desc'].isin(desclist)]
    Number_agg = Number.groupby(['School', 'Desc', 'MonthEndDate'])['Num'].aggregate('sum')
    Number_agg = Number_agg.reset_index()
    Number_agg_all = pd.concat([Number_agg, Number_agg_all], axis=0)
    Number_agg_all['MonthEndDate'] = pd.to_datetime(Number_agg_all['MonthEndDate'])
    Number_agg_all = Number_agg_all.sort_values(by = ['School', 'Desc', 'MonthEndDate'], axis=0, ignore_index=True, key=None)

    Expand_avg_all = pd.concat([Expand_avg, Expand_avg_all], axis=0)
    Expand_avg_all['MonthEndDate'] = pd.to_datetime(Expand_avg_all['MonthEndDate'])
    Expand_avg_all = Expand_avg_all.sort_values(by = ['School', 'Desc', 'MonthEndDate'], axis=0, ignore_index=True, key=None)

    Event_agg_all.to_csv("/Users/.....",
                         index=False)
    Hours_agg_all.to_csv("/Users/....",
                         index=False)
    Number_agg_all.to_csv(
        "/Users/.....", index=False)
    Expand_avg_all.to_csv(
        "/Users/....", index=False)
    return

def edit_target(Target_df):
    Target_df['Target'] = Target_df['Target'].astype(float)
    Target_df = Target_df.replace(np.nan, 0)
    Target_df = Target_df.replace([np.inf], 0)
    Target_df.to_csv("/Users/...",
                          index=False)
    return


def edit_pop(Name, Pop, School_Pop_Hist):
    School_Pop = pd.DataFrame(np.column_stack([Name, Pop]), columns=['School_Name', 'Population'])
    School_Pop['SchoolYear'] = 2024
    School_Pop_Hist = School_Pop_Hist[['School_Name', 'Population', 'SchoolYear']]
    School_Pop_all = pd.concat([School_Pop, School_Pop_Hist], axis=0)
    School_Pop_all = School_Pop_all.sort_values(by=['SchoolYear', 'School_Name'], axis=0, ignore_index=True, key=None)
    School_Pop_all.to_csv(
        "/Users/.....", index=False)
    return






