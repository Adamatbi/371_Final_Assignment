"""
EggNode
Task: control the egg object - major reward in the game
    - xCoordinate, yCoordinate: coordinate of the egg
    - visibleState: a visibility of the egg (on the board) -> True is visible, False otherwise
    - lockState: the lock status of the egg -> True is locked, False otherwise
    - occupyState: the occupy status of the egg eggPoints -> True is Occuppied, False otherwise  
    - eggOnwerID: indicates the owner of the egg
"""

class EggNode:
    #----------------------------------------------------
    #PROPERTIES
    #----------------------------------------------------
    __xCoordinate = 0
    __yCoordinate = 0
    __visibleState = True 
    __lockState = False
    __occupyState = False
    __eggPoints = 0
    __eggOwnerID = 0

    #----------------------------------------------------
    #SETTER_FUNCTIONS
    #----------------------------------------------------
    #setCoordinate() - set the coordinate of the egg
    def setCoordinate(self, xCoord, yCoord):
        self.__xCoordinate = xCoord
        self.__yCoordinate = yCoord
        return None

    #setVisibleState() - set the current state visible of the 
    def setVisible(self, newVisibleState):
        self.__visibleState = newVisibleState
        return None

    #setLockState() - set the current lock state of the egg
    def setLock(self, newlockState):
        self.__lockState = newlockState
        return None

    #setOccupyState() - set the current occupy state of the egg 
    def setOccupy(self, newOccupyState):
        self.__occupyState = newOccupyState
        return None
    
    #setEggPoints() - set the point for an egg
    def setEggPoint(self, newEggPoints):
        self.__eggPoints = newEggPoints
        return None
    
    #setEggOwnerID() - set the new ower for an egg
    def setEggOwnerID(self, newOwnerID):
        self.__eggOwnerID = newOwnerID
        return None

    #----------------------------------------------------
    #SETTER_FUNCTIONS
    #----------------------------------------------------
    #getCoordinate() - return an array of the coordinate of an egg
    def getCoordinate(self):
        return [self.__xCoordinate, self.__yCoordinate]

    #setVisibleState() - set the current state visible of the 
    def isVisible(self):
        return self.__visibleState

    #getLockState() - return the current lock state of an egg
    def isLock(self):
        return self.__lockState
    
    #getOccupyState - return the current occupy state of an egg
    def isOccupied(self):
        return self.__occupyState

    #getEggPoints() - return the point of an egg
    def getEggPoint(self):
        return self.__eggPoints

    #getOwnerID() - return the OnwerID of an egg
    def getOwnerID(self):
        return self.__eggOwnerID