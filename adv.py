from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

explored = {player.current_room.id: {}}

for exits in player.current_room.get_exits():
    explored[player.current_room.id][exits] = '?'


def move_player(direction):
    from_room = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    last_room = player.current_room
    player.travel(direction)
    if player.current_room.id in explored:
        explored[last_room.id][direction] = player.current_room.id
        explored[player.current_room.id][from_room[direction]] = last_room.id
    else:
        explored[player.current_room.id] = {}
        for exits in player.current_room.get_exits():
            explored[player.current_room.id][exits] = '?'
        explored[last_room.id][direction] = player.current_room.id
        explored[player.current_room.id][from_room[direction]] = last_room.id
    traversal_path.append(direction)


def pick():
    unexplored = []
    for exits in player.current_room.get_exits():
        if explored[player.current_room.id][exits] == '?':
            unexplored.append(exits)
    if len(unexplored) == 0:
        return None
    else:
        choice = random.choice(unexplored)
        return choice


def search():
    move = pick()
    while move != None:
        move_player(move)
        move = pick()


def bfs():
    q = Queue()
    q.enqueue(player.current_room.id)
    visited = set()
    path = {}
    path[player.current_room.id] = None

    while q.size() > 0:
        r = q.dequeue()
        if r not in visited:
            if r not in explored:
                back_track = []
                curr = path[r]
                while curr != None:
                    back_track.insert(0, curr[1])
                    curr = path[curr[0]]
                for move in back_track:
                    move_player(move)
                return
            visited.add(r)
            for next_room in world.rooms[r].get_exits():
                rm = getattr(world.rooms[r], f"{next_room}_to")
                if rm.id not in visited:
                    path[rm.id] = [r, next_room]
                q.enqueue(rm.id)

while len(explored) < len(world.rooms):
    search()
    bfs()

def move_player(direction):
    player.travel(direction)
    traversal_path.append(direction)


def dft(visited=None, prev=None, moves=None, p=player):
    current = p.current_room.id
    neighbors = p.current_room.get_exits()
    reverse_dir = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}
    if not visited:
        visited = {}
    if current not in visited:
        visited[current] = {}
    if moves:
        visited[prev][moves] = current
    if prev:
        visited[current][reverse_dir[moves]] = prev
    if len(visited[current]) < len(neighbors):
        for direction in neighbors:
            if direction not in visited[current]:
                move_player(direction)
                dft(visited, prev=current, moves=direction)
    if len(visited) < len(room_graph):
        direction = reverse_dir[moves]
        move_player(direction)
dft()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
