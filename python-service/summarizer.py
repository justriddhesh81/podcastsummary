import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_podcast(segments, model_key="gpt-3.5-turbo"):

    # Combine transcript
    full_text = " ".join([seg["text"] for seg in segments])

    # Trim if too long (important)
    full_text = full_text[:12000]

    prompt = f"""
    You are an AI that summarizes podcasts.

    Provide:
    1. A clear overview (5-6 lines)
    2. Section-wise key points (with timestamps if possible)

    Podcast Transcript:
    {full_text}
    """

    response = client.chat.completions.create(
        model=model_key,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    output = response.choices[0].message.content

    return {
        "overview": output,
        "sections": []
    }