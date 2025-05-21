import pygame
from button_utils import load_all_configs
from button_input import create_button_states, get_buttons_as_bitstring, setup_pygame_and_joystick, shutdown_pygame
from button_mission import check_and_update_mission, get_random_mission_index
from button_print import update_display
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)
    (names, plus, lever_names, missions) = load_all_configs(args)
    mission_index = get_random_mission_index(missions)

    joystick = setup_pygame_and_joystick()
    if joystick is None:
        return

    try:
        while True:
            pygame.event.pump()

            buttons_bits = get_buttons_as_bitstring(joystick)
            lever_plus_pressed = create_button_states(names, plus, lever_names, joystick, buttons_bits)
            (mission, mission_result, mission_index) = check_and_update_mission(plus, missions, mission_index, lever_plus_pressed)
            update_display(names, mission, buttons_bits, lever_plus_pressed, mission_result)

            pygame.time.wait(100) # 16だと点滅が激しくて見づらかった
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        shutdown_pygame()

if __name__ == "__main__":
    main()
