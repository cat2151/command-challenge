import pygame
from lever import get_hat_input_as_fighting_game_notation

def setup_pygame_and_joystick():
    if hasattr(pygame, 'init'):  # こうしないとlinterエラー
        pygame.init()
    joystick = initialize_joystick()
    if joystick is None:
        return None
    return joystick

def initialize_joystick():
    """ジョイスティックを初期化し、接続されていない場合はNoneを返す"""
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("ジョイスティックが接続されていません。")
        return None

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"使用するジョイスティック: {joystick.get_name()}")
    return joystick

def get_buttons_as_bitstring(joystick):
    # ボタン入力を取得（0または1）
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    # アナログ入力を2ビット表現に変換（軸4と軸5を対象とする）
    axes = []
    for i in range(joystick.get_numaxes()):
        axis_value = joystick.get_axis(i)

        if i in [4, 5]:  # 軸4と軸5の場合
            if axis_value == -1:
                axes.extend([0, 0])  # ニュートラル位置を0とする
            elif axis_value > -1:  # 正方向
                axes.extend([1, 0])
            elif axis_value < -1:  # 負方向（理論的には発生しないが念のため）
                axes.extend([0, 1])

    # ビット列を構成
    bitstring = ''.join(map(str, buttons))  # ボタンのビット列
    bitstring += ''.join(map(str, axes))   # アナログ入力の2ビット列

    return bitstring

def create_button_states(names, plus, lever_names, joystick, bitstring):
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

def get_pressed_buttons(names, bitstring, plus):
    """現在押されているボタンを 'A + B' の形式で返す"""
    pressed_buttons = [name for name, state in zip(names, bitstring[:len(names)]) if name and state == '1']
    return plus.join(pressed_buttons)

def shutdown_pygame():
    if hasattr(pygame, 'quit'): # こうしないとlinterエラー
        pygame.quit()
