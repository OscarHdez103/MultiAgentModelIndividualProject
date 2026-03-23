class Opinion:
    def __init__(self, opinion_id: int, bias: float):
        self.opinion_id = opinion_id
        if bias < -1 or bias > 1: raise ValueError(f"Bias must be between -1 and 1, got {bias}")
        self.bias = bias
    def __str__(self):
        return "{'opinion_id': " + str(self.opinion_id) + ", 'bias': " + str(self.bias) + "}"