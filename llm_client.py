"""Phần code chịu trách nhiệm giao tiếp với Hermes Agent."""

import os

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI


def get_llm_response(prompt: str) -> str:
    """Gửi prompt tới Hermes Agent và trả về nội dung dạng chuỗi."""
    load_dotenv()

    base_url = os.getenv("HERMES_BASE_URL")
    api_key = os.getenv("HERMES_API_KEY")
    model = os.getenv("HERMES_MODEL")

    if not base_url:
        raise ValueError(
            "Chưa tìm thấy HERMES_BASE_URL. Hãy cập nhật file .env."
        )
    if not api_key:
        raise ValueError("Chưa tìm thấy HERMES_API_KEY. Hãy cập nhật file .env.")
    if not model:
        raise ValueError("Chưa tìm thấy HERMES_MODEL. Hãy cập nhật file .env.")

    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
    except AuthenticationError as error:
        raise RuntimeError(
            "Hermes Agent từ chối xác thực. "
            "Hãy kiểm tra HERMES_API_KEY có khớp với API_SERVER_KEY của Hermes."
        ) from error
    except APIConnectionError as error:
        raise RuntimeError(
            f"Không thể kết nối tới Hermes Agent tại {base_url}. "
            "Hãy kiểm tra Hermes Agent đã chạy, lệnh 'hermes gateway' đang hoạt động "
            "và cổng 127.0.0.1:8642 đang lắng nghe."
        ) from error
    except APIStatusError as error:
        raise RuntimeError(
            f"Hermes Agent trả về lỗi HTTP {error.status_code}: {error.message}"
        ) from error

    if not response.choices:
        raise RuntimeError("Hermes Agent không trả về lựa chọn phản hồi nào.")

    content = response.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError("Hermes Agent trả về response không có content.")

    return content
