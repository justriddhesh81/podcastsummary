import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_podcast(segments, model_key="gpt-4o-mini"):

    # Limit segments (VERY IMPORTANT for memory)
    segments = segments[:50]

    full_text = " ".join([seg["text"] for seg in segments])
    full_text = full_text[:8000]

    prompt = f"""
    You MUST return ONLY valid JSON.

    No explanation.
    No markdown.
    No text outside JSON.

    Format:
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
    

    try:
        response = client.chat.completions.create(
            model=model_key,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
    except Exception as e:
        print("OPENAI ERROR:", e)
        return {
            "overview": "OpenAI API failed",
            "sections": []
        }

    output = response.choices[0].message.content.strip()

# Remove markdown formatting if present
    if output.startswith("```"):
        output = output.split("```")[1]

    import json

    try:
        parsed = json.loads(output)
        return {
            "overview": parsed.get("overview", ""),
            "sections": parsed.get("sections", [])
        }
    except Exception as e:
        print("JSON PARSE FAILED:", e)
        print("RAW OUTPUT:", output)

        return {
            "overview": output if output else "Summary failed",
            "sections": []
        }