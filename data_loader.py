import json

def action_costs(json_file_path: str = "data/cost.json") -> dict:

    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    cost = {}
    for item_data in data.values():
        cost[item_data["text"]] = item_data["cost"]
    
    return cost

