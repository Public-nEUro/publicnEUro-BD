from pathlib import Path


def resolve_path(dataset_id: str, path: str) -> str:
    base_path = Path("/datasets") / dataset_id
    abs_path = (base_path / path).resolve()

    if not abs_path.is_relative_to(base_path):
        raise ValueError("Invalid path")

    return str(abs_path)
