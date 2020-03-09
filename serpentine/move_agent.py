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

        self._planned = False

    def act(self, obs, action_space):
        self._position = tuple(obs['position'])
        self._board = obs['board']

        print("position = " + str(self._position))

        # the position that we want to reach
        goal = (5, 5)

        nodes = self.bfs([((1, 1), None, None)], goal, [])

        actions = []
        for node in nodes:
            if node[2] is not None:
                actions.append(node[2])
                if not self._planned:
                    self._actionQueue.put(node[2])

        self._planned = True

        print("actions:")
        print(actions)

        if not self._actionQueue.empty():
            return self._actionQueue.get(False)
        else:
            return Action.Stop

    # check if there exists a path between start and goal
    def bfs(self, nodeList, goal, visitedPositions):
        newNodes = []

        for node in nodeList:
            # if this node is the goal position
            if node[0] == goal:
                return [node]

            for child in self.getValidChildren(node):
                if child[0] not in visitedPositions:
                    visitedPositions.append(node[0])
                    newNodes.append(child)

        # if newNodes is not empty we must visit these next
        if newNodes:
            result = self.bfs(newNodes, goal, visitedPositions)
            if result is not None:
                # add the predecessor to the beginning of the list.
                if result[0] is not None:
                    result.insert(0, result[0][1])
                    return result
                else:
                    return result

        # if we did not find a solution so far and newNodes is empty, we go up in the recursion
        return None

    def getValidChildren(self, node):
        # just add all 4 neighbouring tiles and add a reference to ourselves.
        children = [((node[0][0] - 1, node[0][1]), node, Action.Left),
                    ((node[0][0] + 1, node[0][1]), node, Action.Right),
                    ((node[0][0], node[0][1] - 1), node, Action.Up),
                    ((node[0][0], node[0][1] + 1), node, Action.Down)]

        # now we collect the valid moves
        validChildren = []

        # check if node represents a valid position on the board
        for child in children:
            # check if these positions are still in the range
            if 0 <= child[0][0] <= 10 and 0 <= child[0][1] <= 10 and self.isValidPosition(child[0]):
                validChildren.append(child)

        return validChildren

    # TODO: determine whether we may move to this position
    def isValidPosition(self, position):
        return self._board[position[0]][position[1]] == 0

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