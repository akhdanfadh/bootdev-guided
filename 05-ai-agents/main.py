import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info

MODEL = "gemini-2.0-flash-001"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
AVAILABLE_FUNCTIONS = types.Tool(function_declarations=[schema_get_files_info])


def call_llm(client: genai.Client, messages: list[types.Content], verbose: bool = False):
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, tools=[AVAILABLE_FUNCTIONS]
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
    print(f"Response: {response.text}")


def main():
    # Load CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="User prompt/question for the LLM")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print user prompt and token usage to console",
    )
    args = parser.parse_args()

    # Load environment (LLM API key)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Model calling
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]
    call_llm(client, messages, args.verbose)


if __name__ == "__main__":
    main()
