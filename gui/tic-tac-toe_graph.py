import statistics
from tkinter import *
from collections import defaultdict
import pdb

class MinMaxGraph:
    
    def __init__(self, canvas, game):
        self.game = game
        self.width = 1500
        self.height = 1500
        # number of items in each row
        self.terminal_node_count = 0
        self.canvas = canvas

    """
    draws a graph given a root node
    
    returns the x and y location of the object drawn
    """
    def draw_graph(self, state, row = 1):
    
        ySpacing = 120
        currx = None
        curry = row*ySpacing

        if not (self.game.terminal_test(state)):
            child_x_values = list()
        
            legal_moves = self.game.actions(state)
            children = []
            for move in legal_moves:
                result_state = self.game.result(state, move)
                next_row = row + 1
                childx,childy = self.draw_graph(result_state, next_row)
                child_x_values.append(childx)
                children += [(childx,childy)]
                
            mean_child_x = statistics.mean(child_x_values)
            currx = int(mean_child_x)

            childIncrement = -27
            currIncrement = 10
            for child in children:
                self.canvas.create_line(child[0], child[1]+childIncrement, currx, curry+currIncrement) 

        else:
            #pdb.set_trace()
            self.terminal_node_count += 1
            currx = self.terminal_node_count * 25
            

        state_text = minmax_utility_label(state, self.game);    
        state_text = tic_tac_toe_state_text(state, self.game)
        self.canvas.create_text((currx,curry), text = state_text)
        #self.canvas.pack()
        return (currx, curry)
        
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
    return("")
    


