import subprocess
from pathlib import Path


def run_python_file(permitted_dir: str, file_path: str, args: list[str] = None) -> str:
    """Execute a Python file only if it is in permitted directory."""
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
            return f'Error: Python file "{file_path}" does not exists'
        if not str(file_path).startswith(str(permitted_dir)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted directory'
        if not (file_path.is_file() and file_path.suffix == ".py"):
            return f'Error: Target file "{file_path}" is not a Python file'
    except OSError as e:
        return f'Error: Cannot access file "{file_path}": {str(e)}'

    try:
        command = ["python3", str(file_path)]
        if args:
            command.extend(args)
        execution = subprocess.run(
            command, text=True, timeout=30, capture_output=True, cwd=permitted_dir
        )
        output = []
        if execution.stdout:
            output.append(f"STDOUT: {execution.stdout.decode()}")
        if execution.stderr:
            output.append(f"STDERR: {execution.stderr.decode()}")
        if execution.returncode != 0:
            output.append(f"Process exited with code {execution.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
