import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#PyMySQL
import pymysql
pymysql.install_as_MySQLdb()

#Flask
from flask import Flask, jsonify, render_template, redirect

#Pandas
import pandas as pd

#################################################
# 2. Connect to Database
#################################################

#create engine
# TO DO: Set up format for arbitrary name/host/password
engine = create_engine('sqlite:///lahman2016.sqlite')

# create a connection
conn = engine.connect()

statement = "SELECT CONCAT(Master.nameFirst, ' ', Master.nameLast) AS `PlayerName`, \
    Batting.G AS `G`, Batting.AB AS `AB`, Batting.H AS `H`, \
    Batting.`2B` AS `2B`, Batting.`3B` AS `3B`, Batting.HR AS `HR`, Batting.SF AS `SF`, \
    Batting.BB AS `BB`, Batting.HBP AS `HBP`, Batting.SO AS `K` \
    FROM Batting \
    LEFT JOIN Master ON (Batting.playerID = Master.playerID) \
    LEFT JOIN Teams ON (Batting.yearID = Teams.yearID AND Batting.teamID = Teams.teamID) \
    WHERE Teams.franchID = NYY;"

#read the query
batDf = pd.read_sql(statement, conn)

#set some variables to numeric (not counted in early years)
batDf.loc[:, 'SF'] = pd.to_numeric(batDf.loc[:, 'SF'], errors = 'coerce')
batDf.loc[:, 'HBP'] = pd.to_numeric(batDf.loc[:, 'HBP'], errors = 'coerce')

#aggregate stats
groupbat = batDf.groupby(['PlayerName'])
g = groupbat['G'].sum()
ab = groupbat['AB'].sum()
h = groupbat['H'].sum()
twob = groupbat['2B'].sum()
threeb = groupbat['3B'].sum()
hr = groupbat['HR'].sum()
sf = groupbat['SF'].sum()
bb = groupbat['BB'].sum()
hbp = groupbat['HBP'].sum()
k = groupbat['K'].sum()
groupedbatDF = pd.DataFrame({"G": g, "AB": ab, "H": h, "2B": twob, "3B": threeb, "HR": hr, "SF": sf, "BB": bb,
                        "HBP": hbp, "K": k})

#minimum 162 games
battingdf = groupedbatDF[groupedbatDF["G"] >= 162]

#calculate more stats
#singles
battingdf['1B'] = battingdf['H'] - battingdf['2B'] - battingdf['3B'] - battingdf['HR']
#average
battingdf['AVG'] = battingdf['H']/battingdf['AB']
#on base percentage
battingdf['OBP'] = (battingdf['H'] + battingdf['BB'] + battingdf['HBP'])/(battingdf['AB'] + battingdf['BB'] + battingdf['HBP'] + battingdf['SF'])
#slugging percentage
battingdf['SLG'] = (battingdf['1B'] + 2*battingdf['2B'] + 3*battingdf['3B'] + 4*battingdf['HR'])/battingdf['AB']
#on base plus sluggin
battingdf['OPS'] = battingdf['OBP'] + battingdf['SLG']

#reset index
battingdf.reset_index(inplace = True)

#get out data of interest
batdata = battingdf.loc[:, ['PlayerName', bat_stat]]

#sort data and take the top 10
sorted_bat_data = batdata.sort_values(by = bat_stat, ascending = False)
final_bat_data = sorted_bat_data.head(10)

print(final_bat_data)