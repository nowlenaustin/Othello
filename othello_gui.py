import othello_protocol
import tkinter
import math
import sys

rows = 'hi'
columns = 'hi'

DEFAULT_FONT = ('Helvetica', 14, 'bold italic')

class InvalidInputError(Exception):
    pass

class NoMovesGUI:
    def __init__(self, GUI: 'OthelloGUI'):
        self.window = tkinter.Toplevel()

        no_moves_label = tkinter.Label(master = self.window,
                                       text = 'This player has no moves.',
                                       font = DEFAULT_FONT)
        no_moves_label.grid(row = 0, column = 0 , padx = 10, pady = 10)

    def start(self):
        self.window.grab_set()
        self.window.wait_window()

class GameOptionsGUI:
    def __init__(self):
        self.options_window = tkinter.Tk()

        r_c_label = tkinter.Label(master = self.options_window,
                                  text = 'Please pick a even number between 4 and 16.',
                                  font = DEFAULT_FONT)
        r_c_label.grid(row = 0, column = 0, columnspan = 2, sticky = tkinter.W)

        row_label = tkinter.Label(master = self.options_window,
                                  text = 'Number of rows: ', font = DEFAULT_FONT)
        row_label.grid(row = 1, column = 0, sticky = tkinter.W)
        self.row_entry = tkinter.Entry(master = self.options_window, width = 10,
                                  font = DEFAULT_FONT)
        self.row_entry.grid(row = 1, column = 1)

        column_label = tkinter.Label(master = self.options_window,
                                  text = 'Number of columns: ', font = DEFAULT_FONT)
        column_label.grid(row = 2, column = 0, sticky = tkinter.W)
        self.column_entry = tkinter.Entry(master = self.options_window, width = 10,
                                  font = DEFAULT_FONT)
        self.column_entry.grid(row = 2, column = 1)

        b_w_label = tkinter.Label(master = self.options_window,
                                  text = 'Please pick either black or white.',
                                  font = DEFAULT_FONT)
        b_w_label.grid(row = 3, column = 0, columnspan = 2, sticky = tkinter.W)

        top_left_label = tkinter.Label(master = self.options_window,
                                  text = 'Who should start in the top left? ', font = DEFAULT_FONT)
        top_left_label.grid(row = 4, column = 0, sticky = tkinter.W)
        self.top_left_entry = tkinter.Entry(master = self.options_window, width = 10,
                                  font = DEFAULT_FONT)
        self.top_left_entry.grid(row = 4, column = 1)

        starting_player_label = tkinter.Label(master = self.options_window,
                                  text = 'Who should start the game? ', font = DEFAULT_FONT)
        starting_player_label.grid(row = 5, column = 0, sticky = tkinter.W)
        self.starting_player_entry = tkinter.Entry(master = self.options_window, width = 10,
                                  font = DEFAULT_FONT)
        self.starting_player_entry.grid(row = 5, column = 1)

        m_l_label = tkinter.Label(master = self.options_window,
                                      text = 'Please pick either most or least.',
                                      font= DEFAULT_FONT)
        m_l_label.grid(row = 6, column =0, columnspan= 2, sticky = tkinter.W)
        winning_label = tkinter.Label(master = self.options_window,
                                      text = 'How should the game be won? ', font = DEFAULT_FONT)
        winning_label.grid(row = 7, column= 0, sticky = tkinter.W)
        self.winning_entry = tkinter.Entry(master = self.options_window, width = 10,
                                           font = DEFAULT_FONT)
        self.winning_entry.grid(row=7, column = 1)
        
        accept_button = tkinter.Button(master = self.options_window,
                                       text = 'Accept', font = DEFAULT_FONT,
                                       command = self._on_accept_clicked)
        accept_button.grid(row = 8, column = 1)
    
        
        self.options_window.rowconfigure(0, weight = 0)
        self.options_window.rowconfigure(1, weight = 0)
        self.options_window.rowconfigure(2, weight = 0)
        self.options_window.rowconfigure(3, weight = 0)
        self.options_window.rowconfigure(4, weight = 0)
        self.options_window.rowconfigure(5, weight = 0)
        self.options_window.rowconfigure(6, weight = 0)
        self.options_window.rowconfigure(7, weight = 0)
        self.options_window.rowconfigure(8, weight = 0)

        self.options_window.columnconfigure(0, weight = 0)
        self.options_window.columnconfigure(1, weight = 0)
        self.options_window.columnconfigure(2, weight = 0)

        

    def start(self):
        self.options_window.mainloop()

    def _on_accept_clicked(self):
        try:
            self.rows = int(self.row_entry.get())
            self.columns = int(self.column_entry.get())
            self.top_left = self.top_left_entry.get().lower()
            self.starting_player = self.starting_player_entry.get().lower()
            self.winning = self.winning_entry.get().lower()
            if self.rows % 2 == 0 and self.rows >= 2 and self.rows <= 16:
                if self.columns % 2 == 0 and self.columns >= 2 and self.columns <= 16:
                    if self.top_left == 'white' or self.top_left == 'black':
                        if self.starting_player == 'white' or self.starting_player == 'black':
                            if self.winning == 'most' or self.winning == 'least':
                                self.options_window.destroy()
        except:
            pass
    
    
