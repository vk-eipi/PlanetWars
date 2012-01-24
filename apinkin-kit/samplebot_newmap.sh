#!/bin/bash
# runs PyBot (P2) against JavaBot sample bot (P1) on one of fifty new maps
# pass samplebotname, PyBot, map#, logging level as parameters
# for instance, $ ./samplebot_newmap.sh Rage MyBot.py 29 INFO
LOGLVL=${4:-DEBUG}
java -jar tools/PlayGame.jar maps/map_r538_$3.txt 1000 200 log.txt "java -jar example_bots/$1Bot.jar" "python $2 --log MyBot.log --level=$LOGLVL" | python visualizer/visualize_localy.py 
