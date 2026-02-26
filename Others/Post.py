from Model.BaseModel import BaseModel


class Post:
    def __init__(self, creator_id:int, model:BaseModel, opinion_tendency:list[float|None]):
        self.creator_id :int = creator_id
        self.model :BaseModel = model
        self.interacted_ids :list[int] = [creator_id]
        self.opinion_tendency :list[float] = opinion_tendency

    def propagate(self):
        """Propagate the post to direct neighbours of the interacted agents."""
        pass