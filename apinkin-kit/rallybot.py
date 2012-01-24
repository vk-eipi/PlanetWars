'''
Uses alternative python starter kit by RebelXT
'''
from planetwars import BaseBot, Game
from planetwars.universe_custom import MyUniverse
from planetwars.planet2 import Planet2
from planetwars.universe import player
from planetwars.util import Point
from logging import getLogger, sys
import copy
from copy import copy
import random


log = getLogger(__name__)

class MyBot(BaseBot):
#key changes (profit -> rally):
#   ship availables to centralized location
    
    max_dist = 34
    lookahead = 34
    fraction_available = 0.8

    def do_turn(self):
        log.info("I'm starting my turn %s" % self.universe.game.turn_count)

        my_planets = sorted(self.universe.my_planets, key=lambda p: p.id)

        if len(my_planets) == 1 and len(self.universe.enemy_planets) == 1 and len(self.universe.all_fleets) == 0:
            log.debug("turn one tactics")
            enemy_starter = min(self.universe.enemy_planets, key =lambda p:p.id)
            max_x = -999
            max_y = -999
            min_x = 999
            min_y = 999
            for planet in self.universe.planets:
                if planet.position.x > max_x:
                    max_x = planet.position.x
                if planet.position.y > max_y:
                    max_y = planet.position.y
                if planet.position.x < min_x:
                    min_x = planet.position.x
                if planet.position.y < min_y:
                    min_y = planet.position.y
            
            self.universe.center = Point((min_x+max_x)/2, (min_y+max_y)/2)
                    
                
            for p in my_planets:
                start_dist = p.distance(enemy_starter)
                
                p.available = p.ship_count - p.needed_def(worstcase=True)
                #log.debug(p.available)
                if p.available < 0:
                    p.available = 0
                    #needs defense
                elif p.available > p.ship_count:
                    log.warning("p.available = %d > p.shipcount = %d" % p.available, p.ship_count)
                    #shouldn't be possible
                    p.available = p.ship_count

                #0-1 knapsack with objects = targets, costs = ships, values = first_turn_profit
                results = {} #format = (maxcost,maxtarget): best valuesum
                #only target neutrals closer to me than enemy
                neutrals = sorted(self.universe.nobodies_planets, key = lambda x:x.id)
                neutrals = [x for x in neutrals if x.distance(p) <= x.distance(enemy_starter)]
                for i in range(len(neutrals)):
                    results[(0,i)] = 0
                for c in range(p.available+1):
                    results[(c,-1)] = 0
                for maxcost in range(1,p.available+1):
                    for maxtarget in range(len(neutrals)):
                        tgt = neutrals[maxtarget]
                        if tgt.ship_count > maxcost:
                            results[(maxcost,maxtarget)] = results[(maxcost,maxtarget-1)]
                        else:
                            results[(maxcost,maxtarget)] = max(results[(maxcost,maxtarget-1)],
                                p.first_turn_profit(tgt,MyBot.lookahead) + results[(maxcost-tgt.ship_count, maxtarget-1)]
                                )
                best_valuesum = results[(p.available, len(neutrals)-1)]
                #find planets fitting this sum and send orders
                for maxtarget in range(len(neutrals)-1,0,-1): #len(neutrals), ..., 1
                    #log.debug("results[%s, %s] = %s" % (p.available, neutrals[maxtarget], results[(p.available, maxtarget)]))
                    if results[(p.available, maxtarget)] > results[(p.available, maxtarget-1)]:
                        #attack
                        n = neutrals[maxtarget]
                        toAttack = n.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            p.send_fleet(n, toAttack)
                            log.debug("Attacking from %s" % p)
                            p.available -= toAttack


        elif len(my_planets) == 1:
            #if only one planet: neutral grabbing, closest to farthest
            log.debug("one planet tactics")
            for p in my_planets:
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
                    #log.debug("from p: %s, target: %s, target_later: %s" % (p,n,n_later))
                    if n_later.owner != player.ME:
                        toAttack = n_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            p.send_fleet(n, toAttack)
                            p.available -= toAttack
                            log.debug("Attacking from %s future %s at %d distance" % (p,n_later,n.distance(p)))
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
                    #log.debug("from p: %s, target: %s, target_later: %s" % (p,target,target_later))
                    #log.debug(target._future_cache)
                    if target_later.owner != player.ME:
                        toAttack = target_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            p.send_fleet(target, toAttack)
                            p.available -= toAttack
                            log.debug("Attacking from %s future %s at %d distance" % (p,target_later,target.distance(p)))
                            
            #rally to centralized location
            for p in my_planets:
                if p.available*MyBot.fraction_available >= 1:
                    toAttack = int(p.available*MyBot.fraction_available)
                    p.send_fleet(self.universe.rallypoint, toAttack)
                    log.debug("Rallying to %s from %s; %d out of %d available." % (self.universe.rallypoint, p, toAttack, p.available))
                    p.available -= toAttack

Game(MyBot, universe_class=MyUniverse, planet_class=Planet2)
