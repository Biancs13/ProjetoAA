from world import World
from agente import Agent
import random

def main():
    wantSee = True
    n = 40
    g = Agent("G", (2,2))
    world = World(5,g)
    a1 = Agent("A", (0,0))
    a2 = Agent("B", (1,1))
    world.addAgent(a1)  
    world.addAgent(a2)

    if wantSee:
        for i in range(n):
            world.toString()
            if world.updateWorldRandom(i):
                return
            


if __name__ == "__main__":
    main()