import platform
import openai
import os
import core

class Gpt:

    def __init__(self):
        openai.api_key = core.env("OPENAI_API_KEY")
    
    def chat(self, message):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
        return completion.choices[0].message.content
                
if __name__ == "__main__":
    gpt = Gpt()
    while True:
        msg = str(input(">> "))
        answer = gpt.chat(msg)
        print("\nGPT:")
        print("----------------------------------------")
        print(answer.strip())
        print("----------------------------------------")