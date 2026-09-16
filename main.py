"""Điểm bắt đầu của chương trình."""

from llm_client import get_llm_response


def main() -> None:
    prompt = (
        "Bạn có thể tự giới thiệu bản thân không?"
    )

    print("Đang gửi prompt tới LLM...\n")

    try:
        response = get_llm_response(prompt)
        print(response)
    except Exception as error:
        print(f"Có lỗi xảy ra: {error}")


if __name__ == "__main__":
    main()

