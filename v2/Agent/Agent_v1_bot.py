from Agent.Agent_v1 import Agent_v1
from Model.BaseModel import BaseModel
from Others.Post import Post
import numpy as np


class Agent_v1_Bot(Agent_v1):
    def __init__(self, model: BaseModel, opinions: int):
        super().__init__(model, opinions)
        if self.model.extremist_bots:
            for i, opinion in enumerate(self.opinions):
                # Use formula self.opinions[i] = sine(opinion * pi /2) -> cdf_1(x)
                # print(f"From {round(self.opinions[i], 2)} to {round(np.sin(opinion * np.pi / 2), 2)}")
                self.opinions[i] = np.sin(opinion * np.pi / 2)
        # else:
        #     for i, opinion in enumerate(self.opinions):
        #         print(f"Staying at {round(self.opinions[i], 2)}")




    def interact(self, post:Post):
        pass

    # def __str__(self): return f"Agent -{self.unique_id} with state {self.state}"

    def human(self) -> bool:
        return False