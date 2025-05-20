import random
import pygame
from button_utils import get_buttons_as_bitstring, get_pressed_buttons, initialize_joystick, load_all_configs, update_display
from lever import get_hat_input_as_fighting_game_notation
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)
    (names, plus, lever_names) = load_all_configs(args)
    missions = args.missions
    mission_index = get_random_mission_index(missions)

    if hasattr(pygame, 'init'): # こうしないとlinterエラー
        pygame.init()
    joystick = initialize_joystick()
    if joystick is None:
        return

    try:
        while True:
            pygame.event.pump()

            bitstring = get_buttons_as_bitstring(joystick)
            lever_plus_pressed = evaluate_button_states(names, plus, lever_names, joystick, bitstring)

            mission = missions[mission_index]["input"]
            mission_result = check_mission_success(mission, lever_plus_pressed, plus)
            if mission_result == "green":
                mission_index = get_random_mission_index(missions)

            update_display(names, mission, bitstring, lever_plus_pressed, mission_result)

            pygame.time.wait(100) # 16だと点滅が激しくて見づらかった
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        if hasattr(pygame, 'quit'): # こうしないとlinterエラー
            pygame.quit()

def get_random_mission_index(missions):
    mission_index = random.randint(0, len(missions) - 1)
    return mission_index

def evaluate_button_states(names, plus, lever_names, joystick, bitstring):
    lever = get_hat_input_as_fighting_game_notation(joystick, lever_names)
    if lever == lever_names[4]: # ニュートラルの場合は表示なし。なぜなら「ニュートラル+A+B」はわかりづらいと感じた。今後見直す可能性あり。
        lever = None
    pressed = get_pressed_buttons(names, bitstring, plus)
    lever_plus_pressed = "なし"
    if lever and pressed:
        lever_plus_pressed = f"{lever}{plus}{pressed}"
    elif lever:
        lever_plus_pressed = f"{lever}"
    elif pressed:
        lever_plus_pressed = f"{pressed}"
    return lever_plus_pressed

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

if __name__ == "__main__":
    main()
