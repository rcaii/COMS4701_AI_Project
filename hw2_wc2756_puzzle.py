from __future__ import division
from __future__ import print_function

import heapq
import resource
import sys
import math
import time
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index of empty block
        self.blank_index = self.config.index(0)

        # Get the row and col of empty block
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target_index = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target_index] = new_config[target_index], new_config[blank_index]

            return PuzzleState(new_config, self.n, parent=self, action="UP", cost=self.cost+1)

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target_index = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target_index] = new_config[target_index], new_config[blank_index]

            return PuzzleState(new_config, self.n, parent=self, action="Down", cost=self.cost + 1)

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target_index = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target_index] = new_config[target_index], new_config[blank_index]

            return PuzzleState(new_config, self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target_index = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target_index] = new_config[target_index], new_config[blank_index]

            return PuzzleState(new_config, self.n, parent=self, action="Right", cost=self.cost + 1)

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, max_search_depth, running_time, max_ram_usage):
    with open("output.txt", "w") as w:
        w.write("path_to_goal: {}\n".format(path_to_goal))
        w.write("cost_of_path: {}\n".format(cost_of_path))
        w.write("nodes_expanded: {}\n".format(nodes_expanded))
        w.write("search_depth: {}\n".format(cost_of_path))
        w.write("max_search_depth: {}\n".format(max_search_depth))
        w.write("running_time: {:.8f}\n".format(running_time))
        w.write("max_ram_usage: {}".format(max_ram_usage))
        #for Mac, it gives out multiple digits format for max_ram_usage instead of the example


# Helper function to get path_to_goal and cost_of_path
def path_cost(s):
    a_list = [s.action]
    p = s.parent
    for i in range(s.cost - 1):
        a_list.append(p.action)
        p = p.parent
    return a_list[::-1], s.cost


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    t1 = time.time()
    frontier = Q.Queue()
    f_set = set()
    explored = set()

    frontier.put(initial_state)
    f_set.add(tuple(initial_state.config))
    max_depth = 0

    while not frontier.empty():
        current_state = frontier.get()
        if test_goal(current_state):
            t2 = time.time()
            max_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            p_t_g, c_o_p = path_cost(current_state)
            return writeOutput(p_t_g, c_o_p, len(explored), max_depth, t2-t1, max_usage)
        current_config = tuple(current_state.config)
        f_set.remove(current_config)
        explored.add(current_config)
        ns = current_state.expand()
        for n in ns:
            if tuple(n.config) not in explored and tuple(n.config) not in f_set:
                frontier.put(n)
                f_set.add(tuple(n.config))
                if n.cost > max_depth:
                    max_depth = n.cost


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    t1 = time.time()
    frontier = [initial_state]
    f_set = set()
    explored = set()

    f_set.add(tuple(initial_state.config))
    max_depth = 0

    while len(frontier) > 0:
        current_state = frontier.pop()
        f_set.remove(tuple(current_state.config))
        if test_goal(current_state):
            t2 = time.time()
            p_t_g, c_o_p = path_cost(current_state)
            max_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return writeOutput(p_t_g, c_o_p, len(explored), max_depth, t2 - t1, max_usage)
        explored.add(tuple(current_state.config))
        ns = current_state.expand()[::-1]
        for n in ns:
            if tuple(n.config) not in explored and tuple(n.config) not in f_set:
                frontier.append(n)
                f_set.add(tuple(n.config))
                if n.cost > max_depth:
                    max_depth = n.cost


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    t1 = time.time()
    entry = 0
    f_set = set()
    explored = set()
    max_depth = 0

    f_heap = []
    heapq.heappush(f_heap, (0, entry, initial_state))
    f_set.add(tuple(initial_state.config))

    while len(f_heap) > 0:
        current_state = heapq.heappop(f_heap)
        f_set.remove(tuple(current_state[2].config))
        if test_goal(current_state[2]):
            t2 = time.time()
            p_t_g, c_o_p = path_cost(current_state[2])
            max_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return writeOutput(p_t_g, c_o_p, len(explored), max_depth, t2 - t1, max_usage)
        explored.add(tuple(current_state[2].config))
        ns = current_state[2].expand()
        for n in ns:
            entry += 1
            if tuple(n.config) not in explored and tuple(n.config) not in f_set:
                d = calculate_total_cost(n)
                heapq.heappush(f_heap, (d, entry, n))
                f_set.add(tuple(n.config))
                if n.cost > max_depth:
                    max_depth = n.cost


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    total_manhattan_distance = 0
    for idx in range(1, 9):
        total_manhattan_distance += calculate_manhattan_dist(idx, state.config.index(idx), 3)
    return state.cost + total_manhattan_distance


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    return abs(idx % n - value % n) + abs(idx // n - value // n)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    return puzzle_state.config == goal


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()
