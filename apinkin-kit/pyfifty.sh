#!/bin/bash
# example: ./pyfifty.sh firstbot.py MyBot.py
player_1_counter=0
player_1_turn_counter=0

player_2_counter=0
player_2_turn_counter=0

draw_counter=0

maps_played=0

echo "$1 vs $2"
for i in {1..50}
do
  RES=`java -jar tools/PlayGame.jar maps/map_r538_$i.txt 1000 200 log.txt "python $1" "python $2" 2>&1 | tail -n 3 | grep "Turn\|Player"`

  TURN=`echo $RES | grep -i turn | sed 's/.*urn \([0-9]*\).*/\1/'`

  RES2=`echo $RES | grep -i player | sed 's/.*ayer \([0-9]*\).*/\1/'`

  if [ "$RES2" = "1" ] ; then
     player_1_counter=`expr $player_1_counter + 1`
     player_1_turn_counter=`expr $player_1_turn_counter + $TURN`

  elif [ "$RES2" = "2" ] ; then
     player_2_counter=`expr $player_2_counter + 1`
     player_2_turn_counter=`expr $player_2_turn_counter + $TURN`
  else
     draw_counter=`expr $draw_counter + 1`
  fi
  
  maps_played=`expr $maps_played + 1`
  echo "map: $i - Winner: $RES2 - Turns: $TURN"
done
if [ "$player_2_counter" != "0" ] ; then
avg_player_2_turn_counter=`expr $player_2_turn_counter / $player_2_counter`
fi
if [ "$player_1_counter" != "0" ] ; then
avg_player_1_turn_counter=`expr $player_1_turn_counter / $player_1_counter`
fi

echo "$1 won : $player_1_counter/$maps_played, avg turns: $avg_player_1_turn_counter"
echo "$2 won : $player_2_counter/$maps_played, avg turns: $avg_player_2_turn_counter"
echo "draws : $draw_counter/$maps_played"
