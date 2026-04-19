import os
from agents import Agent, Runner, function_tool


@function_tool
def get_server_status(service_name: str) -> str:
    """Return a starter status for a named service.

    This is a simple demo tool so you can see how an OpenAI Agent calls a
    Python function. Later, this can be replaced with real checks for GitHub,
    Vercel, Telegram, local files, shell commands, or other APIs.
    """
    service_name = service_name.strip().lower()

    fake_statuses = {
        "telegram": "Telegram bot status: running normally.",
        "github": "GitHub sync status: repository is reachable.",
        "vercel": "Vercel deploy status: last deploy looks healthy.",
    }

    return fake_statuses.get(
        service_name,
        f"No saved status found for '{service_name}', but the tool is working.",
    )


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please export your API key first."
        )

    agent = Agent(
        name="Simple Ops Agent",
        instructions=(
            "You are a simple helpful assistant. "
            "Use tools when they help answer the user clearly. "
            "Keep answers short and practical."
        ),
        tools=[get_server_status],
    )

    print("Simple agent started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        result = Runner.run_sync(agent, user_input)
        print(f"Agent: {result.final_output}\n")


if __name__ == "__main__":
    main()
