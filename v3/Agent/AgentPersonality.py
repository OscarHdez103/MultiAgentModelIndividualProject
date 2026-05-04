import enum

from Agent.Weights import Weights


class AgentPersonality(enum.Enum):
    BASE = 0, # MAX_DIFFERENCE 0.4, REACTION_FACTOR 0.08, AGREE_FACTOR 1.0, DISAGREE_FACTOR 1.0, LIE_CHANCE 0.05
    EXTREMIST_LIAR = 1, # LIE_CHANCE x10 if Positive opinion making a systemic lie imbalance
    LIAR = 2, # LIE_CHANCE x10
    FACT_CHECKER = 3, # CHECK_LIES -> LIE_FOUND_FACTOR = DISAGREE_FACTOR +0.2
    REACTIVE = 4, # REACTION_FACTOR +0.04
    STUBBORN = 5, # MAX_DIFFERENCE -0.2, REACTION_FACTOR -0.02
    CONTRARIAN = 6, # AGREE_FACTOR -0.1, DISAGREE_FACTOR +0.1
    FLEXIBLE = 7 # MAX_DIFFERENCE +0.2

def get_random(a, weights:Weights) -> "AgentPersonality":
    from Agent.Agent_v1 import Agent_v1
    agent : Agent_v1 = a
    # weights : dict[AgentPersonality, float] = {
    #     AgentPersonality.BASE : 6,
    #     AgentPersonality.EXTREMIST_LIAR : 20,
    #     AgentPersonality.LIAR : 0,
    #     AgentPersonality.FACT_CHECKER : 1,
    #     AgentPersonality.REACTIVE : 2,
    #     AgentPersonality.STUBBORN : 2,
    #     AgentPersonality.CONTRARIAN : 2,
    #     AgentPersonality.FLEXIBLE : 2
    # }
    # weights : dict[AgentPersonality, float] = {
    #     AgentPersonality.BASE : 6,
    #     AgentPersonality.EXTREMIST_LIAR : 0,
    #     AgentPersonality.LIAR : 0,
    #     AgentPersonality.FACT_CHECKER : 0,
    #     AgentPersonality.REACTIVE : 0,
    #     AgentPersonality.STUBBORN : 0,
    #     AgentPersonality.CONTRARIAN : 0,
    #     AgentPersonality.FLEXIBLE : 0
    # }
    weights : dict[AgentPersonality, float] = weights.get()
    total_weight : float = sum(weights.values())
    p = [weight / total_weight for weight in weights.values()]
    return agent.random_state.choice(
        list(weights.keys()),
        p = p
    )



