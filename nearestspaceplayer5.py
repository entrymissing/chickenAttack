import actions
import random

class Player:
    #Get passed all the board information that never changes throughout the game.
    #It is recommended that you store these in member variables since you will probably need to look at them later.
    # PARAMS:

    #  money_payout_rates:
    #   This is a 50x50 2D array of floats between 0.0 and 1.0 that tell your bot how money per turn this spot produces
    #   Food production is the inverse of money production and follow the formula food_payout_rate = 1.0 - money_payout_rate
    #   This means areas that produce a lot of money, produce less food

    #  my_spawn_point:
    #   An (x, y) tuple of where your new chickens will hatch each turn

    #  their_spawn_point:
    #   An (x, y) tuple of where your opponent's chickens will hatch each turn

    def __init__(self, money_payout_rates, my_spawn_point, their_spawn_point):
        self.money_payout_rates = money_payout_rates,
        self.my_spawn_point = my_spawn_point
        self.their_spawn_point = their_spawn_point


    # Gets called each turn and where you decide where your chickens will go
    # PARAMS:

    #   guys:
    #       A 50x50 2D matrix showing where all the guys are on the board.
    #       An entry of 'None' indicates an unoccupied spot.
    #       A space with chickens will be an object with "num_guys" and "is_mine" properties.
    #

    #   my_food:
    #       A float showing how much food you have left over from last turn.

    #   their_food:
    #       A float showing how much food your opponent has left over from last run.

    #   my_money:
    #       A float showing how much money you will earn at market so far

    #   their_money:
    #       A float showing how much money your opponent will earn at market so far

    # RETURN:
    #   a python dict that takes a tuple ((x_pos, y_pos), direction) as a key and the number of guys to move as the value.
    #   direction is defined in action.py

    def take_turn(self, guys, my_food, their_food, my_money, their_money):
        self.width = len(guys)
        self.height = len(guys[0])

        allTargetCells = []
        movedCells = []
        toMoveCells = []

        orders = {}
        for x in range(self.width):
            for y in range(self.height):
                if not guys[x][y]: continue
                num_guys, is_mine = guys[x][y]
                if not is_mine: continue
                if num_guys == 1: continue
                
                toMoveCells.append( [x,y] )
    
        while len(toMoveCells) > 0:
            [x,y] = toMoveCells.pop(0)
            num_guys, is_mine = guys[x][y]

            if not guys[x][y] or guys[x][y] < 1:
                asdf()
                continue
            
            movedCells.append([x,y])
            nextAction = self.getNextAction(guys,x,y)

            if [x,y] in allTargetCells:
                orders[(x,y), nextAction] = num_guys
            else:
                orders[(x,y), nextAction] = num_guys - 1
                

            targetCell = [x + actions.OFFSETS[nextAction][0], y + actions.OFFSETS[nextAction][1]]
            allTargetCells.append(targetCell)
            
            if( self.nextMoveValid(guys, movedCells, targetCell[0], targetCell[1]) ):
                toMoveCells.append( targetCell )
                
        return orders
    
    def nextMoveValid( self, guys, movedCells, newX, newY):
        if [newX,newY] in movedCells:
            return False
        if newX < 0 or newY < 0:
            return False
        if newX > self.width or newY > self.height:
            return False
        if not guys[newX][newY]:
            return False
        num_guys, is_mine = guys[newX][newY]
        return is_mine
        
    def getNextAction( self, guys, x, y ):
        minDist2Free = 100
        pos2Free = [0,0]
        minDist2Enemy = 100
        pos2Enemy = [0,0]
        
        for destX in range(self.width):
            for destY in range(self.height):
                curDist = abs(x-destX) + abs(y-destY)

                if not guys[destX][destY]:
                    if curDist < minDist2Free:
                        pos2Free = [destX, destY]
                        minDist2Free = curDist
                else:
                    num_guys, is_mine = guys[destX][destY]
                    if not is_mine:
                        if curDist < minDist2Enemy:
                            pos2Enemy = [destX,destY]
                            minDist2Enemy = curDist
                                
        if (minDist2Free) < (3*minDist2Enemy):
            dx = x-pos2Free[0]
            dy = y-pos2Free[1]
            #print 'a'
        else:
            dx = x-pos2Enemy[0]
            dy = y-pos2Enemy[1]
            
        #print minDist2Free,minDist2Enemy
        #print dx,dy
        #asdf()
        if abs(dx)>abs(dy):
            if dx < 0:
                return actions.RIGHT
            else:
                return actions.LEFT
        else:
            if dy < 0:
                return actions.UP
            else:
                return actions.DOWN

        