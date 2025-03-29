import requests
from time import sleep
import random
import argparse
from agents.random_agent import RandomAgent
from agents.single_llm import SingleLLM
import json
host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

p1_history = {
    "word_given": [],
    "word_used": [],
    "cost": [],
    "total_spent": 0,
    "wins": []
}

p2_history = {
    "word_given": [],
    "word_used": [],
    "cost": [],
    "total_spent": 0,
    "wins": []
}
# Load the word list
word_list = []
with open("data/cost.json", "r") as f:
    word_list = json.load(f)

def play_game(agent, player_id):
    for round_id in range(1, NUM_ROUNDS+1):
        print(f'******* Round {round_id} ***********')
        round_num = -1
        
        while round_num != round_id:
            response = requests.get(get_url)
            sys_word = response.json()['word']
            round_num = response.json()['round']
            print(response.json())
            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            status = status.json()['status']
            p1_history["word_given"].append(status['system_word'])
            p1_history["cost"].append(status["p1_word_cost"])
            p1_history["total_spent"] = status["p1_total_cost"]
            p1_history["word_used"].append(status["p1_word"])
            p1_history["total_spent"] = status["p1_total_cost"]
            p1_history["wins"].append(status["p1_won"])
            
            p2_history["word_given"].append(status['system_word'])
            p2_history["cost"].append(status["p2_word_cost"])
            p2_history["total_spent"] = status["p2_total_cost"]
            p2_history["word_used"].append(status["p2_word"])
            p2_history["total_spent"] = status["p2_total_cost"]
            p2_history["wins"].append(status["p2_won"])
            
            print(f'P1 history: {p1_history}')
            print(f'P2 history: {p2_history}')
            
            print(status.json())
            
        total_history = f'P1 history: {p1_history}\nP2 history: {p2_history}'
        print(f'System word: {sys_word}')
        if player_id == "p1":
            total_spent = p1_history["total_spent"]
        else:
            total_spent = p2_history["total_spent"]
            
        choosen_word = agent.action(sys_word, total_history, total_spent, player_id)
        print(f'Choosen word: {choosen_word}')
        choosen_word = choosen_word.strip()
        word_id = int(word_list[choosen_word]["id"])
        choosen_word_cost = word_list[choosen_word]["cost"]
        total_spent += choosen_word_cost
        
        print(f'Word id: {word_id}')
        print(f'Word cost: {choosen_word_cost}')
        
        data = {"player_id": player_id, "word_id": word_id, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(f'Round {round_id} response: {response.json()}')
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_id", type=str, required=True)
    parser.add_argument("--agent", type=str, required=True, choices=["random", "single_llm"])
    parser.add_argument("--player_type", type=str, required=True, choices=["p1", "p2"])
    args = parser.parse_args()
    
    if args.agent == "random":
        agent = RandomAgent(args.player_id)
    elif args.agent == "single_llm":
        agent = SingleLLM(args.player_id)
    
    play_game(agent, args.player_id)

if __name__ == "__main__":
    main()