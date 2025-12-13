# %%
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig, AutomaticFunctionCallingConfig
import os
import requests

_ = load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
geocoding_api_key = os.getenv("GEOCODING_API_KEY")
# %%


def get_long_lat(city: str):
    """ Get latitude and longitude for a city name. Specific addresses work as well but need to be URL encoded properly
    Args:
        city (str): Name of the city

    Returns:
        list: A list of candidate locations with lat/lon values
    """
    url = (f"https://geocode.maps.co/"
           f"search?q={city}&api_key={geocoding_api_key}")

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def get_weather(lat: float, long: float):
    """ Get weather data from an API call
    Args:
        lat (float): Latitude
        long (float): Longitude

    Returns:
        dict: Weather timeseries for past 2 month
    """

    lat, long = round(lat, 4), round(long, 4)

    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={long}"
           "&hourly=temperature_2m&current=temperature_2m&timezone=auto")

    response = requests.get(url)
    response.raise_for_status()
    data = response.headers.get("Content-Type")
    data = response.json()
    return data


# %%
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=GenerateContentConfig(
        tools=[get_weather, get_long_lat],
        system_instruction=(
            "You are a weather agent. If the user gives you a city name or address, first call get_long_lat,"
            "extract latitude and longitude from the best result (match the closest find)",
            "then call get_weather and report the current temperature (last result)"
        ),
        automatic_function_calling=AutomaticFunctionCallingConfig(
            disable=False)
    )
)


def print_steps(response):
    for cand in response.candidates:
        for part in cand.content.parts:
            if part.function_call:
                print(f"\n🧠 CALLING TOOL: {part.function_call.name}")
                print(f"   args: {part.function_call.args}")
            elif part.function_response:
                print(f"\n📦 TOOL RESPONSE ({part.function_response.name}):")
                print(part.function_response.response)
            elif part.text:
                print(f"\n📝 MODEL TEXT:")
                print(part.text)


while True:
    user_message = input("Prompt: ").strip()

    if user_message.lower() in {"exit", "quit"}:
        print("Agent: Goodbye! 👋")
        break

    if not user_message:
        continue

    # `chat.send_message`:
    # - Automatically appends your message to the chat history.
    # - Sends the whole conversation to Gemini.
    # - Returns the model's response as a Python object.
    try:
        response = chat.send_message(message=user_message)
        print_steps(response)
    except Exception as e:
        print(f"⚠️  Error talking to Gemini: {e}")
        continue

    # `response.text` is a convenience property that:
    # - Concatenates all text parts of the model's reply.
    # - Gives you a single plain string you can print.
    agent_reply = response.text

    print(f"User: {user_message}\n")
    print(f"Agent: {agent_reply}\n")
    break
