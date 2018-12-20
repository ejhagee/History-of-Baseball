################################################
# 1. Import Dependencies
################################################
# Python SQL toolkit and Object Relational Mapper
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
passwd = ''

if (passwd != ''):
    passphrase = ':' + passwd
else:
    passphrase = ''

engine = create_engine(f'mysql://root{passphrase}@localhost/lahman2016')

# create a connection
conn = engine.connect()

##################################################
# 3. Set Up Flask
##################################################

app = Flask(__name__, static_url_path = '')

###################################################
# 4. Flask Routes
###################################################

#Home Route
@app.route("/")
def index():
    """Return the Homepage"""
    return render_template("index.html")

#Team Winning Percentage Route
@app.route("/teams/winpct")
def winpct():
    """Return the Winning Percentage of All Teams Ever"""

    #SQL statement for database
    statement = "SELECT Teams.yearID AS `Year`, Teams.lgID AS `League`, \
                Teams.franchID AS `FranchiseID`, Teams.divID AS `Division`, \
                Teams.W AS `W`, Teams.L AS `L`, Teams.DivWin AS `WinDiv`, \
                Teams.WCWin AS `WinWC`, Teams.LgWin AS `WinLeague`, \
                Teams.WSWin AS `WinWS`, Teams.name AS `Name`, \
                teamsfranchises.franchName AS `FranchiseName`, \
                teamsfranchises.color1 AS `Color1`, teamsfranchises.color2 AS `Color2`,\
                teamsfranchises.color3 AS `Color3` \
                FROM Teams LEFT JOIN teamsfranchises \
                ON Teams.franchID = teamsfranchises.franchID;"

    #create dataframe with data using Pandas
    teamsDf = pd.read_sql(statement, conn)

    #calculate winning percentage
    teamsDf['WinPrct'] = teamsDf['W']/(teamsDf['W']+teamsDf['L'])

    #create an empty list
    teams = []

    #iterate through teamsDf
    for index, row in enumerate(teamsDf.itertuples(), 1):
        #create a dictionary
        team = {}
        team['Year'] = row.Year
        team['League'] = row.League
        team['FranchiseID'] = row.FranchiseID
        team['Division'] = row.Division
        team['W'] = row.W
        team['L'] = row.L
        team['WinDiv'] = row.WinDiv
        team['WinWC'] = row.WinWC
        team['WinLeague'] = row.WinLeague
        team['WinWS'] = row.WinWS
        team['Name'] = row.Name
        team['FranchiseName'] = row.FranchiseName
        team['WinPrct'] = row.WinPrct
        team['Color1'] = row.Color1
        team['Color2'] = row.Color2
        team['Color3'] = row.Color3

        #add to list
        teams.append(team)

    #return jsonifyed list
    return jsonify(teams)

""" # route to get individual team records
@app.route("/teams/<team>")
def teamRecord(team):
    """"""Return historical winning percentages of selected team.""""""
    #Create statement
    statement = f"SELECT Teams.yearID AS `Year`, Teams.lgID AS `League`, \
        Teams.franchID AS `FranchiseID`, Teams.divID AS `Division`, Teams.W AS `W`, Teams.L AS `L`, \
        Teams.DivWin AS `WinDiv`, Teams.WCWin AS `WinWC`, Teams.LgWin AS `WinLeague`, Teams.WSWin AS `WinWS`, \
        Teams.name AS `Name`, teamsfranchises.franchName AS `FranchiseName` \
        FROM Teams LEFT JOIN teamsfranchises ON Teams.franchID = teamsfranchises.franchID \
        WHERE Teams.franchID = '{team}';"

    #query database
    teamDf = pd.read_sql(statement, conn)

    #calculate winning percentages
    teamDf['WinPrct'] = teamDf['W']/(teamDf['W']+teamDf['L'])

    #get franchise colors
    stmt = f"SELECT teamsfranchises.color1 AS `Color1`, teamsfranchises.color2 AS `Color2`,\
            teamsfranchises.color3 AS `Color3` FROM teamsfranchises \
            WHERE teamsfranchises.franchID = '{team}';"

    colors = pd.read_sql(stmt, conn)

    #create an empty list
    teams = []

    #iterate through teamsDf
    for index, row in enumerate(teamDf.itertuples(), 1):
        #create a dictionary
        team = {}
        team['Year'] = row.Year
        team['League'] = row.League
        team['FranchiseID'] = row.FranchiseID
        team['Division'] = row.Division
        team['W'] = row.W
        team['L'] = row.L
        team['WinDiv'] = row.WinDiv
        team['WinWC'] = row.WinWC
        team['WinLeague'] = row.WinLeague
        team['WinWS'] = row.WinWS
        team['Name'] = row.Name
        team['FranchiseName'] = row.FranchiseName
        team['WinPrct'] = row.WinPrct
        team['Color1'] = colors['Color1'][0]
        team['Color2'] = colors['Color2'][0]
        team['Color3'] = colors['Color3'][0]

        #add to list
        teams.append(team)

    #return jsonifyed list
    return jsonify(teams) """

