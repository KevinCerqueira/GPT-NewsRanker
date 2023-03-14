import platform
import openai
import os

class GPTClass:

    def __init__(self):
        openai.api_key = self.env("OPENAI_API_KEY")
    
    def chat(self, message):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
        return completion.choices[0].message.content
    
    def env(self, var):
        env = '\\.env'
        if(platform.system() == 'Linux'):
            env = '/.env'
            
        with open(os.path.dirname(os.path.realpath(__file__)) + env, 'r', encoding='utf-8') as file_env:
            line = file_env.readline()
            while(line):
                content = line.split('=')
                if(content[0] == var):
                    return content[1]
                line = file_env.readline()
                
if __name__ == "__main__":
    gpt = GPTClass()
    while True:
        msg = str(input(">> "))
        answer = gpt.chat(msg)
        print("\nGPT:")
        print("----------------------------------------")
        print(answer.strip())
        print("----------------------------------------")