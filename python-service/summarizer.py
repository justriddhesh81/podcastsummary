from transformers import pipeline, AutoTokenizer
import torch

device = 0 if torch.cuda.is_available() else -1

AVAILABLE_MODELS = {
    "bart": {
        "name": "facebook/bart-large-cnn",
        "task": "summarization",
        "max_input_tokens": 1024
    },
    "flan": {
        "name": "google/flan-t5-base",
        "task": "text2text-generation",
        "max_input_tokens": 512
    }
}

loaded_models = {}


def get_summarizer(model_key: str):

    if model_key not in AVAILABLE_MODELS:
        raise ValueError(f"Model '{model_key}' not supported.")

    if model_key not in loaded_models:

        config = AVAILABLE_MODELS[model_key]

        tokenizer = AutoTokenizer.from_pretrained(config["name"])

        summarizer = pipeline(
            config["task"],
            model=config["name"],
            tokenizer=tokenizer,
            device=device
        )

        loaded_models[model_key] = summarizer

    return loaded_models[model_key]


def clean_transcript(text: str):

    sentences = text.split(". ")

    seen = set()
    cleaned = []

    for s in sentences:

        s = s.strip()

        if len(s) < 5:
            continue

        if s.lower() in seen:
            continue

        seen.add(s.lower())
        cleaned.append(s)

    return ". ".join(cleaned)


def chunk_text(text, tokenizer, max_input_tokens):

    max_tokens = max_input_tokens - 50

    tokens = tokenizer.encode(text)

    chunks = []

    for i in range(0, len(tokens), max_tokens):

        subset = tokens[i:i + max_tokens]

        chunk = tokenizer.decode(subset, skip_special_tokens=True)

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def summarize_text(text: str, model_key: str = "bart"):

    text = clean_transcript(text)

    if not text.strip():
        raise ValueError("Transcript empty after cleaning.")

    summarizer = get_summarizer(model_key)

    tokenizer = summarizer.tokenizer

    max_input_tokens = AVAILABLE_MODELS[model_key]["max_input_tokens"]

    chunks = chunk_text(text, tokenizer, max_input_tokens)

    chunk_summaries = []

    for chunk in chunks:

        if model_key == "flan":

            prompt = f"Summarize this podcast transcript clearly:\n{chunk}"

            output = summarizer(
                prompt,
                max_new_tokens=120,
                do_sample=False
            )

            chunk_summaries.append(output[0]["generated_text"])

        else:

            output = summarizer(
                chunk,
                max_new_tokens=120,
                do_sample=False,
                truncation=True
            )

            chunk_summaries.append(output[0]["summary_text"])

    combined_summary = " ".join(chunk_summaries)

    final_chunks = chunk_text(combined_summary, tokenizer, max_input_tokens)

    final_summaries = []

    for chunk in final_chunks:

        if model_key == "flan":

            prompt = f"Create a clean final summary:\n{chunk}"

            output = summarizer(
                prompt,
                max_new_tokens=150,
                do_sample=False
            )

            final_summaries.append(output[0]["generated_text"])

        else:

            output = summarizer(
                chunk,
                max_new_tokens=150,
                do_sample=False,
                truncation=True
            )

            final_summaries.append(output[0]["summary_text"])

    return " ".join(final_summaries)


def summarize_podcast(segments, model_key="bart"):

    summarizer = get_summarizer(model_key)

    tokenizer = summarizer.tokenizer

    max_input_tokens = AVAILABLE_MODELS[model_key]["max_input_tokens"]

    segment_groups = []
    group = []
    duration = 0
    group_start = 0

    for seg in segments:

        if not group:
            group_start = seg["start"]

        group.append(seg["text"])
        duration += seg["end"] - seg["start"]

        if duration > 120:

            segment_groups.append({
                "text": " ".join(group),
                "start": group_start
            })

            group = []
            duration = 0

    if group:
        segment_groups.append({
            "text": " ".join(group),
            "start": group_start
        })

    section_summaries = []

    for text_group in segment_groups:

        text = clean_transcript(text_group["text"])

        chunks = chunk_text(text, tokenizer, max_input_tokens)

        partial = []

        for chunk in chunks:

            if model_key == "flan":

                prompt = f"Summarize this podcast section:\n{chunk}"

                output = summarizer(
                    prompt,
                    max_new_tokens=120,
                    do_sample=False
                )

                partial.append(output[0]["generated_text"])

            else:

                output = summarizer(
                    chunk,
                    max_new_tokens=120,
                    do_sample=False,
                    truncation=True
                )

                partial.append(output[0]["summary_text"])

        section_summaries.append({
            "timestamp": text_group["start"],
            "summary": " ".join(partial)
        })

    # FIXED
    full_summary_text = " ".join(
        [section["summary"] for section in section_summaries]
    )

    final_chunks = chunk_text(full_summary_text, tokenizer, max_input_tokens)

    final_parts = []

    for chunk in final_chunks:

        if model_key == "flan":

            prompt = f"Create a final clean podcast summary:\n{chunk}"

            output = summarizer(
                prompt,
                max_new_tokens=150,
                do_sample=False
            )

            final_parts.append(output[0]["generated_text"])

        else:

            output = summarizer(
                chunk,
                max_new_tokens=150,
                do_sample=False,
                truncation=True
            )

            final_parts.append(output[0]["summary_text"])

    final_summary = " ".join(final_parts)

    return {
        "overview": final_summary,
        "sections": section_summaries
    }