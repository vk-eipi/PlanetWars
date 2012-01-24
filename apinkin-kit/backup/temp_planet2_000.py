from planetwars.planet import Planet
from planetwars.player import PLAYER_MAP
from copy import copy
import player

class Planet2(Planet):
    def __repr__(self):
        return "<%d P(%d) #%d +%d>" % (self.owner.id, self.id, self.ship_count, self.growth_rate)
    
    #make cache for future
    def __init__(self, universe, id, x, y, owner, ship_count, growth_rate):
        Planet.__init__(self, universe, id, x, y, owner, ship_count, growth_rate)
        self._future_cache = [copy(self)]
    
    def in_future(self, turns=1):
        """Calculates state of planet in `turns' turns."""
        
        arriving_fleets = self.universe.find_fleets(destination=self)
        first_uncached = len(self._future_cache)
        
        if first_uncached == 0:
            self._future_cache.append(copy(self))
            first_uncached = 1
        if turns < first_uncached:
            return self._future_cache[turns]
        else:
            planet = copy(self._future_cache[-1])
            for i in range(first_uncached, turns+1):
                # account planet growth
                if planet.owner != player.NOBODY:
                    planet.ship_count = planet.ship_count + self.growth_rate

                # get fleets which will arrive in that turn
                fleets = [ x for x in arriving_fleets if x.turns_remaining == i ]

                # assuming 2-player scenario!
                ships = []
                for id in [1,2]:
                    count = sum( [ x.ship_count for x in fleets if x.owner == PLAYER_MAP.get(int(id)) ] )
                    if PLAYER_MAP[id] == planet.owner:
                        count += planet.ship_count

    #                if count > 0:
                    ships.append({'player':PLAYER_MAP.get(id), 'ships':count})

                # neutral planet has own fleet
                if planet.owner == player.NOBODY:
                    ships.append({'player':player.NOBODY,'ships':planet.ship_count})

                # calculate outcome
                if len(ships) > 1:
                    s = sorted(ships, key=lambda s : s['ships'], reverse=True)

                    winner = s[0]
                    second = s[1]

                    if winner['ships'] == second['ships']:
                        planet.ship_count=0
                    else:
                        planet.owner=winner['player']
                        planet.ship_count=winner['ships'] - second['ships']
                self._future_cache.append(copy(planet))
            return planet
        
    def needed_def(self, begin=0, end=40, worstcase=False):
        '''Ships to defend against existing hostile fleets.
        worstcase=True accounts for all enemy planets sending one wave.
        only works for my planets
        '''
        required = 0
        maxrequired = 0
        max_turn = min(begin, end)
        hostile_forces = {} #dist: shipcount
        friendly_forces = {}
        for efleet in self.attacking_fleets:
            dist = efleet.turns_remaining
            if begin <= dist <= end:
                if dist > max_turn:
                    max_turn = dist
                if dist in hostile_forces:
                    hostile_forces[dist] += efleet.ship_count
                else:
                    hostile_forces[dist] = efleet.ship_count
        if worstcase:
            for eplanet in self.universe.find_planets(owner=player.ENEMIES):
                dist = eplanet.distance(self)
                if begin <= dist <= end:
                    if dist > max_turn:
                        max_turn = dist
                    if dist in hostile_forces:
                        hostile_forces[dist] += eplanet.ship_count
                    else:
                        hostile_forces[dist] = eplanet.ship_count
        for myfleet in self.reinforcement_fleets:
            dist = myfleet.turns_remaining
            if begin <= dist <= end:
                if dist > max_turn:
                    max_turn = dist
                if dist in friendly_forces:
                    friendly_forces[dist] += myfleet.ship_count
                else:
                    friendly_forces[dist] = myfleet.ship_count
        for i in range(begin, max_turn+1):
            if i in hostile_forces:
                hforce_count = hostile_forces[i]
            else:
                hforce_count = 0
            if i in friendly_forces:
                fforce_count = friendly_forces[i]
            else:    
                fforce_count = 0
            toDef = hforce_count - fforce_count
            #negative toDef means surplus for next i
            required += toDef
            if required > maxrequired:
                maxrequired = required
            required -= self.growth_rate # grows for next turn
            print 'i', i, 'required',required,'maxrequired',maxrequired

        if required < maxrequired:
            required = maxrequired
        return required
        
    def breakeven(self, target):
        ''' Does not consider any other fleets '''
        if target.owner == player.NOBODY:
            #find # of turns to recover cost of ships
            return self.distance(target)+float(target.ship_count)/target.growth_rate
        elif target.owner in player.ENEMIES:
            return self.distance(target) #any cost offset by enemy losses
    def first_turn_profit(self, target, turns):
        #must be addable and comparable
        #number of ships gained after turns
        trip = self.distance(target)
        if turns >= trip:
            return target.growth_rate*(turns-trip) - target.ship_count
        else:
            return -target.ship_count
    def score(self, target):
        target_later = target.in_future(self.distance(target))
        breakeven = self.breakeven(target)
        return 150-breakeven
            
class Planet_firstbot(Planet):
    def needed_def(self, worstcase=False):
        '''Ships to defend against existing hostile fleets.
        worstcase=True accounts for all enemy planets sending one wave.
        '''
        required = 0
        maxrequired = 0
        time = 0
        hostile_fleets = []
        for efleet in self.attacking_fleets:
            hostile_fleets.append({'shipcount': efleet.ship_count, 'dist':efleet.turns_remaining})
        if worstcase:
            for eplanet in self.universe.find_planets(owner=player.ENEMIES):
                hostile_fleets.append({'shipcount':eplanet.ship_count, 'dist':eplanet.distance(self)})
        hostile_fleets.sort(key=lambda p: p['dist'])
        for hfleet in hostile_fleets:
            interval = hfleet['dist'] - time
            growth = self.growth_rate * interval
            toDef = hfleet['shipcount'] - growth
            #negative toDef means surplus for next ef
            required += toDef
            if required > maxrequired:
                maxrequired = required
            time += interval
        if required < maxrequired:
            required = maxrequired
        return required
            
        
