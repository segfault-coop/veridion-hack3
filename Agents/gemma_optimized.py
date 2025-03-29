from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field

class WordUsed(BaseModel):
    word: str = Field(description="The word used by the player")

class GemmaOptimized:
    def __init__(self, player_id):
        self.player_id = player_id
        # Optimize for M1 with lower temperature and shorter context
        self.llm = OllamaLLM(model="gemma3:latest", temperature=0.8)
        
        # Compact prompt with full word list
        self.prompt = """Counter this word: {word}
Round: {round}/5 | Budget: ${total_spent}

Choose ONE logical counter from:

CHEAP ($1-$3):
Feather($1), Coal($1), Pebble($1)
Leaf($2), Paper($2), Rock($2)
Water($3), Twig($3)

MID-TIER ($4-$10):
Sword($4), Shield($4)
Gun($5), Flame($5), Rope($5)
Disease($6), Cure($6), Bacteria($6)
Shadow($7), Light($7), Virus($7)
Sound($8), Time($8), Fate($8)
Earthquake($9), Storm($9), Vaccine($9)
Logic($10), Gravity($10), Robots($10)

EXPENSIVE ($11-$20):
Stone($11), Echo($11)
Thunder($12), Karma($12)
Wind($13), Ice($13), Sandstorm($13)
Laser($14), Magma($14), Peace($14)
Explosion($15), War($15), Enlightenment($15)
Nuclear Bomb($16), Volcano($16)
Whale($17), Earth($17), Moon($17)
Star($18), Tsunami($18)
Supernova($19), Antimatter($19)
Plague($20), Rebirth($20)

VERY EXPENSIVE ($21+):
Tectonic Shift($21), Gamma-Ray Burst($22)
Human Spirit($23), Apocalyptic Meteor($24)
Earth's Core($25), Neutron Star($26)
Supermassive Black Hole($35), Entropy($45)

Rules: Natural>Man-made, Energy>Matter, Cosmic>Earth

Return only the counter word:"""

    def action(self, word, last_round_history, total_spent, player_id):
        try:
            # Simplify round calculation
            round_num = min(5, (len(last_round_history.split("Words given")) or 1))
            
            # Direct string formatting
            formatted_prompt = self.prompt.format(
                word=word,
                round=round_num,
                total_spent=total_spent
            )
            
            # Direct invocation
            response = self.llm.invoke(formatted_prompt)
            
            # Simple extraction of last word
            final_word = response.strip().split()[-1].strip()
            
            # Clean any punctuation
            import re
            final_word = re.sub(r'[^\w\s]', '', final_word)
            
            # Complete valid words list
            valid_words = {
                "Feather", "Coal", "Pebble", "Leaf", "Paper", "Rock", "Water", "Twig",
                "Sword", "Shield", "Gun", "Flame", "Rope", "Disease", "Cure", "Bacteria",
                "Shadow", "Light", "Virus", "Sound", "Time", "Fate", "Earthquake", "Storm",
                "Vaccine", "Logic", "Gravity", "Robots", "Stone", "Echo", "Thunder", "Karma",
                "Wind", "Ice", "Sandstorm", "Laser", "Magma", "Peace", "Explosion", "War",
                "Enlightenment", "Nuclear", "Bomb", "Volcano", "Whale", "Earth", "Moon",
                "Star", "Tsunami", "Supernova", "Antimatter", "Plague", "Rebirth",
                "Tectonic", "Shift", "Gamma-Ray", "Burst", "Human", "Spirit", "Apocalyptic",
                "Meteor", "Earth's", "Core", "Neutron", "Supermassive", "Black", "Hole", "Entropy"
            }
            
            # Handle combined words
            word_mappings = {
                "Nuclear": "Nuclear Bomb",
                "Bomb": "Nuclear Bomb",
                "Gamma": "Gamma-Ray Burst",
                "Ray": "Gamma-Ray Burst",
                "Burst": "Gamma-Ray Burst",
                "GammaRay": "Gamma-Ray Burst",
                "Tectonic": "Tectonic Shift",
                "Shift": "Tectonic Shift",
                "Human": "Human Spirit",
                "Spirit": "Human Spirit",
                "Apocalyptic": "Apocalyptic Meteor",
                "Meteor": "Apocalyptic Meteor",
                "Earth's": "Earth's Core",
                "Core": "Earth's Core",
                "Neutron": "Neutron Star",
                "Supermassive": "Supermassive Black Hole",
                "Black": "Supermassive Black Hole",
                "Hole": "Supermassive Black Hole",
            }
            
            if final_word in word_mappings:
                final_word = word_mappings[final_word]
                
            # Special case for combined words
            special_cases = [
                "Nuclear Bomb", "Gamma-Ray Burst", "Tectonic Shift",
                "Human Spirit", "Apocalyptic Meteor", "Earth's Core",
                "Neutron Star", "Supermassive Black Hole"
            ]
            
            # Check if the response contains any of the special cases
            for case in special_cases:
                if case.lower() in response.lower():
                    return case
            
            # Round-based fallbacks
            fallbacks = ["Feather", "Coal", "Pebble", "Rock", "Water"]
            if final_word not in valid_words and final_word not in special_cases:
                return fallbacks[min(round_num-1, 4)]
                
            return final_word
            
        except Exception as e:
            print(f"Error in Gemma agent: {e}")
            return "Feather"  # Safe fallback 