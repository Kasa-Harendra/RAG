import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBhW_Cw_QZ0sXsVqGRcSJQ9VzsJtQDP110")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-2.5-flash" 

def generate_answer(prompt: str, context: List[str]) -> str:
    context_text = "\n".join(context)
    print(context_text)
    full_prompt = f"""Answer my question strictly based on the context:
    
    Context:\n{context_text}\n\n
    Question: {prompt}\n
    Answer:
    """
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    response = model.generate_content(full_prompt)
    return response.text
