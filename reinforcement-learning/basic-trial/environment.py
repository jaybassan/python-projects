# mostly from https://towardsdatascience.com/hands-on-introduction-to-reinforcement-learning-in-python-da07f7aaca88
import numpy as np

# define possible actions - up, down, left, and right
ACTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

class Maze(object):
    def __init__(self):
        # starts by defining the maze
        self.maze = np.zeroes((6, 6))
        self.maze[0, 0] = 2 # our robot is labelled as 2 and starts at (0, 0)
        self.maze[5, :5] = 1 # walls of the maze
        self.maze[:4, 5] = 1
        self.maze[2, 2:] = 1
        self.maze[3, 2] = 1

        self.robot_position = (0, 0)
        self.steps = 0 # how many steps has the robot taken

        # not exactly sure what these do
        # self.allowed_states = None
        # self.construct_allowed_states()

    def is_allowed_move(self, state, action):
        y, x = state
        y += ACTIONS[action][0]
        x += ACTIONS[action][1]

        # moving off the board
        if y < 0 or x < 0 or y > 5 or x > 5:
            return False
        
        # only acceptable moves are into an empty square or to stay still
        # TODO is this not simpler as if self.. != 1
        if self.maze[y, x] == 0 or self.maze[y, x] == 2:
            return True
        else:
            return False
        
    def update_maze(self, action):
        y, x = self.robot_position
        self.maze[y, x] = 0 # setting current position to empty
        
        y += ACTIONS[action][0] # get new coords
        x += ACTIONS[action][1]
        
        self.robot_position = (y, x) # updates
        self.maze[y, x] = 2
        self.steps += 1

    def is_game_over(self):
        if self.robot_position == (5, 5):
            return True
        else:
            return False
        
    def give_reward(self):
        if self.robot_position == (5, 5):
            return 0
        else:
            return -1
        
    def get_state_and_reward(self):
        return self.robot_position, self.give_reward()

        
