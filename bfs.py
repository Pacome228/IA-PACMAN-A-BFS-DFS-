"""
Author : DANDJI Ayawo Désiré - s197206
       & SAFFO NGUOANDJO Borel - s204863   

"""
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Queue


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
            self.moves = self.bfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

        return Directions.STOP
    
    def bfs(self, state):
        path = []
        fringe = Queue()
        # update of finge with the startNode 
        fringe.push((state, path))
        # closed that contains states already visited
        list_closed = set()
        # add the states visited in list_closed 
        list_closed.add(state)

        while(True):
            if fringe.isEmpty():
                return path  #failure

            current_node, path = fringe.pop()

            current_node_key = key(current_node)
 			# check if the bfs has finished his exploration
            if current_node.isWin():
                return path 
            # check if current_node_key has already visited and put it in closed
            if current_node_key not in list_closed:
                list_closed.add(current_node_key)
                    
                for next_node, action in current_node.generatePacmanSuccessors():
                    if key(next_node) not in list_closed:
                    	# put the next node and it action in the fringe
                        fringe.push((next_node, path + [action]))

        return path
