import sys

def update_display(names, mission, bitstring, lever_plus_pressed, mission_result):
    clear_screen()
    print_button_status(names, bitstring)
    print(f"レバー+ボタン: {lever_plus_pressed}")
    print(f"mission : {mission} : {mission_result}")

def clear_screen():
    """Windows のエスケープシーケンスを使用して画面をクリア"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def print_button_status(names, bitstring):
    print("入力状態:")
    for name, state in zip(names, bitstring[:len(names)]):
        if name:
            print(f"{name}: {state}")
    print(f"ビット列: {bitstring}")
