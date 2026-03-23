from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
import os

from summarizer import summarize_podcast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Podcast Summarization API Running"}


# ✅ NEW: Get transcript directly (NO WHISPER)
def get_transcript(video_id):

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        segments = [
            {
                "text": t["text"],
                "start": t["start"],
                "end": t["start"] + t["duration"]
            }
            for t in transcript
        ]

        return segments, "en"

    except Exception:
        raise HTTPException(status_code=400, detail="Transcript not available")


@app.get("/summarize/{video_id}")
def summarize(video_id: str):

    try:
        print("Fetching transcript...")
        segments, language = get_transcript(video_id)

        print("Summarizing...")
        summary = summarize_podcast(segments)

        return {
            "video_id": video_id,
            "detected_language": language,
            "overview": summary["overview"],
            "section_summaries": summary["sections"]
        }

    except Exception as e:
        print("FULL ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))