import random
import os      # For clearing console
import time

class IdleGame:
    
    def __init__(self):
        self.attemptsRemaining = 4 # Number of attempts before 10 sec lockout
        self.numOfColumns = 20 # X size of grid
        self.numOfRows = 14 # Y size of grid
        self.gameDifficulty = 5 # Num of letters in word
        self.lineScrollSpeed = 0.03 # How fast text should 'load' onto the terminal
        
        self.staticWords = ["%","!","=","(",")","*","<",">",":",";","'","@","[","]","&"]
        self.chosenWord = ""
        self.outputString = ""
        self.gameOver = False
        self.wordsList = []
        
    def GetWords(self):
        self.wordsList = []
        with open(self.GetWordFileName()) as f:
            for line in f:
                self.wordsList.append(line.strip())
                
    def GetWordFileName(self):
        return 'word' + str(self.gameDifficulty) + '.txt'
    
    def DrawAttemptsRemaining(self):
        attemptBlock = '█ '
        attemptX = 0
        attemptString = "ATTEMPTS REMAINING: "
        while attemptX < self.attemptsRemaining:
            attemptString += attemptBlock
            attemptX += 1
            if self.attemptsRemaining == 1:
                attemptString += "| WARNING: SECURITY LOCKOUT IMMINENT!"
        print(attemptString + '\n')
            
    def GenerateScreen(self):
        self.GetWords()
        self.chosenWord = random.choice(self.wordsList)
        insertChosenWordAtY = random.randint(0, self.numOfRows - 1)
            
        self.DrawAttemptsRemaining()
        
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
            
            time.sleep(self.lineScrollSpeed)
            self.outputString += line + "\n"
            print(line)
        print('\n')
        
    def RedrawScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.DrawAttemptsRemaining()
        output_lines = self.outputString.split('\n')
        for line in output_lines:
            print(line)
            time.sleep(self.lineScrollSpeed)
        
        
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
            print ('[ERROR] Please input a valid difficulty.\n')
            self.SelectDifficulty()
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def AskLogout(self):
        inp = input ("Play again? (Y/N): ")
        if inp.upper() == "Y":
            self.PlayGame()
        elif inp.upper() == "N":
            exit(1)
        else:
            print("Please enter Y or N.")
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
                print("[SYSERROR] Please enter a valid input.")
            elif userIn == self.chosenWord:
                print ("Success! Logging in...\n")
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
                    print (userIn+": Incorrect credentials. " + str(correctCount) + "/" + str(len(self.chosenWord)) + "characters correct.")
                
    def DoLockout(self):
        self.gameOver = True
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SECURITY PROTOCOL ENGAGED. THIS TERMINAL WILL RESTART IN 10 SECONDS...")
        time.sleep(10)
        self.PlayGame()
                   
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
        
        
        
game = IdleGame()
game.PlayGame()
            
            
    