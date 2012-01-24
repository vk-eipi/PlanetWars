# vim:ts=4:shiftwidth=4:et

from planetwars.universe import Universe, player
from planetwars.fleet import Fleet, Fleets
from planetwars.planet import Planet, Planets
from planetwars.player import Player
from planetwars.util import Point
from copy import deepcopy, copy

class MyUniverse(Universe):
    
    def __init__(self, game, planet_class=Planet, fleet_class=Fleet):
        Universe.__init__(self, game, planet_class, fleet_class)
        self._rally_cache = None
        self._frontlines_cache = None
        self.center = (17,17)
        
    def send_fleet(self, source, destination, ship_count):
        new_fleets = Universe.send_fleet(self, source, destination, ship_count)
        del source._future_cache[:]
        if isinstance(destination, set):
            for target in destination:
                del target._future_cache[source.distance(target):]
        else:
            del destination._future_cache[source.distance(destination):]
        return new_fleets
    
    def turn_done(self):   
        Universe.turn_done(self)
        for planet in self.all_planets:
            del planet._future_cache[:]
        self._rally_cache = None
        self._frontlines_cache = None
    
    @property
    def rallypoint(self):
        if self._rally_cache:
            return self._rally_cache
        else:
            central = min(self.my_planets, key = lambda p: (p.distance(self.center), -p.ship_count, p.id))
            self._rally_cache = central
            return central
    
    @property
    def frontlines(self):
        if self._frontlines_cache:
            return self._frontlines_cache
        else:
            frontlines = Planets()
            if len(self.my_planets) > 0:
                for eplanet in self.enemy_planets:
                    frontlines.add(min(self.my_planets, key=lambda p: (p.distance(eplanet), -p.ship_count, p.id)))
            self._frontlines_cache = frontlines
            return frontlines
    
    ##def weakest_planets(self, owner, count=1):
        ##"""
        ##Returns a set of `count' planets with the smallest ship_count.

        ##Returns <Planets> (@see planet.py) objects (a set subclass).
        ##"""
        ##planets = self.find_planets(owner=owner)
        ##if count > 0:
            ##res = []
            ###sorted_planets = sorted(planets, key=lambda p : p.ship_count)
            ##sorted_planets = sorted(planets, key=lambda p : (1.0+p.growth_rate)/(1.0+p.ship_count), reverse=True)
            ##if count >= len(planets):
                ##return sorted_planets
            ##return sorted_planets[:count]
        ##return []

    ### Shortcut / convenience properties
    ##def my_weakest_planets(self, count):
        ##return self.weakest_planets(owner=player.ME, count=count)

    ##@property
    ##def my_weakest_planet(self):
        ##return self.my_weakest_planets(1)[0]

    ##def enemies_weakest_planets(self, count):
        ##return self.weakest_planets(owner=player.ENEMIES, count=count)

    ##@property
    ##def enemies_weakest_planet(self):
        ##return self.enemies_weakest_planets(1)[0]

    ##def strongest_planets(self, owner, count=1):
        ##"""
        ##Returns a set of `count' planets belonging to owner with the biggest ship_count.

        ##Returns <Planets> (@see planet.py) objects (a set subclass).
        ##"""
        ##planets = self.find_planets(owner=owner)
        ##if count > 0:
            ##sorted_planets = sorted(planets, key=lambda p : p.ship_count, reverse=True)
            ##if count >= len(planets):
                ##return sorted_planets
            ##return sorted_planets[:count]
        ##return []

    ### Shortcut / convenience properties
    ##def my_strongest_planets(self, count):
        ##return self.strongest_planets(owner=player.ME, count=count)

    ##@property
    ##def my_strongest_planet(self):
        ##return self.my_strongest_planets(1)[0]

    ##def enemies_strongest_planets(self, count):
        ##return self.strongest_planets(owner=player.ENEMIES, count=count)

    ##@property
    ##def enemies_strongest_planet(self):
        ##return self.enemies_strongest_planets(1)[0]
class MyUniverse2(MyUniverse):
    @property
    def frontlines(self):
        if self._frontlines_cache:
            return self._frontlines_cache
        else:
            frontlines = Planets()
            if len(self.my_planets) > 0:
                for eplanet in self.enemy_planets:
                    frontlines.add(min(self.my_planets, key=lambda p: (p.distance(eplanet), p.ship_count, p.id)))
            self._frontlines_cache = frontlines
            return frontlines
class MyUniverse3(MyUniverse):
    @property
    def frontlines(self):
        if self._frontlines_cache:
            return self._frontlines_cache
        else:
            frontlines = Planets()
            if len(self.my_planets) > 0:
                for eplanet in self.enemy_planets:
                    min_dist = 99999
                    for mplanet in self.my_planets:
                        if mplanet.distance(eplanet) < min_dist:
                            min_dist = mplanet.distance(eplanet)
                    for mplanet in self.my_planets:
                        if mplanet.distance(eplanet) == min_dist:
                            frontlines.add(mplanet)
                        elif mplanet.distance(eplanet) < min_dist:
                            log.warning("min_dist not working in MyUniverse")
                            frontlines.add(mplanet)
            self._frontlines_cache = frontlines
            return frontlines
