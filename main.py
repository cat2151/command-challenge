import pygame
from controller import detect_controller_input, init_joystick
from gui import do_backmost, do_topmost, init_tkinter
from main_check_playing_game import check_playing_game_and_do_backmost, init_timer_for_check_playing_game
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)

    _joystick = init_joystick()
    (root, label) = init_tkinter()
    main_loop(root, label, args)

def main_loop(root, label, args):
    (timer_id_dict, clock, check_interval_msec, last_check_msec) = init_timer_for_check_playing_game(args)

    while True:
        last_check_msec = check_playing_game_and_do_backmost(root, args, check_interval_msec, last_check_msec)

        result = detect_controller_input()
        if result:
            show_input(root, label, result, timer_id_dict)
        root.update_idletasks()
        root.update()
        clock.tick(60) # 60fps

def show_input(root, label, text, timer):
    do_topmost(root)
    label.config(text=text)
    root.update()

    # 入力から指定秒数後にbackmost化する用
    if timer["id"] is not None:
        root.after_cancel(timer["id"])
    timer["id"] = root.after(1000, lambda: do_backmost(root))

try:
    main()
except KeyboardInterrupt:
    print("終了")

    if hasattr(pygame, 'quit'):
        pygame.quit()  # こうしないとlinterでerror
