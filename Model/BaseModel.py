import mesa
from Agent.BaseAgent import BaseAgent as Agent

class BaseModel(mesa.Model):

    def __init__(self, n:int=10, seed=None):
        super().__init__(seed=seed)
        self.num_agents = n

        Agent.create_agents(model=self, n=n)

    def step(self):
        pass