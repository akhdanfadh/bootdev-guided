from pathlib import Path

from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file, constrained to the permitted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the permitted working directory, or absolute path",
            )
        },
    ),
)


def get_file_content(permitted_dir: str, file_path: str) -> str:
    """Get content of a file only if it is in permitted directory."""
    try:
        permitted_dir = Path(permitted_dir).resolve(strict=True)
    except (OSError, RuntimeError) as e:
        return f'Error: Permitted directory "{permitted_dir}" does not exists: {str(e)}'

    try:
        file_path = Path(file_path)
        if not file_path.is_absolute():
            file_path = (permitted_dir / file_path).resolve()
    except (OSError, RuntimeError) as e:
        return f'Error: Invalid file path "{file_path}": {str(e)}'

    try:
        if not file_path.exists():
            return f'Error: Target file "{file_path}" does not exists'
        if not str(file_path).startswith(str(permitted_dir)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted directory'
        if not file_path.is_file():
            return f'Error: Target file "{file_path}" is not a regular file'
    except OSError as e:
        return f'Error: Cannot access file "{file_path}": {str(e)}'

    try:
        with open(file_path, "r") as file:
            file_content = file.read(MAX_CHARS)
            if file.read(1):  # file longer than MAX_CHARS
                file_content += f'\n\n[...File "{file_path}" truncated at 10000 characters]'
    except (OSError, UnicodeDecodeError) as e:
        return f'Error: Cannot read file "{file_path}": {str(e)}'

    return file_content
