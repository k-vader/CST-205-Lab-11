class User(object):
  
  def __init__(self, currentRoom):
    self.currentRoom = currentRoom


class Room(object):
    
    description = "This is the default description"
    northExit = 0
    southExit = 0
    eastExit = 0
    westExit = 0
    
    # default initializer. Supply room name as a string and room
    # number as an integer
    def __init__(self, name, number):
        self.name = name
        self.number = number
    
    # set name to newName
    def set_name(self, newName):
      self.name = newName
    
    # set number to newNumber
    def set_number(self, newNumber):
      self.number = newNumber
    
    # set description variable to newDescription    
    def set_description(self, newDescription):
        self.description = newDescription
    
    # set exit directions to integer values supplied by north
    # south, east, and west. Integers are the room number that
    # the exit leads to, 0 is no exit.    
    def set_exit_directions(self, north, south, east, west):
        self.northExit = north
        self.southExit = south
        self.eastExit = east
        self.westExit = west
    
    def show_room(self):
      roomString = self.name + '\n' + self.description + '\n' + self.show_exits()
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

# Set up rooms and player as global objects
# Create our 5 rooms, name them, and give them each a unique number
roomOne = Room("First Room", 1)
roomTwo = Room("Second Room", 2)
roomThree = Room("Third Room", 3)
roomFour = Room("Fourth Room", 4)
roomFive = Room("Fifth Room", 5)
  
# Set the exits up for our rooms
roomOne.set_exit_directions(5, 0, 2, 0)
roomTwo.set_exit_directions(3, 0, 0, 1)
roomThree.set_exit_directions(0, 2, 0, 4)
roomFour.set_exit_directions(0, 0, 3, 5)
roomFive.set_exit_directions(0, 1, 4, 0)
  
# Create a rooms list and add all of our rooms to it
rooms = []
rooms.append(roomOne)
rooms.append(roomTwo)
rooms.append(roomThree)
rooms.append(roomFour)
rooms.append(roomFive)
  
player = User(1)




# Input function with validation. 
def getInput():
  # Prompt for input and lowercase string before storing
  command = requestString("Enter your command").lower() 

  # Here we check to see if they entered a known command, if not we prompt again
  if command == "north" or command == "south" or command == "east" or command == "west":
    return doMove(rooms, player.currentRoom, command)
  elif command == "help" or command == "exit":
    return command
  elif command == "look":
    return doLook(rooms, player.currentRoom)
  else:
    printNow("Unknown command, please try again.")
    return getInput()

# For movement around map.
def doMove(roomList, currentRoom, direction):
  for room in roomList:
    if room.number == currentRoom:
      if direction == "north" and room.northExit:
        printNow("You move north.")
        player.currentRoom = room.northExit
        doLook(roomList, player.currentRoom)
        break
      elif direction == "south" and room.southExit:
        printNow("You move south.")
        player.currentRoom = room.southExit
        doLook(roomList, player.currentRoom)
        break
      elif direction == "east" and room.eastExit:
        printNow("You move east.")
        player.currentRoom = room.eastExit
        doLook(roomList, player.currentRoom)
        break
      elif direction == "west" and room.westExit:
        printNow("You move west.")
        player.currentRoom = room.westExit
        doLook(roomList, player.currentRoom)
        break
      else:
        printNow("You cannot go in that direction.")

# For 'look' command. Displays name, description, and exits of current room
def doLook(roomList, currentRoom):
  for room in roomList:
    if room.number == currentRoom:
      printNow(room.show_room())
      break

def adventure():
  # Let's show the player where they are
  doLook(rooms, player.currentRoom)
  
  userInput = getInput()
  while userInput != "exit":
    userInput = getInput()
  