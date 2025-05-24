import tkinter
from button_utils import load_all_configs
from button_input import create_button_states, get_buttons_as_bitstring, setup_pygame_and_joystick, shutdown_pygame
from button_mission import check_and_update_mission, get_random_mission_index
# from button_print import print_all
from main import show_input
from main_check_playing_game import check_playing_game_and_do_backmost, init_timer_for_check_playing_game
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)
    (names, plus, lever_names, missions) = load_all_configs(args)
    mission_index = get_random_mission_index(missions)

    joystick = setup_pygame_and_joystick()
    if joystick is None:
        return

    label_count = 3
    tkinter_root, labels = init_tkinter("ボタンチャレンジ 終了はterminalでCTRL+C", "640x120", ("Arial", 20), label_count)

    (timer_id_dict, clock, check_interval_msec, last_check_msec) = init_timer_for_check_playing_game(args)
    score = 0
    old_texts = []

    try:
        while True:
            last_check_msec = check_playing_game_and_do_backmost(tkinter_root, args, check_interval_msec, last_check_msec)

            buttons_bits = get_buttons_as_bitstring(joystick)
            lever_plus_pressed = create_button_states(names, plus, lever_names, joystick, buttons_bits)
            (mission, mission_result, mission_index) = check_and_update_mission(plus, missions, mission_index, lever_plus_pressed)
            # print_all(names, mission, buttons_bits, lever_plus_pressed, mission_result)

            texts = [f"mission : {mission}", f"{lever_plus_pressed}", f"score : {score}"]
            if texts != old_texts:
                show_input(tkinter_root, labels, texts, timer_id_dict)
                if mission_result == "green":
                    score += 1
                old_texts = texts

            tkinter_root.update_idletasks()
            tkinter_root.update()

            clock.tick(60) # 60fps

    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        shutdown_pygame()

def init_tkinter(title, geometry, font, label_count):
    root = tkinter.Tk()
    root.title(title)
    root.geometry(geometry)
    labels = []
    for _ in range(label_count):
        label = tkinter.Label(root, text="", font=font)
        label.pack()
        labels.append(label)
    return root, labels

if __name__ == "__main__":
    main()
