from urllib.request import Request

import mesa

from Agent.BaseAgent import BaseAgent as Agent
import networkx as nx

from Agent.Weights import Weights
from Database.Data import Data
from LLM.RequestLLM import RequestLLM


class BaseModel(mesa.Model):

    def __init__(self, llm:RequestLLM, database:Data, defined_agent:type[Agent], n:int=10, bot_type:type[Agent]=None, bots:int=0, seed=None, graph: nx.Graph = None, opinions: int=-1, EXTREMIST_BOTS:bool=None, weights:Weights=None) -> None:
        super().__init__(seed=seed)
        self.personality_weights :Weights = weights
        self.db :Data = database
        self.seed = seed
        self.num_agents :int = n
        self.defined_agent :type[Agent] = defined_agent
        self.bot_type :type[Agent] = bot_type
        self.graph : nx.Graph = graph
        self.opinions :int = opinions
        self.step_count :int = 0
        self.extremist_bots:bool = EXTREMIST_BOTS
        self.create_bots(bots)
        self.create_agents(n)
        self.fact_checked :list[tuple[int,int]] = []
        # self.llm :RequestLLM = llm

    def create_agents(self, n:int, *args, **kwargs):
        self.defined_agent.create_agents(model=self, n=n, *args, **kwargs)
        # for agent in self.agents:
        #     if agent.human():
        #         print(f"Agent with ID {agent.unique_id} created")
        #     else:
        #         print(f"Bot with ID {agent.unique_id} created")
        self.log_agents(step=self.step_count)
        self.log_graph(step=self.step_count)

    def create_bots(self, n:int, *args, **kwargs):
        # print(f"Should bots be extremists? {self.extremist_bots}")
        self.bot_type.create_agents(model=self, n=n, *args, **kwargs)

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
                personality=agent.personality,
                opinion=agent.opinions,
                model=self
            )
    def log_graph(self, step:int):
        for edge in self.graph.edges():
            self.db.graph(
                step=step,
                source_id=edge[0],
                target_id=edge[1],
                model=self
            )