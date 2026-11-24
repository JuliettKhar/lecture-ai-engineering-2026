"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key
from google.genai import types
import time

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, history: list[types.Content] | None = None, model: str = MODEL) -> str:
    client = genai.Client(api_key=get_api_key())
    contents = list(history) if history is not None else []
    contents.append(
        types.Content(role="user", 
        parts=[types.Part.from_text(text=question)])
        )
    
    start = time.perf_counter()
    response = client.models.generate_content(
        model=model, 
        contents=contents,
        config=types.GenerateContentConfig(temperature=0))

    elapsed = time.perf_counter() - start
    print(f"[latency]: {elapsed:.3f} s")

    usage = response.usage_metadata
    if usage:
        print(f"[input tokens]: {usage.prompt_token_count}")
        print(f"[output tokens]: {usage.candidates_token_count}")
        print(f"[total tokens]: {usage.total_token_count}")
        print(f"[thoughts tokens]: {usage.thoughts_token_count}")

    answer = response.text or ""
    if history is not None:
        history.append(contents[-1])
        history.append(
            types.Content(
                role="model",
                parts=[types.Part.from_text(text=answer)],
            )
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--chat", action="store_true")
    parser.add_argument("--model", default=MODEL)
    args = parser.parse_args()

    print(f"[model] {args.model}")
    # print(f"[質問] {args.question}\n")
    try:
        if args.chat:
             history: list[types.Content] = []
             print("チャットモード（終了するには exit）")

             while True:
                 question = input("\nYou: ").strip()
                 if question.lower() in ("exit", "quit"):
                     break
                 if not question:
                     continue
                 answer = ask(question, history, args.model)
                 print(f"\nGemini: {answer}")
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            answer = ask(question, None, args.model)
            print(f"\nGemini: {answer}")
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
