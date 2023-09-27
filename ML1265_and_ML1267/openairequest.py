#! /usr/bin/env python

# This block of code sends a request to OpenAI Chat Completions
# endpoint. It uses a plain HTTP post request. Other ways to accomplish this
# are by using the official openai Python API or LangChain framework.

import requests

# Place your OpenAI API key here
openai_key = yourKeyHere

# Setup some basic OpenAI API parameters
endpoint    = 'https://api.openai.com/v1/chat/completions' # The API endpoint
temperature = 1.4                                          # Resonse determinism. 0.0-deterministic, 2.0-random
model       = 'gpt-3.5-turbo'                              # AI model
price       = 0.0015                                       # USD price per 1,000 tokens for this model

# Structure the message.
prompt  = "Nice day today, isn't it?"
message =   [
                {'role': 'system', 'content': 'You area helpful assistant.'},
                {'role': 'user',   'content': prompt}
            ]

# Make a POST HTTP request to OpenAI API.
headers  = {'Authorization': f'Bearer {openai_key}'}
data     = {'model': model, 'temperature': temperature, 'messages': message}
response = requests.post(endpoint, headers=headers, json=data).json()

# Parse the information of interest from the OpenAI response.
answer = response['choices'][0]['message']['content']
tokens = response['usage']['total_tokens']

# Get cost in USD for this API call.
cost = tokens / 1000 * price
# Cost can be very small. Suppress the scientific notation.
cost = f'{cost:.6f}'

# Print the results to screen.
print(answer)
print('-'*64)
print('The cost in USD is', cost)
