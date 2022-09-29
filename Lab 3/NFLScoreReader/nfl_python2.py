import requests

url = 'https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York'

r = requests.get(url)
if r.status_code == 200:
    numofGames = len(r.json()["sports"][0]["leagues"][0]["events"])
    matchupDict = {}
    for game in r.json()["sports"][0]["leagues"][0]["events"]:
        tempgameList = game["shortName"].split()
        matchupDict[tempgameList[0]] = tempgameList[2]
        matchupDict[tempgameList[2]] = tempgameList[0]
        
        #print(game["shortName"].split())
    print(matchupDict)
    
    #print(r.json()["sports"][0]["leagues"][0]["events"][1]["shortName"])
else:
    print(f'Oops - status code is {r.status_code}')







# from nfllivepy.requester.pbp_requester import PBPRequester
# 
# requester = PBPRequester()
# 
# # Get live data for all current games
# requester.get_live_pbp_all_games()
# 
# # Get live data for the Chicago Bears
# print(requester.get_live_pbp_for_team("CHI"))





# #!python
# import nflgame
# 
# game = nflgame.one(2011, 17, "NE", "BUF")
# print (game.score_home, game.score_away)
