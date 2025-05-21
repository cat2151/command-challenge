from utils import read_toml

def load_all_configs(args):
    config = read_toml(args.bits_named_toml)
    names = config.get("names", [])
    plus = config.get("plus")
    print(f"読み込まれた設定: {names}")

    config = read_toml(args.lever_toml)
    lever_names = config.get("names", [])
    print(f"読み込まれた設定: {lever_names}")

    return names, plus, lever_names, args.missions
