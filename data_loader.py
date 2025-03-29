import json

def action_costs(json_file_path: str = "data/cost.json") -> dict:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    cost_dict = {}
    for item_name, item_data in data.items():
        cost_dict[item_name] = {"id": item_data["id"], "cost": item_data["cost"]}
    
    return cost_dict
