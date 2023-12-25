import copy
import cProfile
import pstats


class GameBoard:
    def __init__(self, board = [[' ' for _ in range(3)] for _ in range(3)], game_over = False, winner = None):
        self.board = board
        self.game_over = game_over
        self.winner = winner

    def Get_board(self):
        return self.board
    
    def Set_board(self,new_board):
        self.board = new_board

    def Get_winner(self):
        return self.winner

    def Get_game_over(self):
        return self.game_over
    
    def Check_valid_move(self,move):
        if self.game_over:
            return False
        if 0 <= move[0] < 3 and 0 <= move[1] < 3:
            if self.board[move[0]][move[1]] == ' ':
                return True
        return False

    def Place_move(self, move, player) -> None:
        if self.game_over:
            if self.winner:
                print("Cannot place move. The game is over. Player {} won".format(self.winner))
            else:
                print("The game is over with no winner.")
        if player not in ['x', 'o']:
            print("Move for player: {} not accepted. Please use lower case 'x' or 'o' to specify player".format(player))
        if 0 <= move[0] < 3 and 0 <= move[1] < 3:
            if self.board[move[0]][move[1]] != ' ':
                print("There is currently a piece: {} at position {} {}".format(self.board[move[0]][move[1]], move[0],
                                                                                move[1]))
            else:
                self.board[move[0]][move[1]] = player
        else:
            print("Move to row {} col {} is invalid. Please values to 0-2 inclusive".format(move[0], move[1]))
        self.game_over = self.Check_game_over()

    def Check_game_over(self) -> bool:
        for i in range(3):
            col = [self.board[j][i] for j in range(3)]
            if self.board[i][:].count('x') == 3 or self.board[i][:].count('o') == 3:
                if self.board[i][:].count('x') == 3:
                    self.winner = 'x'
                else:
                    self.winner = 'o'
                return True
            elif col.count('x') == 3 or col.count('o') == 3:
                if col.count('x') == 3:
                    self.winner = 'x'
                else:
                    self.winner = 'o'
                return True
        diagonal_one = [self.board[0][0], self.board[1][1], self.board[2][2]]
        diagonal_two = [self.board[2][0], self.board[1][1], self.board[0][2]]

        for diagonal in [diagonal_one, diagonal_two]:
            if diagonal.count('x') == 3 or diagonal.count('o') == 3:
                if diagonal.count('x') == 3:
                    self.winner = 'x'
                else:
                    self.winner = 'o'
                return True
        for row in self.board:
            for p in row:
                if p == ' ':
                    return False
        return True

    def Print_board(self) -> None:
        for i in range(3):
            row_string = ""
            for j in range(3):
                row_string += self.board[i][j]
                if j != 2:
                    row_string += '|'
            print(row_string)
            if i != 2:
                print('-----')
    
    def Get_isomorphic_boards(self) -> []:
        isomorphic_boards = [self.board]
        current_board = self.board
        for _ in range(3):
            new_board = []
            for i in range(3):
                new_row = []
                for j in range(3):
                    new_row.append(current_board[j][i])
                new_board.append(new_row[::-1])
            isomorphic_boards.append(new_board)
            current_board = new_board
        return isomorphic_boards
    
    def Is_board_isomorphic(self,different_board) -> bool:
        return different_board.Get_board() in self.Get_isomorphic_boards()

