#!/usr/bin/env python
#

from math import ceil, sqrt
from sys import stdout


class Fleet:
    def __init__(self, owner, num_ships, source_planet, destination_planet, \
     total_trip_length, turns_remaining):
        self._owner = owner
        self._num_ships = num_ships
        self._source_planet = source_planet
        self._destination_planet = destination_planet
        self._total_trip_length = total_trip_length
        self._turns_remaining = turns_remaining

    def Owner(self):
        return self._owner

    def NumShips(self):
        return self._num_ships

    def SourcePlanet(self):
        return self._source_planet

    def DestinationPlanet(self):
        return self._destination_planet

    def TotalTripLength(self):
        return self._total_trip_length

    def TurnsRemaining(self):
        return self._turns_remaining

class Planet:
    def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
        self._planet_id = planet_id
        self._owner = owner
        self._num_ships = num_ships
        self._growth_rate = growth_rate
        self._x = x
        self._y = y

    def PlanetID(self):
        return self._planet_id

    def Owner(self, new_owner=None):
        if new_owner == None:
            return self._owner
        self._owner = new_owner

    def NumShips(self, new_num_ships=None):
        if new_num_ships == None:
            return self._num_ships
        self._num_ships = new_num_ships

    def GrowthRate(self):
        return self._growth_rate

    def X(self):
        return self._x

    def Y(self):
        return self._y

    def AddShips(self, amount):
        self._num_ships += amount

    def RemoveShips(self, amount):
        self._num_ships -= amount


