import mesa
from Agent.BaseAgent import BaseAgent as Agent
import networkx as nx

from Database.Data import Data


class BaseModel(mesa.Model):

    def __init__(self, database:Data, defined_agent:type[Agent], n:int=10, seed=None, graph: nx.Graph = None, opinions: int=-1):
        super().__init__(seed=seed)
        self.db = database
        self.seed = seed
        self.num_agents :int = n
        self.defined_agent :type[Agent] = defined_agent
        self.graph : nx.Graph = graph
        self.opinions = opinions
        self.current_step :int = 0
        self.create_agents(n)

    def create_agents(self, n:int, *args, **kwargs):
        self.defined_agent.create_agents(model=self, n=n, *args, **kwargs)
        self.log_agents(step=self.current_step)
        self.log_graph(step=self.current_step)

    # Undefined
    def step(self):
        self.current_step += 1
        self.log_agents(step=self.current_step)
        self.log_graph(step=self.current_step)
        pass

    def get_agents(self) -> list[Agent]:
        return [agents for agents in self.agents]

    def log_agents(self, step:int):
        for agent in self.agents:
            self.db.agent(
                step=step,
                agent_id=agent.unique_id,
                opinion=agent.opinions
            )
    def log_graph(self, step:int):
        for edge in self.graph.edges():
            self.db.graph(
                step=step,
                source_id=edge[0],
                target_id=edge[1]
            )