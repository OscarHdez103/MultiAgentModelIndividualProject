from LLM.guides.Opinion import Opinion

class PostGuide:
    def __init__(self, source_id: int, opinion_bias: list[Opinion]):
        self.source_id = source_id
        self.opinion_bias = opinion_bias
    def __str__(self):
        return f"{{'source_id': {self.source_id}, 'opinion_bias': [{', '.join([str(opinion) for opinion in self.opinion_bias])}]}}"