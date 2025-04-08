import pygame

def get_hat_input_as_fighting_game_notation(joystick):
    pygame.event.pump()  # イベント更新

    # ハットスイッチを格ゲー表記に変換
    hats = []
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        # 格ゲー表記の変換
        if hat == (0, 1):  # 上
            hats.append("8")
        elif hat == (1, 1):  # 右上
            hats.append("9")
        elif hat == (1, 0):  # 右
            hats.append("6")
        elif hat == (1, -1):  # 右下
            hats.append("3")
        elif hat == (0, -1):  # 下
            hats.append("2")
        elif hat == (-1, -1):  # 左下
            hats.append("1")
        elif hat == (-1, 0):  # 左
            hats.append("4")
        elif hat == (-1, 1):  # 左上
            hats.append("7")
        else:  # ニュートラル
            hats.append("5")

    # ハットスイッチの入力を結合して返す
    return ''.join(hats)

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
            hat_input = get_hat_input_as_fighting_game_notation(joystick)
            print(f"ハットスイッチ入力: {hat_input}")
            pygame.time.wait(100)  # 少し待機して入力を取得
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()

