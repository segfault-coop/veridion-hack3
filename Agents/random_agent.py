class RandomAgent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.actions_costs = []
        self.history = {
            "word_given": [],
            "word_used": [],
            "cost": []
        }
        
    def history(self, state, word_given, word_used, cost):
        self.history["word_given"].append(word_given)
        self.history["word_used"].append(word_used)
        self.history["cost"].append(cost)
    
    def action(self, state):
        return random.choice(self.actions_costs)