# Austin Nowlen 50132880

import othello_protocol

class InputError(Exception):
    pass

class NoMovesError(Exception):
    pass

def _ask_count(r_or_c:str) -> str:
    '''prompts the user for a even number between 4 and 16 that can be used for row or column count and returns that number'''
    while True:
        try:
            count = int(input('How many '+ r_or_c +' would you like? '))
            if count % 2 == 0 and count >= 4 and count <= 16:
                return count
            else:
                raise InputError
        except:
            print('Error. Please input an even number between 4-16.')


def _ask_starting_player()-> str:
    '''prompts the user for which player should start the game and returns that player'''
    while True:
        try:
            starter = input('Which player do you want to start? ').lower()
            if starter == 'black':
                return 'B'
            elif starter == 'white':
                return 'W'
            else:
                raise InputError
        except:
            print('Error. Please input either black or white.')

def _ask_starting_layout()->str:
    '''prompts the user for which player should be in the top left of the starting center pieces and returns that player'''
    while True:
        try:
            top_left_piece = input('Which piece do you want in the top left starting corner? ').lower()
            if top_left_piece == 'black' or top_left_piece == 'white':
                return top_left_piece
            else:
                raise InputError
        except:
            print('Error. Please input either black or white.')

def _ask_how_to_win()->str:
    '''prompts the user for which way they want the game to be decided and returns the appropriate way'''
    while True:
        try:
            win = input('Which way do you prefer the game to be won? \n\t Most = The player with the most amount of discs at the end wins. \n\t Least = Player with the least amount of discs at the end wins. \n').lower()
            if win == 'most' or win == 'least':
                return win
            else:
                raise InputError
        except:
            print('Error. Please input either Most or Least.')

def _ask_move()-> tuple:
    '''prompts the user for the row and column in which they would like to place a piece and returns the two numbers has a tuple of (row,column)'''
    row = int(input('Which row would you like to place a piece? '))
    column = int(input('Which column would you like to place a piece? ')) 
    return (row, column)

def _make_move(game: 'GameState')->None:
    '''calls the add_move function of the current GameState to add the piece to the gameboard'''
    while True:
        try:
            game.add_move(_ask_move())
            break
        except:
            print('Error. Please pick a row and column that is valid according to Othello rules.')



if __name__ == '__main__':
    game = othello_protocol.GameState(_ask_count('rows'),_ask_count('columns'),_ask_starting_layout(), _ask_starting_player(), _ask_how_to_win())
    while True:
        try:
            game_over = game.is_game_over()
            if game_over == True:
                break
            print()
            game.check_score()
            print('It is ' + game.whose_turn_it_is() + "'s turn.")
            print('Black: ' + str(game.score[0]) + '\tWhite: ' + str(game.score[1]))
            game.print_gameboard()
            if game.any_moves_left_for_player(game.turn) == False:
                print(game.whose_turn_it_is() + ' has no moves and is being skipped.')
                game.change_turn()
                raise NoMovesError()
            _make_move(game)
            game.change_turn()
        except:
            pass

    print('\n')
    print('GAME OVER')
    game.print_gameboard()
    if game.check_who_won() == 'Black' or game.check_who_won() == 'White':
        print(game.check_who_won() + ' Won!!!')
    else:
        print('Tie!!!')
    game.check_score()
    print('Black: ' + str(game.score[0]) + '\tWhite: ' + str(game.score[1]))

    
        


