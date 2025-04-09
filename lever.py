import pygame
import toml

def load_lever_config():
    """lever.toml を読み込む"""
    try:
        with open("lever.toml", "r", encoding="utf-8") as file:
            config = toml.load(file)
            return config.get("names", [])
    except FileNotFoundError:
        print("lever.toml が見つかりません。")
        return []
    except toml.TomlDecodeError as e:
        print(f"lever.toml の読み込み中にエラーが発生しました: {e}")
        return []

def get_hat_input_as_fighting_game_notation(joystick, lever_names):
    # ハットスイッチを格ゲー表記に変換
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        # 格ゲー表記の変換
        if hat == (-1, -1):  # 左下
            return lever_names[0]
        elif hat == (0, -1):  # 下
            return lever_names[1]
        elif hat == (1, -1):  # 右下
            return lever_names[2]
        elif hat == (-1, 0):  # 左
            return lever_names[3]
        elif hat == (0, 0):  # ニュートラル
            return lever_names[4]
        elif hat == (1, 0):  # 右
            return lever_names[5]
        elif hat == (-1, 1):  # 左上
            return lever_names[6]
        elif hat == (0, 1):  # 上
            return lever_names[7]
        elif hat == (1, 1):  # 右上
            return lever_names[8]
    return None  # 入力がない場合

def main():
    pygame.init()

    # lever.toml から設定を読み込む
    lever_names = load_lever_config()
    if not lever_names:
        print("lever.toml の設定が正しく読み込めませんでした。")
        return

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
            pygame.event.pump()
            hat_input = get_hat_input_as_fighting_game_notation(joystick, lever_names)
            if hat_input:
                print(f"ハットスイッチ入力: {hat_input}")
            pygame.time.wait(100)  # 少し待機して入力を取得
    except KeyboardInterrupt:
        print("プログラムを終了します。")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
