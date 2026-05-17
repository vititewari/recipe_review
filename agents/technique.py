import anthropic

client = anthropic.Anthropic()


def technique_reviewer(recipe):
    """
    Analyse a recipe and return technique feedback from an AI coffee brewer.

    Args:
        recipe (str): The recipe text to be examined.

    Returns:
        str: Technique analysis and feedback, or an error string if input is
             invalid or the API call fails.
    """
    if not isinstance(recipe, str):
        return "Error: recipe must be a string"
    if not recipe.strip():
        return "Error: recipe cannot be empty"

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="you are a professional coffee brewer that analyses a recipe and provides feedback on its technique",
            messages=[{"role": "user", "content": recipe}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: API call failed — {e}"
