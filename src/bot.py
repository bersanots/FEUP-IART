from search import *

class Klotski(Problem):

    def __init__(self, initial, goal):
        """ Define goal state and initialize the problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_red_piece(self, state):
        """Return the position of the top leftmost cell of the red piece in a given state"""
        
        return state.index(1)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = []
        all_pieces = set(state)
        all_pieces.remove(0)
        
        #all possible moves for all pieces
        for p in all_pieces:                                #p is the id of the piece
            possible_actions.extend([str(p)+'UP', str(p)+'DOWN', str(p)+'LEFT', str(p)+'RIGHT'])

        for p in all_pieces:
            current_piece_idx = state.index(p)                  #first cell of the piece in the list
            curr_piece_x = current_piece_idx // 4
            curr_piece_y = current_piece_idx % 4

            #piece width
            curr_piece_horiz_size = state[curr_piece_x*4:curr_piece_x*4+4].count(p)

            #piece height
            curr_piece_vert_size = 0
            for v in range(current_piece_idx, len(state), 4):
                if state[v] == p:
                    curr_piece_vert_size += 1

            left_col = curr_piece_y                                     #piece leftmost colummn
            top_row = curr_piece_x                                      #piece topmost row
            right_col = curr_piece_y + curr_piece_horiz_size - 1        #piece rightmost column
            bottom_row = curr_piece_x + curr_piece_vert_size - 1        #piece bottommost row

            if left_col == 0:                               
                possible_actions.remove(str(p) + 'LEFT')
            else: 
                for r in range(top_row, bottom_row + 1):
                    if state[r*4 + left_col - 1] != 0:                  #neighbour cell not empty
                        possible_actions.remove(str(p) + 'LEFT')
                        break
            if top_row == 0:                                
                possible_actions.remove(str(p) + 'UP')
            else: 
                for c in range(left_col, right_col + 1):
                    if state[(top_row - 1)*4 + c] != 0:                 #neighbour cell not empty
                        possible_actions.remove(str(p) + 'UP')       
                        break         
            if right_col == 3:                              
                possible_actions.remove(str(p) + 'RIGHT')
            else: 
                for r in range(top_row, bottom_row + 1):
                    if state[r*4 + right_col + 1] != 0:                 #neighbour cell not empty
                        possible_actions.remove(str(p) + 'RIGHT')
                        break
            if bottom_row == 4:                             
                possible_actions.remove(str(p) + 'DOWN')
            else:
                for c in range(left_col, right_col + 1):
                    if state[(bottom_row + 1)*4 + c] != 0:              #neighbour cell not empty
                        possible_actions.remove(str(p) + 'DOWN')
                        break

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        #check if piece id has 1 or 2 digits
        if action[1].isdigit():
            delim = 2
        else:
            delim = 1

        p = int(action[:delim])                                   #p is the id of the piece to move
        current_piece_idx = state.index(p)                        #first cell of the piece in the list
        curr_piece_x = current_piece_idx // 4
        curr_piece_y = current_piece_idx % 4

        #piece width
        curr_piece_horiz_size = state[curr_piece_x*4:curr_piece_x*4+4].count(p)

        #piece height
        curr_piece_vert_size = 0
        for v in range(current_piece_idx, len(state), 4):
            if state[v] == p:
                curr_piece_vert_size += 1

        left_col = curr_piece_y                                     #piece leftmost colummn
        top_row = curr_piece_x                                      #piece topmost row
        right_col = curr_piece_y + curr_piece_horiz_size - 1        #piece rightmost column
        bottom_row = curr_piece_x + curr_piece_vert_size - 1        #piece bottommost row

        move = action[delim:]
        new_state = list(state)

        delta = {'UP':-4, 'DOWN':4, 'LEFT':-1, 'RIGHT':1}

        #switch between neighbour cells
        for x in range(top_row, bottom_row + 1):
            for y in range(left_col, right_col + 1):
                if move=='DOWN':
                    index = (top_row + bottom_row - x)*4 + y
                elif move=='RIGHT':
                    index = x*4 + (left_col + right_col - y)
                else:
                    index = x*4 + y
                neighbour = index + delta[move]
                new_state[index], new_state[neighbour] = new_state[neighbour], new_state[index]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state
        (if the red piece is on the right position) or False, otherwise """

        return self.find_red_piece(state) == self.goal

    #Manhattan
    """def h(self, node):
        " Return the heuristic value for a given state."

        # Manhattan Heuristic Function
        x1, y1 = self.find_red_piece(node.state) // 4, self.find_red_piece(node.state) % 4
        x2, y2 = self.goal // 4, self.goal % 4

        return abs(x2 - x1) + abs(y2 - y1)"""

    # sums up the number of pieces between the goal (red) block and the final space
    # including whether or not the empty spaces are adjacent
    # and returns that value
    def h(self, node):
        red_idx = self.find_red_piece(node.state)
        red_x = red_idx // 4
        total = 0

        empty_index = int(node.state.index(0))
        if (empty_index % 4 != 0  and  node.state[empty_index % 4] != 0) \
            or (node.state[(empty_index + 4) % 20] != 0):
            total += 2

        for key in sorted(set(node.state) - set([0])):
            piece_idx = node.state.index(key)
            piece_x = piece_idx // 4
            if (piece_x > red_x):
                piece_width = node.state[piece_x*4 : piece_x*4 + 4].count(key)
                piece_heigth = 0
                for v in range(red_idx, len(node.state), 4):
                    if node.state[v] == 3:
                        piece_heigth += 1
                total += piece_width * piece_heigth
        
        return int(total)


def heuristic(node,goal):
        """ Return the heuristic value for a given state."""

        # Manhattan Heuristic Function
        x1, y1 = node.state.index(1) // 4, node.state.index(1) % 4          #index 1 = red piece
        x2, y2 = goal // 4, goal % 4

        return abs(x2 - x1) + abs(y2 - y1)



"""init_state = [3,1,1,4,
              2,1,1,5,
              6,7,8,9,
              6,10,11,9,
              12,0,0,13]
goal_index = 13
puzzle = Klotski(tuple(init_state),goal_index)"""

#print("A*: " + str(astar_search(puzzle).solution()))
#print("dfs: " + str(depth_first_graph_search(puzzle).solution()))
#print("bfs: " + str(breadth_first_graph_search(puzzle).solution()))
#print("uniform: " + str(uniform_cost_search(puzzle).solution()))
#print("iterative: " + str(iterative_deepening_search(puzzle).solution()))
#print("greedy: " + str(greedy_best_first_graph_search(puzzle,lambda n: n.path_cost + heuristic(n,goal_index)).solution()))                                               