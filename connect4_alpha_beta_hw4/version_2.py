import copy
 
class ConnectFour:
    def __init__(self):
        self.moves = 0
        self.turn = 0
 
    def PrintGameBoard(self, board):
        print('  0   1   2   3   4   5   6')
        for i in range(5, -1, -1):
            print('|---|---|---|---|---|---|---|')
            print("| ",end="")
            for j in range(7):
                print(board[i][j],end="")
                if j != 6:
                    print(" | ",end="")
                else:
                    print(" |")
        print('`---------------------------´')
 
    def CanPlay(self, col, board):
        stacks = [[x[i] for x in board] for i in range(len(board[0]))]
        if (stacks[col].count(1) + stacks[col].count(2)) < 6:
            return (stacks[col].count(1) + stacks[col].count(2))
        else:
            return -1
 
    def MakeMove(self, board, col, player, row):
        board[row][col] = player
        self.moves += 1
        return board
       
    def UnmakeMove(self, board, col, row):
        board[row][col] = " "
        self.moves -= 1
        return board
 
    def IsWinning(self, currentplayer, board):
        for i in range(6):
            for j in range(4):
                #find colume 4
                if board[i][j] == currentplayer and board[i][j+1] == currentplayer and board[i][j+2] == currentplayer and board[i][j+3] == currentplayer:
                    return True
        for i in range(3):
            for j in range(7):
                #find row 4
                if board[i][j] == currentplayer and board[i+1][j] == currentplayer and board[i+2][j] == currentplayer and board[i+3][j] == currentplayer:
                    return True    
        for i in range(3):
            for j in range(4):
                #find lower diagonal 4
                if board[i][j] == currentplayer and board[i+1][j+1] == currentplayer and board[i+2][j+2] == currentplayer and board[i+3][j+3] == currentplayer:
                    return True
        for i in range(3,6):
            for j in range(4):
                #find upper diagonal 4
                if board[i][j] == currentplayer and board[i-1][j+1] == currentplayer and board[i-2][j+2] == currentplayer and board[i-3][j+3] == currentplayer:
                    return True
        return False
                       
    def PlayerMove(self, board, player):
        try:
            allowedmove = False
            while not allowedmove:
                print("Choose a column where you want to make your move (0-6): ",end="")
                col =input()
                row = self.CanPlay(int(col), board)
                if row != -1:
                    board[row][int(col)] = player
                    self.moves += 1
                    allowedmove = True
                else:
                    print("This column is full")
        except (NameError, ValueError, IndexError, TypeError, SyntaxError) as e:
            print("Give a number as an integer between 0-6!")
        else:
            return board
           
    def SwitchPlayer(self, player):
        if player==1:
            nextplayer=2
        else:
            nextplayer=1
        return nextplayer
       
    def evaluation(self, board, player):
        list = []
        opponent = self.SwitchPlayer(player)
        #if we are reaching the leaf what score is winning 512, lose -512
        if self.IsWinning(player, board):
            score = 512
        elif self.IsWinning(opponent, board):
            score = -512
        #if running out of move, the score is 0
        elif self.moves==42:
            score=0
        else:
            score = 0
            #find how many 4 together for player and opponent
            for i in range(6):
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i][j+1]),str(board[i][j+2]),str(board[i][j+3])])
            for i in range(3):
                for j in range(7):
                    list.append([str(board[i][j]),str(board[i+1][j]),str(board[i+2][j]),str(board[i+3][j])])
            for i in range(3):
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i+1][j+2]),str(board[i+2][j+2]),str(board[i+3][j+3])])
            for i in range(3, 6):
                for j in range(4):
                    list.append([str(board[i][j]),str(board[i-1][j+2]),str(board[i-2][j+2]),str(board[i-3][j+3])])
            for k in range(len(list)):
                if ((list[k].count(str(player))>0) and (list[k].count(str(opponent))>0)) or list[k].count(" ")==4:
                    score += 0
                if list[k].count(player)==1:
                    score += 1
                if list[k].count(player)==2:
                    score += 10
                if list[k].count(player)==3:
                    score += 50
                if list[k].count(opponent)==1:
                    score -= 1
                if list[k].count(opponent)==2:
                    score -= 10
                if list[k].count(opponent)==3:
                    score -= 50
            #also check who is next player
            if self.turn==player:
                score += 16
            else:
                score -= 16
        return score
       
    def alphabeta(self, board, depth, player, alpha, beta):
        if depth==0 or self.moves==42 or self.IsWinning(1, board) or self.IsWinning(2, board):
            return(self.evaluation(board, player),0)
        pos = 0
        order = [3,2,4,1,5,0,6]
        if player==self.turn:
            for i in order:
                row = self.CanPlay(i, board)
                if row != -1:
                    newboard = self.MakeMove(board, i, player, row)
                    value, dummy = self.alphabeta(newboard, depth-1, self.SwitchPlayer(player), alpha, beta)
                    newboard = self.UnmakeMove(board, i, row)
                    if value>alpha:
                        alpha=value
                        pos=i
                    if beta<=alpha:
                        break
            return alpha, pos
        else:
            for i in order:
                row = self.CanPlay(i, board)
                if row != -1:
                    newboard = self.MakeMove(board, i, player, row)
                    value, dummy = self.alphabeta(newboard, depth-1, self.SwitchPlayer(player), alpha, beta)
                    newboard = self.UnmakeMove(board, i, row)
                    if value<beta:
                        beta = value
                        pos=i
                    if beta<=alpha:
                        break
            return beta, pos
               
    def alphabetapruning(self, board, depth, player):
        self.turn=player
        value, position=self.alphabeta(board, depth, player, -1000000000, 1000000000)
        board = self.MakeMove(board, position, player, self.CanPlay(position, board))
        return board
 
def PlayerMark():
    print("Player 1 starts the game")
    mark = ''
    while not (mark == "1" or mark == "2"):
        print('Do you want to be 1 or 2: ',end="")
        mark = input()
    if mark == "1":
        return 1
    else:
        return 2
 
def PlayAgain():
    print('Do you want to play again? (yes or no) :',end="")
    return input().lower().startswith('y')
   
def main():
    print("Connect4")
    while True:
        mark = PlayerMark()
        connectfour = ConnectFour()
        if mark==1:
            player = 1
            print("You are going to start the game\r\n\r\n")
        else:
            player = 2
            print("Computer (negamax) starts the game")
        gameisgoing = True
        table  = [[],[],[],[],[],[]]
        for i in range(7):
            for j in range(6):
                table[j].append(" ")
        while gameisgoing:
            connectfour.PrintGameBoard(table)
            if mark == 1:
                table = connectfour.PlayerMove(table, player)
                if connectfour.IsWinning(player, table):
                    connectfour.PrintGameBoard(table)
                    print('You won the game!')
                    gameisgoing = False
                else:
                    if connectfour.moves==42:
                        connectfour.PrintGameBoard(table)
                        print('Game is tie')
                        break
                    else:
                        mark = 2
            else:
                opponent = connectfour.SwitchPlayer(player)
                table = connectfour.alphabetapruning(table, 8, opponent)
                if connectfour.IsWinning(opponent, table):
                    connectfour.PrintGameBoard(table)
                    print('Computer won the game')
                    gameisgoing = False
                else:
                    if connectfour.moves==42:
                        connectfour.PrintGameBoard(table)
                        print('Game is tie')
                        break
                    else:
                        mark = 1
        if not PlayAgain():
            print("Game ended")
            break
 
if __name__ == '__main__':
    main()