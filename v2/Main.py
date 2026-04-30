from Agent.Weights import Weights
from Database.Data import Data
from Database.DataVariables import DataVariables
from LLM.RequestLLM import RequestLLM
from Model import Model_v1

class Main:
    def __init__(self,
                 SEED: int|None= 42,
                 # STEPS: int = 30,
                 AGENTS: int = 100,
                 BOTS: int = 20,
                 opinion_size: int = 2,
                 total_steps: int = 1000,
                 EXTREMIST_BOTS :bool = True,
                 weight_name :Weights = Weights.BASE,
                 ):
        """Parameter initialization for the multi-agent model simulation."""
        self.variables = DataVariables(
            SEED=SEED,
            AGENTS=AGENTS,
            BOTS=BOTS,
            opinion_size=opinion_size,
            total_steps=total_steps,
            EXTREMIST_BOTS=EXTREMIST_BOTS,
            weight_name=weight_name,
            weights=weight_name.get()
        )


    def main_model(self):
        llm :RequestLLM = RequestLLM()

        # Make save_path the current directory
        save_path = "./"

        db = Data(save_path=save_path, opinion_size=self.variables.opinion_size, variables=self.variables)
        main_model = Model_v1.Model_v1(
            llm=None,
            database=db,
            opinions=self.variables.opinion_size,
            n=self.variables.AGENTS,
            bots=self.variables.BOTS,
            seed=self.variables.SEED,
            k=4, p=0.5,
            EXTREMIST_BOTS=self.variables.EXTREMIST_BOTS,
            weights=self.variables.weight_name
        )
        # main_model.view_graph()
        for i in range(self.variables.total_steps):
            print(f"\nStep {i}:")
            # if i % 10 == 1: print(f"Step {i}:")
            main_model.step()

        db.save_parquet()

if __name__ == "__main__":
    agents :list[int] = [1000]
    bots :list[float] = [0, 0.1]
    weight_types :list[Weights] = [Weights.BASE, Weights.LIED, Weights.FACT]
    extremist_bots :list[bool] = [False, True]
    for agent in agents:
        for bot in bots:
            for weight_type in weight_types:
                for extremist_bot in extremist_bots:
                    if not (extremist_bot and int(agent*bot) <=0):
                        print(f"Running test for {agent}-{int(agent*bot)} Extremist Bots: {extremist_bot} Weights: {weight_type}")
                        Main(
                            SEED=42,
                            AGENTS=agent-int(agent*bot),
                            BOTS=int(agent*bot),
                            EXTREMIST_BOTS=extremist_bot,
                            weight_name=weight_type
                        ).main_model()
    # Main(SEED=None).main_model()

