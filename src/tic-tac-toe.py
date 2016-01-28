matrix_size = 3
center = matrix_size/2
# Winning possibilities for computer and user at each tile respectively
possibilities = [[[3,3], [2,2], [3,3]],
                 [[2,2], [4,4], [2,2]],
                 [[3,3], [2,2], [3,3]]]

# After each move reduce the possibilities for the next player based on the tile position
def update_possibilities(pos, player):
    row = (pos-1)/matrix_size
    col = (pos-1)%matrix_size
    if player == computer:
        k = 1
    else:
        k = 0
    # For center tile reduce possibilities for all other tiles by one
    if row == center and col == center: 
        for i in range(matrix_size):
            for j in range(matrix_size):
                if possibilities[i][j][k] != -1:
                    possibilities[i][j][k] -= 1
        return
    # For diagonal tile reduce possibilities for row, column and diagonal in which the tile is present
    if pos%2 == 1:
        for i in range(matrix_size):
            if possibilities[row][i][k] != -1:
                possibilities[row][i][k] -= 1
            if possibilities[i][col][k] != -1:
                possibilities[i][col][k] -= 1
        if row == col:
            for i in range(matrix_size):
                if possibilities[i][i][k] != -1:
                    possibilities[i][i][k] -= 1
        else:
            for i in range(matrix_size):
                if possibilities[i][(matrix_size-1)-i][k] != -1:
                    possibilities[i][(matrix_size-1)-i][k] -= 1
        return
    # For edge tile reduce possibilities for row and column in which the tile is present
    else:
        for i in range(matrix_size):
            if possibilities[row][i][k] != -1:
                possibilities[row][i][k] -= 1
            if possibilities[i][col][k] != -1:
                possibilities[i][col][k] -= 1
        return
            
# Switch the turn to next player               
def swap_turn():
    global turn
    if turn == computer:
        turn = user
    else:
        turn = computer

# Display board to the user
def print_board():
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""

# Check if game is finished
def check_done():
    # Check for three in a row or three in a column cases
    for i in range(0,3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            #print turn, "won!!!"
            return 1

    # Check for three in a diagonal cases    
    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
        #print turn, "won!!!"
        return 1

    # Check if game is a draw
    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        #print "Draw"
        return 0

    return -1

# Mark the tile and reset possibilities
def mark_tile(pos, player):
    X = (pos - 1)/3
    Y = (pos - 1)%3
    
    if map[X][Y] == " ":
        map[X][Y] = player
        possibilities[X][Y][0] = -1
        possibilities[X][Y][1] = -1
        return True
    return False

# Reset tile and reload possibilities
def reset_tile(pos, comp_poss, opp_poss):
    X = (pos - 1)/3
    Y = (pos - 1)%3
    map[X][Y] = " "
    possibilities[X][Y][0] = comp_poss
    possibilities[X][Y][1] = opp_poss

# Try to finish the game by winning
def try_finish(player):
    # mark each empty tile and check if that will result in win, if doesn't reset the tile and continue
    for i in range (0, matrix_size*matrix_size):
        X = (i)/3
        Y = (i)%3
        if map[X][Y] == " ":
            comp_poss = possibilities[X][Y][0]
            opp_poss = possibilities[X][Y][1]
            mark_tile(i+1, player)
            if check_done() != -1:
                return i+1
            else:
                reset_tile(i+1, comp_poss, opp_poss)
                
    return -1

# Try to block the opponent if he is about to win
def block_opponent():
    # mark each empty tile (as opponent) and check if that will result in win, if he does block that tile    
    for i in range (0, matrix_size*matrix_size):
        X = (i)/3
        Y = (i)%3
        if map[X][Y] == " ":
            comp_poss = possibilities[X][Y][0]
            opp_poss = possibilities[X][Y][1]
            mark_tile(i+1, computer)
            pos = try_finish(user)
            if pos != -1:
                reset_tile(i+1, comp_poss, opp_poss)
                return pos
    return -1    

# Rules to play computer's turn
def play_turn():        
    # Try to win the game
    pos = try_finish(computer)
    if pos != -1:
        return pos
    # Block the opponent if he is about to win
    pos = try_finish(user)
    if pos != -1:
        reset_tile(pos, -1, -1)
        mark_tile(pos, computer)
        return pos
    # Capture best tile possible
    # Center tile
    if map[center][center] == " ":
        pos = (center*matrix_size) + center + 1
        mark_tile(pos, computer)
        return pos
    # Capture tile with best possibilities
    max_poss = -1
    pos = -1
    # Find the best posibility for computer
    k = 0
    for i in range(matrix_size):
        for j in range(matrix_size):
            if possibilities[i][j][k] > max_poss:
                max_poss = possibilities[i][j][k]
                pos = (i * matrix_size) + j + 1
    # If opponent has equal or better possibility than computer block that tile
    k = 1
    for i in range(matrix_size):
        for j in range(matrix_size):
            if possibilities[i][j][k] >= max_poss:
                max_poss = possibilities[i][j][k]
                pos = (i * matrix_size) + j + 1
    
    if pos != -1:
        mark_tile(pos, computer)
        return pos
            
turn = "X"
map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]
done = -1

print "Select X or O to start:"
user = raw_input()
while user not in ['X','O','x','o']:
    print "Select X or O to start:"
    user = raw_input()
if user in ['X','x']:
    computer = 'O'
    user = 'X'
else:
    computer = 'X'
    user = 'O'

# Iterate till the game is done
while done == -1:
    if turn == computer:
        pos = play_turn()
        update_possibilities(pos, computer)

    else:
        print_board()        
        print "your turn"
        print
        moved = False

        while moved != True:
            print "Please select position by typing in a number between 1 and 9, see below for which number that is which position..."
            print "7|8|9"
            print "4|5|6"
            print "1|2|3"
            print

            try:
                pos = input("Select: ")
                if pos <=9 and pos >=1:
                    moved = mark_tile(pos, user)
                    update_possibilities(pos, user)
            except:
                print "You need to add a numeric value that has empty tile"
        
    done = check_done()
    if done == -1:
        swap_turn()
    else:
        if done == 0:
            print "Draw"
        else:
            print turn, "Wins!!"
        print_board()
