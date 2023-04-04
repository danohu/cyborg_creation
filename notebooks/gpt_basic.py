
from cyborg.utils import *

def summarize_text(text, max_words):
    token_limit = 3000 # allow some room for the instructions
    num_tokens = num_tokens_from_string(text, "gpt2")
    if num_tokens > token_limit:
        start, end = text[:token_limit], text[token_limit:]
        return summarize_text(start, token_limit) + summarize_text(end, token_limit)
    else:
        return text # do the work here


import os
os.environ["OPENAI_API_KEY"] = 'dummy'
from langchain.llms import OpenAI
from IPython.display import Image
import openai

# %%


# res = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )

# print(res)

def simple_gpt_message(query):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]
    )
    return res['choices'][0]['message']['content']

print(simple_gpt_message("Tell me about the history of Prussia"))