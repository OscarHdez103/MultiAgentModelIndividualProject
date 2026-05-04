from Agent.AgentPersonality import AgentPersonality
from Agent.Weights import Weights


class DataVariables:
    def __init__(self,
                 SEED: int|None,
                 AGENTS: int,
                 BOTS: int,
                 opinion_size: int,
                 total_steps: int,
                 EXTREMIST_BOTS :bool,
                 weights : dict[AgentPersonality, float],
                 weight_name: Weights,
                 naming: bool = True
                 ):
        self.SEED = SEED
        self.AGENTS: int = AGENTS
        self.BOTS: int = BOTS
        self.opinion_size: int = opinion_size
        self.total_steps :int = total_steps
        self.EXTREMIST_BOTS: bool = EXTREMIST_BOTS
        self.weights: dict[AgentPersonality, float] = weights,
        self.weight_name: Weights = weight_name
        self.naming = naming

    def name(self) -> str:
        if self.naming:
            if self.EXTREMIST_BOTS:
                return f"{self.weight_name}_a-b={self.AGENTS}-{self.BOTS}_EXTREME"
            else:
                return f"{self.weight_name}_a-b={self.AGENTS}-{self.BOTS}"
        else: return ""

    def save_data(self) -> dict:
        return {
            "SEED": self.SEED,
            "AGENTS": self.AGENTS,
            "BOTS": self.BOTS,
            "opinion_size": self.opinion_size,
            "total_steps": self.total_steps,
            "EXTREMIST_BOTS": self.EXTREMIST_BOTS,
            "weight_name": str(self.weight_name),
        }

    def save_json(self) -> str:
        import json
        return json.dumps(self.save_data(), indent="\t")