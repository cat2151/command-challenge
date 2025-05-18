import pygame
from button_utils import get_buttons_as_bitstring, get_pressed_buttons, initialize_joystick, load_all_configs, update_display
from lever import get_hat_input_as_fighting_game_notation

def main():
    if hasattr(pygame, 'init'): # こうしないとlinterエラー
        pygame.init()

    # TODO config_filename をargsから得る。そのためget_args も他projectから移植してくること。
    (names, plus, lever_names, mission_name, mission) = load_all_configs("button_challenge.toml")

    joystick = initialize_joystick()
    if joystick is None:
        return

    try:
        while True:
            pygame.event.pump()

            bitstring = get_buttons_as_bitstring(joystick)
            lever_plus_pressed = evaluate_button_states(names, plus, lever_names, joystick, bitstring)
            mission_result = check_mission_success(mission_name, mission, lever_plus_pressed)

            update_display(names, mission_name, mission, bitstring, lever_plus_pressed, mission_result)

            pygame.time.wait(100) # 16だと点滅が激しくて見づらかった
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        if hasattr(pygame, 'quit'): # こうしないとlinterエラー
            pygame.quit()

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

def check_mission_success(mission_name, mission, lever_plus_pressed):
    if mission_name and mission:
        if lever_plus_pressed == mission:
            return "green"
        else:
            return "red"

if __name__ == "__main__":
    main()
