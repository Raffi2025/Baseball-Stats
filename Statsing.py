import math, time, requests, os, csv


#special url with all batting player data
batterurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=batting&language=en"
pitcherurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=pitching&team=&round=&split=&team=&split=&language=en"
#special chatgpt code to access all the data in the url
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "application/json, text/javascript, /; q=0.01",
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
    print("\n".join(batterData.split("},{")[743].split(",")))
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


#Create CSV files
def save_players_to_csv(players, filename):
    if not players:
        raise ValueError("The players list is empty.")
    
     #Get the header from the first player's keys
    headers = players[0].keys()
    
    with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for player in players:
            writer.writerow(player)

    print(f"CSV file '{filename}' created successfully.")

save_players_to_csv(batterList, "batter_stats.csv")
save_players_to_csv(pitcherList, "pitcher_stats.csv")




def leagueAverages(arr):
    totalOBP = 0
    totalSLG = 0
    validPeople = 0
    for player in arr:
        if player["PA"] >= 5:
            totalOBP += player["OBP"]
            totalSLG += player["SLG"]
            validPeople += 1
    return totalOBP, totalSLG, validPeople

def PlateAppearances(arr):
    for player in arr:
        PA = player["BB"] + player["HBP"] + player["SF"] + player["SH"] + player["AB"]
        player["PA"] = PA

def WalkPercentage(arr):
    for player in arr:
        try:
            BBPercentage = (player["BB"]/player["PA"])*100
            player["BB%"] = BBPercentage
        except:
            player["BB%"] = "N/A"

def StrikeOutPercentage(arr):
    for player in arr:
        try:
            SOPercentage = (player["SO"]/player["PA"])*100
            player["SO%"] = SOPercentage
        except:
            player["SO%"] = "N/A"

def StealSuccessRate(arr):
    for player in arr:
        try:
            SSR = (player["SB"]/(player["SB"] + player["CS"]))*100
            player["SSR"] = SSR
        except:
            player["SSR"] = "N/A"

def Singles(arr):
    for player in arr:
        OneB = player["H"] - (player["2B"] + player["3B"] + player["HR"])
        player["1B"] = OneB

def IsolatedPower(arr):
    for player in arr:
        ISO = player["SLG"] - player["AVG"]
        player["ISO"] = ISO

def BattingAverageBIP(arr):
    for player in arr:
        try:
            BAbip = (player["H"] - player["HR"])/(player["AB"] - player["SO"] + player["SF"])
            player["BAbip"] = round(BAbip,3)
        except:
            player["BAbip"] = "N/A"

def OnBasePlusSluggingPlus(arr):
    for player in arr:
        OPSPlus = ((player["OBP"]/totalOBP) + (player["SLG"]/totalSLG) - 1)*100
        player["OPS+"] = round(OPSPlus)

def WeightedOnBaseAverage(batting, pitching):
    #Step 1
    TotalIP = 0
    for player in pitching:
        TotalIP += player["IP"]
    NumOuts = TotalIP * 3
    TotalRuns = 0
    for player in batting:
        TotalRuns += player["R"]
    RunsPerOut = TotalRuns/NumOuts
    #Step 2/3
    BBRV = RunsPerOut + 1.14
    HBPRV = BBRV + 1.025
    OneBRV = BBRV + 1.155
    TwoBRV = OneBRV + 1.3
    ThreeBRV = TwoBRV + 1.27
    HRRV = ThreeBRV + 3
    #Calculate 1B
    Singles(batterList)
    #Calculate PA
    PlateAppearances(batterList)
    #Step 4
    TotalBB = 0
    for player in batting:
        TotalBB += player["BB"]
    TotalHBP = 0
    for player in batting:
        TotalHBP += player["HBP"]
    TotalOneB = 0
    for player in batting:
        TotalOneB += player["1B"]
    TotalTwoB = 0
    for player in batting:
        TotalTwoB += player["2B"]
    TotalThreeB = 0
    for player in batting:
        TotalThreeB += player["3B"]
    TotalHR = 0
    for player in batting:
        TotalHR += player["HR"]
    TotalPA = 0
    for player in batting:
        TotalPA += player["PA"]
    #Entire league wOBA
    LeaguewOBA = ((BBRV*TotalBB) + (HBPRV*TotalHBP) + (OneBRV*TotalOneB) + (TwoBRV*TotalTwoB) + (ThreeBRV*TotalThreeB) + (HRRV*TotalHR))/TotalPA
    #Step 5
    totalOBP, totalSLG, validPeople = leagueAverages(batterList)
    wOBAScale = (totalOBP/validPeople)/LeaguewOBA
    #Step 6
    BBRV = BBRV * wOBAScale
    HBPRV = HBPRV * wOBAScale
    OneBRV = OneBRV * wOBAScale
    TwoBRV = TwoBRV * wOBAScale
    ThreeBRV = ThreeBRV * wOBAScale
    HRRV = HRRV * wOBAScale
    #Step 7
    for player in batting:
        try:
            player["wOBA"] = ((BBRV*player["BB"]) + (HBPRV*player["HBP"]) + (OneBRV*player["1B"]) + (TwoBRV*player["2B"]) + (ThreeBRV*player["3B"]) + (HRRV*player["HR"]))/(player["PA"])
        except:
            player["wOBA"] = "N/A"

    for player in batting:
        if player["Player"] == "Charlie Waldman":
            print(player["wOBA"])
    print(LeaguewOBA)

#PlateAppearances(batterList)
#totalOBP, totalSLG, validPeople = leagueAverages(batterList)
#WalkPercentage(batterList)
#StrikeOutPercentage(batterList)
#StealSuccessRate(batterList)
#Singles(batterList)
#IsolatedPower(batterList)
#BattingAverageBIP(batterList)
#OnBasePlusSluggingPlus(batterList)

WeightedOnBaseAverage(batterList, pitcherList)

