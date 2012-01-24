'''
Uses alternative python starter kit by RebelXT
'''
from planetwars import BaseBot, Game
from planetwars.universe_custom import MyUniverse
from planetwars.planet2 import Planet2
from planetwars.universe import player
from logging import getLogger, sys
import copy
from copy import copy
import random


log = getLogger(__name__)

class MyBot(BaseBot):
#key changes (cautiousv0 -> v1): 
#   uses future state for toAttack, which works on all planets   
    def do_turn(self):
        log.info("I'm starting my turn %s" % self.universe.game.turn_count)
        
        my_planets = sorted(self.universe.my_planets, key=lambda p: p.id)
        
        if len(my_planets) == 1:
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
                    n_later = n.in_future(n.distance(p))
                    if n_later.owner != player.ME:
                        toAttack = n_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            p.send_fleet(n, toAttack)
                            p.available -= toAttack
                            log.debug("Attacking from %s" % p) 
        else:
            #minimal guard
            #attack any future vulnerable, closest to farthest
            for p in my_planets:
                p.available = p.ship_count - p.needed_def()
                if p.available < 0:
                    p.available = 0
                    #needs defense
                elif p.available > p.ship_count:
                    log.warning("p.available = %d > p.shipcount = %d" % p.available, p.ship_count)
                    #shouldn't be possible
                    p.available = p.ship_count
                otherplanets = sorted(self.universe.all_planets-p, 
                    key = lambda x: (x.distance(p), x.id)
                    )
                for target in otherplanets:
                    if p.available <= 0:
                        break
                    target_later = target.in_future(target.distance(p))
                    if target_later.owner != player.ME:
                        toAttack = target_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            p.send_fleet(target, toAttack)
                            p.available -= toAttack
                            log.debug("Attacking from %s" % p)      

Game(MyBot, universe_class=MyUniverse, planet_class=Planet2)
