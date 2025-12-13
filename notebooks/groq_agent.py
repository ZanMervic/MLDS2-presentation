

from dotenv import load_dotenv
import os
import json
import requests
from groq import Groq

# Load environment variables (API keys)
_ = load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
geocoding_api_key = os.getenv("GEOCODING_API_KEY")

USE_SYSTEM_PROMPT = True
SYSTEM_INSTRUCTION = (
    "You are a weather agent. If the user gives a city or address, first call get_long_lat "
    "to get latitude and longitude. After you receive the output, you must then call get_weather "
    "using the coordinates from the first location result of get_long_lat. Finally, report the current temperature."
)
#################################
############ TOOLS ##############
#################################

def get_long_lat(city: str):
    """Return candidate locations for a city/address"""

    url = "https://geocode.maps.co/" + \
        f"search?q={city}&api_key={geocoding_api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_weather(lat: float, lon: float):
    """Return current weather for given coordinates"""
    lat, lon = round(lat, 4), round(lon, 4)
    url = f"""https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={
        lon}&hourly=temperature_2m&current_weather=true&timezone=auto"""

    response = requests.get(url)
    response.raise_for_status()
    return response.json()


available_functions = {
    "get_long_lat": get_long_lat,
    "get_weather": get_weather
}


def execute_tool_call(tool_call):
    """Parse and execute a single tool call locally"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    return function_to_call(**function_args)


################################
############ AGENT #############
################################

tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_long_lat",
            "description": "Get latitude and longitude for a city/address",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City or address"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for given coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
                "required": ["lat", "lon"]
            }
        }
    }
]


def call_agent(messages):
    """Handles the multi-step tool call and reasoning chain."""
    model_name = "openai/gpt-oss-20b"

    while True:
        # Call the model
        response = client.chat.completions.create(
            model=model_name,
            tools=tool_definitions,
            messages=messages
        )

        message = response.choices[0].message
        print(f"[REASON]: {message.reasoning}")

        # Check for final text response (end of chain)
        if not message.tool_calls and message.content:
            # Append final assistant message and return
            messages.append({"role": "assistant", "content": message.content})
            return response

        # Check for tool calls
        if message.tool_calls:
            # Append the model's tool call message
            messages.append(message)

            for tool_call in message.tool_calls:
                print(f"[TOOL CALL]: Calling {tool_call.function.name}")

                function_response = execute_tool_call(tool_call)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(function_response)
                })

        else:
            print("Warning: Model returned no text and no tool calls.")
            return response
    

#############################################
############ INTERACTIVE LOOP ###############
#############################################
messages = []

if USE_SYSTEM_PROMPT:
    messages.append(
        {"role": "system", "content": SYSTEM_INSTRUCTION}
    )

init = False
while True:
    user_message = input("Prompt: ").strip()
    init = True

    if user_message.lower() in {"exit", "quit"}:
        print("Agent: Goodbye! 👋")
        break

    if not user_message:
        continue

    messages.append({"role": "user", "content": user_message})

    try:
        print(f"\nUser: {user_message}")
        response = call_agent(messages)

        agent_reply = response.choices[0].message.content

        print("-" * 20)
        print(f"Agent: {agent_reply}\n")

        messages.append({"role": "assistant", "content": agent_reply})

    except Exception as e:
        print(f"⚠️  Error: {e}")
        messages.pop()
    if init:
        break
    continue
