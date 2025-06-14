import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils import call_function

if len(sys.argv) < 2:
    print("No arguments provided. Exiting.")
    sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
isVerbose = False
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        isVerbose = True

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the working directory. If the file is long, the result is truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read.",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python script within the working directory and returns any output or errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to run. Must end with .py.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the given content, within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful and experienced AI software agent.

When a user provides a request or bug report, follow these steps:
1. **Understand the task fully** before taking any action.
2. **Inspect existing files and code** to determine what already exists and where changes should be made.
3. Prefer using and modifying **existing files** over creating new ones.
4. If a change is needed, use the write_file function to update relevant code.
5. Always verify your changes by **executing the actual application entry point** (e.g. main.py or similar), not test scripts.
6. Explain your final result clearly, based on the code and output.

You have access to the following tools:
- List files and directories
- Read file contents
- Execute Python files
- Write or overwrite files

Paths should be **relative to the working directory** — you do not need to provide the working directory manually, it is injected automatically.

Work safely within the defined working directory, and do not create unnecessary files unless explicitly asked.
"""


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

for i in range(20):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    # Add each candidate's response to the messages list
    for candidate in response.candidates:
        messages.append(candidate.content)

    # If there are function calls, handle them
    if response.function_calls:
        for func in response.function_calls:
            function_call_result = call_function(func, isVerbose)

            if not function_call_result.parts or not hasattr(function_call_result.parts[0], "function_response"):
                raise Exception("Invalid function call response")

            # Optionally print the result
            if isVerbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            # Add tool result to the conversation
            messages.append(function_call_result)
    else:
        # No function call → we're done
        print("Final response:")
        print(response.text)
        if isVerbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        break

