# vim:ts=4:shiftwidth=4:et

from planetwars.universe import Universe, player
from planetwars.player import Player
from copy import deepcopy, copy

class MyUniverse(Universe):
    
    def send_fleet(self, source, destination, ship_count):
        new_fleets = Universe.send_fleet(self, source, destination, ship_count)
        del source._future_cache[:]
        if isinstance(destination, set):
            for target in destination:
                del target._future_cache[source.distance(target):]
        else:
            del destination._future_cache[source.distance(destination):]
        return new_fleets
       
    def update(self, game_state_line):
        Universe.update(self, game_state_line)
        for planet in self.all_planets:
            del planet._future_cache[:]
    
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
