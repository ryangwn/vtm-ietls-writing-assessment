import google.generativeai as genai
import os
from openai import OpenAI
from yaspin import yaspin
from yaspin.spinners import Spinners

def call_llm(prompt, model_type=os.environ.get("MODEL_TYPE", "gemini")):
    spinner = yaspin(Spinners.earth, text="Generating response with AI...")
    
    try:
        spinner.start()
            
        if model_type == "gemini":
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            
            model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
            
            # Generate content with temperature=0 for deterministic responses
            generation_config = genai.types.GenerationConfig(
                temperature=0.0,
            )
            
            response = model.generate_content(prompt, generation_config=generation_config)
            result = response.text
        
    
        elif model_type == "chatgpt":
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            result = response.choices[0].message.content
    
        elif model_type == "deepseek":
            client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")
            
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            
            result = response.choices[0].message.content
        
        else:
            raise ValueError(f"Unsupported model type: {model_type}. Choose 'gemini', 'chatgpt', or 'deepseek'.")
            
        return result
    
    finally:
        spinner.stop()
