import json, random, os, time, re
from fuzzywuzzy import fuzz

settings = {
    "ShowExample": True,      # Shows the answer before input (Lots easier)
    "ShowTips": True,          # Shows what words are missing (Medium)
    "DynamicTipLength": True,  # Makes ShowTips easier by having changing gap length
    "ShowNumberOfWords": True,

    "ShowDefinition": True,      # Shows the definition before input (Lots easier)
    "DefinitionShowTips": True,          # Shows what words are missing (Medium)
    "DefinitionDynamicTipLength": True,  # Makes DefinitionShowTips easier by having changing gap length
    "DefinitionShowNumberOfWords": True   # Shows number of words
}

if os.name == "posix":
    clear_command = "clear"
else:
    clear_command = "cls"

current_directory = os.getcwd()
subdir_path = "ChemistryFlow"
if subdir_path not in current_directory:
    os.chdir(subdir_path)

file_path = "flows.json"

with open(file_path, 'r') as file:
    flows = json.load(file)

possible_flow_paths = []
mistakes = 0
start_time = time.time()

class HandleFlow:
    @staticmethod
    def get_message(flow_path):
        return flows[flow_path["Start"]]["Flow"][flow_path["End"]]["Message"]
    
    @staticmethod
    def get_required_words(flow_path):
        return flows[flow_path["Start"]]["Flow"][flow_path["End"]]["Required Words"]

    @staticmethod
    def get_definition(flow_path):
        return flows[flow_path]["Definition"]
    
    @staticmethod
    def replace_words_ignore_case(input_string, substitute_word, replacement_word):
        compiled = re.compile(re.escape(substitute_word), re.IGNORECASE)
        res = compiled.sub(replacement_word, input_string)  
        return str(res)


for starting_compound_name, starting_compound_values in flows.items():
    for ending_compound_name in starting_compound_values["Flow"].keys():
        set_flow_path = {"Start":starting_compound_name, "End":ending_compound_name}
        possible_flow_paths.append(set_flow_path)

for names_for_definitions in flows.keys():
    possible_flow_paths.append(names_for_definitions)

random.shuffle(possible_flow_paths)

test_length = len(possible_flow_paths)

for i, flow_path in enumerate(possible_flow_paths):
    won = False
    while not won:
        if type(flow_path) == dict:
            if settings["ShowExample"]:
                os.system(clear_command)
                print(f"Reaction from {flow_path['Start']} to {flow_path['End']}. ({i + 1}/{test_length})")
                print(HandleFlow.get_message(flow_path))
                input("\nPress enter to continue...")

            os.system(clear_command)
            print(f"Write what is needed for the reaction from {flow_path['Start']} to {flow_path['End']}. ({i + 1}/{test_length})")
            if settings["ShowTips"]:
                answer = HandleFlow.get_message(flow_path)
                for word in HandleFlow.get_required_words(flow_path):
                    if settings["DynamicTipLength"]:
                        replacement_word = "_" * len(word)
                    else:
                        replacement_word = "_" * 5
                    answer = HandleFlow.replace_words_ignore_case(answer, word, replacement_word)
                print(answer)
            elif settings["ShowNumberOfWords"]:
                print(f"{len(HandleFlow.get_required_words(flow_path))} words needed.")
            user_answer = input("").lower()

            missing_words = []
            for word in HandleFlow.get_required_words(flow_path):
                if word.lower() not in user_answer:
                    missing_words.append(word)
                
            if missing_words and not "pass" in user_answer:
                mistakes += 1
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
        else:
            if settings["ShowDefinition"]:
                os.system(clear_command)
                print(f"Definition of {flow_path}. ({i + 1}/{test_length})")
                print(HandleFlow.get_definition(flow_path))
                input("\nPress enter to continue...")

            os.system(clear_command)
            print(f"Write definition of {flow_path}. ({i + 1}/{test_length})")
            answer = HandleFlow.get_definition(flow_path)
            if settings["DefinitionShowTips"]:
                if settings["DefinitionDynamicTipLength"]:
                    answer = re.sub(r'[^ ]', '_', answer)
                else:
                    answer = len(answer.split()) * ("_" * 5 + " ")
                print(answer)
            elif settings["DefinitionShowNumberOfWords"]:
                print(f"{len(answer.split())} words needed.")
            user_answer = input("").lower()

            similarity_ratio = fuzz.ratio(user_answer, HandleFlow.get_definition(flow_path).lower()) / 100

            similarity_ratio_bar = 0.95
            if similarity_ratio < similarity_ratio_bar and not "pass" in user_answer:
                mistakes += 1
                print(f"\nIncorrect. Accuracy is not close enough: {similarity_ratio}/{similarity_ratio_bar}")
                print(HandleFlow.get_definition(flow_path))
                time.sleep(0.5)
                input("\nPress enter to retry...")
                continue
            else:
                print(f"Correct! {similarity_ratio}/{similarity_ratio_bar}")
                print(HandleFlow.get_definition(flow_path))
                input("\nPress enter to continue...")
                won = True

os.system(clear_command)

end_time = time.time() - start_time
minutes, seconds = divmod(end_time, 60)

print("Completed!")
print(f"You had a total of {mistakes} mistakes in a time of {round(minutes)} minutes and {round(seconds, 2)} seconds.")