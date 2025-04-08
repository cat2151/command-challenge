import pygame
import toml
import sys

def get_input_as_bitstring(joystick):
    pygame.event.pump()  # イベント更新

    # ボタン入力を取得（0または1）
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    # アナログ入力を2ビット表現に変換（小数点1桁まで丸め、特定軸に対応）
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
        else:
            continue
            # if axis_value > 0.5:
            #     axes.extend([1, 0])  # 正の値を10とする
            # elif axis_value < -0.5:
            #     axes.extend([0, 1])  # 負の値を01とする
            # else:
            #     axes.extend([0, 0])  # 中間値を00とする

    # ビット列を構成
    bitstring = ''.join(map(str, buttons))  # ボタンのビット列
    bitstring += ''.join(map(str, axes))   # アナログ入力の2ビット列

    return bitstring

def load_config():
    """bits_named.toml を読み込む"""
    try:
        with open("bits_named.toml", "r", encoding="utf-8") as file:
            config = toml.load(file)
            return config
    except FileNotFoundError:
        print("bits_named.toml が見つかりません。")
        return {}
    except toml.TomlDecodeError as e:
        print(f"bits_named.toml の読み込み中にエラーが発生しました: {e}")
        return {}

def clear_screen():
    """Windows のエスケープシーケンスを使用して画面をクリア"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def main():
    pygame.init()

    # 設定ファイルを読み込む
    config = load_config()
    names = config.get("names", [])
    print(f"読み込まれた設定: {names}")

    # ジョイスティックの初期化
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("ジョイスティックが接続されていません。")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"使用するジョイスティック: {joystick.get_name()}")

    try:
        while True:
            bitstring = get_input_as_bitstring(joystick)
            clear_screen()  # 画面をクリア
            print("入力状態:")
            for name, state in zip(names, bitstring[:len(names)]):  # names に対応する部分だけを取得
                if name:
                    print(f"{name}: {state}")
            print(f"ビット列: {bitstring}")
            pygame.time.wait(100)  # 少し待機して入力を取得
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
