from mesa import Agent

import Model.ExampleModel as Model

class Main:
    def __init__(self,
            RANDOM_SEED: int|None= 42,
            STEPS: int = 30,
            AGENTS: int = 10
    ):
        """Parameter initialization for the multi-agent model simulation."""
        self.RANDOM_SEED = RANDOM_SEED
        self.STEPS: int = STEPS
        self.AGENTS: int = AGENTS

    def example_model_run(self) -> list[int]:
        """Run the ExampleModel simulation and return the final wealth distribution among agents."""
        example_model = Model.ExampleModel(n=self.AGENTS, seed=self.RANDOM_SEED)
        for _ in range(self.STEPS):
            example_model.step()

        return [a.wealth for a in example_model.agents]


if __name__ == "__main__":
    wealth_distribution = Main().example_model_run()
    print("Final wealth distribution among agents:", wealth_distribution)


