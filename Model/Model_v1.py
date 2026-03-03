import networkx as nx
import numpy as np
from mesa.agent import AgentSet
from networkx.generators.random_graphs import watts_strogatz_graph

from Agent.Agent_v1 import Agent_v1 as Agent
from Database.Data import Data
from Model.BaseModel import BaseModel
import matplotlib.pyplot as plt


class Model_v1(BaseModel):

    def __init__(self, database:Data, opinions:int, k:int, p:float, n:int=10, seed:float|None=None):
        super().__init__(database=database, defined_agent=Agent, n=n, seed=seed, graph=watts_strogatz_graph(n=n, k=k, p=p, seed=seed), opinions=opinions)
        # Choose one random agent
        self.active_rng = np.random.default_rng(seed)

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
        # agents_to_step: AgentSet = AgentSet([self.agents[i] for i in selected_indices])
        #
        # print(f"Active agents in this step: {len(agents_to_step)}/{num_agents}")
        # agents_to_step.shuffle_do("step")
        pass

        ## TODO: Implement the post version of the step

        pass

    def create_agents(self, n:int, *args, **kwargs):
        """Create agents for the model with parameter in agent innit self.opinions."""
        super().create_agents(n=n, opinions=self.opinions, *args, **kwargs)

    def view_graph(self, override_seed:bool = True, seed:float|None=None):
        # From self.graph draw the graph using matplotlib
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