import networkx as nx
import numpy as np
from networkx.generators.random_graphs import watts_strogatz_graph

from Agent.Agent_v1 import Agent_v1 as Agent
from Agent.Agent_v1_bot import Agent_v1_Bot
from Agent.Weights import Weights
from Database.Data import Data
from Database.TimestampType import TimestampType
from Model.BaseModel import BaseModel
import matplotlib.pyplot as plt

from Others.Post import Post


class Model_v1(BaseModel):

    def __init__(self, database:Data, opinions:int, k:int, p:float, n:int=10, bots:int=0, seed:float|None=None, EXTREMIST_BOTS:bool=None, weights:Weights=None):
        super().__init__(database=database, defined_agent=Agent, n=n, bot_type=Agent_v1_Bot, bots=bots, seed=seed, graph=watts_strogatz_graph(n=n+bots, k=k, p=p, seed=seed), opinions=opinions, EXTREMIST_BOTS=EXTREMIST_BOTS, weights=weights)
        # Choose one random agent
        self.active_rng = np.random.default_rng(seed)
        Post.POSTS = 0
        self.posts :list[Post] = []
        # self.dead_posts :list[Post] = []

        pass

    def step(self):
        """Process one step for all agents in the model."""
        # Call BaseModel step to increment step counter and log agents
        super().step()

        # 1. Select random subset of active agents based on their activity levels
        activity_weights = np.array([0.5 for _ in self.agents])
        activity_weights = activity_weights / activity_weights.sum()
        num_agents = self.random.randint(1, len(self.agents))

        active_agents :list[int] = self.active_rng.choice(len(self.agents), size=num_agents, replace=False, p=activity_weights) # 0-indexed

        # 2. Select random subset of posting agents from active agents based on their privacy levels and a posting chance
        POSTING_CHANCE :float = 0.3
        posting_agents: list[int] = [
            agent_id for agent_id in active_agents
            if self.random.random() < POSTING_CHANCE # 1-indexed agent IDs in self.agents
        ]

        # 3. For each posting agent, create a post
        for agent_id in posting_agents:
            post = self.get_agent(agent_id+1).post() # 1-indexed agent IDs in self.agents
            self.posts.append(post)
            changes : list[float|None] = [None] * self.opinions
            changes[post.opinion_tendency[0]] = post.opinion_tendency[1]
            self.db.timestamp(
                step=self.step_count,
                timestamp_type=TimestampType.POST,
                source_id=agent_id+1,
                target_id_or_lie=1 if post.LIE else 0,
                post_id_or_connection_type=post.unique_id,
                opinion_change=changes,
                model=self,
                is_target=False
            )

        # 4. Propagate all posts and remove dead posts
        for post in self.posts: post.propagate(active_agents)
        self.kill_posts()

        # 5. For each fack-checker (self.fact_checked) reacting, post
        for fact_checker_id, opinion_id in self.fact_checked:
            post = self.get_agent(fact_checker_id).post_about(opinion_id)
            # print(f"Reaction by Agent {fact_checker_id}:{self.get_agent(fact_checker_id).personality} posted from opinions {[round(float(x), 3) for x in self.get_agent(fact_checker_id).opinions]}")
            self.posts.append(post)
            changes : list[float|None] = [None] * self.opinions
            changes[post.opinion_tendency[0]] = post.opinion_tendency[1]
            self.db.timestamp(
                step=self.step_count,
                timestamp_type=TimestampType.POST,
                source_id=fact_checker_id,
                target_id_or_lie=1 if post.LIE else 0,
                post_id_or_connection_type=post.unique_id,
                opinion_change=changes,
                model=self,
                is_target=False
            )

        # 6. Propagate all reaction posts and remove dead posts
        for post in self.posts: post.propagate(active_agents)
        self.kill_posts()
        self.fact_checked = []

    def kill_posts(self):
        # Kill posts
        for post in self.posts.copy():
            # print(f"Post {post.unique_id} is dead in step {self.step_count}.")
            # self.dead_posts.append(post)
            self.posts.remove(post)

    # Override get_agent to return Agent instead of BaseAgent
    def get_agent(self, agent_id:int) -> Agent:
        for agent in self.agents:
            if agent.unique_id == agent_id:
                return agent
        raise ValueError(f"Agent with ID {agent_id} not found.")

    ## Override create_agents to pass opinions parameter to Agent_v1
    def create_agents(self, n:int, *args, **kwargs):
        """Create agents for the model with parameter in agent innit self.opinions."""
        super().create_agents(n=n, opinions=self.opinions, *args, **kwargs)
    def create_bots(self, n:int, *args, **kwargs):
        """Create agents for the model with parameter in agent innit self.opinions."""
        super().create_bots(n=n, opinions=self.opinions, *args, **kwargs)

    ## Graph visualization method
    def view_graph(self, override_seed:bool = True, seed:float|None=None):
        if not override_seed:
            seed = self.seed

        pos = nx.spring_layout(self.graph, seed=seed)
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.axis("off")
        plt.show()
        # nx.draw(self.graph, with_labels=True, pos=pos)
        # plt.show()