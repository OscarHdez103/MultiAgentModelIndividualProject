from numpy import random

from Agent.BaseAgent import BaseAgent


class Agent_v1(BaseAgent):
    def __init__(self, model, opinions:int):
        super().__init__(model)
        self.random_state = random.RandomState(seed=self.seed)
        # Generate opinions amount of random -1..1 values inclusive
        self.opinions :list[float] = (self.random_state.rand(opinions) *2-1).tolist()
        self.activity :float = self.random_state.rand()
        self.privacy :float = self.random_state.rand()

    def post(self):
        print(f"Agent {self.unique_id} posted with state {self.state}")
        ## TODO: Implement posting behaviour
        pass

    def state(self, state_id:str) -> float|list[float]:
        if state_id == "opinions":
            return self.opinions
        elif state_id == "activity":
            return self.activity
        elif state_id == "privacy":
            return self.privacy
        else:
            return super().state(state_id)

    def full_state(self) -> dict[str, object]:
        return {
            "unique_id": self.unique_id,
            "opinions": self.opinions,
            "activity": self.activity,
            "privacy": self.privacy,
        }

    def step(self):
        print(f"Running step for agent {self.unique_id} with state {self.state}")
        pass