class GameState(GameBoard):
    def __init__(self, parent = None, player_turn= None):
        super().__init__()
        self.parent = parent
        self.children = None
        self.value = None
        self.player_turn = player_turn

    def Get_parent(self):
        return self.parent
    
    def Set_parent(self,new_parent):
        self.parent = new_parent
    
    def Get_children(self):
        return self.children
    
    def Get_value(self):
        return self.value
    
    def Set_value(self,new_value):
        self.value = new_value
    
    def Get_player_turn(self):
        return self.player_turn
    
    def Set_player_turn(self,new_player_turn):
        self.player_turn = new_player_turn
    
    def Evaluate_AB(self,alpha,beta):
        if self.Get_game_over():
            if self.winner == 'o':
                self.value = 1
            elif self.winner == 'x':
                self.value = -1
            else:
                self.value = 0
            return self.value
        else:
            if self.player_turn == 'x':
                next_player_turn = 'o'
            else:
                next_player_turn = 'x'
            potential_moves = self.Generate_next_moves()
            if self.player_turn == 'o': #maximize
                max_val = float('-inf')
                for move in potential_moves:
                    new_state = GameState()
                    new_state.Set_board(copy.deepcopy(self.Get_board()))
                    new_state.Set_parent(self)
                    new_state.Set_player_turn(next_player_turn)
                    new_state.Place_move(move, self.player_turn)
                    new_child_flag = self.Add_child(new_state)
                    if new_child_flag:
                            max_val = max(max_val,new_state.Evaluate_AB(alpha,beta))
                            self.value = max_val
                            if max_val >= beta:
                                self.value = beta
                                break
                            alpha = max(max_val,alpha)
                return max_val
            else:
                min_val = float('inf')
                for move in potential_moves:
                    new_state = GameState()
                    new_state.Set_board(copy.deepcopy(self.Get_board()))
                    new_state.Set_parent(self)
                    new_state.Set_player_turn(next_player_turn)
                    new_state.Place_move(move, self.player_turn)
                    new_child_flag = self.Add_child(new_state)
                    if new_child_flag:
                            min_val = min(min_val,new_state.Evaluate_AB(alpha,beta))
                            self.value = min_val
                            if min_val <= alpha:
                                break
                            beta = min(min_val,beta)
                return min_val
                            





    
    def Evaluate_mini_max(self):
        if self.game_over:
            if self.winner == 'o':
                self.value = 1
            elif self.winner == 'x':
                self.value = -1
            else:
                self.value = 0
            return self.value
        else:
            if self.player_turn == 'o':
                value = float('-inf')
                for child in self.children:
                    value = max(value, child.Evaluate_mini_max())
                self.value = value
            else:
                value = float('inf')
                for child in self.children:
                    value = min(value,child.Evaluate_mini_max())
                self.value = value
            return self.value
    
    def Generate_next_moves(self) -> []:
        if self.game_over is False:
            valid_moves = []
            for i in range(3):
                for j in range(3):
                    if self.Check_valid_move([i,j]) :
                        valid_moves.append([i,j])
            return valid_moves
        else:
            return []
    
    def Add_child(self,new_child) -> bool:
        if self.children is None:
            self.children = [new_child]
            return True
        else:
            for child in self.children:
                if child.Is_board_isomorphic(new_child):
                    return False
            self.children.append(new_child)
            return True
    

class Minimax():
    def __init__(self, root=None,maximizer = None) -> None:
        self.root = root #game state
        self.maximizer = maximizer #bot player 'x' or 'o'
    
    def Set_root(self, new_root):
        self.root = new_root

    def Update_state(self, new_state):
        for child in self.root.Get_children():
            if child.Get_board() == new_state.Get_board():
                self.root = child
                break
    
    def Build_tree(self):
        num_states = 0
        queue = [self.root]
        while len(queue) > 0:
            expanded_node = queue.pop(0)
            next_moves = expanded_node.Generate_next_moves()
            current_player = expanded_node.Get_player_turn()
            if current_player == 'x':
                next_player_turn = 'o'
            else:
                next_player_turn = 'x'
            for move in next_moves:
                new_state = GameState()
                new_state.Set_board(copy.deepcopy(expanded_node.Get_board()))
                new_state.Set_parent(expanded_node)
                new_state.Set_player_turn(next_player_turn)
                new_state.Place_move(move, current_player)
                new_child_flag = expanded_node.Add_child(new_state)
                if new_child_flag:
                    queue.append(new_state)
    
    def Get_next_move(self):
        best_move = None
        for child in self.root.Get_children():
            move_value = child.Evaluate_mini_max()
            if best_move is None:
                best_move = [move_value,child]
            else:
                if move_value > best_move[0]:
                    best_move = [move_value,child]
        self.root = best_move[1]
        return self.root
    

class Alpha_Beta():
    def __init__(self, root=None):
        self.root = root
    
        if self.root is not None:
            alpha = float('-inf')
            beta = float('inf')
            best_val = self.root.Evaluate_AB(alpha,beta)
            for child in self.root.Get_children():
                if child.Get_value() == best_val:
                    child.Print_board()
                    break


gstate = GameState()
gstate.Place_move([1,1],'x')
gstate.Place_move([0,1],'o')
gstate.Place_move([1,0],'x')
gstate.Place_move([1,2],'o')
gstate.Place_move([2,0],'x')
gstate.Place_move([0,2],'o')
gstate.Place_move([2,2],'x')
gstate.Print_board()
gstate.Set_player_turn('o')
a_b_test = Alpha_Beta(gstate)