class PlanetWars:
    def __init__(self, gameState):
        self._planets = []
        self._fleets = []
        self.ParseGameState(gameState)

    def NumPlanets(self):
        return len(self._planets)

    def GetPlanet(self, planet_id):
        return self._planets[planet_id]

    def NumFleets(self):
        return len(self._fleets)

    def GetFleet(self, fleet_id):
        return self._fleets[fleet_id]

    def Planets(self):
        return self._planets

    def MyPlanets(self):
        r = []
        for p in self._planets:
            if p.Owner() != 1:
                continue
            r.append(p)
        return r

    def NeutralPlanets(self):
        r = []
        for p in self._planets:
            if p.Owner() != 0:
                continue
            r.append(p)
        return r

    def EnemyPlanets(self):
        r = []
        for p in self._planets:
            if p.Owner() <= 1:
                continue
            r.append(p)
        return r

    def NotMyPlanets(self):
        r = []
        for p in self._planets:
            if p.Owner() == 1:
                continue
            r.append(p)
        return r

    def Fleets(self):
        return self._fleets

    def MyFleets(self):
        r = []
        for f in self._fleets:
            if f.Owner() != 1:
                continue
            r.append(f)
        return r

    def EnemyFleets(self):
        r = []
        for f in self._fleets:
            if f.Owner() <= 1:
                continue
            r.append(f)
        return r

    def ToString(self):
        s = ''
        for p in self._planets:
            s += "P %f %f %d %d %d\n" % \
             (p.X(), p.Y(), p.Owner(), p.NumShips(), p.GrowthRate())
        for f in self._fleets:
            s += "F %d %d %d %d %d %d\n" % \
             (f.Owner(), f.NumShips(), f.SourcePlanet(), f.DestinationPlanet(), \
                f.TotalTripLength(), f.TurnsRemaining())
        return s

    def Distance(self, source_planet, destination_planet):
        source = self._planets[source_planet]
        destination = self._planets[destination_planet]
        dx = source.X() - destination.X()
        dy = source.Y() - destination.Y()
        return int(ceil(sqrt(dx * dx + dy * dy)))
        
    def neededDefMax(self, myplanetID):
        '''ships to defend against single wave from every enemy planet 
        plus existing hostile fleets'''
        mp = self._planets[myplanetID]
        required = 0
        maxrequired = 0
        time = 0
        efs = []
        for fleet in self.EnemyFleets():
            if fleet.DestinationPlanet() == myplanetID:
                efs.append(fleet)
        for ep in self.EnemyPlanets():
            #simulate sending out wave
            f = Fleet(
                0,ep.NumShips(),0,0,0,
                self.Distance(ep.PlanetID(),myplanetID) )
            #only NumShips and TurnsRemaining are relevant
            efs.append(f)
        efs.sort(key = lambda x: x.TurnsRemaining())
        for ef in efs:
            interval = ef.TurnsRemaining() - time
            growth = mp.GrowthRate()*interval
            toDef = ef.NumShips() - growth
            #negative toDef means surplus for next ef
            required += toDef
            if required > maxrequired:
                maxrequired = required
            time += interval
        if required < maxrequired:
            required = maxrequired
        return required
    def neededDefNormal(self, myplanetID):
        '''ships to defend strongest enemy planet, existing fleets'''
        mp = self._planets[myplanetID]
        required = 0
        maxrequired = 0
        time = 0
        efs = []
        for fleet in self.EnemyFleets():
            if fleet.DestinationPlanet() == myplanetID:
                efs.append(fleet)
                
        maxthreat = 0
        max_ep = None
        for ep in self.EnemyPlanets():
            threat = ep.NumShips() - \
                mp.GrowthRate()*self.Distance(ep.PlanetID(),myplanetID)
            if threat > maxthreat:
                maxthreat = threat
                max_ep = ep
        if max_ep != None:
            f = Fleet(
                0,max_ep.NumShips(),0,0,0,
                self.Distance(max_ep.PlanetID(),myplanetID) )
            #only NumShips and TurnsRemaining are relevant
            efs.append(f)
        
        efs.sort(key = lambda x: x.TurnsRemaining())
        for ef in efs:
            interval = ef.TurnsRemaining() - time
            growth = mp.GrowthRate()*interval
            toDef = ef.NumShips() - growth
            #negative toDef means surplus for next ef
            required += toDef
            if required > maxrequired:
                maxrequired = required
            time += interval
        if required < maxrequired:
            required = maxrequired
        return required
        
    def neededDefMin(self, myplanetID):
        '''ships to defend against existing hostile fleets'''
        mp = self._planets[myplanetID]
        required = 0
        maxrequired = 0
        time = 0
        efs = []
        for fleet in self.EnemyFleets():
            if fleet.DestinationPlanet() == myplanetID:
                efs.append(fleet)
        efs.sort(key = lambda x: x.TurnsRemaining())
        for ef in efs:
            interval = ef.TurnsRemaining() - time
            growth = mp.GrowthRate()*interval
            toDef = ef.NumShips() - growth
            #negative toDef means surplus for next ef
            required += toDef
            if required > maxrequired:
                maxrequired = required
            time += interval
        if required < maxrequired:
            required = maxrequired
        return required

    def IssueOrder(self, source_planet, destination_planet, num_ships):
        stdout.write("%d %d %d\n" % \
         (source_planet, destination_planet, num_ships))
        stdout.flush()

    def IsAlive(self, player_id):
        for p in self._planets:
            if p.Owner() == player_id:
                return True
        for f in self._fleets:
            if f.Owner() == player_id:
                return True
        return False

    def ParseGameState(self, s):
        self._planets = []
        self._fleets = []
        lines = s.split("\n")
        planet_id = 0

        for line in lines:
            line = line.split("#")[0] # remove comments
            tokens = line.split(" ")
            if len(tokens) == 1:
                continue
            if tokens[0] == "P":
                if len(tokens) != 6:
                    return 0
                p = Planet(planet_id, # The ID of this planet
                                     int(tokens[3]), # Owner
                                     int(tokens[4]), # Num ships
                                     int(tokens[5]), # Growth rate
                                     float(tokens[1]), # X
                                     float(tokens[2])) # Y
                planet_id += 1
                self._planets.append(p)
            elif tokens[0] == "F":
                if len(tokens) != 7:
                    return 0
                f = Fleet(int(tokens[1]), # Owner
                                    int(tokens[2]), # Num ships
                                    int(tokens[3]), # Source
                                    int(tokens[4]), # Destination
                                    int(tokens[5]), # Total trip length
                                    int(tokens[6])) # Turns remaining
                self._fleets.append(f)
            else:
                return 0
        return 1

    def FinishTurn(self):
        stdout.write("go\n")
        stdout.flush()
