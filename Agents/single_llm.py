from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field

class WordUsed(BaseModel):
    word: str = Field(description="The word used by the player")

class SingleLLM:
    def __init__(self, player_id):
        self.player_id = player_id
        self.llm = OllamaLLM(model="gemma3:latest", temperature=0.7)
        self.actions_costs = []
        system_prompt = """You're playing a strategy game where you must counter system-generated words while minimizing costs over 5 rounds.
Rules:
1. System provides a word each round
2. Choose a word from the list that logically "beats" the system's word (the system's word is not in the list)
3. Words have costs ($) - stronger words cost more
4. Failed counters incur a $30 penalty plus the word's cost
5. Goal: Spend as little as possible across 5 rounds

Word List and Costs:
1. Feather ($1)
2. Coal ($1)
3. Pebble ($1)
4. Leaf ($2)
5. Paper ($2)
6. Rock ($2)
7. Water ($3)
8. Twig ($3)
9. Sword ($4)
10. Shield ($4)
11. Gun ($5)
12. Flame ($5)
13. Rope ($5)
14. Disease ($6)
15. Cure ($6)
16. Bacteria ($6)
17. Shadow ($7)
18. Light ($7)
19. Virus ($7)
20. Sound ($8)
21. Time ($8)
22. Fate ($8)
23. Earthquake ($9)
24. Storm ($9)
25. Vaccine ($9)
26. Logic ($10)
27. Gravity ($10)
28. Robots ($10)
29. Stone ($11)
30. Echo ($11)
31. Thunder ($12)
32. Karma ($12)
33. Wind ($13)
34. Ice ($13)
35. Sandstorm ($13)
36. Laser ($14)
37. Magma ($14)
38. Peace ($14)
39. Explosion ($15)
40. War ($15)
41. Enlightenment ($15)
42. Nuclear Bomb ($16)
43. Volcano ($16)
44. Whale ($17)
45. Earth ($17)
46. Moon ($17)
47. Star ($18)
48. Tsunami ($18)
49. Supernova ($19)
50. Antimatter ($19)
51. Plague ($20)
52. Rebirth ($20)
53. Tectonic Shift ($21)
54. Gamma-Ray Burst ($22)
55. Human Spirit ($23)
56. Apocalyptic Meteor ($24)
57. Earth's Core ($25)
58. Neutron Star ($26)
59. Supermassive Black Hole ($35)
60. Entropy ($45)

You are player {player_id}
Last round history:
{last_round_history}
Total spent: {total_spent} ,  you try to spend as less as possible.
Given word: {word}
Return only the word from the word list that beats the given word in this format: word
"""
        self.prompt = ChatPromptTemplate.from_template(
            system_prompt
        )

    def action(self, word, last_round_history, total_spent, player_id):
        response = self.llm.invoke(self.prompt.format(word=word, last_round_history=last_round_history, total_spent=total_spent, player_id=player_id))
        return response
