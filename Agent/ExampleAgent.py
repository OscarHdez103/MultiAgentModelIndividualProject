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

    def full_state(self) -> dict[str, int]:
        return {"unique_id": self.unique_id, "wealth": self.wealth}

    def state(self, state_id:str) -> float|list[float]:
        if state_id == "wealth":
            return self.wealth
        elif state_id == "unique_id":
            return self.unique_id
        else:
            return super().state(state_id)

