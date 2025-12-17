import re

def extract_session_id(session_str : str) :
    match = re.search(r"sessions/(.*)/contexts" , session_str)
    if match:
        return match.group(1)
    return ""

def get_str_from_food_dict(food_dict : dict) -> str :
    return ', '.join([f"{int(value)} {key}" for key, value in food_dict.items() ])
if __name__ == "__main__":
    print(extract_session_id("projects/monster-rsex/agent/sessions/5ac8ef9d-aad0-3fea-fa47-05fbc908c347/contexts/ongoing-order"))
    print(get_str_from_food_dict({"burger" : 2 , "fries" : 1 , "coke" : 3}))