from pathlib import Path


def write_file(permitted_dir: str, file_path: str, content: str) -> str:
    """Write content to a file only if it is in permitted directory."""
    try:
        permitted_dir = Path(permitted_dir).resolve(strict=True)
    except (OSError, RuntimeError) as e:
        return f'Error: Permitted directory "{permitted_dir}" does not exists: {str(e)}'

    try:
        file_path = Path(file_path)
        if not file_path.is_absolute():
            file_path = (permitted_dir / file_path).resolve()
        if not str(file_path).startswith(str(permitted_dir)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'
        file_path.parent.mkdir(parents=True, exist_ok=True)  # create parent dirs if not yet exist
        if not file_path.exists():  # now the file
            file_path.touch()
    except (OSError, RuntimeError) as e:
        return f'Error: Invalid file path "{file_path}": {str(e)}'

    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except (OSError, UnicodeDecodeError) as e:
        return f'Error: Cannot write to file "{file_path}": {str(e)}'
