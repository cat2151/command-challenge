import sys
import toml
import pygame

def load_all_configs():
    """設定ファイルを読み込み、必要なデータを返す"""
    config = load_config("bits_named.toml")
    names = config.get("names", [])
    plus = config.get("plus")
    print(f"読み込まれた設定: {names}")

    config = load_config("lever.toml")
    lever_names = config.get("names", [])
    print(f"読み込まれた設定: {lever_names}")

    config = load_config("mission.toml")
    mission_name = config.get("mission_name", "")
    mission = config.get("mission", "")
    print(f"読み込まれた設定: {mission_name}")
    print(f"読み込まれた設定: {mission}")

    return names, plus, lever_names, mission_name, mission

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

def load_config(config_path):
    """指定された TOML ファイルを読み込む"""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = toml.load(file)
            return config
    except FileNotFoundError:
        print(f"{config_path} が見つかりません。")
        return {}
    except toml.TomlDecodeError as e:
        print(f"{config_path} の読み込み中にエラーが発生しました: {e}")
        return {}

def clear_screen():
    """Windows のエスケープシーケンスを使用して画面をクリア"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def get_pressed_buttons(names, bitstring, plus):
    """現在押されているボタンを 'A + B' の形式で返す"""
    pressed_buttons = [name for name, state in zip(names, bitstring[:len(names)]) if name and state == '1']
    return plus.join(pressed_buttons)

def update_display(names, mission_name, mission, bitstring, lever_plus_pressed, mission_result):
    clear_screen()
    print_button_status(names, bitstring)
    print(f"レバー+ボタン: {lever_plus_pressed}")
    print(f"{mission_name}: {mission}: {mission_result}")

def print_button_status(names, bitstring):
    print("入力状態:")
    for name, state in zip(names, bitstring[:len(names)]):
        if name:
            print(f"{name}: {state}")
    print(f"ビット列: {bitstring}")
