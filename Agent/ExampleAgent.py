import mesa

from Agent.BaseAgent import BaseAgent


class ExampleAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model)

        self.wealth : int = 1

    def presentation(self):
        print(f"Hello, I am agent {self.unique_id} with wealth {self.wealth}.")

    def exchange_wealth(self):
        if self.wealth > 0:
            other_agent : ExampleAgent = self.random.choice(self.model.agents)
            if other_agent is not None:
                other_agent.wealth += 1
                self.wealth -= 1
