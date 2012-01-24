'''
Uses alternative python starter kit by RebelXT
'''
from planetwars import BaseBot, Game
from planetwars.planet2 import Planet2
from planetwars.universe import player
from logging import getLogger, sys
import copy
from copy import copy
import random


log = getLogger(__name__)

class MyBot(BaseBot):
#key changes: 
#   use len(my_planets)==1 for first turn
#   accounts for enemy growth        
    def do_turn(self):
        log.info("I'm starting my turn %s" % self.universe.game.turn_count)
        
        if len(self.universe.my_planets) == 1:
            #if only one planet: neutral grabbing, closest to farthest
            log.debug("first turns tactics")
            for p in self.universe.my_planets:
                p.available = p.ship_count - p.needed_def(worstcase=True)
                #log.debug(p.available)
                if p.available < 0:
                    p.available = 0
                    #needs defense
                elif p.available > p.ship_count:
                    log.warning("p.available = %d > p.shipcount = %d" % p.available, p.ship_count)
                    #shouldn't be possible
                    p.available = p.ship_count
                neutrals = sorted(self.universe.nobodies_planets, 
                    key = lambda x: (x.distance(p), x.id)
                    )
                for n in neutrals:
                    if p.available <= 0:
                        break
                    toAttack = n.ship_count+1
                    if toAttack <= p.available <= p.ship_count:
                        p.send_fleet(n, toAttack)
                        p.available -= toAttack
                        log.debug("Attacking from %s" % p)
        else:
            #same strategy, but includes enemy and decreases defence
            for p in self.universe.my_planets:
                p.available = p.ship_count - p.needed_def()
                if p.available < 0:
                    p.available = 0
                    #needs defense
                elif p.available > p.ship_count:
                    log.warning("p.available = %d > p.shipcount = %d" % p.available, p.ship_count)
                    #shouldn't be possible
                    p.available = p.ship_count
                notmines = sorted(self.universe.not_my_planets, 
                    key = lambda x: (x.distance(p), x.id)
                    )
                for n in notmines:
                    if p.available <= 0:
                        break
                    toAttack = n.ship_count+1
                    if n.owner in player.ENEMIES:
                        #account for growth
                        toAttack += n.distance(p)*n.growth_rate
                    if toAttack <= p.available <= p.ship_count:
                        p.send_fleet(n, toAttack)
                        p.available -= toAttack
                        log.debug("Attacking from %s" % p)      

Game(MyBot, planet_class=Planet2)
