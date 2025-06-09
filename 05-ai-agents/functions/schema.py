from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the permitted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "target_dir": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the permitted working directory, or absolute path. If not provided, the current working directory is used.",
            )
        },
    ),
)
