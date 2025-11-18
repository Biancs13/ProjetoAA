

class World:
    def __init__(self, gridSize, goal):
        self.map = {(x,y):None for x in range(gridSize) for y in range(gridSize)}
        self.gridSize = gridSize
        self.agents = [goal]
        self.goal = goal
        self.addAgent(goal)

    def addAgent(self, agent):
        if agent is not None and self.map.get(agent.getPosition()) is None:
            self.agents.append(agent)
            self.map[agent.getPosition()] = agent

    def updateAgent(self,agent,i):
        position = agent.getPosition()
        self.map[position] = None
        agent.randomMove(self.gridSize,self)
        self.map[agent.getPosition()] = agent
        if agent.getPosition() == self.goal.getPosition():
            print(f"Agent {agent.getName()} reached the goal in {i} moves!")
            return True
        return False
    
    
    def updateWorldRandom(self,i):
        outcome = False
        for a in self.agents:
            if a is not self.goal:
                outcome = outcome or self.updateAgent(a,i)
        return outcome

    def toString(self):

        for y in range(self.gridSize):
            line = " "
            for x in range(self.gridSize):
                if self.map[(x,y)] is None:
                    line += ". "
                else:
                   line += self.map[(x,y)].getName() + " "
            print(line)
        print()
    
