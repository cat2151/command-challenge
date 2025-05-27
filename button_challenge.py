import tkinter
from button_utils import load_all_configs
from button_input import create_button_states, get_buttons_as_bitstring, setup_pygame_and_joystick, shutdown_pygame
from button_mission import check_and_update_mission, get_new_mission_index
from main import show_input
from main_check_playing_game import check_playing_game_and_do_backmost, init_timer_for_check_playing_game
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)
    (names, plus, lever_names, missions) = load_all_configs(args)

    missions_set = set(mission["input"] for mission in missions)
    success_missions = set()
    mission_index = get_new_mission_index(missions, missions_set)

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

            # input
            buttons_bits = get_buttons_as_bitstring(joystick)
            lever_plus_pressed = create_button_states(names, plus, lever_names, joystick, buttons_bits)

            # check
            (mission, mission_index, missions_set, success_missions, score) = check_and_update_mission(plus, missions, mission_index, lever_plus_pressed, missions_set, success_missions, score)

            # display
            old_texts = update_display_with_mission(tkinter_root, labels, timer_id_dict, score, old_texts, lever_plus_pressed, mission)
            tkinter_root.update_idletasks()
            tkinter_root.update()

            clock.tick(60) # 60fps

    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        shutdown_pygame()

def update_display_with_mission(tkinter_root, labels, timer_id_dict, score, old_texts, lever_plus_pressed, mission):
    texts = [f"mission : {mission}", f"{lever_plus_pressed}", f"score : {score}"]
    if texts != old_texts:
        show_input(tkinter_root, labels, texts, timer_id_dict)
        old_texts = texts
    return old_texts

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
