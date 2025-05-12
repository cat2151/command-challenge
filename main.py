import pygame
from controller import detect_controller_input
from gui import do_backmost, do_topmost, init_tkinter

def main():
    joystick = init_joystick()
    (root, label) = init_tkinter()
    main_loop(root, label, joystick)

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

def main_loop(root, label, _joystick):
    timer_id_dict = {"id": None}
    clock = pygame.time.Clock()
    while True:
        result = detect_controller_input()
        if result:
            show_input(root, label, result, timer_id_dict)
        root.update_idletasks()
        root.update()
        clock.tick(60)

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
