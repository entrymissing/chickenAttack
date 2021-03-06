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

        orders = {}
        for x in range(self.width):
            for y in range(self.height):
                if not guys[x][y]: continue

                num_guys, is_mine = guys[x][y]
                if not is_mine: continue
                if num_guys == 1: continue
                
                orders[(x,y), self.getNextAction(guys,x,y)] = num_guys - 1
                #orders[((x, y), random.choice(actions.ALL_ACTIONS))] = num_guys - 1

        return orders

    def getNextAction( self, guys, x, y ):
        if random.random() < 0.1:
            return random.choice(actions.ALL_ACTIONS)
        
        sums = [0,0,50,0,0]
        
        freeCell = False;
        for curCell in guys[x:self.width]:
            if not curCell[y]:
                freeCell = True
                break
            else:
                sums[actions.RIGHT] += 1
        if freeCell == False:
            sums[actions.RIGHT] = 50

        freeCell = False;
        for curCell in reversed(guys[0:x]):
            if not curCell[y]:
                freeCell = True
                break
            else:
                sums[actions.LEFT] += 1
        if freeCell == False:
            sums[actions.LEFT] = 50
        
        freeCell = False;
        for curCell in guys[x][y:self.height]:
            if not curCell:
                freeCell = True
                break
            else:
                sums[actions.UP] += 1
        if freeCell == False:
            sums[actions.UP] = 50

        freeCell = False;
        for curCell in reversed(guys[x][0:y]):
            if not curCell:
                freeCell = True
                break
            else:
                sums[actions.DOWN] += 1
        if freeCell == False:
            sums[actions.DOWN] = 50
        
        
        return sums.index(min(sums))
