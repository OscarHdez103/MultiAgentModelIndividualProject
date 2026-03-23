from LLM.guides.Opinion import Opinion

class AgentInfo:
    def __init__(self, agent_id: int, opinions: list[Opinion]):
        self.agent_id = agent_id
        self.opinions = opinions
    def __str__(self):
        return f"{{'agent_id': {self.agent_id}, 'opinions': [{', '.join([str(opinion) for opinion in self.opinions])}]}}"