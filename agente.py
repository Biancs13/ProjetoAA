import random


class Agent:
    def __init__(self, name, position):
        self.name = name
        self.position = position
    
    def move(self, new_position):
        self.position = new_position
    
    def randomMove(self,gridSize,world=None):
        newPos = random.choice([(self.position[0]+1,self.position[1]), (self.position[0]-1,self.position[1]), (self.position[0],self.position[1]+1), (self.position[0],self.position[1]-1)])

        if (newPos[0] < 0 or newPos[0] >= gridSize or newPos[1] < 0 or newPos[1] >= gridSize):
            return
        if (world.map[newPos] is not None and world.map[newPos] != world.goal ):
            return
        else:
            self.position = newPos
    

    def getPosition(self):
        return self.position
    
    def getName(self):
        return self.name
    

