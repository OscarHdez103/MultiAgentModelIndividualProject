import json

import numpy as np
from numpy import random

from Agent.BaseAgent import BaseAgent
from Database.TimestampType import TimestampType
from LLM.guides.AgentInfo import AgentInfo
from LLM.guides.FriendIds import FriendIds
from LLM.guides.Opinion import Opinion
from LLM.guides.PromptInfo import PromptInfo
from LLM.guides.Post import PostGuide
from Model.BaseModel import BaseModel
from Others.Post import Post


class Agent_v1(BaseAgent):
    def __init__(self, model:BaseModel, opinions:int):
        super().__init__(model)
        self.random_state = random.RandomState(seed=self.seed+model.random.randint(0, 1000000))
        # Generate opinions amount of random -1..1 values inclusive
        self.opinions :list[float] = (self.random_state.rand(opinions) *2-1).tolist()
        # self.activity_ :float = self.random_state.rand() # Frequency of interacting of any kind
        # self.privacy_ :float = self.random_state.rand()  # Frequency of posting content

    def post(self) -> Post:
        print(f"Agent {self.unique_id} posted with state {self.state}")
        # 1. Get random number of opinions to be influenced by the post
        min_tendencies, max_tendencies = 1, len(self.opinions)
        num_tendencies = self.random_state.randint(min_tendencies, max_tendencies + 1)

        # 2. Randomly select num_tendencies opinions to be influenced
        selected_indices = self.random_state.choice(len(self.opinions), size=num_tendencies, replace=False)

        # 3. For each selected opinion, set the opinion tendency to the same as the Agent's opinions, for the rest set it to None
        opinion_tendency :list[float|None] = [
            self.opinions[i]
            if i in selected_indices else None
            for i in range(len(self.opinions))
        ]

        return Post(self.unique_id, self.model, opinion_tendency)
    def interact(self, post:Post):
        """For now this method will simply change the agent's opinions based on the post's opinion tendency"""
        ## TODO: Implement graph reactions and post reactions
        # Get prompt and response for AI
        prompt_info :PromptInfo = PromptInfo(
            agent_info=AgentInfo(
                agent_id=self.unique_id,
                opinions=[
                    Opinion(
                        opinion_id=i,
                        bias=self.opinions[i]
                    )
                    for i in range(len(self.opinions))
                ]
            ),
            friend_ids=FriendIds(
                friend_ids=[
                    friend_id
                    for friend_id in self.model.graph.neighbors(self.unique_id)
                ]
            ),
            post=PostGuide(
                source_id=post.creator_id,
                opinion_bias=[
                    Opinion(opinion_id=i, bias=tendency)
                    for i, tendency in enumerate(post.opinion_tendency)
                    if tendency is not None
                ]
            )
        )
        print(f"-------- Prompt Info --------\n{prompt_info}\n-------- =========== --------")
        m :BaseModel = self.model
        response =  json.loads(m.llm.chat(prompt_info))
        print(f"-------- Response --------\n{response}\n-------- =========== --------")

        # Use the response into changing the agent's opinions and logging the changes
        changes :list[float|None] = [None] * len(self.opinions)
        reaction :int = 1 if response["reaction"] == "positive" else -1
        if response["opinions_changed"] is not None:
            for change in response["opinions_changed"]:
                i :int = change["opinion_id"]
                bias :float = np.clip(change["change"], 0.0, 0.2) * reaction
                self.opinions[i] += bias

                self.opinions[i] = np.clip(self.opinions[i], -1, 1)
                changes[i] = bias

            m.db.timestamp(
                step=m.step_count,
                timestamp_type=TimestampType.INTERACTION,
                source_id=post.creator_id,
                target_id=self.unique_id,
                post_id_or_connection_type=post.unique_id,
                opinion_change=changes
            )

        # ## TODO: Implement graph changes as well
        # changes : list[float|None] = [None] * len(self.opinions)
        # # Random reaction (50% for a 1, 50% for a -1)
        # reaction :int = self.random_state.randint(0, 2) * 2 - 1
        # for i in range(len(self.opinions)):
        #     if post.opinion_tendency[i] is not None:
        #         # Copy reaction into local_reaction
        #         local_reaction :int = reaction
        #         # If no discrepancy between opinion and tendency (Same +/- sign), then set reaction to 1 (reinforcement)
        #         if np.sign(self.opinions[i]) == np.sign(post.opinion_tendency[i]): local_reaction = 1
        #         # Change opinion by 5% of the tendency value
        #         changes[i] = 0.10 * post.opinion_tendency[i] * local_reaction
        #         self.opinions[i] += changes[i]
        #         # Ensure opinions stay within -1 and 1
        #         self.opinions[i] = np.clip(self.opinions[i], -1, 1)
        #
        # m :BaseModel = self.model
        # m.db.timestamp(
        #     step=m.step_count,
        #     timestamp_type=TimestampType.INTERACTION,
        #     source_id=post.creator_id,
        #     target_id=self.unique_id,
        #     post_id_or_connection_type=post.unique_id,
        #     opinion_change=changes
        # )

    def state(self, state_id:str) -> float|list[float]:
        if state_id == "opinions":
            return self.opinions
        # elif state_id == "activity":
            return self.activity
        # elif state_id == "privacy":
            return self.privacy
        else:
            return super().state(state_id)

    def full_state(self) -> dict[str, object]:
        return {
            "unique_id": self.unique_id,
            "opinions": self.opinions,
            # "activity": self.activity,
            # "privacy": self.privacy,
        }

    def step(self):
        print(f"Running step for agent {self.unique_id} with state {self.state}")
        pass