#Student name = Younghwan Youn

import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import gameboard


class Playertwo:
    connected = False
    #set board object
    board = None
    
    #tkinter class variable
    HOST = ''
    PORT = 0
    clientsocket = None
    clientaddr = ''
    
    #tkinter object
    window = 0
    
    def __init__(self):
        #import boardclass class
        self.board = gameboard.Boardclass()
        self.board.last_username = ''

        #call my canvas setup
        self.canvassetup()
        self.initTkvar()
        self.hostinfo()
        self.portinfo()
        self.connectSubmitButton()
        self.gridgameboard()
        self.quitbutton()
        self.runUI()

    #method that initialize the tk variables
    def initTkvar(self):
        #initialize class variable
        self.HOST = tk.StringVar()
        self.PORT = tk.IntVar()
        self.turns = tk.StringVar()


    def canvassetup(self):
        #canvas setup
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe Game Client")
        self.window.configure(background='#34A2FE')
        self.window.resizable(1,1)

    def quitbutton(self):
        self.quitButton = tk.Button(master = self.window, text="Quit",command = self.window.destroy).grid(row= 60, column=1, padx=5, pady=5)

    def hostinfo(self):
        self.host_text = tk.Label(text = "Enter the player1's host information: ").grid(row= 21, column=1, padx=5, pady=2)
        self.host_entry = tk.Entry(textvariable = self.HOST).grid(row= 22, column=1, padx=5, pady=5)

    def portinfo(self):
        self.port_text = tk.Label(text = "Enter the player1's port information: ").grid(row= 23, column=1, padx=5, pady=2)
        self.port_entry = tk.Entry(textvariable = self.PORT).grid(row= 24, column=1, padx=5, pady=5)

    def connectSubmitButton(self):
        self.serversubmit = tk.Button(text = "Submit", command = self.connectServer).grid(row= 25, column=1, padx=5, pady=5)


    def usernamesubmission(self):
        user1byte = str.encode(self.board.user1)
        self.clientsocket.send(user1byte)

    def askuserconnectagain(self):
        self.askagianbox = tk.messagebox.askquestion ('Re-connect',"Didn't work. Do you want to try to connect again?")
        if self.askagianbox == 'no':
           self.window.destroy()
        else:
            pass

    def connectServer(self):
        self.clientsocket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientsocket.connect((self.HOST.get(), self.PORT.get()))
            self.connected = True
        except:
            self.askuserconnectagain()
            return

        self.board.user1 = simpledialog.askstring(title = "Player2's username", prompt = "Enter Player2's Username:")
        self.usernamesubmission()

        try:
            user2 = self.clientsocket.recv(1024)
        except:

            return None

        self.board.user2 = user2.decode('ascii')
        self.connectedddd = tk.Label(text = "Connected to " + self.board.user2,fg="blue").grid(row= 26, column=1, padx=5, pady=15)
        self.turns.set(self.board.user1)
        self.itis = tk.Label(text = "Whose's turn is it: ",fg="black",background='#0f91fc').grid(row= 27, column=1, padx=5, pady=5)
        self.whoseturn = tk.Label(textvariable = self.turns,fg="blue", background='#34A2FE').grid(row= 28, column=1, padx=5, pady=5)
        self.board.last_username = self.board.user2
        self.clientsocket.setblocking(False)
        self.refresh()
        self.startgame()

                
    def gridgameboard(self):
        #Code to make a gameboard with grid function
        self.boardsquare = {}
        for i in range(3):
            for j in range(3):
                self.frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                self.frame.grid(row= i + 50, column=j, padx=5, pady=5)
                
                self.boardsquare[i*3 + j + 1] = tk.Button(master=self.frame, text="",width=4, height=2, command = lambda row = i, col = j: self.entermove(row*3 + col + 1))
                self.boardsquare[i*3 + j + 1].pack(padx=5, pady=5)

    def changeturn(self):
        if self.board.last_username != self.board.user1:
            self.turns.set(self.board.user1)
        elif self.board.last_username == self.board.user1:
            self.turns.set(self.board.user2)


    #function to enter a move
    def entermove(self, move):
        if self.board.last_username != self.board.user1:
            if self.boardsquare[move]['text'] == '':
                self.boardsquare[move]['text'] = 'X'
                self.board.playMoveOnBoard(self.board.user1, move)
                self.changeturn()
                self.movementsend(move)
                self.wincheck()
    
    def movementsend(self, move):
        movebyte = str.encode(str(move))
        if self.clientsocket != None and self.connected == True:
            self.clientsocket.send(movebyte)
        

    def movementrec(self):
        try:
            oppomove = self.clientsocket.recv(1024)
        except:

            return None
        
        move = oppomove.decode('ascii')
        move = int(move)
        
        if move != 0:
            if self.boardsquare[move]['text'] == '':
                self.boardsquare[move]['text'] = 'O'
                self.board.playMoveOnBoard(self.board.user2, move)
                self.changeturn()
                self.wincheck()
        
    
    def wincheck(self):
        state = self.board.isGameFinished()
        if state == 'Win':
            tk.messagebox.showinfo("Player2's Game Result", "You have won the game!")
            self.board.recordGamePlayed()
            self.askretry()
            
        elif state == 'Lose':
            tk.messagebox.showinfo("Player2's Game Result", "You have lost the game..")
            self.board.recordGamePlayed()
            self.askretry()

        elif state == 'Tie':
            tk.messagebox.showinfo("Player2's Game Result", "The game has been tied.")
            self.board.recordGamePlayed()
            self.askretry()

    def resetgame(self):
        self.board.resetGameBoard()

        for i in range(1,10):
            self.boardsquare[i]['text'] = ''


    def aftergameagain(self):
        self.clientsocket.send(b'Play Again')


    def aftergamedone(self):
        self.clientsocket.send(b'Fun Times')


    def askretry(self):
        whetretry = tk.messagebox.askyesno("Retry", "Do you want to play one more time?")
        if whetretry == True:
            self.turns.set(self.board.user1)
            self.aftergameagain()
            self.resetgame()
        else:
            self.aftergamedone()
            self.result()
    
    
    def startgame(self):
        pass

    
    def refresh(self):
        self.window.update()

        self.window.after(500,self.refresh)

        if self.clientsocket != None and self.connected == True:
            self.movementrec()
    
    
    def runUI(self):
        self.window.mainloop()

    def result(self):
        [user1, user2, last_username, total_game_played, total_win, total_lose, total_tie] = self.board.computeStats()
        self.connectedddd = tk.Label(text = "---------------------------------------",fg="blue",background='#34A2FE').grid(row= 1, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Final Statistics",fg="blue", background='#34A2FE').grid(row= 2, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "---------------------------------------",fg="blue", background='#34A2FE').grid(row= 3, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Player1's name" +' : '+ user1,fg="blue", background='#34A2FE').grid(row= 4, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Player2's name" +' : '+ user2,fg="blue", background='#34A2FE').grid(row= 5, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Last person that made a move" +' : '+ last_username,fg="blue", background='#34A2FE').grid(row= 6, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Total Games Played" +' : '+ str(total_game_played),fg="blue", background='#34A2FE').grid(row= 7, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Total Win" +' : '+ str(total_win),fg="blue", background='#34A2FE').grid(row= 8, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Total Lose" +' : '+ str(total_lose),fg="blue", background='#34A2FE').grid(row= 9, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "Total Tie" +' : '+ str(total_tie),fg="blue", background='#34A2FE').grid(row= 10, column=1, padx=5, pady=2)
        self.connectedddd = tk.Label(text = "---------------------------------------",fg="blue", background='#34A2FE').grid(row= 11, column=1, padx=5, pady=2)
    
        
    

if __name__ == "__main__":
    player2UI = Playertwo()


