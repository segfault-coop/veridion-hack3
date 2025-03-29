class RandomAgent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.actions_costs = []``
        
    def action(self, state):
        return random.choice(self.actions_costs)