import pygame
from controller import detect_controller_input
from get_window_info import get_active_window_process_name
from gui import do_backmost, do_topmost, init_tkinter
from utils import get_args, update_args_by_toml

def main():
    args = get_args()
    args = update_args_by_toml(args, args.config_filename)

    joystick = init_joystick()
    (root, label) = init_tkinter()
    main_loop(root, label, joystick, args)

def init_joystick():
    if hasattr(pygame, 'init'):
        pygame.init()  # こうしないとlinterでerror
    pygame.joystick.init()

    joystick = None
    print("接続されているジョイスティック:")
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"{i}: {joystick.get_name()} - ボタン数: {joystick.get_numbuttons()}")
    return joystick

def main_loop(root, label, _joystick, args):
    timer_id_dict = {"id": None}
    clock = pygame.time.Clock()
    check_interval_msec = int(args.backmost_mode["check_interval_sec"] * 1000)
    last_check_msec = pygame.time.get_ticks()

    while True:
        check_and_do_backmost(root, args, check_interval_msec, last_check_msec)

        result = detect_controller_input()
        if result:
            show_input(root, label, result, timer_id_dict)
        root.update_idletasks()
        root.update()
        clock.tick(60)

def check_and_do_backmost(root, args, check_interval_msec, last_check_msec):
    current_msec = pygame.time.get_ticks()
    if current_msec - last_check_msec >= check_interval_msec:
        if is_playing_game(args):
            do_backmost_and_wait(root, args)
        last_check_msec = current_msec

def is_playing_game(args):
    return get_active_window_process_name() == args.backmost_mode["process_name"]

def do_backmost_and_wait(root, args):
    do_backmost(root)
    while is_playing_game(args):
        pygame.time.wait(10000)

def show_input(root, label, text, timer):
    def reset_topmost():
        do_backmost(root)

    do_topmost(root)
    label.config(text=text)
    root.update()

    if timer["id"] is not None:
        root.after_cancel(timer["id"])
    timer["id"] = root.after(1000, reset_topmost)

try:
    main()
except KeyboardInterrupt:
    print("終了")

    if hasattr(pygame, 'quit'):
        pygame.quit()  # こうしないとlinterでerror
