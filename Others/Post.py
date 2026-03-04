import numpy as np

from Model.BaseModel import BaseModel


class Post:
    def __init__(self, creator_id:int, model:BaseModel, opinion_tendency:list[float|None]):
        self.creator_id :int = creator_id
        self.model :BaseModel = model
        self.interacted_ids :list[int] = [creator_id]
        self.opinion_tendency :list[float|None] = opinion_tendency

        # model.rng.normal between 1 and 50 (mean=25.5, std=10)
        self.relevancy :int = np.clip(model.rng.normal(loc=25.5, scale=10), 1, 50)

    def propagate(self):
        """Propagate the post to direct neighbours of the interacted agents."""
        self.relevancy -= 1

        pass

    def is_dead(self) -> bool:
        """Check if the post is dead (relevancy <= 0)."""
        return self.relevancy <= 0