# Austin Nowlen 50132880

class GameState:
    def __init__(self, row_count: int, column_count: int, starting_top_left: str, starting_player: str, how_to_win: str):
        self.new_gameboard(row_count, column_count)
        self.create_starting_layout(starting_top_left)
        self.turn = starting_player
        self.winning_option = how_to_win
        
    def new_gameboard(self, num_rows: int, num_columns: int)->None:
        '''creates a new empty gameboard in self.board'''
        new_board = []
        for r_num in range(num_rows):
            row = []
            for c_num in range(num_columns):
                row.append('.')
            new_board.append(row)
        self.board = new_board

    def print_gameboard(self)->None:
        '''prints the existing game board (self.board) to the console'''
        for row in self.board:
            a = ''
            for column in row:
                a += (' ' + column)
            print(a)

    def change_turn(self)->None:
        '''changes the current turn (slef.turn) to the opposite player'''
        if self.turn == 'B':
            self.turn = 'W'
        elif self.turn == 'W':
            self.turn = 'B'

    def create_starting_layout(self, top_left: str)->None:
        ''' takes in a GameState class (self) and prompts the user for which piece they want in top left corner then creates the layout in the self.board'''
        # Finds two middle rows and columns
        row_count = _find_row_count(self)
        column_count = _find_column_count(self)
        middle_row_1 = int(row_count / 2) - 1
        middle_row_2 = int(middle_row_1 + 1)
        middle_column_1 = int(column_count / 2) - 1
        middle_column_2 = int(middle_column_1 + 1)
        # Adds the correct colors in correct rows depending on user preference
        if top_left == 'white':
            self.board[middle_row_1][middle_column_1] = 'W'
            self.board[middle_row_1][middle_column_2] = 'B'
            self.board[middle_row_2][middle_column_1] = 'B'
            self.board[middle_row_2][middle_column_2] = 'W'
        elif top_left == 'black':
            self.board[middle_row_1][middle_column_1] = 'B'
            self.board[middle_row_1][middle_column_2] = 'W'
            self.board[middle_row_2][middle_column_1] = 'W'
            self.board[middle_row_2][middle_column_2] = 'B'
            
    def add_move(self, move: (int, int))->None:
        '''checks if the desired move is vaild according to Othello rules. If so adds move to the gameboard. If not a valid move, raises an exception.'''
        row ,column = move
        row_index = row -1
        column_index = column -1
        try:
            _check_if_occupied(self, row_index, column_index)
            valid_directions = _check_validity_all_directions(self, row_index, column_index, self.turn)
            _add_move_to_board(self, row_index, column_index, self.turn)
            _change_pieces_in_between(self, row_index, column_index, valid_directions, self.turn)
        except:
            raise InvalidMoveError

    def whose_turn_it_is(self)->str:
        '''returns the current turn'''
        if self.turn == 'B':
            return 'Black'
        else:
            return 'White'
        
    def any_moves_left_for_player(self, turn: str)-> bool:
        '''takes in a player in form of B or W and checks every open move to see if there is a valid move left for that player. If no valid moves, returns False.'''
        if _check_for_valid_moves_of_player(self, turn) == True:
            return False
        else:
            return True

    def is_game_over(self)->bool:
        '''checks to see if game is over by checking for valid moves for both players. If no vaild moves left for either player, returns True.'''
        possible_moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == '.':
                    try:
                        possible_moves.extend(_check_validity_all_directions(self, row, column, 'B')) #only raise exception if no valid moves for this piece
                    except:
                        pass
                    try:
                        possible_moves.extend(_check_validity_all_directions(self, row, column, 'W')) #only raise exception if no valid moves for this piece
                    except:
                        pass
        if possible_moves == []:
            return True
        #returns True if no possible moves left for given color/player
        elif possible_moves != []:
            return False
    
    def check_who_won(self)-> str:
        '''checks to see who won (either most or least which was specified at the beginning of the game) and returns the player with the appropriate winning score.'''
        if self.winning_option == 'most':
            return _win_by_most(self)
        elif self.winning_option == 'least':
            return _win_by_least(self)
        
    def check_score(self)-> None:
        '''checks the score for each player and updates self.score as a tuple (black,white).'''
        black_score = 0
        white_score = 0
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == 'B':
                    black_score += 1
                elif self.board[row][column] == 'W':
                    white_score += 1
        self.score = (black_score, white_score)



        

class InvalidMoveError(Exception):
    pass

def _win_by_most(game:'GameState')->str:
    '''takes in a GameState and returns the player with the highest score as a str.'''
    game.check_score()
    if game.score[0] > game.score [1]:
        return 'Black'
    elif game.score[1] > game.score[0]:
        return 'White'
    elif game.score[0] == game.score[1]:
        return 'Tie'

def _win_by_least(game: 'GameState')->str:
    '''takes in a GameState and returns the player with the lowest score as a str.'''
    game.check_score()
    if game.score[0] > game.score [1]:
        return 'White'
    elif game.score[1] > game.score[0]:
        return 'Black'
    elif game.score[0] == game.score[1]:
        return 'Tie'

def _find_row_count(game: 'GameState')-> int:
    '''takes in a GameState and returns the total amount of rows as an int.'''
    row_count = 0
    for row in game.board:
        row_count += 1
    return row_count

