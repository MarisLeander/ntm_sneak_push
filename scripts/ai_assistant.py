import json
from google import genai
from pathlib import Path
from datetime import datetime
from google.genai import types
from google.genai.errors import ClientError
from google.genai.errors import ServerError

def get_gemini_api_key() -> str:
    """Gets the users Google Gemini api key from the config file

    Args:
        None

    Returns:
        The Google Gemini api key of the user
    """

    home_dir = Path.home()
    path = home_dir / "stance-detection-german-llm" / "secrets.json"
    try:
        with open(path, "r") as config_file:
            config = json.load(config_file)
        return config.get("gemini_api_key")
    except FileNotFoundError:
        print(f"Error: secrets file not found at {path}")
        return None


def get_client() -> genai.Client:
    return genai.Client(api_key=get_gemini_api_key())


def do_gemini_api_call(instruction_string: str, user_prompt: str, input_data, client: genai.Client) -> dict:
    """ Calls the Gemini API with the given prompt and input data

    Args:
        prompt: The prompt to be sent to the API
        input_data: The data to be sent to the API
        client: The Google Gemini client
    Returns:
        The response from the API
    """
    client_config = None
    if instruction_string:
        client_config = types.GenerateContentConfig(system_instruction=instruction_string, temperature=0.0,
                                                    thinking_config=types.ThinkingConfig(include_thoughts=True))
    else:
        client_config = types.GenerateContentConfig(temperature=0.0,
                                                    thinking_config=types.ThinkingConfig(include_thoughts=True))

    response = None
    successful_api_call = False
    i = 0

    while not successful_api_call:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=user_prompt,
                config=client_config
            )
            successful_api_call = True
        except (ClientError, ServerError) as e:
            i += 1
            if i == 2:
                error = f"""Failed to call the gemini api 5 times
                        Error: {e}
                        Input data: {input_data}"""
                write_log(error, "api_call_error.txt")
                return None
            else:
                time.sleep(5)  # Sleep before retrying
                continue

    # If we exit the loop normally, we got a successful API call
    return response