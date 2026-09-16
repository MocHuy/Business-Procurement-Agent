"""Phần code chịu trách nhiệm giao tiếp với LLM."""

import os

from dotenv import load_dotenv
from openai import OpenAI


def get_llm_response(prompt: str) -> str:
    """Gửi prompt tới OpenAI và trả về nội dung dạng chuỗi."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "Chưa tìm thấy API key. Hãy cập nhật OPENAI_API_KEY trong file .env."
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text

