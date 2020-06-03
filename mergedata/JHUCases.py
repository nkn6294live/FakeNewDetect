import os
import pandas as pd
import dateutil

pd.options.display.max_rows = None
pd.options.display.max_columns = None 

def split_by_day(df, day, label):
    day_df = df[['stateFips', 'countyFips', day]].copy()
    day_df.rename(columns={day: label}, inplace=True)
    day_df['date'] = day
    return day_df

# US cummulative confirmed
confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",  dtype='str')
confirmed = confirmed.fillna('')
confirmed['FIPS'] = confirmed['FIPS'].str.replace('\.0', '')

# fips codes
county_confirmed = confirmed.query("Admin2 != ''").query("FIPS != ''").copy()
# state fips code: 2 character with '0'-padding, e.g. 06
county_confirmed['stateFips'] = county_confirmed['FIPS'].str[:-3]
county_confirmed['stateFips'] = county_confirmed['stateFips'].apply(lambda s: '0' + s if len(s) == 1 else s)
county_confirmed['countyFips'] = county_confirmed['FIPS'].str[-3:]

days = county_confirmed.columns.tolist()[11:-2]

df_list = []
for day in days:
    df_list.append(split_by_day(county_confirmed, day, 'cummulativeConfirmed'))

cases_confirmed = pd.concat(df_list)
cases_confirmed['date'] = cases_confirmed['date'].apply(dateutil.parser.parse)

#  US cummulative deaths
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv",  dtype='str')
deaths = deaths.fillna('')
deaths['FIPS'] = deaths['FIPS'].str.replace('\.0', '')

# Update fips code
county_deaths = deaths.query("Admin2 != ''").query("FIPS != ''").copy()
county_deaths['stateFips'] = county_deaths['FIPS'].str[:-3]
county_deaths['stateFips'] = county_deaths['stateFips'].apply(lambda s: '0' + s if len(s) == 1 else s)
county_deaths['countyFips'] = county_deaths['FIPS'].str[-3:]

df_list = []
for day in days:
    df_list.append(split_by_day(county_deaths, day, 'cummulativeDeaths'))

cases_deaths = pd.concat(df_list)
cases_deaths['date'] = cases_deaths['date'].apply(dateutil.parser.parse)

#
cases = cases_confirmed.merge(cases_deaths, on=['stateFips', 'countyFips', 'date'])
cases = cases[(cases['cummulativeConfirmed'] != '0') | (cases['cummulativeDeaths'] != '0')]

#  global cummulative confirmed
confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",  dtype='str')
confirmed = confirmed.fillna('')
confirmed.rename(columns={'Province/State': 'admin1', 'Country/Region': 'country'}, inplace=True)

days = confirmed.columns.tolist()[4:]

def split_by_day(df, day, label):
    day_df = df[['country', 'admin1', day]].copy()
    day_df.rename(columns={day: label}, inplace=True)
    day_df['date'] = day
    return day_df

df_list = []
for day in days:
    df_list.append(split_by_day(confirmed, day, 'cummulativeConfirmed'))

cases_confirmed = pd.concat(df_list)
cases_confirmed['date'] = cases_confirmed['date'].apply(dateutil.parser.parse)

# global cummulative deaths
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",  dtype='str')
deaths = deaths.fillna('')
deaths.rename(columns={'Province/State': 'admin1', 'Country/Region': 'country'}, inplace=True)

df_list = []
for day in days:
    df_list.append(split_by_day(deaths, day, 'cummulativeDeaths'))

cases_deaths = pd.concat(df_list)
cases_deaths['date'] = cases_deaths['date'].apply(dateutil.parser.parse)

# Merge US cases
cases = cases_confirmed.merge(cases_deaths, on=['country', 'admin1', 'date'])
cases = cases[(cases['cummulativeConfirmed'] != '0') | (cases['cummulativeDeaths'] != '0')]

cases.to_csv("JHUCasesGlobal.csv", index=False)