from openai import OpenAI
import json
from dotenv import load_dotenv

# Assummeing you have a .env file containing OPENAI_API_KEY=<your key> in the same directory
load_dotenv()

client = OpenAI()

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_data = {
        "Tokyo": {"temperature": "10", "unit": "celsius"},
        "San Francisco": {"temperature": "72", "unit": "fahrenheit"},
        "Paris": {"temperature": "22", "unit": "celsius"}
    }
    return json.dumps(weather_data.get(location.title(), {"temperature": "unknown"}))

def start_conversation():
    """Start the conversation with the model"""
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    return messages

def define_tools():
    """Define the tools (functions) available for the model to call"""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    return tools

def process_response(messages, tools):
    """Process the model's response and handle function calls"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return response

def handle_function_calls(response, messages,  
                          available_functions = {"get_current_weather": get_current_weather}):
    """Handle function calls based on the model's response"""
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        # Append the assistant's response message to the conversation
        messages.append(response.choices[0].message)

        # Iterate over each tool call and process them
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)

            # Ensure the function exists
            if function_to_call:
                # Parse the function arguments from JSON
                function_args = json.loads(tool_call.function.arguments)

                # Call the function with the parsed arguments
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit")
                )
                # Append the function response to the conversation
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
    return messages


def complete_conversation(messages):
    """Complete the conversation with the final response from the model"""
    final_response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return final_response.choices[0].message.content

# Main execution flow
if __name__ == "__main__":
    messages = start_conversation()
    tools = define_tools()
    response = process_response(messages, tools)
    messages = handle_function_calls(response, messages, 
                                     available_functions = 
                                     {"get_current_weather": get_current_weather})
    final_output = complete_conversation(messages)
    print(final_output)
