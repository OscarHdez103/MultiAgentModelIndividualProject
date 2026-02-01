# python
# File: `Repo/MultiAgentModelIndividualProject/Model/ExampleModel.py`
import mesa
from Agent.ExampleAgent import ExampleAgent


class ExampleModel(mesa.Model):

    def __init__(self, n:int=10, seed=None):
        super().__init__(seed=seed)
        self.num_agents = n

        ExampleAgent.create_agents(model=self, n=n)

    def step(self):
        self.agents.shuffle_do("exchange_wealth")