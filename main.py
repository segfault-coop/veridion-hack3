import requests
from time import sleep
import random
import argparse
from Agents.random_agent import RandomAgent

host = ""
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

def play_game(agent, player_id):
    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']
            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = agent.action(sys_word)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player_id", type=int, required=True)
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--agent", type=str, required=True, choices=["random", "single_llm"])
    args = parser.parse_args()
    
    if args.agent == "random":
        agent = RandomAgent(args.player_id)
    elif args.agent == "single_llm":
        agent = SingleLLM(args.player_id)
    
    play_game(agent, args.player_id)

if __name__ == "__main__":
    main()