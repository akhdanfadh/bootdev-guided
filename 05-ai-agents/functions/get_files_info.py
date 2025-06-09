import os
from pathlib import Path


def get_files_info(permitted_dir: str, target_dir: str = None) -> str:
    """Get non-recursive file information inside the target directory."""
    try:
        permitted_dir = Path(permitted_dir).resolve(strict=True)
    except OSError as _:
        return f'Error: Permitted directory "{permitted_dir}" does not exists'

    if target_dir:
        target_dir = Path(target_dir)
        if not target_dir.is_absolute():
            target_dir = (permitted_dir / target_dir).resolve()
        if not target_dir.exists():
            return f'Error: Target directory "{target_dir}" does not exists'
        if not str(target_dir).startswith(str(permitted_dir)):
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted directory'
        if not target_dir.is_dir():
            return f'Error: Target directory "{target_dir}" is not a directory'
    else:
        target_dir = permitted_dir

    file_path = []
    for file in target_dir.iterdir():
        try:
            file_size = f"{os.path.getsize(file)} bytes"
        except Exception as _:
            file_size = "(Error: Getting the file size)"
        file_path.append(f"- {file.name}: file_size={file_size}, is_dir={file.is_dir()}")

    if not file_path:
        return f'Directory "{target_dir}" is empty'
    return "\n".join(file_path)
