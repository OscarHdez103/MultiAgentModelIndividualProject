import mesa


class BaseAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.seed :int = self.model.seed

    # Undefined
    def full_state(self) -> dict[str, object]:
        pass

    # Semi-undefined
    def state(self, state_id:str) -> float|list[float]:
        raise ValueError(f"State ID {state_id} not recognized.")