import json, random, os, time, re

settings = {
    "ShowExample": True,
    "ShowTips": True,
    "DynamicTipLength": True
}

current_directory = os.getcwd()
subdir_path = "ChemistryFlow"
os.chdir(subdir_path)

file_path = "flows.json"

with open(file_path, 'r') as file:
    flows = json.load(file)

possible_flow_paths = []

class HandleFlow:
    @staticmethod
    def get_message(flow_path):
        return flows[flow_path["Start"]]["Flow"][flow_path["End"]]["Message"]
    
    @staticmethod
    def get_required_words(flow_path):
        return flows[flow_path["Start"]]["Flow"][flow_path["End"]]["Required Words"]
    
    @staticmethod
    def replace_words_ignore_case(input_string, substitute_word, replacement_word):
        compiled = re.compile(re.escape(substitute_word), re.IGNORECASE)
        res = compiled.sub(replacement_word, input_string)  
        return str(res)


for starting_compound_name, starting_compound_values in flows.items():
    for ending_compound_name in starting_compound_values["Flow"].keys():
        set_flow_path = {"Start":starting_compound_name, "End":ending_compound_name}
        possible_flow_paths.append(set_flow_path)

random.shuffle(possible_flow_paths)

for flow_path in possible_flow_paths:
    won = False
    while not won:
        os.system("cls")
        print(f"Reaction between {flow_path['Start']} and {flow_path['End']}.")
        if settings["ShowExample"]:
            print(HandleFlow.get_message(flow_path))
        input("\nPress enter to continue...")

        os.system("cls")
        time.sleep(0.5)
        if settings["ShowTips"]:
            answer = HandleFlow.get_message(flow_path)
            for word in HandleFlow.get_required_words(flow_path):
                if settings["DynamicTipLength"]:
                    replacement_word = "_" * len(word)
                else:
                    replacement_word = "_" * 5
                answer = HandleFlow.replace_words_ignore_case(answer, word, replacement_word)
            print(answer)
        print(f"Write what is needed for the reaction between {flow_path['Start']} and {flow_path['End']}:")
        user_answer = input("").lower()

        missing_words = []
        for word in HandleFlow.get_required_words(flow_path):
            if word.lower() not in user_answer:
                missing_words.append(word)
            
        if missing_words:
            print("\nIncorrect. You forgot to include the following words:")
            for missing_word in missing_words:
                print(missing_word)
            time.sleep(0.5)
            input("\nPress enter to retry...")
            continue
        else:
            print("Correct!")
            input("\nPress enter to continue...")
            won = True


