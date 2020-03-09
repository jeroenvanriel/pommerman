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
        self._position = None

        # this will hold the board state
        self._board = None

        # this queue will hold the actions for future turns
        self._actionQueue = queue.SimpleQueue()

    def act(self, obs, action_space):
        self._position = tuple(obs['position'])
        self._board = obs['board']

        # the position that we want to reach
        goal = (5, 5)

        self.moveToPosition(goal)

        return self._actionQueue.get(False)

    # check if there exists a path between start and goal
    # TODO: backtracking of path
    def bfs(self, nodeList, goal, visited=None):
        newNodes = []

        if visited:
            visited = visited + nodeList
        else:
            visited = nodeList

        for node in nodeList:
            # if this node is the goal position
            if node == goal:
                return True

            for child in self.getValidChildren(node):
                if child not in newNodes and child not in visited:
                    newNodes.append(child)

        # if newNodes is not empty we must visit these next
        if newNodes:
            return self.bfs(newNodes, goal, visited)

        # if we did not find a solution so far and newNodes is empty, we go up in the recursion
        return False

    def getValidChildren(self, node):
        # just add all 4 neighbouring tiles
        children = [(node[0] - 1, node[1]), (node[0] + 1, node[1]), (node[0], node[1] - 1), (node[0], node[1] + 1)]

        # now we collect the valid moves
        validChildren = []

        # check if node represents a valid position on the board
        for child in children:
            # check if these positions are still in the range
            if 0 <= child[0] <= 10 and 0 <= child[1] <= 10 and self.board[child[0], child[1]] == 0:
                validChildren.append(child)

        return validChildren

    def moveToPosition(self, goal):
        # determine if we must go left or right
        if self._position[0] < goal[0]:
            # we must go to the right
            self._actionQueue.put(Action.Right)
        elif self._position[0] > goal[0]:
            # we must go to the left
            self._actionQueue.put(Action.Left)

        # determine if we must go up or down
        if self._position[1] < goal[1]:
            # we are above the goal
            self._actionQueue.put(Action.Down)
        elif self._position[1] > goal[1]:
            # we are under the goal
            self._actionQueue.put(Action.Up)