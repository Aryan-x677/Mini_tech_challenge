from fastapi import FastAPI
from grok_utils import Summarize_transcript, analyze_sentiment
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()
csv_file_path = 'call_analysis.csv'

class TranscriptRequest(BaseModel):
    transcript: str
    
def save_to_csv(transcript, summary, sentiment, file_path):
    df = pd.DataFrame([[transcript, summary, sentiment]],columns=["Transcript", "Summary", "Sentiment"])
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


@app.post("/analyze")
def analyze_transcript(request: TranscriptRequest):
    transcript = request.transcript
    summary = Summarize_transcript(transcript)
    sentiment = analyze_sentiment(transcript)
    
    try:
        save_to_csv(transcript, summary, sentiment, csv_file_path)
    except Exception as e:
        return {"error": str(e)}
    
    result = {
        "transcript": transcript,
        "summary": summary,
        "sentiment": sentiment
    }

    return result