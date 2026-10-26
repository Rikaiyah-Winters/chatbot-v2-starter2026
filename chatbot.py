from openai import OpenAI

client = OpenAI()

# accepts a preferred model and a list of messages
# makes chat completions API call
# returns the response message content
def get_api_chat_response_message(model, messages):
    # make the API call
    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    # extract the response text
    response_content = api_response.choices[0].message.content

    # return the response text
    return response_content

model = "gpt-6-luna"

chat_history = []

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Chatbot: Hello User! What is your name? If you'd like to end the chat, type 'exit'. ")
        user_name = f"User name is {user_input}"
        chat_history.append({
            "role": "user",
            "content": user_name
        })

    else:
        user_input = input("You: ")
    if user_input.lower() == "exit":
        exit()

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = get_api_chat_response_message(model, chat_history)

    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": response
    })