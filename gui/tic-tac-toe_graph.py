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
        #note: odd rows are max, even rows are min
        utility = None
        x = None
    
        #recursive case: this is not an end-state of the tic-tac-toe game
        if not (self.game.terminal_test(state)):
            child_x_values = list()
            child_utility_values = list()
        
            #find all the legal moves
            legal_moves = self.game.actions(state)
            for move in legal_moves:
                result_state = self.game.result(state, move)
                
                next_row = row + 1
                
                #draw the result state of each legal move from the current node
                #as a new node
                x,y,utility = self.draw_graph(result_state, next_row)
                child_x_values.append(x)
                child_utility_values.append(utility)
                
            #set this nodes horizontal location to the average of its children's 
            #horizontal locations
            mean_child_x = statistics.mean(child_x_values)
            x = int(mean_child_x)
            
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
            x = self.terminal_node_count * 40
            utility = self.game.utility(state, 'X')
            
        y = row*55

        state_text = minmax_utility_label(state, utility); 
        state_text += '\n'
        state_text += tic_tac_toe_state_text(state, self.game)
        self.canvas.create_text((x,y), text = state_text)
        #self.canvas.pack()
        
        
        
        return (x, y, utility)
        
    """
    given an x and y coordinate of a point, expand the canvas to include this point
    with a 20 pixel margin
    """
    def expand_canvas(self, x, y):
        if(x + 20 > self.width):
            self.width += 100
        if(y + 20 > self.height):
            self.height += 100
        self.canvas.configure(width=self.width, height=self.height)    
    
     
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
def minmax_utility_label(state, points):
    player_name = ""
    if(state.to_move == 'X'):
        player_name = "Max"
    else:
        player_name = "Min"
    return("{}: {}".format(player_name, points))


