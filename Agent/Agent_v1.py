from numpy import random

from Agent.BaseAgent import BaseAgent
from Others.Post import Post


class Agent_v1(BaseAgent):
    def __init__(self, model, opinions:int):
        super().__init__(model)
        self.random_state = random.RandomState(seed=self.seed)
        # Generate opinions amount of random -1..1 values inclusive
        self.opinions :list[float] = (self.random_state.rand(opinions) *2-1).tolist()
        self.activity :float = self.random_state.rand() # Frequency of interacting of any kind
        self.privacy :float = self.random_state.rand()  # Frequency of posting content

    def post(self) -> Post:
        print(f"Agent {self.unique_id} posted with state {self.state}")
        ## TODO: Implement posting behaviour
        # 1. Get random number of opinions to be influenced by the post
        min_tendencies, max_tendencies = 1, len(self.opinions)
        num_tendencies = self.random_state.randint(min_tendencies, max_tendencies + 1)

        # 2. Randomly select num_tendencies opinions to be influenced
        selected_indices = self.random_state.choice(len(self.opinions), size=num_tendencies, replace=False)

        # 3. For each selected opinion, generate a random influence tendency between -1 and 1, for the rest set it to None
        opinion_tendency :list[float|None] = [
            self.random_state.rand() * 2 - 1
            if i in selected_indices else None
            for i in range(len(self.opinions))
        ]

        return Post(self.unique_id, self.model, opinion_tendency)

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