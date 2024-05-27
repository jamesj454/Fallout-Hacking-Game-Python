import random
import os      # For clearing console
import time

class TerminalGame:
    
    def __init__(self):
        self.attemptsRemaining = 5    # Number of attempts before 10 sec lockout
        self.numOfColumns = 24        # X size of grid
        self.numOfRows = 17           # Y size of grid
        self.gameDifficulty = 5       # Num of letters in word
        self.lineScrollSpeed = 0.03   # How fast text should 'load' onto the terminal
        self.securityLockoutTime = 10 # How long the user will be locked out if game is lost
        
        self.staticWords = ["%","!","=","(",")","*","<",">",":",";","'","@","[","]","&"]
        self.chosenWord = ""
        self.outputString = ""
        self.gameOver = False
        self.wordsList = []
    
    # Reads words from word list
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
                self.PrintAndSleep(line, self.lineScrollSpeed)
    
    # Returns mem address + first column
    def GenerateLine(self, insertChosenWordAtY, row):
        line = []
        if row == insertChosenWordAtY and self.outputString.find(self.chosenWord) != -1:
            insertWordAtX = random.randint(0, self.numOfColumns - len(self.chosenWord))
            for col in range(self.numOfColumns):
                if col == insertWordAtX:
                    line.append(self.chosenWord)
                    col += len(self.chosenWord) - 1  
                else:
                    line.append(random.choice(self.staticWords))
            line = ''.join(line)[:self.numOfColumns]
        else:
            if random.random() < 0.5:
                randomWord = random.choice(self.wordsList)
                insertWordAtX = random.randint(0, self.numOfColumns - len(randomWord))
                for col in range(self.numOfColumns):
                    if col == insertWordAtX and self.outputString.find(self.chosenWord) == -1:
                        line.append(randomWord)
                        col += len(randomWord) - 1  
                    else:
                        line.append(random.choice(self.staticWords))
                line = ''.join(line)[:self.numOfColumns]
            else:
                line = ''.join(random.choice(self.staticWords) for _ in range(self.numOfColumns))
        return line

    def GenerateScreen(self):
        self.PrintLine("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL")
        self.DrawAttemptsRemaining()

        self.GetWords()
        self.chosenWord = random.choice(self.wordsList)
        insertChosenWordAtY = random.randint(0, self.numOfRows - 1)

        for row in range(self.numOfRows):
            # Generate two separate columns
            line1 = self.GenerateLine(insertChosenWordAtY, row)
            line2 = self.GenerateLine(insertChosenWordAtY, row)

            memory_address1 = hex(id(line1))
            memory_address2 = hex(id(line2))

            self.outputString += f"{memory_address1} {line1}  {memory_address2} {line2}\n"
            self.PrintLine(f"{memory_address1} {line1}  {memory_address2} {line2}")
        print('\n')
    
    # Refreshes the game and header, used to display messages without updating game content, or refreshing the game
    # after a word is selected and erased with static characters
    def RedrawScreen(self):
        self.ClearTerminal()
        print ("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL")
        self.DrawAttemptsRemaining()
        output_lines = self.outputString.split('\n')
        for line in output_lines:
            if line != "":
                self.PrintLine(line)
        print(' ')
    
    # Difficulty is the length of the word that will be guessed. 3 = Easy -> 5 = Hard
    def SelectDifficulty(self):
        self.ClearTerminal()
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
        self.ClearTerminal()
        
    # Ask whether to restart or close game
    def AskLogout(self):
        inp = input ("Play again? (Y/N): ")
        if inp.upper() == "Y":
            self.PlayGame()
        elif inp.upper() == "N":
            exit(1)
        else:
            self.PrintLine("Please enter Y or N.")
            self.AskLogout()
        
    # Select difficulty, mock boot, then generate screen, and enter game loop
    def PlayGame(self):
        self.__init__()
        self.SelectDifficulty()
        self.BootUpSequence()
        
        self.ClearTerminal()
        self.GenerateScreen()
        self.gameOver = False
        
        while self.gameOver == False:
            userIn = input("ENTER PASSWORD: ").upper()
            if  len(userIn) != len(self.chosenWord):
                self.RedrawScreen()
                self.PrintLine("[SYSERROR] Please enter a valid input.")
            elif userIn == self.chosenWord:
                self.ClearTerminal()
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
                    self.ClearTerminal()
                    self.ReplaceInputtedWordWithStatic(userIn)
                    self.RedrawScreen()
                    self.PrintLine (userIn+": Incorrect credentials. " + str(correctCount) + "/" + str(len(self.chosenWord)) + " characters correct.")
    
    # Sleeps terminal for 10 seconds after game is lost, then restarts the game    
    def DoLockout(self):
        self.gameOver = True
        timePassed = 0
        while timePassed <= self.securityLockoutTime:
            self.ClearTerminal()
            print("SECURITY PROTOCOL ENGAGED. PLEASE CONTACT AN ADMINISTRATOR.\nTHIS TERMINAL WILL RESTART IN " + str(self.securityLockoutTime-timePassed) + " SECOND(S)...")
            timePassed+=1
            time.sleep(1)
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
    
    # Simulated boot sequence, played after difficulty is selected.
    def BootUpSequence(self):
        self.ClearTerminal() # Screen 1
        self.PrintAndSleep("WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK\n", 3)
        self.PrintAndSleep(">SET TERMINAL/INQUIRE\n", 1)
        self.PrintAndSleep("RIT-V300\n", 2)
        self.PrintAndSleep(">SET FILE/PROTECTION=OWNER:RWED ACCOUNTS.F\n", 2)
        self.PrintAndSleep(">SET HALT RESTART/MAINT\n\n",1)
        
        self.ClearTerminal() # Screen 2
        self.PrintAndSleep("Initializing Robco Industries(TM) MF Boot Agent v2.3.0\n",1.5)
        self.PrintAndSleep("RETROS BIOS",0.2)
        self.PrintAndSleep("RBIOS-4.02.08.00 52EE5.E7.E8\nCopyright 2201-2203 Robco Ind.",1)
        self.PrintAndSleep("Uppermem: 64 KB",0.2)
        self.PrintAndSleep("Root (5A8)",0.2)
        self.PrintAndSleep("Maintenance Mode\n",2)
        self.PrintAndSleep(">RUN DEBUG/ACCOUNTS.F",3)

    # Used to simulate line load
    def PrintAndSleep(self, string, timeToSleepSec):
        print(string)
        time.sleep(timeToSleepSec)
        
    def ClearTerminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
game = TerminalGame()      
game.PlayGame()
            
            
    