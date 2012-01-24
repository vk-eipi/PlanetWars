#!/bin/bash
# runs PyBots against each other on one of fifty new maps
# pass PyBot1, PyBot2, map#, logging level as parameters
# for instance, $ ./pymatch.sh firstbot.py MyBot.py 29 INFO
case $4 in
	"DEBUG" | "INFO" | "WARNING" | "ERROR" | "FATAL" )
		LOGGING1=" --log=$1.log --level=$4"
		LOGGING2=" --log=$2.log --level=$4"
		;;
	* ) LOGGING1=""; LOGGING2="";;
esac
java -jar tools/PlayGame.jar maps/map_r538_$3.txt 1000 200 log.txt "python $1$LOGGING1" "python $2$LOGGING2" | python visualizer/visualize_localy.py 
