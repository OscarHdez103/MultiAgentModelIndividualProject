import json

import numpy as np
from numpy import random

from Agent.AgentPersonality import AgentPersonality as Personality
from Agent import AgentPersonality
from Agent.BaseAgent import BaseAgent
from Database.TimestampType import TimestampType
from Model.BaseModel import BaseModel
from Others.Post import Post


class Agent_v1(BaseAgent):
    def __init__(self, model:BaseModel, opinions:int):
        super().__init__(model)
        self.random_state = random.RandomState(seed=(self.seed+model.random.randint(0, 1000000) if self.seed is not None else model.random.randint(0, 1000000)))
        # Generate opinions amount of random -1..1 values inclusive
        self.opinions :list[float] = (self.random_state.rand(opinions) *2-1).tolist()

        self.personality : Personality = AgentPersonality.get_random(self, model.personality_weights)
        self.MAX_DIFFERENCE :float = \
            0.6 if self.personality == Personality.FLEXIBLE else \
            0.2 if self.personality == Personality.STUBBORN else \
            0.4
        self.REACTION_FACTOR :float = \
            0.12 if self.personality == Personality.REACTIVE else \
            0.06 if self.personality == Personality.STUBBORN else \
            0.08
        self.AGREE_FACTOR :float = \
            0.9 if self.personality == Personality.CONTRARIAN else \
            1.0
        self.DISAGREE_FACTOR :float = \
            1.1 if self.personality == Personality.CONTRARIAN else \
            1.0
        self.LIE_CHANCE :float = \
            0.5 if self.personality == Personality.LIAR else \
            0.05
        self.LIE_FOUND_FACTOR :float = self.DISAGREE_FACTOR + 0.2
        self.LIE_BIAS_FACTOR :float = 10

    def post(self) -> Post:
        if self.human():
            print(f"Agent {self.unique_id} posted from opinions {[round(float(x),3) for x in self.opinions]}")
        else:
            print(f"Bot -{self.unique_id} posted from opinions {[round(float(x),3) for x in self.opinions]}")
        # Get random opinion to post about
        opinion_id :int = self.random_state.randint(0, len(self.opinions))
        return self.post_about(opinion_id)
    def post_about(self, opinion_id:int) -> Post:
        # Get opinion tendency
        opinion_tendency :tuple[int, float] = (opinion_id, self.opinions[opinion_id])
        # Lie?
        lie: bool
        if self.personality == Personality.EXTREMIST_LIAR and abs(opinion_tendency[1]) >= 0.8:
            lie = self.random_state.rand() < (self.LIE_CHANCE * self.LIE_BIAS_FACTOR)
        elif self.personality == Personality.FACT_CHECKER:
            lie = False
        else:
            lie = self.random_state.rand() < self.LIE_CHANCE

        return Post(self.unique_id, self.model, opinion_tendency, lie)

    def interact(self, post:Post):
        """For now this method will simply change the agent's opinions based on the post's opinion tendency"""
        # Get id and empty changes list
        changes : list[float|None] = [None] * len(self.opinions)
        i :int = post.opinion_tendency[0]

        # Get opinion difference
        post_opinion :float = post.opinion_tendency[1]
        agent_opinion :float = self.opinions[i]
        diff = post_opinion - agent_opinion

        # Calculate if there is agreement between post and user or not
        local_reaction = self.AGREE_FACTOR if abs(diff) < self.MAX_DIFFERENCE else -self.DISAGREE_FACTOR

        # Fact-checker's job
        ## TODO: Potential anti post for next iteration
        if self.personality == Personality.FACT_CHECKER and post.LIE:
            local_reaction = -self.LIE_FOUND_FACTOR
            m :BaseModel = self.model
            m.fact_checked.append((self.unique_id, i))

        # Calculate effective changes and apply them
        old = self.opinions[i]
        changes[i] = self.REACTION_FACTOR * (1 if diff > 0 else -1 if diff < 0 else 0) * local_reaction
        self.opinions[i] += changes[i]
        self.opinions[i] = np.clip(self.opinions[i], -1, 1)
        changes[i] = old - self.opinions[i]

        if changes[i] >= 0:
            # Log the interaction in the database
            m :BaseModel = self.model
            m.db.timestamp(
                step=m.step_count,
                timestamp_type=TimestampType.INTERACTION,
                source_id=post.creator_id,
                target_id_or_lie=self.unique_id,
                post_id_or_connection_type=post.unique_id,
                opinion_change=changes,
                model=self.model,
                is_target=True
            )

    def state(self, state_id:str) -> float|list[float]:
        if state_id == "opinions":
            return self.opinions
        else:
            return super().state(state_id)
    def full_state(self) -> dict[str, object]:
        return {
            "unique_id": self.unique_id,
            "opinions": self.opinions,
        }
    def __str__(self): return f"Agent {self.unique_id} with state {self.state}"

    def human(self) -> bool:
        return True