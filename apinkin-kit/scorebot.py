'''
Uses alternative python starter kit by RebelXT
'''
from planetwars import BaseBot, Game
from planetwars.universe_custom import MyUniverse
from planetwars.temp_planet2 import Planet2
from planetwars.universe import player
from logging import getLogger, sys
import copy
from copy import copy
import random


log = getLogger(__name__)

class MyBot(BaseBot):
#key changes (profit -> score):
#   new needed_def
#   ordering based on "score" function
    
    max_dist = 34
    lookahead = 34

    def do_turn(self):
        log.info("I'm starting my turn %s" % self.universe.game.turn_count)

        my_planets = sorted(self.universe.my_planets, key=lambda p: p.id)

        if len(my_planets) == 1 and len(self.universe.enemy_planets) == 1 and len(self.universe.all_fleets) == 0:
            log.debug("turn one tactics")
            enemy_starter = min(self.universe.enemy_planets, key =lambda p:p.id)
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
                neutrals = [x for x in self.universe.nobodies_planets if x.in_future(p.distance(x)).owner != player.ME]
                neutrals.sort(key = lambda x: (-p.score(x), x.id))
                for n in neutrals:
                    if p.available <= 0 or p.score(n) < -100:
                        break
                    n_later = n.in_future(n.distance(p))
                    #log.debug("from p: %s, target: %s, target_later: %s" % (p,n,n_later))
                    if n_later.owner != player.ME:
                        toAttack = n_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            log.debug("score %f" % p.score(n))
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
                otherplanets = [x for x in (self.universe.all_planets-p) if x.in_future(p.distance(x)).owner != player.ME]
                otherplanets.sort(key = lambda x: (-p.score(x), x.id))
                for target in otherplanets:
                    if p.available <= 0 or p.score(target) < -100:
                        break
                    target_later = target.in_future(target.distance(p))
                    #log.debug("from p: %s, target: %s, target_later: %s" % (p,target,target_later))
                    #log.debug(target._future_cache)
                    if target_later.owner != player.ME:
                        toAttack = target_later.ship_count + 1
                        if toAttack <= p.available <= p.ship_count:
                            log.debug("Attacking from %s future %s at %d distance" % (p,target_later,target.distance(p)))
                            log.debug("score %f" % p.score(target))
                            p.send_fleet(target, toAttack)
                            p.available -= toAttack
                            

Game(MyBot, universe_class=MyUniverse, planet_class=Planet2)
