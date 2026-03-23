from Agent.BaseAgent import BaseAgent
from Model.BaseModel import BaseModel


class Stats:
    def __init__(self, model:BaseModel):
        self.model :BaseModel = model

    def agents(self) -> list[BaseAgent]: return self.model.get_agents()
    def get_agents(self) -> list[int]: return [agent.unique_id for agent in self.agents()]
    def get_agent(self, agent_id:int) -> BaseAgent:
        agents = self.agents()
        for agent in agents:
            if agent.unique_id == agent_id: return agent
        raise ValueError(f"Agent with ID {agent_id} not found.")

    def states_str(self, agent_ids:list[int] = None, agents:list[BaseAgent] = None, state_ids:list[str] = None, to_print:bool = True) -> str:
        if agents is None:
            if agent_ids is None: agent_ids = self.get_agents()
            agents = [self.get_agent(agent) for agent in agent_ids]

        if state_ids is None:
            if to_print:
                for agent in agents: print(agent.full_state())
            else:
                if len(agents) == 1: return agents[0].full_state().__str__()
                return [agent.full_state() for agent in agents].__str__()
        else:
            if to_print:
                for agent in agents:
                    if len(state_ids) == 1: print(agent.state(state_ids[0]))
                    else: print([agent.state(state_id) for state_id in state_ids])
            else:
                if len(state_ids) == 1: return [agent.state(state_ids[0]) for agent in agents].__str__()
                return [[agent.state(state_id) for state_id in state_ids] for agent in agents].__str__()

        return ""
