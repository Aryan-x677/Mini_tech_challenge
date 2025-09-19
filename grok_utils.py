from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
HEADER = {"Authorization": f"Bearer {api_key}"}

url = "https://api.groq.com/openai/v1/chat/completions"

def Summarize_transcript(transcript: str) -> str:
    prompt = f"Summarize the following Customer service call transcript in 2-3 sentences:\n{transcript}"
    payload = {
        "model": "llama-3.3-70b-versatile"
        ,"messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,            
    }    

    response = requests.post(url, json=payload, headers=HEADER)
    if response.status_code == 200:
        summary = response.json()["choices"][0]["message"]["content"]
        return summary
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
def analyze_sentiment(transcript: str) -> str:
    prompt = f"Analyze the sentiment of the following Customer service call transcript and classify it as Positive, Negative, or Neutral:\n{transcript}"
    payload = {
        "model": "llama-3.3-70b-versatile"
        ,"messages": [{"role": "user", "content": prompt}],
        "max_tokens": 20,            
    }    

    response = requests.post(url, json=payload, headers=HEADER)
    if response.status_code == 200:
        sentiment = response.json()["choices"][0]["message"]["content"]
        if "positive" in sentiment.lower():
            return "Positive" 
        elif "negative" in sentiment.lower():
            return "Negative"
        elif "neutral" in sentiment.lower():
            return "Neutral"
        
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
        
