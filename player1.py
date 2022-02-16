#Student name = Younghwan Youn

import socket
import tkinter as tk
from tkinter import messagebox
import gameboard

class Playerone:
    #set board object
    board = None
    connected = False
    
    #tkinter class variable
    HOST = ''
    PORT = 0
    clientsocket = None
    serversocket = None
    clientaddr = ''
    turns = ''
    
    #tkinter object
    window = 0
    
    def __init__(self):
        #import boardclass class
        self.board = gameboard.Boardclass()
        self.board.user1 = 'player1'
        self.board.last_username = self.board.user1

        #call my canvas setup
        self.canvassetup()
        self.initTkvar()
        self.hostinfo()
        self.portinfo()
        self.connectSubmitButton()
        self.gridgameboard()
        self.quitbutton()
        self.refresh()
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
        self.window.title("Tic Tac Toe Server")
        self.window.configure(background='#34A2FE')
        self.window.resizable(1,1)

    def quitbutton(self):
        self.quitButton = tk.Button(master = self.window, text="Quit",command = self.window.destroy).grid(row= 60, column=1, padx=5, pady=5)

    def hostinfo(self):
        self.host_text = tk.Label(text = "Enter the host information: ").grid(row= 20, column=1, padx=5, pady=2)
        self.host_entry = tk.Entry(textvariable = self.HOST).grid(row= 21, column=1, padx=5, pady=5)

    def portinfo(self):
        self.port_text = tk.Label(text = "Enter the port information: ").grid(row= 22, column=1, padx=5, pady=2)
        self.port_entry = tk.Entry(textvariable = self.PORT).grid(row= 23, column=1, padx=5, pady=5)

    def connectSubmitButton(self):
        self.serversubmit = tk.Button(text = "Submit", command = self.connectServer).grid(row= 24, column=1, padx=5, pady=5)

    def usernamesubmission(self):
        user1byte = str.encode(self.board.user1)
        self.clientsocket.send(user1byte)


    def connectServer(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.settimeout(0.5)
        self.serversocket.bind((self.HOST.get(), self.PORT.get()))
        self.serversocket.listen()

                
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
                

            


    #function to enter a move
    def entermove(self, move):
        if self.board.last_username != self.board.user1:
            if self.boardsquare[move]['text'] == '':
                self.boardsquare[move]['text'] = 'O'
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
        
        if move == 'Fun Times':
            self.board.recordGamePlayed()
            self.result()
            self.fungame = tk.messagebox.showinfo('From Player2','Fun Times')
            return
        elif move == 'Play Again':
            self.playagain = tk.messagebox.showinfo('From Player2','Play Again')
            self.board.recordGamePlayed()
            self.turns.set(self.board.user2)
            self.resetgame()
            return
        elif move.isnumeric() != True:
            self.board.user2 = move
            self.connectedddd = tk.Label(text = self.board.user2 + " connected",fg="blue").grid(row= 25, column=1, padx=5, pady=15)
            self.turns.set(self.board.user2)
            self.itis = tk.Label(text = "Whose's turn is it: ",fg="black",background='#0f91fc').grid(row= 26, column=1, padx=5, pady=5)
            self.whoseturn = tk.Label(textvariable = self.turns,fg="blue", background='#34A2FE').grid(row= 27, column=1, padx=5, pady=5)
        

            self.startgame()
        
            #send data to client           
            self.usernamesubmission()
            return
        
        move = int(move)
        
        if move != 0:
            if self.boardsquare[move]['text'] == '':
                self.boardsquare[move]['text'] = 'X'
                self.board.playMoveOnBoard(self.board.user2, move)
                self.changeturn()
                self.wincheck()
            
    def changeturn(self):
        if self.board.last_username != self.board.user1:
            self.turns.set(self.board.user1)
        elif self.board.last_username == self.board.user1:
            self.turns.set(self.board.user2)


    def wincheck(self):
        state = self.board.isGameFinished()
        if state == 'Win':
            tk.messagebox.showinfo("Player1's Game Result", "You have won the game!")
        elif state == 'Lose':
            tk.messagebox.showinfo("Player1's Game Result", "You have lost the game..")
        elif state == 'Tie':
            tk.messagebox.showinfo("Player1's Game Result", "The game has been tied.")

    def resetgame(self):
        self.board.resetGameBoard()

        for i in range(1,10):
            self.boardsquare[i]['text'] = ''

        self.board.last_username = self.board.user1




    def startgame(self):
        pass

    
    def refresh(self):
        self.window.update()

        self.window.after(500,self.refresh)

        if self.clientsocket != None and self.connected == True:
            self.movementrec()

        if self.serversocket != None and self.connected != True:
            self.waitingaccept()


    def waitingaccept(self):
        try:
            self.clientsocket, self.clientaddr = self.serversocket.accept()  
            self.clientsocket.setblocking(False)
            self.connected = True
        except socket.timeout:
            return None
        
    
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
    player1UI = Playerone()


