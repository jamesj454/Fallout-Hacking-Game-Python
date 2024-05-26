import random
import os      # For clearing console
import time

class IdleGame:
    
    def __init__(self):
        self.attemptsRemaining = 4  # Number of attempts before 10 sec lockout
        self.numOfColumns = 20      # X size of grid
        self.numOfRows = 17         # Y size of grid
        self.gameDifficulty = 5     # Num of letters in word
        self.lineScrollSpeed = 0.03 # How fast text should 'load' onto the terminal
        
        self.staticWords = ["%","!","=","(",")","*","<",">",":",";","'","@","[","]","&"]
        self.chosenWord = ""
        self.outputString = ""
        self.gameOver = False
        self.wordsList = []
    
    # Gets the file that words are stored in based on difficulty.    
    def GetWords(self):
        self.wordsList = []
        with open(self.GetWordFileName()) as f:
            for line in f:
                self.wordsList.append(line.strip())
                
    def GetWordFileName(self):
        return 'word' + str(self.gameDifficulty) + '.txt'
    
    # Prints out the formatted attempts remaining
    def DrawAttemptsRemaining(self):
        attemptBlock = '█ '
        attemptX = 0
        attemptString = str(self.attemptsRemaining) + " ATTEMPT(S) REMAINING: "
        while attemptX < self.attemptsRemaining:
            attemptString += attemptBlock
            attemptX += 1
            if self.attemptsRemaining == 1:
                self.PrintLine("!!! WARNING: LOCKOUT IMMINENT !!!\n")
        self.PrintLine(attemptString + '\n')
    
    # Prints each line in string with a delay on each line to simulate loading
    def PrintLine(self, string): 
        output_lines = string.split('\n')
        for line in output_lines:
                time.sleep(self.lineScrollSpeed)
                print(line)
    
    # Called at start of game to put words in the correct places
    def GenerateScreen(self):
        self.PrintLine ("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL")
        self.DrawAttemptsRemaining()
        
        self.GetWords()
        self.chosenWord = random.choice(self.wordsList)
        insertChosenWordAtY = random.randint(0, self.numOfRows - 1)
        for row in range(self.numOfRows):
            insertWordAtX = random.randint(0, self.numOfColumns - 1)
            line = ""
            for col in range(self.numOfColumns):
                if row == insertChosenWordAtY and col == insertWordAtX:
                    line += self.chosenWord
                    col += len(self.chosenWord) - 1 
                elif col == insertWordAtX:
                    line += random.choice(self.wordsList)
                    col += len(self.chosenWord)
                else:
                    line += random.choice(self.staticWords)
            
            self.outputString += hex(id(row)) + ' ' + line + "\n"
            self.PrintLine(hex(id(row)) + ' ' + line)
        print('\n')
        
    def RedrawScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL")
        self.DrawAttemptsRemaining()
        output_lines = self.outputString.split('\n')
        for line in output_lines:
            if line != "":
                self.PrintLine(line)
        print(' ')
        
    def SelectDifficulty(self):
        print ("1) Easy 2) Intermediate 3) Hard")
        userIn = input ("Enter Difficulty: ")
        if userIn == '1':
            self.gameDifficulty = 3
        elif userIn == '2':
            self.gameDifficulty = 4
        elif userIn == '3':
            self.gameDifficulty = 5
        else:
            self.PrintLine ('[ERROR] Please input a valid difficulty.\n')
            self.SelectDifficulty()
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def AskLogout(self):
        inp = input ("Play again? (Y/N): ")
        if inp.upper() == "Y":
            self.PlayGame()
        elif inp.upper() == "N":
            exit(1)
        else:
            self.PrintLine("Please enter Y or N.")
            self.AskLogout()
        
    def PlayGame(self):
        self.__init__()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.SelectDifficulty()
        self.GenerateScreen()
        self.gameOver = False
        while self.gameOver == False:
            userIn = input("ENTER PASSWORD: ").upper()
            if  len(userIn) != len(self.chosenWord):
                self.RedrawScreen()
                self.PrintLine("[SYSERROR] Please enter a valid input.")
            elif userIn == self.chosenWord:
                self.PrintLine ("Success! Logging in...\n")
                self.AskLogout()
            else:
                self.attemptsRemaining -= 1
                if self.attemptsRemaining == 0:
                    self.gameOver = True
                    self.DoLockout()
                else:
                    correctCount = 0
                    x = 0
                    while x < len(userIn):
                        x+=1
                        if userIn[x-1] == self.chosenWord[x-1]:
                            correctCount+=1
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.ReplaceInputtedWordWithStatic(userIn)
                    self.RedrawScreen()
                    self.PrintLine (userIn+": Incorrect credentials. " + str(correctCount) + "/" + str(len(self.chosenWord)) + " characters correct.")
    
    # Sleeps terminal for 10 seconds after game is lost, then restarts the game    
    def DoLockout(self):
        self.gameOver = True
        os.system('cls' if os.name == 'nt' else 'clear')
        self.PrintLine("SECURITY PROTOCOL ENGAGED. THIS TERMINAL WILL RESTART IN 10 SECONDS...")
        self.PlayGame()
    
    # Removes userIn from the screen if found. Need to redraw screen after!            
    def ReplaceInputtedWordWithStatic(self, userIn):
        try:
            output_list = list(self.outputString)
            start_index = self.outputString.index(userIn)
            end_index = start_index + len(self.chosenWord)
        
            for i in range(start_index, end_index):
                output_list[i] = random.choice(self.staticWords)
        
            self.outputString = ''.join(output_list)
    
        except ValueError:
            print(f"{userIn} not found in outputString.")
            
    def BootUpSequence(self):
        bootupStr =  "ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM\n"
        bootupStr += "COPYRIGHT 2075-2077 ROBCO INDUSTRIES\n"
        #for line
        
game = IdleGame()
game.PlayGame()
            
            
    