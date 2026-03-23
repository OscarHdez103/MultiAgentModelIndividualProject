import numpy as np

from Agent.BaseAgent import BaseAgent


class Post:
    POSTS :int = 0
    def __init__(self, creator_id:int, model, opinion_tendency:list[float|None]):
        from Model.Model_v1 import Model_v1 as Model
        self.unique_id :int = Post.POSTS
        Post.POSTS += 1

        self.creator_id :int = creator_id
        self.model :Model = model
        self.interacted_ids :list[int] = [creator_id]
        self.opinion_tendency :list[float|None] = opinion_tendency

        # model.rng.normal between 1 and 50 (mean=20, std=3)
        # self.relevancy :int = np.clip(model.rng.normal(loc=20, scale=3), 1, 50)

    def propagate(self, active_agents:list[int]): # 0-indexed agent IDs
        """Propagate the post to direct neighbours of the interacted agents."""
        # Get direct neighbours of all interacted agents
        neighbours :set[int] = set() # 0-indexed agent IDs
        for agent_id in self.interacted_ids:
            neighbours.update(self.model.graph.neighbors(agent_id-1))
        # Remove already interacted agents from neighbours
        neighbours.difference_update([agent_id-1 for agent_id in self.interacted_ids])
        # Remove agents that are not active in this step
        neighbours.intersection_update(active_agents)

        ## TODO: I do not like this method of deciding whether the post interacts with a neighbour, maybe change it later
        # INTERACTION_CHANCE :float = self.relevancy / 50
        INTERACTION_CHANCE :float = 0.8

        for neighbour_id in neighbours:
            if self.model.rng.random() < INTERACTION_CHANCE:
                self.interacted_ids.append(neighbour_id+1)
                self.model.get_agent(neighbour_id+1).interact(self)

        # self.relevancy -= 1
        pass

    def is_dead(self) -> bool:
        """Check if the post is dead (relevancy <= 0)."""
        # return self.relevancy <= 0
        return True