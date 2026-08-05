from pathlib import Path

def list_data_files(directory: str) -> list[str]:
    path = Path(directory)
    return sorted(str(p) for p in path.glob("*.csv"))