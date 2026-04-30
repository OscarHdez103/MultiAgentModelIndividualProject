import enum

class Weights(enum.Enum):
    BASE = 1,
    LIED = 2,
    FACT = 3

    def __str__(self):
        if self == Weights.BASE:
            return "Base"
        elif self == Weights.LIED:
            return "Lied"
        elif self == Weights.FACT:
            return "Fact"
        else:
            raise ValueError(f"Invalid weight name: {self}")

    def get(self) -> dict:
        from Agent.AgentPersonality import AgentPersonality
        base_weights: dict[AgentPersonality, float] = {
            AgentPersonality.BASE: 1,
            AgentPersonality.EXTREMIST_LIAR: 0,
            AgentPersonality.LIAR: 0,
            AgentPersonality.FACT_CHECKER: 0,
            AgentPersonality.REACTIVE: 0,
            AgentPersonality.STUBBORN: 0,
            AgentPersonality.CONTRARIAN: 0,
            AgentPersonality.FLEXIBLE: 0
        }
        lied_weights: dict[AgentPersonality, float] = {
            AgentPersonality.BASE: 3,
            AgentPersonality.EXTREMIST_LIAR: 0,
            AgentPersonality.LIAR: 3,
            AgentPersonality.FACT_CHECKER: 1,
            AgentPersonality.REACTIVE: 0,
            AgentPersonality.STUBBORN: 0,
            AgentPersonality.CONTRARIAN: 0,
            AgentPersonality.FLEXIBLE: 0
        }
        fact_weights: dict[AgentPersonality, float] = {
            AgentPersonality.BASE: 1,
            AgentPersonality.EXTREMIST_LIAR: 0,
            AgentPersonality.LIAR: 1,
            AgentPersonality.FACT_CHECKER: 1,
            AgentPersonality.REACTIVE: 0,
            AgentPersonality.STUBBORN: 0,
            AgentPersonality.CONTRARIAN: 0,
            AgentPersonality.FLEXIBLE: 0
        }
        weights: dict[AgentPersonality, float]
        if self == Weights.BASE:
            weights = base_weights
        elif self == Weights.LIED:
            weights = lied_weights
        elif self == Weights.FACT:
            weights = fact_weights
        else:
            raise ValueError(f"Invalid weight name: {self}")

        return weights