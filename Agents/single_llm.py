from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel

class WordUsed(BaseModel):
    word: str = Field(description="The word used by the player")

class SingleLLM:
    def __init__(self, player_id):
        self.player_id = player_id
        self.llm = OllamaLLM(model="llama3.1:8b")
        self.actions_costs = []
        self.prompt = ChatPromptTemplate.from_template(
            "You are a helpful assistant. You are given a question and you need to answer it."
        )

    def action(self, state):
        response = self.llm.invoke(self.prompt.format(state=state))
        return response
