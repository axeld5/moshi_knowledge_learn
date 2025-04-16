import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

class pair(BaseModel):
    question: str
    answer: str

def load_kingdom_text():
    with open('files/kingdom.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def save_qa_pairs(pairs, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)

def qa_pairs_prompt():
    prompt = """Generate 100 Q/A pairs about the following text: <text>{content}</text> 
    Generate the Question/Answers and only the question/answers."""
    return prompt

def eval_qa_pairs_prompt():
    prompt = """Given the following text: <text>{content}</text> 
    and the following QA pairs <qa_pairs>{pairs}</qa_pairs>. 
    Generate a list of 20 Q/A different pairs that can be answered if you only dispose of the information of the previous QA pairs."""
    return prompt

def generate_qa_pairs(content=None):
    if content is None:
        content = load_kingdom_text()
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=qa_pairs_prompt().format(content=content),
        config={
            'response_mime_type': 'application/json',
            'response_schema': list[pair],
        },
    )
    pairs = eval(response.text)
    save_qa_pairs(pairs, 'files/qa_pairs.json')

    new_response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25',
        contents=eval_qa_pairs_prompt().format(content=content, pairs=pairs),
        config={
            'response_mime_type': 'application/json',
            'response_schema': list[pair],
        },
    )
    eval_pairs = eval(new_response.text)
    save_qa_pairs(eval_pairs, 'files/eval_pairs.json')

if __name__ == "__main__":
    generate_qa_pairs()