#route to get batting stats
@app.route("/batting/<team>/<bat_stat>")
def batting(team, bat_stat):
    """Return the Top Ten Batters For a Team By Selected Statistic (Min. 162 Games)"""

    #SQL statement
    statement = f"SELECT CONCAT(Master.nameFirst, ' ', Master.nameLast) AS `PlayerName`, \
        Batting.G AS `G`, Batting.AB AS `AB`, Batting.H AS `H`, \
        Batting.`2B` AS `2B`, Batting.`3B` AS `3B`, Batting.HR AS `HR`, Batting.SF AS `SF`, \
        Batting.BB AS `BB`, Batting.HBP AS `HBP`, Batting.SO AS `K` \
        FROM Batting \
        LEFT JOIN Master ON (Batting.playerID = Master.playerID) \
        LEFT JOIN Teams ON (Batting.yearID = Teams.yearID AND Batting.teamID = Teams.teamID) \
        WHERE Teams.franchID = '{team}';"

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

    #sort data and take the top 10
    batdata = battingdf.loc[:, ['PlayerName', bat_stat]]
    sorted_bat_data = batdata.sort_values(by = bat_stat, ascending = False)
    final_bat_data = sorted_bat_data.head(10)
    
    #get franchise colors
    stmt = f"SELECT teamsfranchises.color1 AS `Color1`, teamsfranchises.color2 AS `Color2`,\
            teamsfranchises.color3 AS `Color3` FROM teamsfranchises \
            WHERE teamsfranchises.franchID = '{team}';"

    colors = pd.read_sql(stmt, conn)

    #get out data of interest
    data = {'PlayerName': final_bat_data.iloc[:,0].values.tolist(), 'Stat': final_bat_data.iloc[:,1].values.tolist()}

    #add color
    data["Color1"] = colors["Color1"][0]
    data["Color2"] = colors["Color2"][0]
    data["Color3"] = colors["Color3"][0]

    #return jsonifyed list
    return jsonify(data)

#route to get pitching stats
@app.route("/pitching/<team>/<pitch_stat>")
def pitching(team, pitch_stat):
    """Returns Top 10 performers for a particular pitching stat for selected team."""
      #SQL statement
    statement = f"SELECT CONCAT(Master.nameFirst, ' ', Master.nameLast) AS `PlayerName`, \
        Pitching.G AS `G`, Pitching.GS AS `GS`, Pitching.SV AS `SV`,  Pitching.HR AS `HR`,\
        Pitching.`IPouts` AS `IPouts`, Pitching.`ER` AS `ER`, Pitching.ERA AS `ERA`, Pitching.SHO AS `SHO`, \
        Pitching.BB AS `BB`,  Pitching.H AS `H`, Pitching.BFP AS `BF`, Pitching.SO AS `K`, Pitching.CG AS `CG` \
        FROM Pitching \
        LEFT JOIN Master ON (Pitching.playerID = Master.playerID) \
        LEFT JOIN Teams ON (Pitching.yearID = Teams.yearID AND Pitching.teamID = Teams.teamID) \
        WHERE Teams.franchID = '{team}';"

    #read the query
    pitchDf = pd.read_sql(statement, conn)

    #set some variables to numeric (not counted in early years)
    pitchDf.loc[:, 'BF'] = pd.to_numeric(pitchDf.loc[:, 'BF'], errors = 'coerce')

    #aggregate stats
    grouppitch = pitchDf.groupby(['PlayerName'])
    g = grouppitch['G'].sum()
    gs = grouppitch['GS'].sum()
    sv = grouppitch['SV'].sum()
    ip = grouppitch['IPouts'].sum()/3
    er = grouppitch['ER'].sum()
    era = (er*9)/ip
    sho = grouppitch['SHO'].sum()
    cg = grouppitch['CG'].sum()
    bb = grouppitch['BB'].sum()
    k = grouppitch['K'].sum()
    bbrate = bb/ip
    hrrate = grouppitch['HR'].sum()/ip
    groupedpitchDF = pd.DataFrame({"G": g, "GS": gs, "SV": sv, "IP": ip , "ER": er, "ERA": era, "SHO": sho,
                            "CG": cg, "BB": bb, "K": k, "BB_Rate": bbrate,"HR_Rate": hrrate})

    #minimum 200 IP
    pitchingdf = groupedpitchDF[groupedpitchDF["IP"] >= 200]

    #reset index
    pitchingdf.reset_index(inplace = True)

    #get out data of interest
    pitchdata = pitchingdf.loc[:, ['PlayerName', pitch_stat]]
    if pitch_stat in ['G','GS','SV','IP','SHO','CG', 'BB', 'K']:
        asc = False
    else:
        asc = True
    #sort data and take the top 10
    sorted_pitch_data = pitchdata.sort_values(by = pitch_stat, ascending = asc)
    final_pitch_data = sorted_pitch_data.head(10)

    #get data of interest
    data = {'PlayerName': final_pitch_data.iloc[:,0].values.tolist(), 'Stat': final_pitch_data.iloc[:,1].values.tolist()}

    #get franchise colors
    stmt = f"SELECT teamsfranchises.color1 AS `Color1`, teamsfranchises.color2 AS `Color2`,\
            teamsfranchises.color3 AS `Color3` FROM teamsfranchises \
            WHERE teamsfranchises.franchID = '{team}';"

    colors = pd.read_sql(stmt, conn)

    #add colors
    data["Color1"] = colors["Color1"][0]
    data["Color2"] = colors["Color2"][0]
    data["Color3"] = colors["Color3"][0]

    #return jsonifyed list
    return jsonify(data)




    


#####################################################
# 5. Code to Run
#####################################################
if __name__ == "__main__":
    app.run()



