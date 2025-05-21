
import random

def check_and_update_mission(plus, missions, mission_index, lever_plus_pressed):
    mission = missions[mission_index]["input"]
    mission_result = check_mission_success(mission, lever_plus_pressed, plus)
    if mission_result == "green":
        mission_index = get_random_mission_index(missions)
    return mission, mission_result, mission_index

def check_mission_success(mission, lever_plus_pressed, plus):
    formated_mission = format_mission_string(mission, plus)
    formated_lever_plus_pressed = format_mission_string(lever_plus_pressed, plus)

    # print(f"mission: {formated_mission}, lever_plus_pressed: {formated_lever_plus_pressed}")
    if formated_lever_plus_pressed == formated_mission:
        return "green"
    return "red"

def format_mission_string(mission, plus):
    tokens = mission.split(plus)
    trimmed = [x.strip() for x in tokens]
    sorted_tokens = sorted(trimmed)
    combined = plus.join(sorted_tokens)
    return combined

def get_random_mission_index(missions):
    mission_index = random.randint(0, len(missions) - 1)
    return mission_index
