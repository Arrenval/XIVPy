import json

from pathlib import Path

from ..definition import Definition


_FOLDER   = Path(__file__).parent
_DEF_FILE = "definitions.json"

def get_definitions() -> dict[str, dict]:
    with open(_FOLDER / _DEF_FILE, 'r') as file:
        return json.load(file)
    
def add_definitions(definitions: list[Definition]) -> None: 
    existing = get_definitions()
    for defn in definitions:
        if defn is None:
            continue
        if defn.name not in existing:
            existing[defn.name] = defn.to_dict()
        if defn.version != existing[defn.name]["version"]:
            print(f"{defn.name} Version Difference: {existing[defn.name]['version']} (Stored), {defn.version} (Read)")
            
    with open(_FOLDER / _DEF_FILE, 'w') as file:
        file.write(json.dumps(existing, indent=4))
