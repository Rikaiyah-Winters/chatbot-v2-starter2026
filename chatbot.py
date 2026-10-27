from openai import OpenAI
import tiktoken
import logging
import datetime

log = logging.getLogger("chatbot_token_count")

#creates a log file
logging.basicConfig(filename = "chatbot_token_count.log", level = logging.INFO)


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

def get_api_chat_round_total_tokens(model, messages):
    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    #extract total amount of tokens PER ITERATION
    total_tokens_for_iteration = api_response.usage.total_tokens

    return total_tokens_for_iteration

model = "gpt-5.5"
encoding = tiktoken.encoding_for_model(model)
#print(encoding)
token_input_limit = 12289

chat_history = []

user_input = ""

#conversation_token_usage = []

total_token_count = 0


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
        #integer_conversation_token_usage = sum(map(int, conversation_token_usage))
        #print(integer_conversation_token_usage)
        #print(logging.info(f"The total tokens from this conversation is: {integer_conversation_token_usage}"))
        log.info("\nDate: " + str(datetime.datetime.now()) + "\nTotal tokens: " + str(total_token_count) + "\n\n")
        exit()

    #counts the number of tokens in prompt
    token_count = len(encoding.encode(user_input))

    if(token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue

    #print(token_count)

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = get_api_chat_response_message(model, chat_history)

    round_token_usage = get_api_chat_round_total_tokens(model, chat_history)

    #conversation_token_usage.append(round_token_usage) #need to turn to number?

    total_token_count += round_token_usage
    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": response
    })

#This model produces emojis, yet can't read the same encode character it produces in bash I guess...