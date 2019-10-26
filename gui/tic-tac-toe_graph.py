import statistics
from tkinter import *
from collections import defaultdict
import pdb

class MinMaxGraph:
    
    def __init__(self, root, game):
        self.root = root
        self.game = game
        # number of items in each row
        self.terminal_node_count = 0
        self.canvas = Canvas(root, width = 500, height = 500)

    """
    draws a graph given a root node
    
    returns the x and y location of the object drawn
    """
    def draw_graph(self, state, row = 1):
    
        x = None
    
        if not self.game.terminal_test(state):
            child_x_values = list()
        
            legal_moves = self.game.actions(state)
            for move in legal_moves:
                result_state = self.game.result(state, move)
                
                next_row = row + 1
                
                x,y = self.draw_graph(result_state, next_row)
                child_x_values.append(x)
                
            mean_child_x = statistics.mean(child_x_values)
            x = int(mean_child_x)
            
        else:
            #pdb.set_trace()
            self.terminal_node_count += 1
            x = self.terminal_node_count * 15
            
        y = row*40
        
        
        state_text = tic_tac_toe_state_text(state, self.game)
        self.canvas.create_text((x,y), text = state_text)
        self.canvas.pack()
        return (x, y)
     
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
        