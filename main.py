
import ollama
import subprocess
import webbrowser
import time

MODEL = "qwen2.5:3b"

# Approved Windows applications
APP_LIST = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": "code",
    "visual studio code": "code"
}


# Open Windows applications
def open_application(name):
    name = name.lower().strip()

    if name not in APP_LIST:
        return f"Sorry, {name} is not in my approved application list."

    try:
        subprocess.Popen(APP_LIST[name])
        return f"Successfully opened {name}."

    except Exception as error:
        return f"Could not open {name}: {error}"


# Open websites
def open_website(url):
    try:
        if not url.startswith(("https://", "http://")):
            url = "https://" + url

        webbrowser.open(url)
        return f"Successfully opened {url}."

    except Exception as error:
        return f"Could not open website: {error}"


# Available tools for the AI
TOOLS = [
    open_application,
    open_website
]

TOOL_FUNCTIONS = {
    "open_application": open_application,
    "open_website": open_website
}


# JARVIS system instructions
SYSTEM_PROMPT = """
You are JARVIS, a personal AI assistant running on Windows.

You can:
1. Answer normal questions.
2. Open Windows applications.
3. Open websites.

Rules:
- When asked to open an application, call open_application.
- Use names such as chrome, google chrome, notepad,
  calculator, and vscode.
- When asked to visit a website, call open_website.
- Do not claim an application or website was opened
  unless the tool reports success.
- Be friendly and concise.
"""


# Start JARVIS
print("=" * 40)
print("          JARVIS AI ONLINE")
print("=" * 40)
print("Model:", MODEL)
print("Type 'exit' to close JARVIS.\n")


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:

    try:
        user_input = input("\nYOU: ").strip()

        if user_input.lower() == "exit":
            print("\nJARVIS: Goodbye!")
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        print("\nJARVIS: Thinking...")
        start_time = time.time()

        # Ask AI
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        # Process tool calls
        while response.message.tool_calls:

            messages.append(response.message)

            for tool_call in response.message.tool_calls:

                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\nJARVIS: Executing {function_name}...")

                function = TOOL_FUNCTIONS.get(function_name)

                if function:
                    result = function(**arguments)
                else:
                    result = "Unknown tool requested."

                print("JARVIS:", result)

                messages.append({
                    "role": "tool",
                    "content": str(result)
                })

            # Ask AI again after tool execution
            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=TOOLS
            )

        # Display final AI response
        messages.append(response.message)

        if response.message.content:
            print("\nJARVIS:", response.message.content)

        print(
            f"\nResponse time: {time.time() - start_time:.2f} seconds"
        )

    except KeyboardInterrupt:
        print("\n\nJARVIS: Interrupted.")
        break

    except Exception as error:
        print("\nJARVIS ERROR:", repr(error))
