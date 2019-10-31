import statistics
from tkinter import *
from collections import defaultdict
import pdb

class MinMaxGraph:
    
    def __init__(self, graph, canvas, game):
        self.game = game
        self.width = 1500
        self.height = 1500
        # number of items in each row
        self.terminal_node_count = 0
        self.canvas = canvas
        self.graph = graph

    """
    draws a graph given a root node
    
    returns the x and y location of the object drawn
    """
    def draw_graph(self, state, row = 1):
        #note: odd rows are max, even rows are min
        utility = None
        #recursive case: this is not an end-state of the tic-tac-toe game
        ySpacing = 120
        currx = None
        curry = row*ySpacing

        if not (self.game.terminal_test(state)):
            child_x_values = list()
            child_utility_values = list()
        
            #find all the legal moves
            legal_moves = self.game.actions(state)
            children = []
            for move in legal_moves:
                result_state = self.game.result(state, move)
                next_row = row + 1
                childx,childy,utility = self.draw_graph(result_state, next_row)
                child_x_values.append(childx)
                child_utility_values.append(utility)
                children += [(childx,childy)]
            #set this nodes horizontal location to the average of its children's 
            #horizontal locations
            mean_child_x = statistics.mean(child_x_values)
            currx = int(mean_child_x)
            childYIncrement = -33
            currYIncrement = 20
            currXIncrement = -5
            for child in children:
                self.canvas.create_line(child[0], child[1]+childYIncrement, currx+currXIncrement, curry+currYIncrement) 
            #on max row, find the max utility of the child elements
            if(row%2 == 1):
                utility = max(child_utility_values)
            #on min row, find the min utility of the child elements
            else:
                utility = min(child_utility_values)
        #base case: this is an end state of the tic-tac-toe game
        else:
            #pdb.set_trace()
            self.terminal_node_count += 1
            currx = self.terminal_node_count * 40
            utility = self.game.utility(state, state.to_move)
            
        state_text = minmax_utility_label(state, self.game)
        state_text += '\n'
        state_text += tic_tac_toe_state_text(state, self.game)
        self.canvas.create_text((currx,curry), text = state_text)
        #self.canvas.pack()
        
        return (currx, curry, utility)
        
"""
translates the state of a tic-tac-toe game into a string
"""
def tic_tac_toe_state_text(state, game):
    output = ""
    board = state.board
    
    for x in range(1, game.h + 1):
        for y in range(1, game.v + 1):
            output += board.get((x, y), '#')
        output += "\n"
    return output
      
"""
returns a text string indicating the min/max utility of a given node
"""
def minmax_utility_label(state, game):
    points = game.utility(state,state.to_move)
    player_name = ""
    if(state.to_move == 'X'):
        player_name = "Max"
    else:
        player_name = "Min"
    return("{}: {}".format(player_name, points))