def _find_column_count(game: 'GameState')->int:
    '''takes in a GameState and returns the total amount of columns as an int.'''
    column_count = 0
    for column in game.board[0]:
        column_count += 1
    return column_count

def _check_if_occupied(game: 'GameState', row_of_piece: int, column_of_piece: int)->None:
    '''takes in a GameState, desired row of piece, and desired column of piece and raises and exception if the space if already occupied by a piece of either player.'''
    if game.board[row_of_piece][column_of_piece] == 'B' or game.board[row_of_piece][column_of_piece] == 'W':
        raise InvalidMoveError

def _check_if_valid(game: 'GameState', row :int, column: int, turn, direction: (int,int)):
    '''takes in a GameState, row of desired piece, column of desired piece, the current turn, and a direction as a tuple (int,int) of either 1,0,-1 and returns False if an invalid move
or the coordinates of the next player's piece in that direction and the direction if it is a vaild move as a tuple (int,int,(int,int)).
    '''
    try:
        row_change, column_change = direction
        row_check = row + row_change
        column_check = column + column_change
        opposite_turn = _return_opposite_turn(turn)
        game_piece = game.board[row_check][column_check]
        if game_piece == turn:
            return False
        elif game_piece == opposite_turn:
            new_row_check = row_check
            new_column_check = column_check
            while True:
                new_row_check = new_row_check + row_change
                new_column_check = new_column_check + column_change
                next_game_piece = game.board[new_row_check][new_column_check]
                if next_game_piece == turn:
                    return (new_row_check, new_column_check, direction)
                elif next_game_piece == '.':
                    return False
        elif game_piece == '.':
            return False
    except:
        return False
    
def _check_validity_all_directions(game: 'GameState', row: int, column: int, turn: str):
    '''takes in a GameState, desired row of piece, desired column of piece, and the current turn and raise an exception if it is not valid to place a piece there
or returns a list of coordinates of the players pieces that were encountered during a valid move as a tuple [(int,int,(int,int))].
'''
    valid_directions= []
    for checking_row in [-1, 0, 1]:
        for checking_column in [-1, 0 ,1]:
            current_direction_check = _check_if_valid(game, row, column, turn, (checking_row, checking_column))
            if current_direction_check != False:
                if current_direction_check[0] >= 0 and current_direction_check[1] >= 0:
                    valid_directions.append(current_direction_check)
    if valid_directions != []:
        return valid_directions
    else:
        raise InvalidMoveError
            
def _return_opposite_turn(turn: str)->str:
    '''takes in a turn and returns the opposite turn.'''
    if turn == 'B':
        return 'W'
    else:
        return 'B'

def _add_move_to_board(game: 'GameState', row: int, column: int, turn: str)->None:
    '''takes in a GameState, row of desired piece, column of desired piece, and the current turn and adds the piece of that player to the gameboard (self.board).'''
    if turn == 'B':
        game.board[row][column] = 'B'
    else:
        game.board[row][column] = 'W'

def _change_pieces_in_between(game: 'GameState', starting_row: int, starting_column: int, valid_directions: [(int,int, (int,int))], turn: str)->int:
    '''takes in a GameState, desired row of piece, desired column of piece, list of coordinates and directions from _check_validity_all_directions, and the current turn
and changes every piece betweent the given row and column to each coordinate in the list of coordinates and directions.
    '''
    for valid_direction in valid_directions:
        row, column, direction = valid_direction
        row_change, column_change = direction
        row_to_change = starting_row
        column_to_change = starting_column 
        while True:
            row_to_change = row_to_change + row_change
            column_to_change = column_to_change + column_change
            game.board[row_to_change][column_to_change] = turn
            if (row_to_change, column_to_change) == (valid_direction[0],valid_direction[1]):
                break

def _get_space(game: 'GameState', row: int, column: int)->str:
    '''takes in a GameState, row, and column and returns the current player or empty piece in that space on the gameboard.'''
    return game.board[row][column]

def _check_next_piece(game: 'GameState', row: int, column: int, turn: str, direction: (int, int))->bool:
    '''takes in a GameState, row, column, current turn, and a direction as tuple (int,int) and returns True next piece in that direction is of the opposite player and False if of the current player.'''
    x_axis, y_axis = direction
    opposite_turn = _return_opposite_turn(turn)
    checking_row = row + x_axis
    checking_column = column + y_axis
    next_piece_over = game.board[checking_row][checking_column]
    if next_piece_over == opposite_turn:
        return True
    else:
        return False

def _check_for_valid_moves_of_player(game: 'GameState', turn: str)->bool:
    '''takes in a GameState and a current turn and returns True if there is no valid moves left for the current turn or False if there is still valid moves left for the current turn'''
    possible_moves = []
    for row in range(len(game.board)):
        for column in range(len(game.board[row])):
            if game.board[row][column] == '.':
                try:
                    possible_moves.extend(_check_validity_all_directions(game, row, column, turn)) #only raise exception if no valid moves for this piece
                except:
                    pass
    if possible_moves == []:
        return True
    #returns True if no possible moves left for given color/player
    elif possible_moves != []:
        return False
