import json
from random import seed

from mesa import Agent

from Database.Data import Data
from LLM.RequestLLM import RequestLLM
from LLM.guides.AgentInfo import AgentInfo
from LLM.guides.FriendIds import FriendIds
from LLM.guides.Opinion import Opinion
from LLM.guides.Post import PostGuide
from LLM.guides.PromptInfo import PromptInfo
from Model import *
from Model import ExampleModel, Model_v1
from Model.BaseModel import BaseModel
from Others.Stats import Stats


class Main:
    def __init__(self,
            SEED: int|None= 42,
            STEPS: int = 30,
            AGENTS: int = 100
    ):
        """Parameter initialization for the multi-agent model simulation."""
        self.SEED = SEED
        self.STEPS: int = STEPS
        self.AGENTS: int = AGENTS

    def example_model_run(self) -> str:
        """Run the ExampleModel simulation and return the final wealth distribution among agents."""
        example_model = ExampleModel.ExampleModel(n=self.AGENTS, seed=self.SEED)
        stats = Stats(example_model)
        stats.states_str()
        for i in range(self.STEPS):
            example_model.step()
            if i % 3 == 0:
                print(f"\nStep {i}:")
                stats.states_str()

        return stats.states_str(state_ids=["wealth"], to_print=False)

    def main_model(self):
        llm :RequestLLM = RequestLLM()

        opinion_size:int = 4

        # Make save_path the current directory
        save_path = "./"

        db = Data(save_path=save_path, opinion_size=opinion_size)
        main_model = Model_v1.Model_v1(llm=llm, database=db, opinions=opinion_size, n=self.AGENTS, seed=self.SEED, k=4, p=0.5)
        main_model.view_graph()
        for i in range(5):
            print(f"\nStep {i}:")
            main_model.step()

        db.save_parquet()




if __name__ == "__main__":
    # EXAMPLE MODEL RUN
    # wealth_distribution = Main().example_model_run()
    # print("Final wealth distribution among agents:", wealth_distribution)

    # PREVIOUS MODEL
    Main(SEED=42).main_model()

    # r = RequestLLM()
    # # # print(r.model)
    # # print(r.prompt)
    # # # print(r.response)
    # #
    # prompt = PromptInfo(
    #     agent_info=AgentInfo(
    #         agent_id=1,
    #         opinions=[
    #             Opinion(
    #                 opinion_id=1,
    #                 bias=0.5
    #             ),
    #             Opinion(
    #                 opinion_id=2,
    #                 bias=-0.3
    #             )
    #         ]
    #     ),
    #     friend_ids=FriendIds(
    #         friend_ids=[
    #             2,
    #             3,
    #             9
    #         ]
    #     ),
    #     post=PostGuide(
    #         source_id=9,
    #         opinion_bias=[
    #             Opinion(
    #                 opinion_id=2,
    #                 bias=0.4
    #             )
    #         ]
    #     )
    # )
    # print(prompt)
    #
    # text = r.chat(prompt)
    # # Check if correct json
    # data = json.loads(text)
    # print(data)
    # print(data["opinions_changed"])

