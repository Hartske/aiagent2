import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("No API key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User Prompt: {args.user_prompt}")
    
    for _ in range(20):
        if generate_content(client, messages, args.verbose):
            return

    print("Agent reached the iteration limit without a final response")
    raise SystemExit(1)

def generate_content(client: OpenAI, messages: list, verbose: bool) -> bool:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if not response.usage:
        raise RuntimeError("No usage data")

    message = response.choices[0].message
    messages.append(message)
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message['content']:
                raise Exception("Error: 'content' is empty")
            if verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
            return False

    else:
        if verbose:
            if response.usage:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            else:
                print("Token usage unavailable")
        print("Response:")
        print(message.content)
        return True


if __name__ == "__main__":
    main()
