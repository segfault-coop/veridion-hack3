from agent.single_llm import SingleLLM

def main():
    p1 = SingleLLM(player_id="p1")
    p2 = SingleLLM(player_id="p2")
    
    for i in range(5):
        # Enter a word
        sys_word = input("Enter a word: ")
        p1_word = p1.action(sys_word, "", 0)
        p2_word = p2.action(sys_word, "", 0)
        
        print(f'P1 word: {p1_word}')
        print(f'P2 word: {p2_word}')
        
    pass

if __name__ == "__main__":
    main()