from urllib.request import Request

import mesa
from Agent.BaseAgent import BaseAgent as Agent
import networkx as nx

from Database.Data import Data
from LLM.RequestLLM import RequestLLM


class BaseModel(mesa.Model):

    def __init__(self, llm:RequestLLM, database:Data, defined_agent:type[Agent], n:int=10, seed=None, graph: nx.Graph = None, opinions: int=-1):
        super().__init__(seed=seed)
        self.db = database
        self.seed = seed
        self.num_agents :int = n
        self.defined_agent :type[Agent] = defined_agent
        self.graph : nx.Graph = graph
        self.opinions = opinions
        self.step_count :int = 0
        self.create_agents(n)
        self.llm :RequestLLM = llm

    def create_agents(self, n:int, *args, **kwargs):
        self.defined_agent.create_agents(model=self, n=n, *args, **kwargs)
        self.log_agents(step=self.step_count)
        self.log_graph(step=self.step_count)

    # Undefined
    def step(self):
        self.step_count += 1
        self.log_agents(step=self.step_count)
        self.log_graph(step=self.step_count)
        pass

    def get_agents(self) -> list[Agent]:
        return [agents for agents in self.agents]
    def get_agent(self, agent_id:int) -> Agent:
        for agent in self.agents:
            if agent.unique_id == agent_id:
                return agent
        raise ValueError(f"Agent with ID {agent_id} not found.")

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