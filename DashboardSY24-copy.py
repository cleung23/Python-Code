import pandas as pd
import datetime as dt
import sys
sys.path.append("/Users/...")
import SY24_25_prep as prep
import numpy as np

def main():
    #Create a datetable from 2021 to the most recent month end date
    StartDate = pd.to_datetime("1st of July, 2021")
    EndDate = pd.to_datetime("1st of July, 2025")
    SYBeginDate = pd.to_datetime("30th of June, 2024")
    DateTable = prep.first_day_of_month(StartDate, EndDate)
    DateTable_All = prep.last_day_of_month(DateTable)
    DateTable_AllCol = prep.get_school_year(DateTable_All)
    DateTable_Current = prep.get_datetable_ready(DateTable_AllCol)
    DateTable_Current['ColNo'] = prep.get_column_num(SYBeginDate)

    All, Target_all, Pop, Name = prep.get_current_data(DateTable_Current)

    School_Pop_Hist, Event_agg_all, Hour_agg_all, Number_agg_all, Expand_avg_all = prep.get_past_data()

    Expand_avg = prep.get_avg_attendance(All)

    prep.combine_new_and_old_data(All, Event_agg_all, Hour_agg_all, Number_agg_all, Expand_avg_all, Expand_avg)

    prep.edit_target(Target_all)

    prep.edit_pop(Name, Pop, School_Pop_Hist)

if __name__ == "__main__":
    main()


