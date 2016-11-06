import sys
from sets import Set
# import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class GameState(object):
    def __init__(self, width, height, my_id, live_players, round_count, player_box_count):
        self.my_id = my_id
        self.players = live_players  # [list of id's]
        self.width = width
        self.height = height
        self.bomb_max_counter = 8
        # self.bombs = {}  # {player_id: {(x, y): timer}}
        self.box_positions = Set()  # (x, y)
        self.bomb_timer = {}  # {player_id: {(x, y): timer}}
        self.bomb_range = {}  # {player_id: {(x, y): range}}
        self.bomb = {}  # {(x, y): [[owner_id, timer, range]]}

        for player in self.players:
            self.bomb_timer[player] = {}
            self.bomb_range[player] = {}

        # self.bomb_to_explode = {}  # {(x, y): player_id}
        # for player in self.players:
        #    self.bomb_to_explode[player] = []

        self.bomb_to_explode = Set()
        self.player_bomb_range = {}  # {player_id: range}
        self.player_bomb_timer = {}  # {player_id: timer}
        self.player_positions = {}  # {player_id: (x, y)}
        self.player_box_count = player_box_count  # (player_id: box_count}
        self.player_bomb_count = {}  # (player_id: bomb_count}
        self.player_bomb_left = {}  # (player_id: bomb_left}
        self.round_count = round_count

    def load_board_from_input(self):
        for i in xrange(self.height):
            row = raw_input()
            for j in xrange(len(row)):
                if row[j] == '0':
                    self.box_positions.add((j, i))
        entities = int(raw_input())
        for i in xrange(entities):
            entity_type, owner, x, y, param_1, param_2 = [int(j) for j in raw_input().split()]
            if entity_type == 0:
                self.player_positions[owner] = (x, y)
                self.player_bomb_left[owner] = param_1
                self.player_bomb_range[owner] = param_2
            if entity_type == 1:
                self.bomb_timer[owner][(x, y)] = param_1
                self.bomb_range[owner][(x, y)] = param_2
                if (x, y) not in self.bomb:
                    self.bomb[(x, y)] = [[owner, param_1, param_2]]
                else:
                    self.bomb[(x, y)].append([owner, param_1, param_2])

    def update_board_from_input(self):
        self.box_positions.clear()
        self.bomb_to_explode.clear()
        for player in self.players:
            self.bomb_timer[player] = {}
            self.bomb_range[player] = {}
            self.bomb = {}

        for i in xrange(self.height):
            row = raw_input()
            for j in xrange(len(row)):
                if row[j] == '0':
                    self.box_positions.add((j, i))

        entities = int(raw_input())
        for i in xrange(entities):
            entity_type, owner, x, y, param_1, param_2 = [int(j) for j in raw_input().split()]
            if entity_type == 0:
                self.player_positions[owner] = (x, y)
                self.player_bomb_left[owner] = param_1
                self.player_bomb_range[owner] = param_2
            if entity_type == 1:
                self.bomb_timer[owner][(x, y)] = param_1
                self.bomb_range[owner][(x, y)] = param_2
                if (x, y) not in self.bomb:
                    self.bomb[(x, y)] = [[owner, param_1, param_2]]
                else:
                    self.bomb[(x, y)].append([owner, param_1, param_2])

        for bomb in self.bomb:
            for i in xrange(len(self.bomb[bomb])):
                if self.bomb[bomb][i][1] == 1:
                    self.bomb_to_explode.add(bomb)

    def box_count_update(self):
        box_to_destroy = {}  # {player_id: [box_list]}
        for player in self.players:
            box_to_destroy[player] = Set()

        bombs_exploded = Set()
        while len(self.bomb_to_explode) != 0:
            bomb = self.bomb_to_explode.pop()
            self.explode_bombs_on_square(bomb[0], bomb[1], box_to_destroy, bombs_exploded)
        for player in self.players:
            self.player_box_count[player] += len(box_to_destroy[player])

    def explode_bombs_on_square(self, bomb_x, bomb_y, boxes, bombs_exploded):

        for i in xrange(0, len(self.bomb[bomb_x, bomb_y])):
            player = self.bomb[bomb_x, bomb_y][i][0]
            bomb_range = self.bomb[bomb_x, bomb_y][i][2]

            for x in xrange(bomb_x - 1, max(-1, bomb_x - bomb_range), -1):
                if (x, bomb_y) in self.bomb:
                    if (x, bomb_y) not in bombs_exploded:
                        self.bomb_to_explode.add((x, bomb_y))
                    break
                if (x, bomb_y) in self.box_positions:
                    boxes[player].add((x, bomb_y))
                    break

            for x in xrange(bomb_x + 1, min(self.width, bomb_x + bomb_range)):
                if (x, bomb_y) in self.bomb:
                    if (x, bomb_y) not in bombs_exploded:
                        self.bomb_to_explode.add((x, bomb_y))
                    break
                if (x, bomb_y) in self.box_positions:
                    boxes[player].add((x, bomb_y))
                    break

            for y in xrange(bomb_y - 1, max(-1, bomb_y - bomb_range), -1):
                if (bomb_x, y) in self.bomb:
                    if (bomb_x, y) not in bombs_exploded:
                        self.bomb_to_explode.add((bomb_x, y))
                    break
                if (bomb_x, y) in self.box_positions:
                    boxes[player].add((bomb_x, y))
                    break

            for y in xrange(bomb_y + 1, min(self.height, bomb_y + bomb_range)):
                if (bomb_x, y) in self.bomb:
                    if (bomb_x, y) not in bombs_exploded:
                        self.bomb_to_explode.add((bomb_x, y))
                    break
                if (bomb_x, y) in self.box_positions:
                    boxes[player].add((bomb_x, y))
                    break

        bombs_exploded.add((bomb_x, bomb_y))

        # def next_state(self):

width, height, my_id = [int(i) for i in raw_input().split()]

state = GameState(width, height, my_id, [0, 1], 1, {0: 0, 1: 0})
if my_id == 0:
    enemy_id = 1
else:
    enemy_id = 0

# game loop
while True:
    if state.round_count == 1:
        state.load_board_from_input()
    else:
        state.update_board_from_input()

    print >> sys.stderr, "my_id: {}".format(state.my_id)
    # print >> sys.stderr, state.bomb_timer
    print >> sys.stderr, "player positions:\n {}".format(state.player_positions)
    print >> sys.stderr, "bombs:\n {}".format(state.bomb)
    # print >> sys.stderr, state.box_positions

    if state.player_positions[enemy_id][0] == state.player_positions[my_id][0] and\
       state.player_positions[enemy_id][1] == state.player_positions[my_id][1]:
        print "BOMB {} {}".format(state.player_positions[enemy_id][0], state.player_positions[enemy_id][1])
    else:
        print "MOVE {} {}".format(state.player_positions[enemy_id][0], state.player_positions[enemy_id][1])

    state.box_count_update()
    for player in state.players:
        print >> sys.stderr, "player {}, boxes: {}".format(player, state.player_box_count[player])

    #if state.round_count == 1:
    #    print "BOMB 0 0"
    #else:
    #    print "MOVE 0 1"

    state.round_count += 1
    #state = GameState(width, height, my_id, [0, 1], 0, {0: 0, 1: 0})
