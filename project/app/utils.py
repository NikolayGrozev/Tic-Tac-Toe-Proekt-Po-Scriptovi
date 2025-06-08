winning_combinations = [
    [1, 2, 3], [4, 5, 6], [7, 8, 9],
    [1, 4, 7], [2, 5, 8], [3, 6, 9],
    [1, 5, 9], [3, 5, 7]
]

def calculate_winner(moves):
    moves_x = []
    moves_o = []

    for move in moves:
        if move['symbol'] == 'X':
            moves_x.append(move['position'])
        elif move['symbol'] == 'O':
            moves_o.append(move['position'])
        else:
            return None

    for combination in winning_combinations:
        won = True
        for position in combination:
            if position not in moves_x:
                won = False
                break
        if won:
            return 'X'
        
    for combination in winning_combinations:
        won = True
        for position in combination:
            if position not in moves_o:
                won = False
                break
        if won:
            return 'O'
    
    return None

                
            

    
