import streamlit as st
import requests, csv

#script for updating data:
#special url with all batting player data
batterurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=batting&language=en"
pitcherurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=pitching&team=&round=&split=&team=&split=&language=en"
#special chatgpt code to access all the data in the url
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://stats.britishbaseball.org.uk/",
    "Origin": "https://stats.britishbaseball.org.uk",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9",
}

#function for splitting the data into individual players
def SplitDataIntoPlayers(data, batter):
    playerList = []
    items = data.split("},{")
    for item in items:
        player = item.split(",")
        if (batter and (len(player) == 26 or len(player) == 28)) or (not batter and (len(player) == 31 or len(player) == 33)):
            playerList.append(player)
    return playerList

#function for parsing batter data
def ParseBatterData(unparsedBatterList):
    batters = []
    for batter in unparsedBatterList:
        #batter = unparsed batter
        player = {}
        player["Player"] = ParseName(batter[23])
        player["Team"] = batter[24].split(":")[1].strip('"')
        player["G"] = int(batter[0][-1:])
        player["AB"] = int(batter[2].split(":")[1])
        player["R"] = int(batter[3].split(":")[1])
        player["H"] = int(batter[4].split(":")[1])
        player["2B"] = int(batter[5].split(":")[1])
        player["3B"] = int(batter[6].split(":")[1])
        player["HR"] = int(batter[7].split(":")[1])
        player["RBI"] = int(batter[8].split(":")[1])
        player["TB"] = int(batter[9].split(":")[1])
        player["AVG"] = float(batter[10].split(":")[1]) / 1000
        player["SLG"] = float(batter[11].split(":")[1]) / 1000
        player["OBP"] = float(batter[12].split(":")[1]) / 1000
        player["OPS"] = float(batter[13].split(":")[1]) / 1000
        player["BB"] = int(batter[14].split(":")[1])
        player["HBP"] = int(batter[15].split(":")[1])
        player["SO"] = int(batter[16].split(":")[1])
        player["GDP"] = int(batter[17].split(":")[1])
        player["SF"] = int(batter[18].split(":")[1])
        player["SH"] = int(batter[19].split(":")[1])
        player["SB"] = int(batter[20].split(":")[1])
        player["CS"] = int(batter[21].split(":")[1])
        batters.append(player)
    return batters

#function for parsing pitcher data
def ParsePitcherData(unparsedPitcherList):
    pitchers = []
    for pitcher in unparsedPitcherList:
        #pitcher = unparsed pitcher
        player = {}
        player["Player"] = ParseName(pitcher[28])
        player["Team"] = pitcher[29].split(":")[1].strip('"')
        player["W"] = int(pitcher[0][-1:])
        player["L"] = int(pitcher[1].split(":")[1])
        player["ERA"] = float(pitcher[2].split(":")[1].strip('"'))
        player["APP"] = int(pitcher[3].split(":")[1])
        player["SV"] = int(pitcher[5].split(":")[1])
        player["CG"] = int(pitcher[6].split(":")[1])
        player["SHO"] = int(pitcher[7].split(":")[1])
        player["IP"] = float(pitcher[8].split(":")[1].strip('"'))
        player["H"] = int(pitcher[9].split(":")[1])
        player["R"] = int(pitcher[10].split(":")[1])
        player["ER"] = int(pitcher[11].split(":")[1])
        player["BB"] = int(pitcher[12].split(":")[1])
        player["SO"] = int(pitcher[13].split(":")[1])
        player["2B"] = int(pitcher[14].split(":")[1])
        player["3B"] = int(pitcher[15].split(":")[1])
        player["HR"] = int(pitcher[16].split(":")[1])
        player["AB"] = int(pitcher[17].split(":")[1])
        player["BAVG"] = float(pitcher[18].split(":")[1]) / 1000
        player["WP"] = int(pitcher[19].split(":")[1])
        player["HB"] = int(pitcher[20].split(":")[1])
        player["BK"] = int(pitcher[21].split(":")[1])
        player["SFA"] = int(pitcher[22].split(":")[1])
        player["SHA"] = int(pitcher[23].split(":")[1])
        player["GO"] = int(pitcher[24].split(":")[1])
        player["FO"] = int(pitcher[25].split(":")[1])
        player["WHIP"] = float(pitcher[26].split(":")[1].strip('"'))
        pitchers.append(player)
    return pitchers

#function for parsing player name
def ParseName(unparsedName):
    firstName = unparsedName.split(">")[4].split("<")[0]
    lastName = unparsedName.split(">")[1].split("<")[0]
    lastName = lastName[0] + lastName[1:].lower()
    name = firstName + " " + lastName
    return name

#function for calling functions to procure batter data
def GetBatterData():
    batterData = requests.get(batterurl, headers=headers).text
    unparsedBatterList = SplitDataIntoPlayers(batterData, batter=True)
    batterList = ParseBatterData(unparsedBatterList)
    return batterList

#function for calling functions to procure pitcher data
def GetPitcherData():
    pitcherData = requests.get(pitcherurl, headers=headers).text
    unparsedPitcherList = SplitDataIntoPlayers(pitcherData, batter=False)
    pitcherList = ParsePitcherData(unparsedPitcherList)
    return pitcherList

batterList = GetBatterData()
pitcherList = GetPitcherData()

def WriteListToCSV(fileName, playerList):
    with open(fileName, "w") as csvFile:
        columnNames = list(playerList[0].keys())
        writer = csv.DictWriter(csvFile, fieldnames=columnNames)
        writer.writeheader()
        for player in playerList:
            writer.writerow(player)

WriteListToCSV("Data\\batters.csv", batterList)
WriteListToCSV("Data\\pitchers.csv", pitcherList)

#streamlit app
page = st.navigation([st.Page("Pages\\Batters.py"), st.Page("Pages\\Pitchers.py")])
page.run()

#to run streamlit application:
#run file
#in terminal, run:
#python -m streamlit run "MainApp.py"