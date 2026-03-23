import ollama
import json

from LLM.guides.PromptInfo import PromptInfo


def response_format_check(response) -> bool:
    # Check if the response follows the self.RESPONSE_SCHEMA manually except for integer limits
    try:
        response_json = json.loads(response)
        if "reaction" not in response_json or response_json["reaction"] not in ["positive", "negative"]:
            return False
        if "opinions_changed" not in response_json or not isinstance(response_json["opinions_changed"], list):
            return False
        for change in response_json["opinions_changed"]:
            if "opinion_id" not in change or "change" not in change:
                return False
        return True
    except json.JSONDecodeError:
        return False


class RequestLLM:
    model:str = "my-qwen"

    def __init__(self):
        path = "./LLM/guides/"
        self.prompt_guide = json.load(open(path+"prompt.json", "r"))
        self.response_guide = json.load(open(path+"response.json", "r"))

        self.basic_info :str = "You are an individual person in a social network and you have just received a post! You will have to react to it depending on what your opinions are on topics compared to the post's opinion biases."
        self.agent_info :str = "This is information about who you are, what your opinions are on different topics, who are your friends in the network, and information about the post you just received:"
        self.opinions_changed_info :str = "The opinions changed should only cover opinions changed due to the received post bias, and shouldn't always change all opinions in the post bias."
        self.response_info :str = "This is the JSON format the response output should follow:"
        self.rules_info :str = "Follow the range limits in the response and make sure to only answer following the output JSON structure. NEVER change opinions that the post doesn't have bias for, only the ones it has bias for."

        # AI generated response schema based on response_guide:
        self.RESPONSE_SCHEMA = {
            "type": "object",
            "properties": {
                "reaction": {
                    "type": "string",
                    "enum": ["positive", "negative"]
                },
                "opinions_changed": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "opinion_id": {"type": "integer"},
                            "change": {
                                "type": "number",
                                "minimum": 0.0,
                                "maximum": 0.2
                            }
                        },
                        "required": ["opinion_id", "change"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["reaction", "opinions_changed"],
            "additionalProperties": False
        }

        self.max_reps = 3
    def full_message(self, prompt_info:PromptInfo) -> str:
        return f"""{self.basic_info}\n{self.agent_info}\n{str(prompt_info)}\n{self.opinions_changed_info}\n{self.response_info}\n{self.response_guide}\n{self.rules_info}"""

    def chat(self, prompt_info:PromptInfo, repetitions:int =0):
        full_message = self.full_message(prompt_info)
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'system', 'content': 'Return only valid JSON. No extra text.'},
                {'role': 'user', 'content': full_message}
            ],
            format=self.RESPONSE_SCHEMA,
            options={"temperature":0.2}
        )
        result = response['message']['content'] if response_format_check(response['message']['content']) else None
        if result is None:
            if repetitions < self.max_reps:
                print("Failed to get valid response, retrying... Attempt number:", repetitions+1)
                self.chat(prompt_info=prompt_info, repetitions=repetitions+1)
            else:
                raise ValueError(f"Failed to get valid response after {self.max_reps} attempts. Last response: {response['message']['content']}")
        return result



