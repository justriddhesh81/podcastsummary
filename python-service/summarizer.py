import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_podcast(segments, model_key="gpt-4o-mini"):

    # Limit segments (VERY IMPORTANT for memory)
    segments = segments[:50]

    full_text = " ".join([seg["text"] for seg in segments])
    full_text = full_text[:8000]

    prompt = f"""
    Summarize this podcast transcript.

    Return STRICT JSON in this format:
    {{
      "overview": "5-6 line summary",
      "sections": [
        {{"timestamp": 30, "summary": "point"}},
        {{"timestamp": 120, "summary": "point"}}
      ]
    }}

    Transcript:
    {full_text}
    """

    response = client.chat.completions.create(
        model=model_key,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    output = response.choices[0].message.content

    import json

    try:
        parsed = json.loads(output)
        return parsed
    except:
        return {
            "overview": output,
            "sections": []
        }