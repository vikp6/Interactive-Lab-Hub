#arecord -f cd -r 16000 -d 5 -t wav recorded.wav && sox recorded.wav recorded_mono.wav remix 1,2

# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Select an NFL Team" | aplay


arecord -D hw:2,0 -f cd -c1 -r 44100 -d 5 -t wav recorded_mono.wav
python nfl_teams.py recorded_mono.wav