import mesa
from Agent.ExampleAgent import ExampleAgent
from Model.BaseModel import BaseModel


class ExampleModel(BaseModel):

    def __init__(self, n:int=10, seed=None):
        super().__init__(defined_agent=ExampleAgent, n=n, seed=seed)
        # Additional inits can be added here
        self.agent_action = "exchange_wealth"
        pass


    def step(self):
        self.agents.shuffle_do(self.agent_action)