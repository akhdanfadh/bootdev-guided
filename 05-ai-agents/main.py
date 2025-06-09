import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    model = "gemini-2.0-flash-001"
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]
    response = client.models.generate_content(model=model, contents=messages)

    if args.verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
