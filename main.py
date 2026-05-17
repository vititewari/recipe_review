import anthropic
from agents.nutrition import nutrition_calculator
from agents.technique import technique_reviewer

client = anthropic.Anthropic()

tools = [
    {
        "name": "nutrition_calculator",
        "description": "Analyses a recipe and provides feedback on its nutritional value. Use this when the user wants to know about calories, macros, vitamins, or overall healthiness of a recipe.",
        "input_schema": {
            "type": "object",
            "required": ["recipe"],
            "properties": {
                "recipe": {
                    "type": "string",
                    "description": "The full recipe text to be analysed for nutritional content.",
                }
            },
        },
    },
    {
        "name": "technique_reviewer",
        "description": "Analyses a recipe and provides feedback on its brewing or cooking technique. Use this when the user wants to know about method, steps, timing, temperature, or technique quality.",
        "input_schema": {
            "type": "object",
            "required": ["recipe"],
            "properties": {
                "recipe": {
                    "type": "string",
                    "description": "The full recipe text to be analysed for technique quality.",
                }
            },
        },
    },
]

tool_router = {
    "nutrition_calculator": nutrition_calculator,
    "technique_reviewer": technique_reviewer,
}


def run_agent(user_message):
    """
    Run the agentic loop for a given user message.

    Coordinates between the nutrition and technique subagents, handling
    sequential and parallel tool calls until the model signals end_turn.

    Args:
        user_message (str): The user's recipe review request.

    Returns:
        str: The final response from the head barista coordinator.
    """
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=(
                "You are a head barista who coordinates recipe reviews. "
                "When given a recipe, you delegate to the appropriate specialist agents: "
                "use nutrition_calculator for nutritional feedback and technique_reviewer "
                "for brewing or cooking technique feedback. "
                "Synthesise their responses into a single, clear review for the user."
            ),
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            # Collect all tool-use blocks (handles parallel calls)
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            # Append the assistant turn with all content blocks
            messages.append({"role": "assistant", "content": response.content})

            # Execute every tool call and collect results
            tool_results = []
            for block in tool_use_blocks:
                fn = tool_router.get(block.name)
                if fn is None:
                    result = f"Error: unknown tool '{block.name}'"
                else:
                    result = fn(**block.input)

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

            messages.append({"role": "user", "content": tool_results})
            continue

        return f"Error: unexpected stop reason '{response.stop_reason}'"


if __name__ == "__main__":
    print("Recipe Review Assistant — type 'quit' to exit.\n")
    while True:
        user_input = input("Enter your recipe or question: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue
        print("\nReviewing...\n")
        result = run_agent(user_input)
        print(f"{result}\n")
