from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import whisper
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

print("Loading Whisper model...")

whisper_model = whisper.load_model("tiny")

AVAILABLE_MODELS = ["bart", "flan"]


@app.get("/")
def home():
    return {"message": "Podcast Summarization API Running"}


def download_audio(video_id):

    url = f"https://www.youtube.com/watch?v={video_id}"

    output_file = f"{video_id}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{video_id}.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3"
            }
        ],
        "quiet": False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.exists(output_file):
        raise Exception("Audio download failed")

    return output_file


def transcribe_audio(audio_path):

    import whisper  # import inside

    model = whisper.load_model("tiny")  # load only when needed

    result = model.transcribe(
        audio_path,
        task="translate",
        fp16=False,
        temperature=0
    )

    segments = result["segments"]
    language = result["language"]

    return segments, language


@app.get("/summarize/{video_id}")
def summarize(video_id: str, model: str = "bart"):

    audio_path = None

    try:

        if model not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail="Invalid model")

        print("Downloading audio...")
        audio_path = download_audio(video_id)

        print("Transcribing...")
        segments, language = transcribe_audio(audio_path)

        print("Detected language:", language)

        print("Summarizing...")
        summary = {
            "overview": "Summary temporarily disabled due to memory limits",
            "sections": []
        }

        return {
            "video_id": video_id,
            "detected_language": language,
            "overview": summary["overview"],
            "section_summaries": summary["sections"]
        }

    except Exception as e:

        print("FULL ERROR:", e)

        raise HTTPException(status_code=500, detail=str(e))

    finally:

        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print("Deleted temporary audio file")
