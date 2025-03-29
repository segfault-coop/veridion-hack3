from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field

class WordUsed(BaseModel):
    word: str = Field(description="The word used by the player")

class StructuredLLM:
    def __init__(self, player_id):
        self.player_id = player_id
        self.llm = OllamaLLM(model="gemma3:latest", temperature=0.8)
        
        system_message = """Battle AI: Counter words efficiently. Natural > Man-made. Stronger > Weaker. Stay in budget!"""

        word_categories = """WEAPONS:
$1: Feather, Coal, Pebble
$2-$3: Rock, Water
$4-$6: Sword, Flame
$7-$10: Shadow, Storm, Logic
$11-$15: Thunder, Wind, War
$16-$20: Nuclear, Star
$35-$45: Black Hole, Entropy"""

        thought_format = """Word: {word}
Spent: ${total_spent}
R{round}/5
Choice:"""

        self.prompt = ChatPromptTemplate([
            ("system", system_message),
            ("user", word_categories + "\n" + thought_format)
        ])

    def action(self, word, last_round_history, total_spent, player_id):
        try:
            round_num = len(last_round_history.split("Round")) if last_round_history else 1
            response = self.llm.invoke(
                self.prompt.invoke({
                    "word": word,
                    "round": round_num,
                    "total_spent": total_spent
                })
            )
            final_word = response.strip().split()[-1]
            final_word = ''.join(c for c in final_word if c.isalnum() or c.isspace()).strip()
            
            valid_words = {"Feather", "Coal", "Pebble", "Rock", "Water", 
                         "Sword", "Flame", "Shadow", "Storm", "Logic",
                         "Thunder", "Wind", "War", "Nuclear", "Star",
                         "Black Hole", "Entropy"}
            
            return final_word if final_word in valid_words else "Feather"
            
        except Exception:
            return "Feather" 