class OthelloGUI:
    def __init__(self):
        try:
            options = GameOptionsGUI()
            options.start()
            self.rows = options.rows
            self.columns = options.columns
            self.top_left = options.top_left
            self.starting_player = options.starting_player
            self.winning = options.winning
        except:
            sys.exit()
            
        self.game = othello_protocol.GameState(self.rows, self.columns,
                                               self.top_left, self._return_player_game_format(),
                                               self.winning)
        self.status = 'Status: ' + self.starting_player.title() + "'s turn."
        
        self.root_window = tkinter.Tk()
        
        self.canvas = tkinter.Canvas(
            master = self.root_window, width = self.rows * 95, height = self.columns *95,
            background = 'Green')
        self.canvas.grid(
            row = 1, column = 0, columnspan=3, padx = 5, pady = 5,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.canvas.bind('<Button-1>', self._full_turn)
        self.canvas.bind('<Configure>', self.draw_gameboard)
        
        self.black_score = tkinter.StringVar()
        self.white_score = tkinter.StringVar()
        self._check_score()
        game_label = tkinter.Label(master = self.root_window, text= 'Othello',
                                   font = DEFAULT_FONT)
        game_label.grid(row = 0, column = 1)
        black_score_label = tkinter.Label(master= self.root_window,
                                          textvariable= self.black_score,
                                          font = DEFAULT_FONT)
        black_score_label.grid(row = 0, column = 0, sticky = tkinter.W)
        
        white_score_label = tkinter.Label(master= self.root_window,
                                          textvariable= self.white_score,
                                          font = DEFAULT_FONT)
        white_score_label.grid(row = 0, column = 2, sticky = tkinter.E)

        self.status = tkinter.StringVar()
        self.status.set('Status: ' + self.game.whose_turn_it_is() + "'s turn.")
        game_status_label = tkinter.Label(master = self.root_window, textvariable = self.status,
                                    font = DEFAULT_FONT)
        game_status_label.grid(row = 3, column = 0, columnspan = 3,
                               sticky = tkinter.W)

        self.root_window.rowconfigure(0, weight = 0)
        self.root_window.rowconfigure(1, weight = 1)
        self.root_window.rowconfigure(2, weight = 0)
        self.root_window.columnconfigure(0, weight = 1)
        self.root_window.columnconfigure(1, weight = 1)
        self.root_window.columnconfigure(2, weight = 1)
        
        self.game_is_over = False
        
    def start(self):
        self.root_window.mainloop()

    def draw_gameboard(self, event: tkinter.Event):
        last_drawn_row_position = 0
        last_drawn_column_position = 0
        row_width = self.canvas.winfo_width() / self.rows
        column_width = self.canvas.winfo_height() / self.columns
        self.canvas.delete(tkinter.ALL)
        self._row_positions = []
        self._column_positions = []
        for row in range(self.rows +1):
            self.canvas.create_line(
                last_drawn_row_position, 0,
                last_drawn_row_position, self.canvas.winfo_height(),
                fill = 'black', width = 3)
            self._row_positions.append(last_drawn_row_position)
            last_drawn_row_position += row_width
        for column in range(self.columns +1):
            self.canvas.create_line(
                0, last_drawn_column_position,
                self.canvas.winfo_width(), last_drawn_column_position,
                fill = 'black', width = 3)
            self._column_positions.append(last_drawn_column_position)
            last_drawn_column_position += column_width
        self._create_box_positions()
        self._draw_pieces(self.game)

    def _create_box_positions(self):
        self.boxes = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.columns):
                tl_y = self._column_positions[column_index]
                tl_x = self._row_positions[row_index]
                br_y = self._column_positions[column_index + 1]
                br_x = self._row_positions[row_index + 1]
                row.append((self._return_frac_x_y(tl_x, tl_y),
                            self._return_frac_x_y(br_x, br_y)))
            self.boxes.append(row)
    
    def _add_piece_to_gameboard(self, event: tkinter.Event):
        try:
            row ,column = self._return_row_and_column(event)
            self.game.add_move((row +1, column +1))
            self.draw_gameboard(event)
        except:
            raise othello_protocol.InvalidMoveError

    def _full_turn(self, event: tkinter.Event):
        try:
            game_over = self.game.is_game_over()
            if game_over == True:
                self.game_is_over = True
                self.status.set('Status: Game over! ' + self._winning_player() + ' won!')
                return
            if self.game.any_moves_left_for_player(self.game.turn) == False:
                # maybe create modal window to say the player has no turns and then resume with next player upon close
                no_moves_window = NoMovesGUI(self)
                no_moves_window.start()
                self.game.change_turn()
                self.status.set('Status: ' + self.game.whose_turn_it_is() + "'s turn.")
                return
            self._add_piece_to_gameboard(event)
            self.game.change_turn()
            self.status.set('Status: ' + self.game.whose_turn_it_is() + "'s turn.")
            self._check_score()
            game_over = self.game.is_game_over()
            if game_over == True:
                self.game_is_over = True
                if self._winning_player() == 'Tie':
                    self.status.set("Status: Game Over! It's a Tie")
                else:
                    self.status.set('Status: Game over! ' + self._winning_player() + ' won!')
                return
        except:
            self.status.set('Status: Invalid move. Try another move.')

    def _draw_pieces(self, game: 'GameState')->None:
        '''takes in self draws all the pieces that are in self.game.board'''
        gameboard = self.game.board
        for row_index in range(len(gameboard)):
            for column_index in range(len(gameboard[0])):
                if gameboard[row_index][column_index] == 'B':
                    self._draw_piece((row_index, column_index), 'Black')
                elif gameboard[row_index][column_index] == 'W':
                    self._draw_piece((row_index, column_index), 'White')
                
    def _draw_piece(self, move: (int,int), turn_color: str)-> None:
        '''takes in self, a move as a tuple (int,int), and a color as a str and adds a piece of that color to that row and column of the gameboard'''
        row, column = move
        top_left, bottom_right = self.boxes[row][column]
        tl_x, tl_y = self._return_pixels_x_y(top_left)
        br_x, br_y = self._return_pixels_x_y(bottom_right)
        self.canvas.create_oval(tl_x +5, tl_y +5, br_x -5, br_y -5, fill = turn_color)

    def _return_row_and_column(self, event: tkinter.Event)->tuple:
        print(event.x , event.y)
        row_frac, column_frac = self._return_frac_x_y(event.x ,event.y)
        column_index = int(math.floor(column_frac * self.columns))
        row_index = int(math.floor(row_frac * self.rows))
        return (row_index , column_index)
    
    def _return_frac_x_y(self, x:int, y:int):
        column_frac = x / self.canvas.winfo_width()
        row_frac = y / self.canvas.winfo_height()
        return (column_frac, row_frac)
    
    def _return_pixels_x_y(self, fracs: (float,float)):
        x_frac, y_frac = fracs
        x = x_frac * self.canvas.winfo_width()
        y = y_frac * self.canvas.winfo_height()
        return (x, y)

    def _check_score(self):
        self.game.check_score()
        black_score, white_score = self.game.score
        self.black_score.set('Black: ' + str(black_score))
        self.white_score.set('White: ' + str(white_score))

    def _return_player_game_format(self):
        if self.starting_player == 'black':
            return 'B'
        elif self.starting_player == 'white':
            return 'W'

    def _winning_player(self):
        return self.game.check_who_won()
        
if __name__ == '__main__':
    gui = OthelloGUI()
    gui.start()


    
