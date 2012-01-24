#!/bin/bash
# runs MyBot (B, blue) against sample bot (A, red)
# pass map #, samplebot as parameters, for instance exbot.sh 42 example_bots/DualBot.jar
java -jar tools/PlayGame.jar maps/map$1.txt 1000 200 log.txt "java -jar $2" "python MyBot.py" | python visualizer/visualize_localy.py 
