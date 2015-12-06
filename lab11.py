# Ken Vader
# Ngoan Nguyen
# Chris Pina
# Lab 11
# 12/1/2015


# User class
# Holds location and custom action information
class User(object):
  
  def __init__(self, currentRoom):
    self.currentRoom = currentRoom
    self.win = false
    self.customActions = []
                
  def set_lose(self, lose):
    self.lose = lose
    
  def set_win(self, win):
    self.win = win

# Custom Action Class, accepts an action string
class CustomAction(object):
  
  # action string = description
  # trigger string = the word that triggers the action
  # slug = the slug of the item in question
  def __init__(self, actionString, triggerString, slug):
    self.actionString = actionString
    self.triggerString = triggerString
    self.slug = slug

# Room class. Stores exit information, room name, room description, and room number
# Methods exist for displaying all room information or just the exits
class Room(object):
	
    # Room exits. 0 is for no exit. Other integers indicate a valid exit, with the integer indicating
    # which room that exit leads to
    northExit = 0
    southExit = 0
    eastExit = 0
    westExit = 0
    
    # default initializer. Supply room name as a string and room
    # number as an integer
    def __init__(self, name, action, description):
        self.name = name
        self.customAction = action
        self.description = description
    
    # is this room a losing room? If the user enters this room, he/she will LOSE!
    def set_losingRoom(self, losingRoom):
      self.losingRoom = losingRoom
    
    # set name to newName
    def set_name(self, newName):
      self.name = newName
    
    # set number to newNumber
    def set_number(self, newNumber):
      self.number = newNumber
            
    # set exit directions to integer values supplied by north
    # south, east, and west. Integers are the room number that
    # the exit leads to, 0 is no exit.    
    def set_exit_directions(self, north, south, east, west):
        self.northExit = north
        self.southExit = south
        self.eastExit = east
        self.westExit = west
    
    # Returns a string consisting of the room name followed by a line break, the room description followed by a line break
    # and the exits
    def show_room(self):
      roomString = "Room Name: " + self.name + '\n' +  "Description: " + self.description + '\n' + "Exits: " + self.show_exits() + '\n' + self.show_action()
      return roomString
        
    # returns a string based on available exits in current room    
    def show_exits(self):
        if self.northExit == 0 and self.southExit == 0 and self.eastExit == 0 and self.westExit == 0:
            return "This room has no exits!"
        else:
            exitString = "The exits in this room: "
            if self.northExit:
                exitString = exitString + "North "
            if self.southExit:
                exitString = exitString + "South "
            if self.eastExit:
                exitString = exitString + "East "
            if self.westExit:
                exitString = exitString + "West "
                
            return exitString

    # returns the user's custom action if available
    def show_action(self):
      if self.customAction:
        returnString = "Optional: " + self.customAction.actionString + " Enter [" + self.customAction.triggerString + "] to trigger"
        return returnString
      else:
        return ""

# Set up rooms and player as global objects
# Create our 5 rooms, name them, and give them each a description
roomOne = Room("The Foyer", None, "You are in the dark, gloomy foyer. The door has locked behind you.\n")
roomOne.losingRoom = false

roomTwo = Room("The Kitchen", None, "You have entered the kitchen. The counters are covered in red.")
roomTwo.losingRoom = false

roomThreeAction = CustomAction("There's something here, would you like to pick it up?", "Yes", "Flashlight")
roomThree = Room("The Dining Room", roomThreeAction, "You are in the dining room. The table is set, but there is no one in sight. Eat some food, make sure it is light.")
roomThree.losingRoom = false

roomFourAction = CustomAction("There's something here, would you like to pick it up?", "Yes", "Key")
roomFour = Room("The Library", roomFourAction, "Bookshelves from floor to ceiling. The books have vanished. Nothing but dust remains. I heard knowledge is the KEY to success...")
roomFour.losingRoom = false

roomFive = Room("The Dungeon", None, "You have entered the dungeon. YOU LOSE!")  
roomFive.losingRoom = true

# Set the exits up for our rooms
roomOne.set_exit_directions(5, 0, 2, 0)
roomTwo.set_exit_directions(3, 0, 0, 1)
roomThree.set_exit_directions(0, 2, 0, 4)
roomFour.set_exit_directions(0, 0, 3, 5)
roomFive.set_exit_directions(0, 0, 0, 0)
  
# Create a rooms list and add all of our rooms to it
rooms = []
rooms.append(roomOne)
rooms.append(roomTwo)
rooms.append(roomThree)
rooms.append(roomFour)
rooms.append(roomFive)

