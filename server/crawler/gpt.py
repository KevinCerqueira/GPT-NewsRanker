from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import numpy as np
import openai
import core
import math
class Gpt:

    def __init__(self):
        openai.api_key = core.env("OPENAI_API_KEY")
    
    def chat(self, message):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}])
        return completion.choices[0].message.content

class GptLocal:
    def __init__(self, model_name='gpt2', max_loss=5.0):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()  # para avaliação
        self.max_loss = max_loss
        if torch.cuda.is_available():  # se há uma GPU disponível, use-a
            self.model.cuda()

    def score_news(self, title, description, repetitions=5):
        news = f"{title} {description}"
        scores = []

        for _ in range(repetitions):
            inputs = self.tokenizer.encode(news, return_tensors='pt')

            if torch.cuda.is_available():  # se há uma GPU disponível, use-a
                inputs = inputs.cuda()

            with torch.no_grad():
                outputs = self.model(inputs, labels=inputs)
                loss = outputs.loss
                scores.append(loss.item())

        avg_loss = np.mean(scores)
        normalized_score = 10 * np.log(avg_loss + 1) / np.log(self.max_loss + 1)
        rounded_down_score = math.floor(normalized_score)  # arredondamento para baixo
        return min(rounded_down_score, 10)


if __name__ == "__main__":
    gpt = Gpt()
    while True:
        msg = str(input(">> "))
        answer = gpt.chat(msg)
        print("\nGPT:")
        print("----------------------------------------")
        print(answer.strip())
        print("----------------------------------------")
        
#     if __name__ == "__main__":
# 	evaluator = NewsEvaluator()
# 	title = str(input("Titulo da notícia: "))
# 	description = str(input("\nDescrição da notícia: "))
# 	print(evaluator.score_news(title, description))