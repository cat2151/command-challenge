import pygame

def get_input_as_bitstring(joystick):
    pygame.event.pump()  # イベント更新

    # ボタン入力を取得（0または1）
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    # ハットスイッチを2ビット表現に変換
    hats = []
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        # ハットスイッチのX軸
        if hat[0] > 0:
            hats.extend([1, 0])  # 正方向
        elif hat[0] < 0:
            hats.extend([0, 1])  # 負方向
        else:
            hats.extend([0, 0])  # ニュートラル
        # ハットスイッチのY軸
        if hat[1] > 0:
            hats.extend([1, 0])  # 正方向
        elif hat[1] < 0:
            hats.extend([0, 1])  # 負方向
        else:
            hats.extend([0, 0])  # ニュートラル

    # アナログ入力を2ビット表現に変換（小数点1桁まで丸め、特定軸に対応）
    axes = []
    for i in range(joystick.get_numaxes()):
        axis_value = round(joystick.get_axis(i), 1)  # 小数点1桁に丸める

        # アナログ軸4と5の特別処理
        if i in [4, 5]:  # 軸4と軸5の場合
            if axis_value == -1:
                axes.extend([0, 0])  # ニュートラル位置を0とする
            elif axis_value > -1:  # 正方向
                axes.extend([1, 0])
            elif axis_value < -1:  # 負方向（理論的には発生しないが念のため）
                axes.extend([0, 1])
        else:
            if axis_value > 0.5:
                axes.extend([1, 0])  # 正の値を10とする
            elif axis_value < -0.5:
                axes.extend([0, 1])  # 負の値を01とする
            else:
                axes.extend([0, 0])  # 中間値を00とする

#        print(f"アナログ軸 {i} の値: {axis_value}")  # アナログ値を出力

    # ビット列を構成
    bitstring = ''.join(map(str, buttons))  # ボタンのビット列
    bitstring += ''.join(map(str, hats))    # ハットスイッチの2ビット列
    bitstring += ''.join(map(str, axes))   # アナログ入力の2ビット列

    return bitstring

def main():
    pygame.init()

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
            print(f"入力状態のビット列: {bitstring}")
            pygame.time.wait(100)  # 少し待機して入力を取得
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