# Create a player object and set it to start in room 1  
player = User(roomOne)
player.lose = false

# Input function with validation. 
def getInput():
  # Prompt for input and lowercase string before storing
  command = requestString("Enter your command").lower() 

  # Here we check to see if they entered a known command, if not we prompt again
  if command == "north" or command == "south" or command == "east" or command == "west":
    return doMove(rooms, player.currentRoom, command)
  elif command == "enter":
    return doLook(rooms, player.currentRoom)
  elif command == "exit":
    return command
  elif command == "help":
    return welcome()
  elif command == "look":
    return doLook(rooms, player.currentRoom)
  elif player.currentRoom.customAction:
    if command == player.currentRoom.customAction.triggerString.lower():
      triggerActionForPlayer(player)
      return getInput()
  else:
    printNow("Unknown command, please try again.")
    return getInput()

def triggerActionForPlayer(player):

    # prevent duplicate items
    containsItem = false
    for customAction in player.customActions:
      if customAction.slug == player.currentRoom.customAction.slug:
        containsItem = true
        break;
      
    if containsItem == false:
      player.customActions.append(player.currentRoom.customAction)
      printNow("You picked up a " + player.currentRoom.customAction.slug + " from the " + player.currentRoom.name)
    else:
      printNow("You already picked this item up...")
    
# For movement around map.
def doMove(roomList, currentRoom, direction):
  # first find the current room in the room list
  for room in roomList:
    if room == currentRoom:
      # now we check if the direction passed in has a valid exit in the current room
      # if there is, we send a message to the player that we moved, set the player's
      # current room to the new room, and perform a look to display the new room to
      # the player
      # if not, we output a message stating the player cannot go in that direction
      if direction == "north" and room.northExit:
        printNow("You move north.")
        player.currentRoom = getRoomForRoomNumber(room.northExit)
        doLook(roomList, player.currentRoom)
        break
      elif direction == "south" and room.southExit:
        printNow("You move south.")
        player.currentRoom = getRoomForRoomNumber(room.southExit)
        doLook(roomList, player.currentRoom)
        break
      elif direction == "east" and room.eastExit:
        printNow("You move east.")
        player.currentRoom = getRoomForRoomNumber(room.eastExit)
        doLook(roomList, player.currentRoom)
        break
      elif direction == "west" and room.westExit:
        printNow("You move west.")
        player.currentRoom = getRoomForRoomNumber(room.westExit)
        doLook(roomList, player.currentRoom)
        break
      else:
        printNow("You cannot go in that direction.")

def getRoomForRoomNumber(roomNumber):
  return rooms[roomNumber-1]

# We need 2 actions stored to win
def didWin(player):
  return len(player.customActions) == 2
      
# For 'look' command. Displays name, description, and exits of current room
def doLook(roomList, currentRoom):
  
  if currentRoom.losingRoom:
    player.lose = true
    return
  
  if didWin(player):
    player.win = true
    return
    
  for room in roomList:
    if room == currentRoom:
      printNow(room.show_room())
      break

def welcome():
  welcomeMsg = "***Welcome to Mystery Mansion***\nWhen entering each room, you will be able to move north, south, east and west into a different room. Type the direction to move. Type LOOK to get room details. Type HELP to redisplay this message. Type EXIT to quit the game. ENTER if you dare!"
  showInformation(welcomeMsg)
  #printNow("***Welcome to Mystery Mansion***")
  #printNow("When entering each room, you will be able to move north, south,")
  #printNow("east and west into a different room. Type the direction to move. Type")
  #printNow("LOOK to get room details. Type HELP to redisplay this message. Type EXIT")
  #printNow("to quit the game. ENTER if you dare!")

userName = ""

def getName():
  name = requestString("Please enter your name")
  
  if len(name) == 0:
    return getName(name)
  else:
    return name
	  
def adventure():
  #Let's welcome the player to the game
  welcome()
  
  userName = getName()
  
  userInput = getInput()
  while userInput != "exit":
    if player.lose == true:
      showInformation(userName + " you have entered THE DUNGEON, it has no exits. YOU LOSE!")
      #printNow("You entered THE DUNGEON, it has no exits. YOU LOSE")
      clearVars()
      return
    elif player.win == true:
      showInformation(userName + " you used your flashlight and key to exit the Foyer, you win! All hail " + userName + "!")
      #printNow("You used your flashlight and key to exit the Froyer, you win!")
      clearVars()
      return
    else:
      userInput = getInput()

def clearVars():
  player.lose = false
  player.currentRoom = rooms[0]
  player.customActions = []
  player.win = false
