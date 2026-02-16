---
license: mit
---

## Usage

You can use the models in your Python project with the Hugging Face Transformers library. Here is a simple example of how to load the model and predict the result:

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
print(device)
MODEL_PATH="lzw1008/ConspEmoLLM-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map='auto')

prompt = '''Human:
Task: Classify the text regarding COVID-19 conspiracy theories or misinformation into one of the following three classes: 0. Unrelated. 1. Related (but not supporting). 2. Conspiracy (related and supporting).  Text: The truth is this race towards the \"Green New Deal\" and Agenda 2030 is the globalists' plan to stick all the people who have not died from the vaccine and the planned pandemic of 2024 into 8 \"Mega Cities\" where the government will have full 24/7 control and surveillance over you Class: 
Assistant:
'''
inputs = tokenizer(prompt, return_tensors="pt")
input_ids = inputs["input_ids"].to(device)
attention_mask = inputs["attention_mask"].to(device)
generate_ids = model.generate(input_ids = input_ids,attention_mask = attention_mask, max_length=256)
response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True)[0]
print(response)

>>> 2. Conspiracy (related and supporting).
```

