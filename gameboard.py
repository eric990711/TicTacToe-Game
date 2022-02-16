# Student name = Younghwan Youn

class Boardclass:
    current_board = []
    user1 = ''
    user2 = ''
    last_username = ''
    total_game_played = 0
    total_win = 0
    total_tie = 0
    total_lose = 0
    
    def __init__(self):
        self.current_board = []
        self.user1 = ''
        self.user2 = ''
        self.last_username = ''
        self.total_game_played = 0
        self.total_win = 0
        self.total_tie = 0
        self.total_lose = 0    

    def recordGamePlayed(self):
        self.total_game_played += 1

    def resetGameBoard(self):
        self.current_board = []
        self.last_username = ''

    def playMoveOnBoard(self,name,move):
        self.current_board.append({'Player':name, 'Position':move})
        self.last_username = name
        

    def isBoardFull(self): 
        if len(self.current_board) == 9:
            return True
        else:
            return False

    def isGameFinished(self):     
        user1_list = []
        user2_list = []
        success_list = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9],[1,5,9], [3,5,7]]
        
        for ele in self.current_board:
            if ele['Player'] == self.user1:
                user1_list.append(int(ele['Position']))
            elif ele['Player'] == self.user2:
                user2_list.append(int(ele['Position']))

        user1_list.sort()
        user2_list.sort()

        for lists in success_list:
            count = 0
            for num in lists:
                if num in user1_list:
                    count += 1
                else:
                    pass
            if count == 3:
                self.total_win += 1
                print("You won the game!")
                return 'Win'
            else:
                pass
            
            count = 0
            for num in lists:
                if num in user2_list:
                    count += 1
                else:
                    pass
            if count == 3:
                self.total_lose += 1
                print("You lost the game..")
                return "Lose"
            else:
                pass

        if self.isBoardFull() == True:
            self.total_tie += 1
            print("The Game is tied")
            return "Tie"

        return None

            
            

    def computeStats(self):
        return [self.user1, self.user2, self.last_username, self.total_game_played, self.total_win, self.total_lose, self.total_tie]
    
