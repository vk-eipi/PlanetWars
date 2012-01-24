#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""

from PlanetWars import PlanetWars

def DoTurn(pw, turnNum):
    myplanets = pw.MyPlanets()
    riskfactor = 0 # + is more defensive, - is more aggressive
    
    if turnNum < 10:
        #first turns: neutral grabbing, from closest to farthest
        for p in myplanets:
            #probably only one
            source = p.PlanetID()
            available = p.NumShips() - (pw.neededDefMax(source)+riskfactor)
            if available < 0:
                available = 0
            elif available > p.NumShips():
                available = p.NumShips()
            neutrals = sorted(pw.NeutralPlanets(),
                key = lambda x:(pw.Distance(source,x.PlanetID()), x.PlanetID())
                )
            for n in neutrals:
                if available <= 0:
                    break
                toAttack = n.NumShips()+1
                if toAttack <= available <= p.NumShips():
                    dest = n.PlanetID()
                    pw.IssueOrder(source, dest, toAttack)
                    available -= toAttack
    else:
        #same strategy but also Enemies
        #introduce risk by only defending fleets, strongest enemy
        
        ##if 10 <= turnNum < 30:
            ##riskfactor = 0
        ##elif 30 <= turnNum < 100:
            ##riskfactor = -20
        ##elif 100 <= turnNum < 150:
            ##riskfactor = -40
        ##else:
            ##riskfactor = 0
        
        for p in myplanets:
            #probably only one
            source = p.PlanetID()
            available = p.NumShips() - (pw.neededDefMin(source)+riskfactor)
            if available < 0:
                available = 0
            elif available > p.NumShips():
                available = p.NumShips()
            notmines = sorted(pw.NotMyPlanets(),
                key = lambda x:(pw.Distance(source,x.PlanetID()), x.PlanetID())
                )
            for n in notmines:
                if available <= 0:
                    break
                toAttack = n.NumShips()+1
                if toAttack <= available <= p.NumShips():
                    dest = n.PlanetID()
                    pw.IssueOrder(source, dest, toAttack)
                    available -= toAttack
    

def main():
    map_data = ''
    turnNum = 0
    while(True):
        current_line = raw_input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            pw = PlanetWars(map_data)
            DoTurn(pw, turnNum)
            pw.FinishTurn()
            map_data = ''
            turnNum = turnNum + 1
        else:
            map_data += current_line + '\n'


if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
