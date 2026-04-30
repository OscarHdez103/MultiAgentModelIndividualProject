from datetime import datetime

import pandas as pd
import os

from Agent.AgentPersonality import AgentPersonality
from Database.DataVariables import DataVariables
from Database.TimestampType import TimestampType


def empty_check(db) -> bool:
    if len(db) == 0:
        return True
    return False


class Data:
    class _Timestamp:
        step :int
        timestamp_type :str
        source :int
        target_or_lie :int
        post_id_or_connection_type :int
        opinion :list[float|None]
        def __init__(self, step:int, timestamp_type:str, source:int, target_or_lie:int, post_id_or_connection_type:int, opinion:list[float|None]):
            self.step = step
            self.timestamp_type = timestamp_type
            self.source = source
            self.target_or_lie = target_or_lie
            self.post_id_or_connection_type = post_id_or_connection_type
            self.opinion = opinion
    class _Agent:
        step :int
        agent_id :int
        personality :str
        opinion :list[float]
        def __init__(self, step:int, agent_id:int, personality:AgentPersonality, opinion:list[float]):
            self.step = step
            self.agent_id = agent_id
            self.personality = personality.name
            self.opinion = opinion
    class _Graph:
        step :int
        source_id :int
        target_id :int
        def __init__(self, step:int, source_id:int, target_id:int):
            self.step = step
            self.source_id = source_id
            self.target_id = target_id

    def __init__(self, save_path, opinion_size:int, variables:DataVariables):
        self.save_path = save_path
        self.opinion_size :int = opinion_size
        self.variables = variables

        """
        Timestamp types and data:
        - type=Post ->          creator_id  :int, lie?      :int, post_id   :int, opinion_tendency      :list[float|None]
        - type=Interaction ->   source_id   :int, target_id :int, post_id   :int, opinion_change        :list[float|None]
        - type=Connection ->    source_id   :int, target_id :int, +/-       :int, opinion_difference    :list[float|None]
        """
        self.timestamp_db : list[Data._Timestamp] = []

        """
        Agent database data:
        - step      :int
        - agent_id  :int
        - personality :str
        - opinions  :list[float]
        """
        self.agents_db : list[Data._Agent] = []

        """
        Graph database data:
        - step      :int
        - source_id :int
        - target_id :int
        """
        self.graphs_db : list[Data._Graph] = []

    def timestamp(self, step:int, timestamp_type:TimestampType, source_id:int, target_id_or_lie:int, post_id_or_connection_type:int, opinion_change:list[float|None], model, is_target:bool):
        if len(opinion_change) != self.opinion_size:
            raise ValueError(f"Opinion change list must be of size {self.opinion_size}, got {len(opinion_change)}")
        self.timestamp_db.append(
            Data._Timestamp(
                step=step,
                timestamp_type=timestamp_type.name,
                source=self.bot_id(source_id, model),
                target_or_lie=self.bot_id(target_id_or_lie, model) if is_target else target_id_or_lie,
                post_id_or_connection_type=post_id_or_connection_type,
                opinion=list(opinion_change)
            )
        )
    def agent(self, step:int, agent_id:int, personality:AgentPersonality, opinion:list[float], model):
        if len(opinion) != self.opinion_size:
            raise ValueError(f"Opinion list must be of size {self.opinion_size}, got {len(opinion)}")
        self.agents_db.append(
            Data._Agent(
                step=step,
                agent_id=self.bot_id(agent_id, model),
                personality=personality,
                opinion=list(opinion)
            )
        )
    def graph(self, step:int, source_id:int, target_id:int, model):
        self.graphs_db.append(
            Data._Graph(
                step=step,
                source_id=self.bot_id(source_id+1, model),
                target_id=self.bot_id(target_id+1, model)
            )
        )

    def bot_id(self, agent_id:int, model) -> int:
        # agent_id is 1-indexed
        # return agent_id
        from Agent.Agent_v1_bot import Agent_v1_Bot

        agent = model.get_agent(agent_id)

        if isinstance(agent, Agent_v1_Bot): return -agent_id
        else: return agent_id

    def save_parquet(self):
        if not os.path.exists(f"{self.save_path}/Data"):
            os.makedirs(f"{self.save_path}/Data")

        run_path = self.data_name(f"{self.save_path}/Data")
        if not empty_check(self.timestamp_db):
            timestamp_df = pd.DataFrame(self.opinions_df(self.timestamp_db))
            timestamp_df.to_parquet(f"{run_path}/timestamp.parquet")
        if not empty_check(self.agents_db):
            agent_df = pd.DataFrame(self.opinions_df(self.agents_db))
            agent_df.to_parquet(f"{run_path}/agents.parquet")
        if not empty_check(self.graphs_db):
            graph_df = pd.DataFrame([vars(graph) for graph in self.graphs_db])
            graph_df.to_parquet(f"{run_path}/graph.parquet")

        # Save variables.json
        with open(f"{run_path}/variables.json", "w") as f:
            f.write(self.variables.save_json())

    def opinions_df(self, db):
        # To list of dicts from db
        pre_df = [vars(individual) for individual in db]

        # Expand opinion list into opinion_0, opinion_1, ... columns, and remove the original opinion column
        for i in range(self.opinion_size):
            pre_df = [{**individual, f"opinion_{i}": individual["opinion"][i]} for individual in pre_df]
        return [{k: v for k, v in individual.items() if k != "opinion"} for individual in pre_df]

    def data_name(self, data_path:str) -> str:
        counted_folders :int = len([name for name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, name))])
        current_date :str = datetime.now().strftime("%Y-%m-%d")
        name :str = f"data_{counted_folders}_{current_date}{f"_{self.variables.name()}" if self.variables.name() != "" else ""}"
        path :str = os.path.join(data_path, name)
        os.makedirs(path)
        return path



