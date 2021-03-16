"""
Author : DANDJI Ayawo Désiré - s197206
	   & SAFFO NGUOANDJO Borel - s204863   

"""
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue


def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return hash((state.getPacmanPosition(), state.getFood()))


def mHeuristic(state, foodState):
        """
        Given a pacman game and food state,returns the cost of heuristic in heuristic .

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                    `pacman.GameState`.
        - `foodState`: set that contains the coordinates a and b of every food

        Return:
        -------
        - the heuristic.
        """
        pacmanPosition = state.getPacmanPosition()
        mDistance = []
        
        for x, y in foodState:
            gCost = abs(x - pacmanPosition[0]) + abs(y - pacmanPosition[1])
            mDistance.append(gCost)
        
        if mDistance:
            heuristic = mDistance[0]
            for x in mDistance:
                if (x < heuristic):
                    heuristic = x

            return heuristic
        return 0
    



       

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        if not self.moves:
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

        return Directions.STOP


    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves who allow to go fast in the goal.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves in the maze
        """
        path = []
        fringe = PriorityQueue()
        # update of finge with the startNode
        fringe.push((state, 0, path), 0)
        # list_closed that contains states already visited
        list_closed = set()
        # add the states visited in list_closed 
        list_closed.add(state)
        gCost = 0
        food = state.getFood()
        # list of each food position
        foodState = list()
        # width and height of food
        fWidth = food.width
        fHeight = food.height
        
        for x in range (fWidth):
            for y in range (fHeight):
                if(food[x][y]):
                    foodState.append((x, y))

        while(True):
            if fringe.isEmpty():
                return path  #failure

            _,(current_node, gCost, path) = fringe.pop()
            current_node_key = key(current_node)
            # check if the astar has finished his exploration
            if current_node.isWin():
                return path 
            # check if current_node_key has already visited and put it in closed
            if current_node_key not in list_closed:
                list_closed.add(current_node_key)
                # recovery of the current pacman position
                a, b = current_node.getPacmanPosition()
                if(food[a][b]):
                    gCost -= 1
 
                for next_node, action in current_node.generatePacmanSuccessors():
                    if key(next_node) not in list_closed:
                    	# compute of fCost
                        fCost = gCost + mHeuristic(next_node, foodState)
                        # update of the firnge 
                        fringe.push((next_node, gCost, path + [action]), fCost)

        return path