import openai
from dotenv import load_dotenv

# Assummes you have a .env file containing OPENAI_API_KEY=<your key> in the same directory
load_dotenv()

# Initialize OpenAI Client
openai_client = openai.Client()

def get_completion(prompt, model="gpt-4-1106-preview", client = openai_client):

    # run the completions api
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model=model
    )

    # Extract the response content
    response_content = chat_completion.choices[0].message.content

    # Extract token usage
    prompt_tokens = chat_completion.usage.prompt_tokens
    output_tokens = chat_completion.usage.completion_tokens
    total_tokens = chat_completion.usage.total_tokens

    return response_content, prompt_tokens, output_tokens, total_tokens


prompt = 'Write a short bio on Elon Musk?'
response, prompt_tokens,  output_tokens = get_completion(prompt=prompt)

print(f"Prompt: prompt")
print(f"\nPrompt Tokens: {prompt_tokens}")
print(f"\nOutput: {response}")
print(f"\nOutput tokens: {output_tokens}")
