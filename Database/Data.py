import pandas as pd
import os

from Database.TimestampType import TimestampType


def empty_check(db) -> bool:
    if len(db) == 0:
        return True
    return False


class Data:
    class _Timestamp:
        step :int
        timestamp_type :TimestampType
        source :int
        target :int
        post_id_or_connection_type :int
        opinion :list[float|None]
        def __init__(self, step:int, timestamp_type:TimestampType, source:int, target:int, post_id_or_connection_type:int, opinion:list[float|None]):
            self.step = step
            self.timestamp_type = timestamp_type
            self.source = source
            self.target = target
            self.post_id_or_connection_type = post_id_or_connection_type
            self.opinion = opinion
    class _Agent:
        step :int
        agent_id :int
        opinion :list[float]
        def __init__(self, step:int, agent_id:int, opinion:list[float]):
            self.step = step
            self.agent_id = agent_id
            self.opinion = opinion
    class _Graph:
        step :int
        source_id :int
        target_id :int
        def __init__(self, step:int, source_id:int, target_id:int):
            self.step = step
            self.source_id = source_id
            self.target_id = target_id

    def __init__(self, save_path, opinion_size:int):
        self.save_path = save_path
        self.opinion_size :int = opinion_size

        """
        Timestamp types and data:
        - type=Post ->          creator_id  :int, ()        :int, post_id   :int, opinion_tendency      :list[float|None]
        - type=Interaction ->   source_id   :int, target_id :int, post_id   :int, opinion_change        :list[float|None]
        - type=Connection ->    source_id   :int, target_id :int, +/-       :int, opinion_difference    :list[float|None]
        """
        self.timestamp_db : list[Data._Timestamp] = []

        """
        Agent database data:
        - step      :int
        - agent_id  :int
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

    def timestamp(self, step:int, timestamp_type:TimestampType, source_id:int, target_id:int, post_id_or_connection_type:int, opinion_change:list[float|None]):
        if len(opinion_change) != self.opinion_size:
            raise ValueError(f"Opinion change list must be of size {self.opinion_size}, got {len(opinion_change)}")
        self.timestamp_db.append(
            Data._Timestamp(
                step=step,
                timestamp_type=timestamp_type,
                source=source_id,
                target=target_id,
                post_id_or_connection_type=post_id_or_connection_type,
                opinion=opinion_change
            )
        )
    def agent(self, step:int, agent_id:int, opinion:list[float]):
        if len(opinion) != self.opinion_size:
            raise ValueError(f"Opinion list must be of size {self.opinion_size}, got {len(opinion)}")
        self.agents_db.append(
            Data._Agent(
                step=step,
                agent_id=agent_id,
                opinion=opinion
            )
        )
    def graph(self, step:int, source_id:int, target_id:int):
        self.graphs_db.append(
            Data._Graph(
                step=step,
                source_id=source_id,
                target_id=target_id
            )
        )

    def save_parquet(self):
        # Create /Data directory if it doesn't exist
        if not os.path.exists(f"{self.save_path}/Data"):
            os.makedirs(f"{self.save_path}/Data")
        if not empty_check(self.timestamp_db):
            timestamp_df = pd.DataFrame(self.opinions_df(self.timestamp_db))
            timestamp_df.to_parquet(f"{self.save_path}/Data/timestamp.parquet")
        if not empty_check(self.agents_db):
            agent_df = pd.DataFrame(self.opinions_df(self.agents_db))
            agent_df.to_parquet(f"{self.save_path}/Data/agents.parquet")
        if not empty_check(self.graphs_db):
            graph_df = pd.DataFrame([vars(graph) for graph in self.graphs_db])
            graph_df.to_parquet(f"{self.save_path}/Data/graph.parquet")

    def opinions_df(self, db):
        # To list of dicts from db
        pre_df = [vars(individual) for individual in db]

        # Expand opinion list into opinion_0, opinion_1, ... columns, and remove the original opinion column
        for i in range(self.opinion_size):
            pre_df = [{**individual, f"opinion_{i}": individual["opinion"][i]} for individual in pre_df]
        return [{k: v for k, v in individual.items() if k != "opinion"} for individual in pre_df]



