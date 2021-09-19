import json
import pickle

save_db_filepath = "saves/demo_world/world_data.db"
savename = "demo_world"


def save(obj, filepath) -> None:
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)

def load(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def get_prefix(client, ctx) -> str:
    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(ctx.guild.id)]

