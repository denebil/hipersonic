# import sys
# import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class GameState(object):
    def __init__(self, my_id, width, height):
        self.my_id = my_id
        self.width = width
        self.height = height
        # self.players_count = players_count
        self.box_positions = []  # [(x, y)]
        self.bomb_list = []
        self.player_list = []
        self.players_positions = {}  # {player_id: (x, y)}
        self.round_count = 0

    # def next_state(self):


width, height, my_id = [int(i) for i in raw_input().split()]

# game loop
while True:
    for i in xrange(height):
        row = raw_input()
    entities = int(raw_input())
    for i in xrange(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in raw_input().split()]

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    print "BOMB 6 5"
