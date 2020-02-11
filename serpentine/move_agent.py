import numpy as np
import queue

from pommerman import characters
from pommerman.constants import Action
from pommerman.agents import BaseAgent


class MoveAgent(BaseAgent):
    """ Simple agent that is allowed to move randomly. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)

        # this will hold our current position
        self.position = None

        # this will hold the board state
        self.board = None

        # this queue will hold the actions for future turns
        self._actionQueue = queue.SimpleQueue()

    def act(self, obs, action_space):
        self.position = tuple(obs['position'])
        self.board = obs['board']

        # the position that we want to reach
        goal = (5, 5)

        self.moveToPosition(goal)

        return self._actionQueue.get(False)

    def moveToPosition(self, my_position, goal):
        # determine if we must go left or right
        if self.position[0] < goal[0]:
            # we must go to the right
            self._actionQueue.put(Action.Right)
        elif self.position[0] > goal[0]:
            # we must go to the left
            self._actionQueue.put(Action.Left)

        # determine if we must go up or down
        if self.position[1] < goal[1]:
            # we are above the goal
            self._actionQueue.put(Action.Down)
        elif self.position[1] > goal[1]:
            # we are under the goal
            self._actionQueue.put(Action.Up)