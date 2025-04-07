import tkinter as tk
import pygame
from controller import detect_controller_input

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

def show_jump_notification(root, label, text, timer):
    def reset_topmost():
        do_backmost(root)

    do_topmost(root)
    label.config(text=text)
    root.update()

    if timer["id"] is not None:
        root.after_cancel(timer["id"])
    timer["id"] = root.after(1000, reset_topmost)

def do_topmost(root):
    root.attributes("-topmost", True)
    root.update()

def do_backmost(root):
    root.attributes("-topmost", False)
    root.lower()
    root.update()

def main_loop(root, label, _joystick):
    timer = {"id": None}  # タイマーIDを管理する辞書
    while True:
        result = detect_controller_input()
        if result:
            show_jump_notification(root, label, result, timer)
        root.update_idletasks()
        root.update()

def init_tkinter():
    root = tk.Tk()
    root.title("ジャンプ通知 終了はterminalでCTRL+C")
    root.geometry("800x100")
    label = tk.Label(root, text="", font=("Arial", 24))
    label.pack()
    return root, label

def main():
    joystick = init_joystick()
    (root, label) = init_tkinter()

    main_loop(root, label, joystick)

try:
    main()
except KeyboardInterrupt:
    print("終了")

    if hasattr(pygame, 'quit'):
        pygame.quit()  # こうしないとlinterでerror
