from LLM.guides.AgentInfo import AgentInfo
from LLM.guides.FriendIds import FriendIds
from LLM.guides.Post import PostGuide

class PromptInfo:
    def __init__(self, agent_info:AgentInfo, friend_ids:FriendIds, post:PostGuide):
        self.agent_info = agent_info
        self.friend_ids = friend_ids
        self.post = post
    def __str__(self):
        return f"'agent_info': {self.agent_info}, 'friend_ids': {self.friend_ids}, 'post': {self.post}"