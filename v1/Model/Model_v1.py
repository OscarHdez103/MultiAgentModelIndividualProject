import networkx as nx
import numpy as np
from networkx.generators.random_graphs import watts_strogatz_graph

from Agent.Agent_v1 import Agent_v1 as Agent
from Database.Data import Data
from Database.TimestampType import TimestampType
from LLM.RequestLLM import RequestLLM
from Model.BaseModel import BaseModel
import matplotlib.pyplot as plt

from Others.Post import Post


class Model_v1(BaseModel):

    def __init__(self, llm:RequestLLM, database:Data, opinions:int, k:int, p:float, n:int=10, seed:float|None=None):
        super().__init__(llm=llm, database=database, defined_agent=Agent, n=n, seed=seed, graph=watts_strogatz_graph(n=n, k=k, p=p, seed=seed), opinions=opinions)
        # Choose one random agent
        self.active_rng = np.random.default_rng(seed)
        self.posts :list[Post] = []
        self.dead_posts :list[Post] = []

        pass

    def step(self):
        """Process one step for all agents in the model."""
        # Call BaseModel step to increment step counter and log agents
        super().step()

        ## First version of step where the active users are simply chosen randomly from step

        # # Select random subset of agents to be considered active and append self.active_agents with them
        # # GAUSSIAN DISTRIBUTION
        # # mean = (len(self.agents) + 1) / 2
        # # std = (len(self.agents)) / 6
        # # num_agents = int(self.random.gauss(mean, std))
        # # num_agents = max(1, min(num_agents, len(self.agents)))
        #
        # # UNIFORM DISTRIBUTION
        # num_agents = self.random.randint(1, len(self.agents) + 1)
        #
        # # Subset selection based on activity weights
        # activity_weights = np.array([agent.activity for agent in self.agents])
        # activity_weights = activity_weights / activity_weights.sum()
        # selected_indices = self.active_rng.choice(len(self.agents), size=num_agents, replace=False, p=activity_weights )
        # agents_to_step: AgentSet = AgentSet([self.get_agent(i) for i in selected_indices])
        #
        # print(f"Active agents in this step: {len(agents_to_step)}/{num_agents}")
        # agents_to_step.shuffle_do("step")

        ## TODO: Implement the post version of the step
        # 1. Select random subset of active agents based on their activity levels
        # activity_weights = np.array([agent.activity for agent in self.agents])
        activity_weights = np.array([0.5 for _ in self.agents])
        activity_weights = activity_weights / activity_weights.sum()
        num_agents = self.random.randint(1, len(self.agents) + 1)

        active_agents :list[int] = self.active_rng.choice(len(self.agents), size=num_agents, replace=False, p=activity_weights) # 0-indexed

        # 2. Select random subset of posting agents from active agents based on their privacy levels and a posting chance
        POSTING_CHANCE :float = 0.3
        # posting_agents :list[int] = [
        #     agent_id for agent_id in active_agents
        #     if self.random.random() < POSTING_CHANCE * self.get_agent(agent_id+1).privacy # 1-indexed agent IDs in self.agents
        # ]
        posting_agents: list[int] = [
            agent_id for agent_id in active_agents
            if self.random.random() < POSTING_CHANCE # 1-indexed agent IDs in self.agents
        ]

        # 3. For each posting agent, create a post
        for agent_id in posting_agents:
            post = self.get_agent(agent_id+1).post() # 1-indexed agent IDs in self.agents
            self.posts.append(post)
            self.db.timestamp(
                step=self.step_count,
                timestamp_type=TimestampType.POST,
                source_id=agent_id+1,
                target_id=-1,
                post_id_or_connection_type=post.unique_id,
                opinion_change=post.opinion_tendency
            )

        # 4. Propagate all posts and remove dead posts
        for post in self.posts: post.propagate(active_agents)
        self.kill_posts()

    def kill_posts(self):
        # Kill posts
        for post in self.posts.copy():
            if post.is_dead():
                # print(f"Post {post.unique_id} is dead in step {self.step_count}.")
                self.dead_posts.append(post)
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