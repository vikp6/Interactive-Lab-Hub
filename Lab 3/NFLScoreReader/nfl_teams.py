#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import requests


if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), '["oh giants cardinals falcons ravens bills panthers bears bengals browns cowboys broncos lions packers texans colts jaguars chiefs raiders chargers rams dolphins vikings patriots saints jets eagles steelers fortyniners seahawks buccaneers titans washington", "[unk]","giants"]')
#dict matching team name to abv
nameToABV = {'giants':'NYG','cardinals':'ARI','falcons':'ATL','ravens':'BAL','bills':'BUF','panthers':'CAR','bears':'CHI','bengals':'CIN','browns':'CLE','cowboys':'DAL','broncos':'DEN','lions':'DET','packers':'GB','texans':'HOU','colts':'IND','jaguars':'JAX','chiefs':'KC','raiders':'LV','chargers':'LAC','rams':'LAR','dolphins':'MIA','vikings':'MIN','patriots':'NE','saints':'NO','jets':'NYJ','eagles':'PHI','steelers':'PIT','fortyniners':'SF','seahawks':'SEA','buccaneers':'TB','titans':'TEN','washington':'WSH'}
while True:
    data = wf.readframes(6000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
        
        #voiceTeamSelect = rec.Result()
    else:
        print(rec.PartialResult())
        #voiceTeamSelect = rec.PartialResult()

#print(rec.FinalResult())

voiceTeamSelect = rec.FinalResult()
print(voiceTeamSelect)

voiceTeamSelect = 'giants'

if(nameToABV.get(voiceTeamSelect)==None):
    print("Invalid Team")
else:
    teamABV = nameToABV[voiceTeamSelect]
    print('Team Selected: '+teamABV)
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
        opponentABV = matchupDict[teamABV]
        print('Next Week Matchup against: '+opponentABV)
        
        
        
        os.system("espeak -ven+f2 -k5 -s150 --stdout  "+list(nameToABV.keys())[list(nameToABV.values()).index(teamABV)]+" | aplay")
        os.system("espeak -ven+f2 -k5 -s150 --stdout  "+"versus"+" | aplay")
        os.system("espeak -ven+f2 -k5 -s150 --stdout  "+list(nameToABV.keys())[list(nameToABV.values()).index(opponentABV)]+" | aplay")

        #print(matchupDict)
        
        #print(r.json()["sports"][0]["leagues"][0]["events"][1]["shortName"])
    else:
        print(f'Oops - status code is {r.status_code}')


